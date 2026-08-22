from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ParameterModel(BaseModel):
    model_config = {"populate_by_name": True}

    name: str
    in_location: str = Field(alias="in")
    required: bool = False
    description: Optional[str] = None
    schema_def: Dict[str, Any] = Field(default_factory=dict)
    example: Any = None


class RequestBodyModel(BaseModel):
    required: bool = False
    content_type: str = "application/json"
    schema_def: Dict[str, Any] = Field(default_factory=dict)
    example: Any = None


class ResponseModel(BaseModel):
    status_code: str
    description: Optional[str] = None
    headers: Dict[str, Any] = Field(default_factory=dict)
    content_type: Optional[str] = "application/json"
    schema_def: Optional[Dict[str, Any]] = None


class EndpointModel(BaseModel):
    id: str  # e.g., "GET:/users/{id}"
    path: str
    method: str  # GET, POST, PUT, DELETE, PATCH, etc.
    summary: Optional[str] = None
    description: Optional[str] = None
    operation_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    parameters: List[ParameterModel] = Field(default_factory=list)
    request_body: Optional[RequestBodyModel] = None
    responses: Dict[str, ResponseModel] = Field(default_factory=dict)
    security: List[Dict[str, List[str]]] = Field(default_factory=list)
    deprecated: bool = False


class ServerModel(BaseModel):
    url: str
    description: Optional[str] = None


class ApiMetadata(BaseModel):
    title: str
    version: str
    description: Optional[str] = None


class ApiSpecification(BaseModel):
    openapi_version: str
    metadata: ApiMetadata
    servers: List[ServerModel] = Field(default_factory=list)
    endpoints: List[EndpointModel] = Field(default_factory=list)
    raw_spec: Dict[str, Any] = Field(default_factory=dict)
