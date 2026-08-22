from pathlib import Path
import pytest
from typer.testing import CliRunner
from api_tester.cli.commands import app
from api_tester.core.constants import ExitCode
from tests.fixtures.mock_server import run_mock_server

runner = CliRunner()


@pytest.fixture(scope="module")
def running_server():
    server = run_mock_server(host="127.0.0.1", port=8899)
    yield "http://127.0.0.1:8899"
    server.shutdown()


def test_cli_validate_success():
    root = Path(__file__).resolve().parent.parent.parent
    spec_path = str(root / "examples" / "openapi.yaml")
    res = runner.invoke(app, ["validate", spec_path])
    assert res.exit_code == ExitCode.SUCCESS
    assert "Specification is valid" in res.stdout


def test_cli_validate_failure():
    res = runner.invoke(app, ["validate", "/non/existent/spec.yaml"])
    assert res.exit_code == ExitCode.SPEC_ERROR


def test_cli_discover():
    root = Path(__file__).resolve().parent.parent.parent
    spec_path = str(root / "examples" / "openapi.yaml")
    res = runner.invoke(app, ["discover", spec_path])
    assert res.exit_code == ExitCode.SUCCESS
    assert "/users" in res.stdout
    assert "/products" in res.stdout


def test_cli_generate():
    root = Path(__file__).resolve().parent.parent.parent
    spec_path = str(root / "examples" / "openapi.yaml")
    res = runner.invoke(app, ["generate", spec_path, "--suite", "smoke"])
    assert res.exit_code == ExitCode.SUCCESS
    assert "Generated Test Cases" in res.stdout


def test_cli_run_success(running_server, tmp_path):
    root = Path(__file__).resolve().parent.parent.parent
    spec_path = str(root / "examples" / "openapi.yaml")
    out_dir = str(tmp_path / "cli_reports")

    res = runner.invoke(app, [
        "run",
        spec_path,
        "--base-url", running_server,
        "--output", out_dir,
        "--method", "GET",
        "--workers", "1",
    ])
    assert res.exit_code in (ExitCode.SUCCESS, ExitCode.TESTS_FAILED)
    assert "Test Execution Summary" in res.stdout
    assert "Pass Rate" in res.stdout
