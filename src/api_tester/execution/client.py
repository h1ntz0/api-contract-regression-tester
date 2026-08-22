import time
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel, Field

from api_tester.config.models import ProjectConfig, ExecutionConfig, RetryConfig
from api_tester.core.constants import FailureType


class ExecutionHttpResponse(BaseModel):
    status_code: int
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Any = None
    raw_text: str = ""
    duration_ms: float = 0.0
    is_success: bool = True
    error_message: Optional[str] = None
    failure_type: Optional[FailureType] = None
    retries_occurred: int = 0


class HttpClient:
    """HTTP client wrapper with configurable timeouts, retries, SSL verification, and timing."""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.exec_config: ExecutionConfig = config.execution
        self.retry_config: RetryConfig = config.retry

        # Build timeouts
        timeout = httpx.Timeout(
            timeout=self.exec_config.timeout_read,
            connect=self.exec_config.timeout_connect,
        )

        auth = config.auth.get_basic_auth()

        self._client = httpx.Client(
            timeout=timeout,
            verify=self.exec_config.verify_tls,
            auth=auth,
            follow_redirects=True,
        )

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Any] = None,
    ) -> ExecutionHttpResponse:
        max_attempts = self.retry_config.max_attempts if self.retry_config.enabled else 1
        attempts = 0
        last_error = None
        last_failure_type = None

        while attempts < max_attempts:
            attempts += 1
            start_time = time.perf_counter()

            try:
                # Decide how to send body based on headers
                is_json = headers and "application/json" in headers.get("Content-Type", "")
                if json_body is not None and is_json:
                    resp = self._client.request(method, url, headers=headers, params=params, json=json_body)
                elif json_body is not None:
                    resp = self._client.request(method, url, headers=headers, params=params, content=str(json_body))
                else:
                    resp = self._client.request(method, url, headers=headers, params=params)

                duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

                # Parse JSON if possible
                parsed_json = None
                raw_text = resp.text
                if resp.headers.get("content-type", "").startswith("application/json") or raw_text.strip().startswith(("{", "[")):
                    try:
                        parsed_json = resp.json()
                    except Exception:
                        parsed_json = None

                return ExecutionHttpResponse(
                    status_code=resp.status_code,
                    headers=dict(resp.headers),
                    body=parsed_json if parsed_json is not None else raw_text,
                    raw_text=raw_text,
                    duration_ms=duration_ms,
                    is_success=True,
                    retries_occurred=attempts - 1,
                )

            except httpx.ConnectTimeout as e:
                duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
                last_error = f"Connect timeout after {self.exec_config.timeout_connect}s: {e}"
                last_failure_type = FailureType.TIMEOUT
            except httpx.ReadTimeout as e:
                duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
                last_error = f"Read timeout after {self.exec_config.timeout_read}s: {e}"
                last_failure_type = FailureType.TIMEOUT
            except httpx.ConnectError as e:
                duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
                last_error = f"Connection failed to '{url}': {e}"
                last_failure_type = FailureType.CONNECTION_ERROR
            except Exception as e:
                duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
                last_error = f"Network request error: {e}"
                last_failure_type = FailureType.NETWORK_ERROR

            if attempts < max_attempts:
                time.sleep(self.retry_config.backoff_factor * attempts)

        return ExecutionHttpResponse(
            status_code=0,
            headers={},
            body=None,
            raw_text="",
            duration_ms=duration_ms,
            is_success=False,
            error_message=last_error,
            failure_type=last_failure_type,
            retries_occurred=attempts - 1,
        )
