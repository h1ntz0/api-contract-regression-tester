import concurrent.futures
import time
from typing import List, Callable, Optional
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

from api_tester.config.models import ProjectConfig
from api_tester.core.constants import TestStatus, FailureType
from api_tester.execution.client import HttpClient, ExecutionHttpResponse
from api_tester.execution.request_builder import RequestBuilder
from api_tester.generator.models import TestCase, TestPlan
from api_tester.reporting.models import TestResultItem
from api_tester.validation.response import ResponseValidator


class TestRunner:
    """Executes test plan against target base URL with worker concurrency and validation."""

    def __init__(self, config: ProjectConfig, base_url: str):
        self.config = config
        self.base_url = base_url

    def run_plan(
        self,
        test_plan: TestPlan,
        progress_callback: Optional[Callable[[TestResultItem], None]] = None,
    ) -> List[TestResultItem]:
        results: List[TestResultItem] = []
        workers = self.config.execution.workers

        if workers <= 1:
            # Sequential execution
            with HttpClient(self.config) as client:
                for tc in test_plan.test_cases:
                    res = self._execute_single_test(client, tc)
                    results.append(res)
                    if progress_callback:
                        progress_callback(res)
                    if self.config.execution.delay_ms > 0:
                        time.sleep(self.config.execution.delay_ms / 1000.0)
        else:
            # Multi-worker concurrency
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {
                    executor.submit(self._run_with_isolated_client, tc): tc
                    for tc in test_plan.test_cases
                }
                for future in concurrent.futures.as_completed(futures):
                    res = future.result()
                    results.append(res)
                    if progress_callback:
                        progress_callback(res)

        # Ensure order matches test_plan
        results_map = {r.test_id: r for r in results}
        ordered_results = [results_map[tc.id] for tc in test_plan.test_cases if tc.id in results_map]
        return ordered_results

    def _run_with_isolated_client(self, tc: TestCase) -> TestResultItem:
        with HttpClient(self.config) as client:
            return self._execute_single_test(client, tc)

    def _execute_single_test(self, client: HttpClient, tc: TestCase) -> TestResultItem:
        url, headers, params, body = RequestBuilder.build(tc, self.base_url, self.config)
        sanitized_headers = RequestBuilder.redact_headers(headers)

        http_resp: ExecutionHttpResponse = client.request(
            method=tc.method,
            url=url,
            headers=headers,
            params=params,
            json_body=body,
        )

        val_result = ResponseValidator.validate(http_resp, tc)

        status = TestStatus.PASSED if val_result.is_valid else TestStatus.FAILED
        if not http_resp.is_success and http_resp.failure_type in (FailureType.TIMEOUT, FailureType.CONNECTION_ERROR, FailureType.NETWORK_ERROR):
            status = TestStatus.ERROR

        failure_reason = None
        if val_result.violations:
            failure_reason = val_result.violations[0].message

        return TestResultItem(
            test_id=tc.id,
            name=tc.name,
            endpoint_id=tc.endpoint_id,
            path=tc.path,
            method=tc.method,
            suite=tc.suite,
            status=status,
            severity=tc.severity,
            duration_ms=http_resp.duration_ms,
            status_code=http_resp.status_code,
            expected_status_codes=tc.expected_status_codes,
            request_url=url,
            request_headers=sanitized_headers,
            request_params=params,
            request_body=body,
            response_headers=http_resp.headers,
            response_body=http_resp.body,
            violations=val_result.violations,
            failure_reason=failure_reason,
            retries=http_resp.retries_occurred,
        )
