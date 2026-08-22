from enum import Enum, IntEnum


class ExitCode(IntEnum):
    SUCCESS = 0
    TESTS_FAILED = 1
    CONFIG_ERROR = 2
    SPEC_ERROR = 3
    EXECUTION_ERROR = 4


class TestStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


class TestType(str, Enum):
    SMOKE = "smoke"
    REGRESSION = "regression"
    CONTRACT = "contract"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    ALL = "all"


class FailureType(str, Enum):
    ASSERTION_FAILURE = "ASSERTION_FAILURE"
    CONTRACT_VIOLATION = "CONTRACT_VIOLATION"
    NETWORK_ERROR = "NETWORK_ERROR"
    TIMEOUT = "TIMEOUT"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    AUTH_ERROR = "AUTH_ERROR"
    EXECUTION_ERROR = "EXECUTION_ERROR"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
