from typing import Dict, Any
from api_tester.core.constants import FailureType, Severity
from api_tester.validation.models import ValidationResult, ViolationDetail


class HeaderValidator:
    """Validates response headers against contract expectations."""

    @classmethod
    def validate(cls, actual_headers: Dict[str, str], expected_headers: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult()
        normalized_actual = {k.lower(): v for k, v in actual_headers.items()}

        for header_name, header_def in expected_headers.items():
            h_name_lower = header_name.lower()
            is_required = header_def.get("required", False) if isinstance(header_def, dict) else False

            if is_required and h_name_lower not in normalized_actual:
                result.add_violation(
                    ViolationDetail(
                        field=f"header.{header_name}",
                        expected="present",
                        actual="missing",
                        message=f"Missing required response header: '{header_name}'",
                        failure_type=FailureType.CONTRACT_VIOLATION,
                        severity=Severity.HIGH,
                    )
                )
        return result
