from typing import List, Optional
from pydantic import BaseModel, Field
from api_tester.core.constants import FailureType, Severity


class ViolationDetail(BaseModel):
    field: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    message: str
    failure_type: FailureType = FailureType.CONTRACT_VIOLATION
    severity: Severity = Severity.HIGH


class ValidationResult(BaseModel):
    is_valid: bool = True
    violations: List[ViolationDetail] = Field(default_factory=list)

    def add_violation(self, violation: ViolationDetail):
        self.is_valid = False
        self.violations.append(violation)
