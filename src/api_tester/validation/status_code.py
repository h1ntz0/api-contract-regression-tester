from typing import List
from api_tester.core.constants import FailureType, Severity
from api_tester.validation.models import ValidationResult, ViolationDetail


class StatusCodeValidator:
    """Validates HTTP status code against expected contract codes."""

    @classmethod
    def validate(cls, actual_status: int, expected_statuses: List[int]) -> ValidationResult:
        result = ValidationResult()
        if actual_status not in expected_statuses:
            expected_str = ", ".join(str(s) for s in expected_statuses)
            result.add_violation(
                ViolationDetail(
                    field="status_code",
                    expected=expected_str,
                    actual=str(actual_status),
                    message=f"Expected HTTP status in [{expected_str}] but received {actual_status}",
                    failure_type=FailureType.ASSERTION_FAILURE,
                    severity=Severity.CRITICAL if actual_status >= 500 else Severity.HIGH,
                )
            )
        return result
