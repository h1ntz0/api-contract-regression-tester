from api_tester.validation.status_code import StatusCodeValidator
from api_tester.validation.schema import SchemaValidator
from api_tester.validation.headers import HeaderValidator
from api_tester.core.constants import FailureType


def test_status_code_validator():
    res_valid = StatusCodeValidator.validate(200, [200, 201])
    assert res_valid.is_valid is True

    res_invalid = StatusCodeValidator.validate(500, [200])
    assert res_invalid.is_valid is False
    assert res_invalid.violations[0].failure_type == FailureType.ASSERTION_FAILURE


def test_header_validator():
    headers = {"Content-Type": "application/json", "X-Custom": "val"}
    expected = {"x-custom": {"required": True}, "x-missing": {"required": True}}

    res = HeaderValidator.validate(headers, expected)
    assert res.is_valid is False
    assert len(res.violations) == 1
    assert "x-missing" in res.violations[0].field


def test_schema_validator():
    schema = {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "role": {"type": "string", "enum": ["admin", "user"]}
        }
    }

    # Valid payload
    assert SchemaValidator.validate({"id": 1, "name": "test", "role": "admin"}, schema).is_valid is True

    # Missing required field
    res_missing = SchemaValidator.validate({"id": 1}, schema)
    assert res_missing.is_valid is False
    assert any("required" in v.message.lower() for v in res_missing.violations)

    # Type mismatch
    res_type = SchemaValidator.validate({"id": "not_an_int", "name": "test"}, schema)
    assert res_type.is_valid is False
    assert any("Type mismatch" in v.message for v in res_type.violations)

    # Invalid enum
    res_enum = SchemaValidator.validate({"id": 1, "name": "test", "role": "invalid_role"}, schema)
    assert res_enum.is_valid is False
    assert any("enum" in v.message.lower() for v in res_enum.violations)
