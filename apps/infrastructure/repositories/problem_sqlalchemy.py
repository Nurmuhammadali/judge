from sqlalchemy.orm import Session

from apps.domain.entities.problem import Problem
from apps.domain.interfaces.problem_repository import ProblemRepository
from apps.infrastructure.db.models.problem import ProblemModel


class ProblemSQLAlchemyRepository(ProblemRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, problem_id: int) -> Problem | None:
        model = self.session.get(ProblemModel, problem_id)
        if not model:
            return None

        return Problem(
            id=model.id,
            title=model.title,
            description=model.description,
            input_description=model.input_description,
            output_description=model.output_description,
            constraints=model.constraints,
            time_limit_sec=model.time_limit_sec,
            memory_limit_mb=model.memory_limit_mb,
            created_at=model.created_at,
        )

    def list(self) -> list[Problem]:
        return [
            Problem(
                id=m.id,
                title=m.title,
                description=m.description,
                input_description=m.input_description,
                output_description=m.output_description,
                constraints=m.constraints,
                time_limit_sec=m.time_limit_sec,
                memory_limit_mb=m.memory_limit_mb,
                created_at=m.created_at,
            )
            for m in self.session.query(ProblemModel).all()
        ]

    def create(self, problem: Problem) -> Problem:
        model = ProblemModel(
            title=problem.title,
            description=problem.description,
            input_description=problem.input_description,
            output_description=problem.output_description,
            constraints=problem.constraints,
            time_limit_sec=problem.time_limit_sec,
            memory_limit_mb=problem.memory_limit_mb,
        )
        self.session.add(model)
        self.session.commit()

        return self.get_by_id(model.id)
