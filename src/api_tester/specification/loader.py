import json
import os
import re
from pathlib import Path
from typing import Dict, Any
from urllib.parse import urlparse
import httpx
import yaml

from api_tester.core.exceptions import SpecificationError


class SpecificationLoader:
    """Loads OpenAPI specifications from local JSON/YAML files or remote HTTPS URLs."""

    def __init__(self, allow_insecure_http: bool = False, verify_tls: bool = True, timeout: float = 15.0):
        self.allow_insecure_http = allow_insecure_http
        self.verify_tls = verify_tls
        self.timeout = timeout

    def load(self, source: str) -> Dict[str, Any]:
        """Load specification dictionary from file path or URL."""
        if not source:
            raise SpecificationError("Specification source cannot be empty")

        if self._is_url(source):
            return self._load_from_url(source)
        else:
            return self._load_from_file(source)

    def _is_url(self, source: str) -> bool:
        parsed = urlparse(source)
        return parsed.scheme in ("http", "https")

    def _load_from_file(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise SpecificationError(f"Specification file not found: {file_path}")

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            raise SpecificationError(f"Error reading specification file '{file_path}': {e}") from e

        return self._parse_content(content, source_name=file_path)

    def _load_from_url(self, url: str) -> Dict[str, Any]:
        parsed = urlparse(url)
        if parsed.scheme == "http" and not self.allow_insecure_http:
            raise SpecificationError(
                f"Insecure HTTP URL blocked: '{url}'. Use HTTPS or enable 'allow_insecure_http' in configuration."
            )

        # Basic SSRF prevention: block local loopback / cloud metadata when resolving remote specs if needed
        hostname = (parsed.hostname or "").lower()
        if hostname in ("169.254.169.254", "metadata.google.internal") and not self.allow_insecure_http:
            raise SpecificationError(f"Prohibited remote address in specification URL: {url}")

        try:
            with httpx.Client(verify=self.verify_tls, timeout=self.timeout, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                content = response.text
        except httpx.HTTPStatusError as e:
            raise SpecificationError(f"Failed to fetch remote specification (HTTP {e.response.status_code}): {url}") from e
        except Exception as e:
            raise SpecificationError(f"Network error fetching specification from '{url}': {e}") from e

        return self._parse_content(content, source_name=url)

    def _parse_content(self, content: str, source_name: str) -> Dict[str, Any]:
        if not content.strip():
            raise SpecificationError(f"Specification content is empty: {source_name}")

        # Try JSON first
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # Try YAML
        try:
            data = yaml.safe_load(content)
            if isinstance(data, dict):
                return data
            raise SpecificationError(f"Specification root must be a JSON/YAML mapping/dict: {source_name}")
        except yaml.YAMLError as e:
            raise SpecificationError(f"Invalid JSON/YAML in specification '{source_name}': {e}") from e
