from apps.domain.entities.testcase import TestCase


class FakeTestCaseRepository:
    def __init__(self, testcases: list[TestCase]):
        self._testcases = testcases

    def list_by_problem_id(self, problem_id: int) -> list[TestCase]:
        return [tc for tc in self._testcases if tc.problem_id == problem_id]
