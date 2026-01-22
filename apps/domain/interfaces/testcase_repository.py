from typing import Protocol
from apps.domain.entities.testcase import TestCase


class TestCaseRepository(Protocol):
    def list_by_problem_id(self, problem_id: int) -> list[TestCase]: ...
    def bulk_create(self, testcases: list[TestCase]) -> list[TestCase]: ...
