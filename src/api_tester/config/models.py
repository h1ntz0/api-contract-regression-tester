import os
import re
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, field_validator


class AuthConfig(BaseModel):
    type: str = Field(default="none", description="Authentication type: none, bearer, api_key, basic")
    token_env: Optional[str] = Field(default=None, description="Environment variable name for bearer token")
    api_key_name: Optional[str] = Field(default="X-API-Key", description="Header or query param name for API key")
    api_key_env: Optional[str] = Field(default=None, description="Environment variable name for API key")
    api_key_in: str = Field(default="header", description="Location of API key: header or query")
    username_env: Optional[str] = Field(default=None, description="Env var for basic auth username")
    password_env: Optional[str] = Field(default=None, description="Env var for basic auth password")

    def get_headers(self) -> Dict[str, str]:
        headers = {}
        auth_type_lower = self.type.lower()
        if auth_type_lower == "bearer" and self.token_env:
            token = os.environ.get(self.token_env, "")
            if token:
                headers["Authorization"] = f"Bearer {token}"
        elif auth_type_lower == "api_key" and self.api_key_in == "header" and self.api_key_env:
            key = os.environ.get(self.api_key_env, "")
            if key and self.api_key_name:
                headers[self.api_key_name] = key
        return headers

    def get_params(self) -> Dict[str, str]:
        params = {}
        if self.type.lower() == "api_key" and self.api_key_in == "query" and self.api_key_env:
            key = os.environ.get(self.api_key_env, "")
            if key and self.api_key_name:
                params[self.api_key_name] = key
        return params

    def get_basic_auth(self) -> Optional[tuple[str, str]]:
        if self.type.lower() == "basic" and self.username_env:
            username = os.environ.get(self.username_env, "")
            password = os.environ.get(self.password_env, "") if self.password_env else ""
            return (username, password)
        return None


class ExecutionConfig(BaseModel):
    timeout_connect: float = Field(default=5.0, description="Connect timeout in seconds")
    timeout_read: float = Field(default=30.0, description="Read timeout in seconds")
    workers: int = Field(default=1, description="Concurrency level (worker count)")
    delay_ms: int = Field(default=0, description="Delay between requests in milliseconds")
    allow_insecure_http: bool = Field(default=False, description="Allow insecure plain HTTP for remote specs/APIs")
    verify_tls: bool = Field(default=True, description="Verify SSL/TLS certificates")

    @field_validator("workers")
    @classmethod
    def validate_workers(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("workers must be greater than 0")
        return v

    @field_validator("timeout_connect", "timeout_read")
    @classmethod
    def validate_timeouts(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Timeout values must be greater than 0")
        return v


class RetryConfig(BaseModel):
    enabled: bool = Field(default=False, description="Whether retry is enabled")
    max_attempts: int = Field(default=2, description="Max attempts if retry enabled")
    backoff_factor: float = Field(default=0.5, description="Backoff multiplier")


class TestingConfig(BaseModel):
    positive: bool = Field(default=True, description="Run positive contract tests")
    negative: bool = Field(default=True, description="Run negative tests")
    contract: bool = Field(default=True, description="Run schema and contract validation")
    suites: List[str] = Field(default_factory=lambda: ["all"], description="Suites to execute")


class ReportConfig(BaseModel):
    output_dir: str = Field(default="./reports", description="Report directory")
    generate_html: bool = Field(default=True, description="Generate standalone HTML report")
    generate_json: bool = Field(default=True, description="Generate JSON test result")
    generate_junit: bool = Field(default=True, description="Generate JUnit XML")


class ApiConfig(BaseModel):
    base_url: Optional[str] = Field(default=None, description="Target base URL")
    headers: Dict[str, str] = Field(default_factory=dict, description="Default headers")


class ProjectConfig(BaseModel):
    name: str = Field(default="API Contract & Regression Tester", description="Project name")
    api: ApiConfig = Field(default_factory=ApiConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    testing: TestingConfig = Field(default_factory=TestingConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)
