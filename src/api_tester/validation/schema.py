from typing import Any, Dict, Optional
import jsonschema
from jsonschema import Draft202012Validator, ValidationError as JsonSchemaValidationError

from api_tester.core.constants import FailureType, Severity
from api_tester.validation.models import ValidationResult, ViolationDetail


class SchemaValidator:
    """Validates response JSON body against OpenAPI JSON schema definitions."""

    @classmethod
    def validate(cls, response_data: Any, schema: Optional[Dict[str, Any]]) -> ValidationResult:
        result = ValidationResult()
        if schema is None:
            return result

        if response_data is None and schema:
            result.add_violation(
                ViolationDetail(
                    field="body",
                    expected="valid json body according to schema",
                    actual="empty / None",
                    message="Response body is empty but schema definition was expected",
                    failure_type=FailureType.CONTRACT_VIOLATION,
                    severity=Severity.HIGH,
                )
            )
            return result

        # Validate with jsonschema
        try:
            validator = Draft202012Validator(schema)
            errors = sorted(validator.iter_errors(response_data), key=lambda e: e.path)

            for err in errors:
                field_path = ".".join(str(p) for p in err.path) if err.path else "root"
                expected_desc = str(err.validator_value) if err.validator else "schema_rule"
                actual_val = str(err.instance)

                # Determine error category & severity
                if err.validator == "required":
                    message = f"Missing required property: '{err.message}'"
                    severity = Severity.HIGH
                elif err.validator == "type":
                    message = f"Type mismatch at '{field_path}': expected {err.validator_value}, got {type(err.instance).__name__}"
                    severity = Severity.HIGH
                elif err.validator == "enum":
                    message = f"Invalid enum value at '{field_path}': '{err.instance}'. Allowed: {err.validator_value}"
                    severity = Severity.HIGH
                else:
                    message = f"Schema validation failed at '{field_path}': {err.message}"
                    severity = Severity.MEDIUM

                result.add_violation(
                    ViolationDetail(
                        field=field_path,
                        expected=expected_desc,
                        actual=actual_val,
                        message=message,
                        failure_type=FailureType.CONTRACT_VIOLATION,
                        severity=severity,
                    )
                )
        except Exception as e:
            result.add_violation(
                ViolationDetail(
                    field="schema",
                    expected="valid_schema_check",
                    actual=str(e),
                    message=f"Schema validator error: {e}",
                    failure_type=FailureType.EXECUTION_ERROR,
                    severity=Severity.CRITICAL,
                )
            )

        return result
