import random
from typing import Iterable

from apps.domain.entities.testcase import TestCase
from apps.domain.interfaces.testcase_repository import TestCaseRepository


class TestCaseGenerationService:
    """
    Responsible for generating and persisting test cases for a problem.
    """

    def __init__(self, testcase_repo: TestCaseRepository):
        self.testcase_repo = testcase_repo

    def generate_simple_int_cases(
        self,
        *,
        problem_id: int,
        count: int,
        min_value: int,
        max_value: int,
        seed: int | None = None,
    ) -> list[TestCase]:
        """
        Example generator:
        input: single integer
        output: same integer (identity problem)
        """

        if seed is not None:
            random.seed(seed)

        testcases: list[TestCase] = []

        for _ in range(count):
            x = random.randint(min_value, max_value)

            testcases.append(
                TestCase(
                    id=0,  # will be set by DB
                    problem_id=problem_id,
                    input_data=f"{x}\n",
                    expected_output=f"{x}\n",
                )
            )

        return self.testcase_repo.bulk_create(testcases)
