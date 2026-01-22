from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from apps.dependencies import get_testcase_generation_service

router = APIRouter(prefix="/testcases", tags=["TestCases"])


class GenerateIntTestCaseRequest(BaseModel):
    problem_id: int
    count: int
    min_value: int
    max_value: int
    seed: int | None = None


@router.post("/generate/int", status_code=status.HTTP_201_CREATED)
def generate_int_testcases(
    payload: GenerateIntTestCaseRequest,
    service=Depends(get_testcase_generation_service),
):
    return service.generate_simple_int_cases(
        problem_id=payload.problem_id,
        count=payload.count,
        min_value=payload.min_value,
        max_value=payload.max_value,
        seed=payload.seed,
    )
