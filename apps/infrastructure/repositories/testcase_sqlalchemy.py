from sqlalchemy.orm import Session

from apps.domain.entities.testcase import TestCase
from apps.domain.interfaces.testcase_repository import TestCaseRepository
from apps.infrastructure.db.models.testcase import TestCaseModel


class TestCaseSQLAlchemyRepository(TestCaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def bulk_create(self, testcases: list[TestCase]) -> list[TestCase]:
        models = [
            TestCaseModel(
                problem_id=tc.problem_id,
                input_data=tc.input_data,
                expected_output=tc.expected_output,
            )
            for tc in testcases
        ]

        self.session.add_all(models)
        self.session.commit()

        return [
            TestCase(
                id=m.id,
                problem_id=m.problem_id,
                input_data=m.input_data,
                expected_output=m.expected_output,
            )
            for m in models
        ]
    
    def list_by_problem_id(self, problem_id: int) -> list[TestCase]:
        """List testcases for a specific problem"""
        models = (
            self.session
            .query(TestCaseModel)
            .filter(TestCaseModel.problem_id == problem_id)
            .all()
        )
        
        return [
            TestCase(
                id=m.id,
                problem_id=m.problem_id,
                input_data=m.input_data,
                expected_output=m.expected_output,
            )
            for m in models
        ]