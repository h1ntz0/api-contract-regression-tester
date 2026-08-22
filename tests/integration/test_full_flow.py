import os
from pathlib import Path
import pytest
from api_tester.config.loader import load_config
from api_tester.specification.loader import SpecificationLoader
from api_tester.specification.parser import OpenApiParser
from api_tester.generator.generator import TestGenerator
from api_tester.execution.runner import TestRunner
from api_tester.reporting.aggregator import ResultAggregator
from api_tester.reporting.html import ReportWriter
from tests.fixtures.mock_server import run_mock_server


@pytest.fixture(scope="module")
def mock_api():
    server = run_mock_server(host="127.0.0.1", port=8888)
    yield "http://127.0.0.1:8888"
    server.shutdown()


def test_full_regression_flow(mock_api, tmp_path):
    root = Path(__file__).resolve().parent.parent.parent
    loader = SpecificationLoader()
    raw = loader.load(str(root / "examples" / "openapi.yaml"))
    parser = OpenApiParser(raw)
    spec = parser.parse()

    cfg = load_config(str(root / "examples" / "config.yaml"))
    cfg.report.output_dir = str(tmp_path / "reports")

    generator = TestGenerator(cfg.testing)
    plan = generator.generate(spec)

    runner = TestRunner(cfg, mock_api)
    results = runner.run_plan(plan)

    report = ResultAggregator.aggregate(
        results=results,
        project_name=cfg.name,
        base_url=mock_api,
        spec_source="examples/openapi.yaml",
        total_duration_sec=1.5,
    )

    created = ReportWriter.write_all(report, cfg.report)

    assert os.path.exists(created["json"])
    assert os.path.exists(created["junit"])
    assert os.path.exists(created["html"])

    assert report.summary.total_tests > 0
    assert report.summary.passed > 0
