from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from api_tester.core.constants import TestType, Severity


class TestCase(BaseModel):
    id: str  # e.g., "TC-001"
    name: str  # e.g., "POST /users — Valid Request"
    endpoint_id: str  # e.g., "POST:/users"
    path: str
    method: str
    test_type: TestType = TestType.POSITIVE
    suite: str = "regression"
    severity: Severity = Severity.HIGH
    description: str = ""

    # Request specifications
    headers: Dict[str, str] = Field(default_factory=dict)
    query_params: Dict[str, Any] = Field(default_factory=dict)
    path_params: Dict[str, Any] = Field(default_factory=dict)
    body: Optional[Any] = None
    content_type: Optional[str] = "application/json"

    # Expectations
    expected_status_codes: List[int] = Field(default_factory=lambda: [200])
    expected_response_schema: Optional[Dict[str, Any]] = None
    expected_headers: Dict[str, Any] = Field(default_factory=dict)
    validate_schema: bool = True
    validate_headers: bool = True
    tags: List[str] = Field(default_factory=list)


class TestPlan(BaseModel):
    total_cases: int = 0
    test_cases: List[TestCase] = Field(default_factory=list)
