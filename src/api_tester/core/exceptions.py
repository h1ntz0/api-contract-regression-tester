class ApiTesterException(Exception):
    """Base exception for API tester."""
    pass


class SpecificationError(ApiTesterException):
    """Raised when OpenAPI specification is missing, unreadable, or invalid."""
    pass


class ConfigurationError(ApiTesterException):
    """Raised when user configuration is invalid or missing."""
    pass


class ExecutionError(ApiTesterException):
    """Raised when request execution encounters unhandled or fatal errors."""
    pass


class ValidationError(ApiTesterException):
    """Raised when contract or response assertion validation fails."""
    pass
