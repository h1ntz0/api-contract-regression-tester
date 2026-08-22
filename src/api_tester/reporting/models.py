from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from api_tester.core.constants import TestStatus, FailureType, Severity
from api_tester.validation.models import ViolationDetail


class TestResultItem(BaseModel):
    test_id: str
    name: str
    endpoint_id: str
    path: str
    method: str
    suite: str
    status: TestStatus
    severity: Severity = Severity.HIGH
    duration_ms: float = 0.0
    status_code: int = 0
    expected_status_codes: List[int] = Field(default_factory=list)

    # Request details (sanitized)
    request_url: str = ""
    request_headers: Dict[str, str] = Field(default_factory=dict)
    request_params: Dict[str, Any] = Field(default_factory=dict)
    request_body: Optional[Any] = None

    # Response details
    response_headers: Dict[str, str] = Field(default_factory=dict)
    response_body: Optional[Any] = None

    # Violations & failures
    violations: List[ViolationDetail] = Field(default_factory=list)
    failure_reason: Optional[str] = None
    retries: int = 0


class SummaryStats(BaseModel):
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    pass_rate: float = 0.0
    total_duration_sec: float = 0.0
    avg_response_time_ms: float = 0.0
    method_breakdown: Dict[str, int] = Field(default_factory=dict)
    status_breakdown: Dict[str, int] = Field(default_factory=dict)
    endpoint_breakdown: Dict[str, Dict[str, int]] = Field(default_factory=dict)


class TestExecutionReport(BaseModel):
    project_name: str
    timestamp: str
    base_url: str
    spec_source: str
    summary: SummaryStats
    results: List[TestResultItem] = Field(default_factory=list)
