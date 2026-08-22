from datetime import datetime
from typing import List, Dict
from api_tester.core.constants import TestStatus
from api_tester.reporting.models import TestResultItem, SummaryStats, TestExecutionReport


class ResultAggregator:
    """Aggregates individual test results into complete summary metrics and breakdown stats."""

    @classmethod
    def aggregate(
        cls,
        results: List[TestResultItem],
        project_name: str,
        base_url: str,
        spec_source: str,
        total_duration_sec: float,
    ) -> TestExecutionReport:
        total = len(results)
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        errors = sum(1 for r in results if r.status == TestStatus.ERROR)

        pass_rate = round((passed / total * 100), 2) if total > 0 else 0.0
        total_dur_ms = sum(r.duration_ms for r in results)
        avg_resp_time = round(total_dur_ms / total, 2) if total > 0 else 0.0

        method_breakdown: Dict[str, int] = {}
        status_breakdown: Dict[str, int] = {
            TestStatus.PASSED.value: passed,
            TestStatus.FAILED.value: failed,
            TestStatus.SKIPPED.value: skipped,
            TestStatus.ERROR.value: errors,
        }
        endpoint_breakdown: Dict[str, Dict[str, int]] = {}

        for r in results:
            # Method breakdown
            m = r.method.upper()
            method_breakdown[m] = method_breakdown.get(m, 0) + 1

            # Endpoint breakdown
            ep = r.endpoint_id
            if ep not in endpoint_breakdown:
                endpoint_breakdown[ep] = {"passed": 0, "failed": 0, "errors": 0}
            if r.status == TestStatus.PASSED:
                endpoint_breakdown[ep]["passed"] += 1
            elif r.status == TestStatus.FAILED:
                endpoint_breakdown[ep]["failed"] += 1
            elif r.status == TestStatus.ERROR:
                endpoint_breakdown[ep]["errors"] += 1

        summary = SummaryStats(
            total_tests=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            pass_rate=pass_rate,
            total_duration_sec=round(total_duration_sec, 2),
            avg_response_time_ms=avg_resp_time,
            method_breakdown=method_breakdown,
            status_breakdown=status_breakdown,
            endpoint_breakdown=endpoint_breakdown,
        )

        return TestExecutionReport(
            project_name=project_name,
            timestamp=datetime.now().isoformat(),
            base_url=base_url,
            spec_source=spec_source,
            summary=summary,
            results=results,
        )
