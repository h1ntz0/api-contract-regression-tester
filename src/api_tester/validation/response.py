from typing import Any, Dict, Optional
from api_tester.execution.client import ExecutionHttpResponse
from api_tester.generator.models import TestCase
from api_tester.validation.models import ValidationResult, ViolationDetail
from api_tester.validation.status_code import StatusCodeValidator
from api_tester.validation.headers import HeaderValidator
from api_tester.validation.schema import SchemaValidator
from api_tester.core.constants import FailureType, Severity


class ResponseValidator:
    """Combines status code, header, schema, type, and enum checks into unified response validation."""

    @classmethod
    def validate(cls, response: ExecutionHttpResponse, test_case: TestCase) -> ValidationResult:
        result = ValidationResult()

        # Check if HTTP execution failed at transport/network level
        if not response.is_success:
            result.add_violation(
                ViolationDetail(
                    field="transport",
                    expected="successful http connection",
                    actual=response.error_message or "Connection failed",
                    message=response.error_message or "Network connection failed",
                    failure_type=response.failure_type or FailureType.NETWORK_ERROR,
                    severity=Severity.CRITICAL,
                )
            )
            return result

        # 1. Status Code Validation
        status_res = StatusCodeValidator.validate(response.status_code, test_case.expected_status_codes)
        for v in status_res.violations:
            result.add_violation(v)

        # 2. Header Validation
        if test_case.validate_headers and test_case.expected_headers:
            header_res = HeaderValidator.validate(response.headers, test_case.expected_headers)
            for v in header_res.violations:
                result.add_violation(v)

        # 3. Schema Validation (only if response status indicates success or schema explicitly configured)
        if test_case.validate_schema and test_case.expected_response_schema and (200 <= response.status_code < 300):
            schema_res = SchemaValidator.validate(response.body, test_case.expected_response_schema)
            for v in schema_res.violations:
                result.add_violation(v)

        return result
