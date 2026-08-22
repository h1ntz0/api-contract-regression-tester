import re
from typing import Dict, Any, Tuple
from urllib.parse import urljoin
from api_tester.config.models import ProjectConfig
from api_tester.generator.models import TestCase


class RequestBuilder:
    """Builds full URL, redacted headers, query params, and body for HTTP request execution."""

    @classmethod
    def build(cls, test_case: TestCase, base_url: str, config: ProjectConfig) -> Tuple[str, Dict[str, str], Dict[str, Any], Any]:
        # 1. Format path parameters
        url_path = test_case.path
        for param_name, param_val in test_case.path_params.items():
            pattern = re.compile(rf"\{{{re.escape(param_name)}\}}")
            url_path = pattern.sub(str(param_val), url_path)

        # Normalize base_url and path
        base = base_url.rstrip("/")
        if not url_path.startswith("/"):
            url_path = "/" + url_path
        full_url = f"{base}{url_path}"

        # 2. Build headers
        headers: Dict[str, str] = {}
        # Global config headers
        headers.update(config.api.headers)
        # Auth headers
        headers.update(config.auth.get_headers())
        # Content-Type
        if test_case.content_type:
            headers["Content-Type"] = test_case.content_type
        # Test case specific headers
        headers.update(test_case.headers)

        # 3. Build query parameters
        query_params: Dict[str, Any] = {}
        query_params.update(config.auth.get_params())
        query_params.update(test_case.query_params)

        # 4. Body
        body = test_case.body

        return full_url, headers, query_params, body

    @classmethod
    def redact_headers(cls, headers: Dict[str, str]) -> Dict[str, str]:
        """Redacts sensitive authorization tokens and API keys from logging/reports."""
        redacted = {}
        sensitive_keywords = ("auth", "key", "token", "secret", "password")
        for k, v in headers.items():
            k_lower = k.lower()
            if any(kw in k_lower for kw in sensitive_keywords):
                if v.lower().startswith("bearer "):
                    redacted[k] = "Bearer " + "*" * 8
                elif v.lower().startswith("basic "):
                    redacted[k] = "Basic " + "*" * 8
                else:
                    redacted[k] = "*" * 8
            else:
                redacted[k] = v
        return redacted
