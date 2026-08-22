from typing import List, Optional
from api_tester.config.models import TestingConfig
from api_tester.generator.models import TestCase, TestPlan
from api_tester.generator.positive import PositiveTestGenerator
from api_tester.generator.negative import NegativeTestGenerator
from api_tester.specification.models import ApiSpecification


class TestGenerator:
    """Generates execution test plans containing positive and negative test cases from OpenAPI models."""

    def __init__(self, testing_config: Optional[TestingConfig] = None):
        self.config = testing_config or TestingConfig()

    def generate(self, spec: ApiSpecification, filter_method: Optional[str] = None, filter_suite: Optional[str] = None) -> TestPlan:
        all_test_cases: List[TestCase] = []
        counter = 1

        for endpoint in spec.endpoints:
            if filter_method and endpoint.method.upper() != filter_method.upper():
                continue

            # 1. Generate Positive Tests
            if self.config.positive:
                pos_tests = PositiveTestGenerator.generate(endpoint, counter)
                counter += len(pos_tests)
                all_test_cases.extend(pos_tests)

            # 2. Generate Negative Tests
            if self.config.negative:
                neg_tests = NegativeTestGenerator.generate(endpoint, counter)
                counter += len(neg_tests)
                all_test_cases.extend(neg_tests)

        # Apply suite filtering if requested
        if filter_suite and filter_suite != "all":
            all_test_cases = [tc for tc in all_test_cases if tc.suite.lower() == filter_suite.lower()]

        return TestPlan(total_cases=len(all_test_cases), test_cases=all_test_cases)
