from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.services.problem_service import ProblemService
from apps.infrastructure.repositories.problem_sqlalchemy import ProblemSQLAlchemyRepository
from apps.dependencies import get_db

router = APIRouter(prefix="/problems", tags=["Problems"])


class CreateProblemRequest(BaseModel):
    title: str
    description: str
    input_description: str
    output_description: str
    constraints: str | None = None
    time_limit_sec: int = 2
    memory_limit_mb: int = 256


@router.post("")
def create_problem(
        payload: CreateProblemRequest,
        db=Depends(get_db),
):
    service = ProblemService(ProblemSQLAlchemyRepository(db))
    return service.create_problem(**payload.dict())


@router.get("")
def list_problems(db=Depends(get_db)):
    service = ProblemService(ProblemSQLAlchemyRepository(db))
    return service.list_problems()
