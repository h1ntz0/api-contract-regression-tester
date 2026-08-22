from typing import Any, Dict, List, Optional
import copy


class DataGenerator:
    """Generates synthetic valid and invalid data values based on OpenAPI JSON schema specs."""

    @classmethod
    def generate_valid_data(cls, schema: Dict[str, Any], depth: int = 0) -> Any:
        if depth > 10:
            return None

        if not schema or not isinstance(schema, dict):
            return "example_value"

        # Explicit example
        if "example" in schema:
            return copy.deepcopy(schema["example"])
        if "default" in schema:
            return copy.deepcopy(schema["default"])

        # Enum value
        if "enum" in schema and schema["enum"]:
            return schema["enum"][0]

        # Handle oneOf / anyOf / allOf
        if "allOf" in schema and isinstance(schema["allOf"], list) and schema["allOf"]:
            combined = {}
            for sub_schema in schema["allOf"]:
                if isinstance(sub_schema, dict):
                    combined.update(cls.generate_valid_data(sub_schema, depth + 1) or {})
            return combined
        if "oneOf" in schema and isinstance(schema["oneOf"], list) and schema["oneOf"]:
            return cls.generate_valid_data(schema["oneOf"][0], depth + 1)
        if "anyOf" in schema and isinstance(schema["anyOf"], list) and schema["anyOf"]:
            return cls.generate_valid_data(schema["anyOf"][0], depth + 1)

        schema_type = schema.get("type", "string")

        if schema_type == "string":
            str_format = schema.get("format", "")
            if str_format == "email":
                return "test.user@example.com"
            elif str_format == "uuid":
                return "123e4567-e89b-12d3-a456-426614174000"
            elif str_format == "date":
                return "2026-08-22"
            elif str_format in ("date-time", "date_time"):
                return "2026-08-22T10:00:00Z"
            elif str_format == "uri":
                return "https://example.com"
            min_len = schema.get("minLength", 1)
            return "sample_str" if min_len <= 10 else "sample_string_value_extended"

        elif schema_type in ("integer", "number"):
            minimum = schema.get("minimum")
            maximum = schema.get("maximum")
            if minimum is not None:
                return minimum + 1 if maximum is not None and minimum < maximum else minimum
            if maximum is not None:
                return maximum - 1 if maximum > 1 else maximum
            return 1 if schema_type == "integer" else 1.5

        elif schema_type == "boolean":
            return True

        elif schema_type == "array":
            items_schema = schema.get("items", {})
            item_val = cls.generate_valid_data(items_schema, depth + 1)
            return [item_val] if item_val is not None else []

        elif schema_type == "object" or "properties" in schema:
            properties = schema.get("properties", {})
            required_fields = set(schema.get("required", []))
            obj = {}
            for prop_name, prop_schema in properties.items():
                # Include all required fields, and optional fields for valid payloads
                if isinstance(prop_schema, dict):
                    obj[prop_name] = cls.generate_valid_data(prop_schema, depth + 1)
            return obj

        return "val"
