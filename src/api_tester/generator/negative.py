from typing import List, Dict, Any
import copy
from api_tester.core.constants import TestType, Severity
from api_tester.generator.models import TestCase
from api_tester.generator.data_generator import DataGenerator
from api_tester.specification.models import EndpointModel


class NegativeTestGenerator:
    """Generates negative test cases (missing required fields, invalid types, invalid enums)."""

    @classmethod
    def generate(cls, endpoint: EndpointModel, start_counter: int) -> List[TestCase]:
        test_cases: List[TestCase] = []
        counter = start_counter

        # Derive expected negative status codes from contract 4xx responses or default to 400, 422
        expected_4xx = [
            int(code) for code in endpoint.responses.keys()
            if code.startswith("4") and code.isdigit()
        ]
        if not expected_4xx:
            expected_4xx = [400, 422, 404]

        # 1. Negative tests for parameters (Path, Query, Header)
        for param in endpoint.parameters:
            # Missing required query/header param
            if param.required and param.in_location != "path":
                tc_id = f"TC-{counter:03d}"
                counter += 1
                tc = TestCase(
                    id=tc_id,
                    name=f"{endpoint.method} {endpoint.path} — Missing Required {param.in_location.capitalize()} Param '{param.name}'",
                    endpoint_id=endpoint.id,
                    path=endpoint.path,
                    method=endpoint.method,
                    test_type=TestType.NEGATIVE,
                    suite="negative",
                    severity=Severity.MEDIUM,
                    description=f"Negative test omitting required parameter '{param.name}' in {param.in_location}.",
                    path_params=cls._generate_default_path_params(endpoint),
                    query_params={p.name: "valid" for p in endpoint.parameters if p.in_location == "query" and p.name != param.name},
                    headers={},
                    body=None,
                    expected_status_codes=expected_4xx,
                    validate_schema=False,
                    tags=endpoint.tags,
                )
                test_cases.append(tc)

            # Invalid data type for param
            param_type = param.schema_def.get("type", "string")
            if param_type in ("integer", "number"):
                tc_id = f"TC-{counter:03d}"
                counter += 1
                invalid_val = "invalid_not_a_number"
                path_params = cls._generate_default_path_params(endpoint)
                query_params = {}
                if param.in_location == "path":
                    path_params[param.name] = invalid_val
                elif param.in_location == "query":
                    query_params[param.name] = invalid_val

                tc = TestCase(
                    id=tc_id,
                    name=f"{endpoint.method} {endpoint.path} — Invalid Type for {param.in_location.capitalize()} Param '{param.name}'",
                    endpoint_id=endpoint.id,
                    path=endpoint.path,
                    method=endpoint.method,
                    test_type=TestType.NEGATIVE,
                    suite="negative",
                    severity=Severity.MEDIUM,
                    description=f"Send string instead of {param_type} for parameter '{param.name}'.",
                    path_params=path_params,
                    query_params=query_params,
                    headers={},
                    body=None,
                    expected_status_codes=expected_4xx,
                    validate_schema=False,
                    tags=endpoint.tags,
                )
                test_cases.append(tc)

        # 2. Negative tests for Request Body
        if endpoint.request_body and endpoint.request_body.schema_def:
            schema = endpoint.request_body.schema_def
            base_body = DataGenerator.generate_valid_data(schema)
            path_params = cls._generate_default_path_params(endpoint)

            if isinstance(base_body, dict):
                required_fields = schema.get("required", [])
                properties = schema.get("properties", {})

                # Missing required fields
                for req_field in required_fields:
                    if req_field in base_body:
                        mutated_body = copy.deepcopy(base_body)
                        del mutated_body[req_field]
                        tc_id = f"TC-{counter:03d}"
                        counter += 1
                        test_cases.append(
                            TestCase(
                                id=tc_id,
                                name=f"{endpoint.method} {endpoint.path} — Missing Required Field '{req_field}'",
                                endpoint_id=endpoint.id,
                                path=endpoint.path,
                                method=endpoint.method,
                                test_type=TestType.NEGATIVE,
                                suite="negative",
                                severity=Severity.HIGH,
                                description=f"Omit required field '{req_field}' in request payload.",
                                path_params=path_params,
                                body=mutated_body,
                                content_type=endpoint.request_body.content_type,
                                expected_status_codes=expected_4xx,
                                validate_schema=False,
                                tags=endpoint.tags,
                            )
                        )

                # Invalid data types in body
                for prop_name, prop_schema in properties.items():
                    if isinstance(prop_schema, dict):
                        p_type = prop_schema.get("type")
                        mutated_body = copy.deepcopy(base_body)
                        invalid_value = None
                        if p_type == "integer" or p_type == "number":
                            invalid_value = "invalid_string_val"
                        elif p_type == "string":
                            invalid_value = 999999
                        elif p_type == "boolean":
                            invalid_value = "not_a_bool"

                        if invalid_value is not None:
                            mutated_body[prop_name] = invalid_value
                            tc_id = f"TC-{counter:03d}"
                            counter += 1
                            test_cases.append(
                                TestCase(
                                    id=tc_id,
                                    name=f"{endpoint.method} {endpoint.path} — Invalid Data Type for Field '{prop_name}'",
                                    endpoint_id=endpoint.id,
                                    path=endpoint.path,
                                    method=endpoint.method,
                                    test_type=TestType.NEGATIVE,
                                    suite="negative",
                                    severity=Severity.HIGH,
                                    description=f"Send invalid type for field '{prop_name}'.",
                                    path_params=path_params,
                                    body=mutated_body,
                                    content_type=endpoint.request_body.content_type,
                                    expected_status_codes=expected_4xx,
                                    validate_schema=False,
                                    tags=endpoint.tags,
                                )
                            )

                # Invalid Enum values
                for prop_name, prop_schema in properties.items():
                    if isinstance(prop_schema, dict) and "enum" in prop_schema:
                        mutated_body = copy.deepcopy(base_body)
                        mutated_body[prop_name] = "__INVALID_ENUM_CHOICE_VALUE__"
                        tc_id = f"TC-{counter:03d}"
                        counter += 1
                        test_cases.append(
                            TestCase(
                                id=tc_id,
                                name=f"{endpoint.method} {endpoint.path} — Invalid Enum Value for Field '{prop_name}'",
                                endpoint_id=endpoint.id,
                                path=endpoint.path,
                                method=endpoint.method,
                                test_type=TestType.NEGATIVE,
                                suite="negative",
                                severity=Severity.MEDIUM,
                                description=f"Send non-enum value for field '{prop_name}'.",
                                path_params=path_params,
                                body=mutated_body,
                                content_type=endpoint.request_body.content_type,
                                expected_status_codes=expected_4xx,
                                validate_schema=False,
                                tags=endpoint.tags,
                            )
                        )

        return test_cases

    @classmethod
    def _generate_default_path_params(cls, endpoint: EndpointModel) -> Dict[str, Any]:
        path_params = {}
        for param in endpoint.parameters:
            if param.in_location == "path":
                val = param.example or DataGenerator.generate_valid_data(param.schema_def) or "1"
                path_params[param.name] = val
        return path_params
