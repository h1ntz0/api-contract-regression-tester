from copy import deepcopy
from typing import Dict, Any, List, Optional
import jsonschema

from api_tester.core.exceptions import SpecificationError
from api_tester.specification.models import (
    ApiSpecification,
    ApiMetadata,
    ServerModel,
    EndpointModel,
    ParameterModel,
    RequestBodyModel,
    ResponseModel,
)


class OpenApiParser:
    """Parses and validates OpenAPI 3.x specifications into structured domain models."""

    def __init__(self, raw_spec: Dict[str, Any]):
        self.raw_spec = raw_spec
        self.resolved_spec: Dict[str, Any] = {}

    def parse(self) -> ApiSpecification:
        """Validate, resolve $ref references, and build ApiSpecification model."""
        self._validate_basic_structure()
        self.resolved_spec = self._resolve_refs(deepcopy(self.raw_spec), self.raw_spec)

        openapi_ver = str(self.resolved_spec.get("openapi", ""))
        info = self.resolved_spec.get("info", {})
        metadata = ApiMetadata(
            title=info.get("title", "Untitled API"),
            version=str(info.get("version", "1.0.0")),
            description=info.get("description"),
        )

        servers = [
            ServerModel(url=s.get("url", ""), description=s.get("description"))
            for s in self.resolved_spec.get("servers", [])
            if "url" in s
        ]

        endpoints = self._parse_endpoints()

        return ApiSpecification(
            openapi_version=openapi_ver,
            metadata=metadata,
            servers=servers,
            endpoints=endpoints,
            raw_spec=self.raw_spec,
        )

    def _validate_basic_structure(self) -> None:
        if not isinstance(self.raw_spec, dict):
            raise SpecificationError("Specification root must be an object/dict")

        openapi_ver = self.raw_spec.get("openapi")
        if not openapi_ver:
            if "swagger" in self.raw_spec:
                raise SpecificationError("Swagger 2.0 detected. Please use OpenAPI 3.0+ specification.")
            raise SpecificationError("Missing required field: 'openapi'")

        if not str(openapi_ver).startswith("3."):
            raise SpecificationError(f"Unsupported OpenAPI version '{openapi_ver}'. Only 3.x is supported.")

        if "info" not in self.raw_spec or not isinstance(self.raw_spec["info"], dict):
            raise SpecificationError("Missing required field: 'info'")

        if "title" not in self.raw_spec["info"]:
            raise SpecificationError("Missing required field: 'info.title'")

        if "version" not in self.raw_spec["info"]:
            raise SpecificationError("Missing required field: 'info.version'")

        if "paths" not in self.raw_spec or not isinstance(self.raw_spec["paths"], dict):
            raise SpecificationError("Missing required field: 'paths'")

    def _resolve_refs(self, node: Any, root: Dict[str, Any], depth: int = 0) -> Any:
        """Deeply resolves internal $ref references within the OpenAPI document."""
        if depth > 50:
            # Prevent infinite recursion for cyclic schemas
            return node

        if isinstance(node, dict):
            if "$ref" in node and isinstance(node["$ref"], str):
                ref_path = node["$ref"]
                if ref_path.startswith("#/"):
                    resolved = self._lookup_json_pointer(root, ref_path[2:])
                    # Merge any sibling keys (OpenAPI 3.1 allows sibling description etc.)
                    merged = deepcopy(resolved)
                    if isinstance(merged, dict):
                        for k, v in node.items():
                            if k != "$ref":
                                merged[k] = self._resolve_refs(v, root, depth + 1)
                        return self._resolve_refs(merged, root, depth + 1)
                    return merged
            return {k: self._resolve_refs(v, root, depth + 1) for k, v in node.items()}
        elif isinstance(node, list):
            return [self._resolve_refs(elem, root, depth + 1) for elem in node]
        return node

    def _lookup_json_pointer(self, root: Dict[str, Any], pointer: str) -> Any:
        parts = pointer.split("/")
        current = root
        for part in parts:
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
                current = current[int(part)]
            else:
                raise SpecificationError(f"Failed to resolve internal $ref '#/{pointer}' (missing key '{part}')")
        return current

    def _parse_endpoints(self) -> List[EndpointModel]:
        endpoints: List[EndpointModel] = []
        paths = self.resolved_spec.get("paths", {})

        http_methods = {"get", "post", "put", "delete", "patch", "options", "head", "trace"}

        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue

            # Path-level parameters
            common_params = path_item.get("parameters", [])

            for method_name, op in path_item.items():
                method_lower = method_name.lower()
                if method_lower not in http_methods or not isinstance(op, dict):
                    continue

                method_upper = method_lower.upper()
                endpoint_id = f"{method_upper}:{path}"

                # Combine path-level and operation-level parameters
                op_params = op.get("parameters", [])
                merged_param_dict = {}
                for p in common_params + op_params:
                    if isinstance(p, dict) and "name" in p and "in" in p:
                        key = (p["name"], p["in"])
                        merged_param_dict[key] = p

                parameters = [
                    ParameterModel(
                        name=p["name"],
                        in_location=p["in"],
                        required=p.get("required", p["in"] == "path"),
                        description=p.get("description"),
                        schema_def=p.get("schema", {}),
                        example=p.get("example"),
                    )
                    for p in merged_param_dict.values()
                ]

                # Parse Request Body
                request_body = None
                rb_data = op.get("requestBody")
                if isinstance(rb_data, dict):
                    content = rb_data.get("content", {})
                    # Prefer application/json
                    ct = "application/json" if "application/json" in content else (next(iter(content.keys())) if content else "application/json")
                    media_type = content.get(ct, {}) if ct in content else {}
                    request_body = RequestBodyModel(
                        required=rb_data.get("required", False),
                        content_type=ct,
                        schema_def=media_type.get("schema", {}),
                        example=media_type.get("example"),
                    )

                # Parse Responses
                responses = {}
                for status_code, resp_data in op.get("responses", {}).items():
                    if isinstance(resp_data, dict):
                        content = resp_data.get("content", {})
                        ct = "application/json" if "application/json" in content else (next(iter(content.keys())) if content else None)
                        media_type = content.get(ct, {}) if ct and ct in content else {}
                        schema_def = media_type.get("schema") if media_type else None

                        responses[str(status_code)] = ResponseModel(
                            status_code=str(status_code),
                            description=resp_data.get("description"),
                            headers=resp_data.get("headers", {}),
                            content_type=ct,
                            schema_def=schema_def,
                        )

                endpoints.append(
                    EndpointModel(
                        id=endpoint_id,
                        path=path,
                        method=method_upper,
                        summary=op.get("summary"),
                        description=op.get("description"),
                        operation_id=op.get("operationId"),
                        tags=op.get("tags", []),
                        parameters=parameters,
                        request_body=request_body,
                        responses=responses,
                        security=op.get("security", self.resolved_spec.get("security", [])),
                        deprecated=op.get("deprecated", False),
                    )
                )

        return endpoints
