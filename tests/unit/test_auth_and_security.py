import os
from api_tester.config.models import ProjectConfig, AuthConfig
from api_tester.execution.request_builder import RequestBuilder
from api_tester.generator.models import TestCase


def test_auth_bearer():
    os.environ["MY_TEST_TOKEN"] = "secret_12345"
    cfg = ProjectConfig()
    cfg.auth = AuthConfig(type="bearer", token_env="MY_TEST_TOKEN")

    headers = cfg.auth.get_headers()
    assert headers.get("Authorization") == "Bearer secret_12345"

    redacted = RequestBuilder.redact_headers(headers)
    assert redacted.get("Authorization") == "Bearer ********"


def test_auth_api_key():
    os.environ["MY_API_KEY"] = "key_999"
    cfg = ProjectConfig()
    cfg.auth = AuthConfig(type="api_key", api_key_name="X-Custom-Key", api_key_env="MY_API_KEY", api_key_in="header")

    headers = cfg.auth.get_headers()
    assert headers.get("X-Custom-Key") == "key_999"

    redacted = RequestBuilder.redact_headers(headers)
    assert redacted.get("X-Custom-Key") == "********"


def test_auth_basic():
    os.environ["MY_USER"] = "alice"
    os.environ["MY_PASS"] = "secret_pass"
    cfg = ProjectConfig()
    cfg.auth = AuthConfig(type="basic", username_env="MY_USER", password_env="MY_PASS")

    basic_auth = cfg.auth.get_basic_auth()
    assert basic_auth == ("alice", "secret_pass")
