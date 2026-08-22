from typing import List, Dict, Any, Optional
from api_tester.core.constants import TestType, Severity
from api_tester.generator.models import TestCase
from api_tester.generator.data_generator import DataGenerator
from api_tester.specification.models import EndpointModel, ResponseModel


class PositiveTestGenerator:
    """Generates valid happy-path test cases complying with the OpenAPI contract."""

    @classmethod
    def generate(cls, endpoint: EndpointModel, test_counter: int) -> List[TestCase]:
        test_cases: List[TestCase] = []

        # Determine expected status code and response schema
        expected_status = 200
        expected_schema = None
        expected_headers = {}

        # Look for 2xx responses in contract
        success_responses = [
            (code, resp) for code, resp in endpoint.responses.items()
            if code.startswith("2") or code == "default"
        ]

        if success_responses:
            code_str, resp_obj = success_responses[0]
            if code_str.isdigit():
                expected_status = int(code_str)
            else:
                expected_status = 200
            expected_schema = resp_obj.schema_def
            expected_headers = resp_obj.headers
        elif endpoint.method == "POST":
            expected_status = 201
        elif endpoint.method == "DELETE":
            expected_status = 204

        # Generate path params
        path_params = {}
        query_params = {}
        headers = {}

        for param in endpoint.parameters:
            val = param.example
            if val is None:
                val = DataGenerator.generate_valid_data(param.schema_def)
            if val is None:
                val = "1"

            if param.in_location == "path":
                path_params[param.name] = val
            elif param.in_location == "query":
                # Include query params
                query_params[param.name] = val
            elif param.in_location == "header":
                headers[param.name] = str(val)

        # Generate Request Body
        body = None
        content_type = "application/json"
        if endpoint.request_body:
            content_type = endpoint.request_body.content_type
            if endpoint.request_body.example is not None:
                body = endpoint.request_body.example
            elif endpoint.request_body.schema_def:
                body = DataGenerator.generate_valid_data(endpoint.request_body.schema_def)

        tc_id = f"TC-{test_counter:03d}"
        tc = TestCase(
            id=tc_id,
            name=f"{endpoint.method} {endpoint.path} — Valid Request",
            endpoint_id=endpoint.id,
            path=endpoint.path,
            method=endpoint.method,
            test_type=TestType.POSITIVE,
            suite="smoke" if endpoint.method in ("GET", "HEAD") else "regression",
            severity=Severity.CRITICAL if endpoint.method in ("GET", "POST") else Severity.HIGH,
            description=f"Verify {endpoint.method} {endpoint.path} returns successful response ({expected_status}) with valid schema.",
            headers=headers,
            query_params=query_params,
            path_params=path_params,
            body=body,
            content_type=content_type,
            expected_status_codes=[expected_status] if expected_status else [200, 201, 204],
            expected_response_schema=expected_schema,
            expected_headers=expected_headers,
            validate_schema=expected_schema is not None,
            tags=endpoint.tags,
        )
        test_cases.append(tc)
        return test_cases
