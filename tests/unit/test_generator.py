from api_tester.config.models import TestingConfig
from api_tester.generator.data_generator import DataGenerator
from api_tester.generator.generator import TestGenerator
from api_tester.specification.loader import SpecificationLoader
from api_tester.specification.parser import OpenApiParser


def test_data_generator_primitives():
    assert isinstance(DataGenerator.generate_valid_data({"type": "string"}), str)
    assert isinstance(DataGenerator.generate_valid_data({"type": "integer"}), int)
    assert isinstance(DataGenerator.generate_valid_data({"type": "boolean"}), bool)
    assert isinstance(DataGenerator.generate_valid_data({"type": "number"}), float)
    assert isinstance(DataGenerator.generate_valid_data({"type": "array", "items": {"type": "string"}}), list)


def test_data_generator_enum():
    val = DataGenerator.generate_valid_data({"type": "string", "enum": ["apple", "banana"]})
    assert val in ("apple", "banana")


import os
from pathlib import Path

def test_generator_from_examples():
    root = Path(__file__).resolve().parent.parent.parent
    loader = SpecificationLoader()
    raw = loader.load(str(root / "examples" / "openapi.yaml"))
    parser = OpenApiParser(raw)
    spec = parser.parse()

    gen = TestGenerator(TestingConfig(positive=True, negative=True))
    plan = gen.generate(spec)

    assert plan.total_cases > 0
    test_ids = [tc.id for tc in plan.test_cases]
    assert len(test_ids) == len(set(test_ids))  # unique IDs

    # Check method filter
    plan_get = gen.generate(spec, filter_method="GET")
    assert all(tc.method == "GET" for tc in plan_get.test_cases)
