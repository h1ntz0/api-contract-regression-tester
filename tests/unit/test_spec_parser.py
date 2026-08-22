import pytest
from api_tester.core.exceptions import SpecificationError, ConfigurationError
from api_tester.specification.loader import SpecificationLoader
from api_tester.specification.parser import OpenApiParser
from api_tester.config.loader import load_config
from api_tester.config.models import ProjectConfig


def test_config_loader_default():
    cfg = load_config(None)
    assert isinstance(cfg, ProjectConfig)
    assert cfg.execution.workers == 1
    assert cfg.execution.timeout_read == 30.0


def test_config_loader_file(tmp_path):
    conf_file = tmp_path / "custom_config.yaml"
    conf_file.write_text("""
name: Custom Test
execution:
  workers: 4
  timeout_read: 10
""")
    cfg = load_config(str(conf_file))
    assert cfg.name == "Custom Test"
    assert cfg.execution.workers == 4
    assert cfg.execution.timeout_read == 10.0


def test_config_loader_invalid_file():
    with pytest.raises(ConfigurationError):
        load_config("/non/existent/path.yaml")


def test_spec_loader_empty():
    loader = SpecificationLoader()
    with pytest.raises(SpecificationError):
        loader.load("")


def test_spec_loader_missing_file():
    loader = SpecificationLoader()
    with pytest.raises(SpecificationError):
        loader.load("/path/to/missing_spec.yaml")


def test_spec_parser_invalid_version():
    spec_data = {
        "swagger": "2.0",
        "info": {"title": "Old API", "version": "1.0"},
        "paths": {}
    }
    parser = OpenApiParser(spec_data)
    with pytest.raises(SpecificationError, match="Swagger 2.0 detected"):
        parser.parse()


def test_spec_parser_missing_fields():
    parser = OpenApiParser({"openapi": "3.0.0"})
    with pytest.raises(SpecificationError, match="Missing required field: 'info'"):
        parser.parse()


def test_spec_parser_valid(tmp_path):
    spec_file = tmp_path / "valid_spec.yaml"
    spec_file.write_text("""
openapi: 3.0.1
info:
  title: Test API
  version: 1.2.3
servers:
  - url: https://api.test.com
paths:
  /items:
    get:
      summary: Get Items
      responses:
        '200':
          description: Ok
""")
    loader = SpecificationLoader()
    data = loader.load(str(spec_file))
    parser = OpenApiParser(data)
    spec = parser.parse()

    assert spec.metadata.title == "Test API"
    assert spec.metadata.version == "1.2.3"
    assert len(spec.endpoints) == 1
    assert spec.endpoints[0].id == "GET:/items"
