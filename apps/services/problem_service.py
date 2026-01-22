from datetime import datetime
from apps.domain.entities.problem import Problem
from apps.domain.interfaces.problem_repository import ProblemRepository


class ProblemService:
    def __init__(self, repo: ProblemRepository):
        self.repo = repo

    def create_problem(
        self,
        *,
        title: str,
        description: str,
        input_description: str,
        output_description: str,
        constraints: str | None,
        time_limit_sec: int,
        memory_limit_mb: int,
    ) -> Problem:
        problem = Problem(
            id=0,
            title=title,
            description=description,
            input_description=input_description,
            output_description=output_description,
            constraints=constraints,
            time_limit_sec=time_limit_sec,
            memory_limit_mb=memory_limit_mb,
            created_at=datetime.utcnow(),
        )
        return self.repo.create(problem)

    def list_problems(self) -> list[Problem]:
        return self.repo.list()
