from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query

from apps.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
    SubmissionListItem,
    SubmissionListResponse,
)
from apps.services.judge_service import JudgeService
from apps.dependencies import get_judge_service
from apps.tasks.judge_tasks import run_submission_task
router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_submission(
    payload: SubmissionCreate,
    service: JudgeService = Depends(get_judge_service),
):
    submission = service.create_submission(
        problem_id=payload.problem_id,
        language=payload.language.value,
        source_code=payload.source_code,
    )
    run_submission_task.delay(str(submission.id))
    return submission


@router.post(
    "/{submission_id}/rejudge",
    response_model=SubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def rejudge_submission(
    submission_id: UUID,
    service: JudgeService = Depends(get_judge_service),
):
    submission = service.rejudge(submission_id)
    if not submission:
        raise HTTPException(
            status_code=404,
            detail="Submission not found or already running",
        )

    run_submission_task.delay(str(submission.id))
    return submission


@router.get(
    "",
    response_model=SubmissionListResponse,
    status_code=status.HTTP_200_OK,
)
def list_submissions(
    problem_id: int | None = Query(None, description="Filter by problem ID"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of submissions to return"),
    offset: int = Query(0, ge=0, description="Number of submissions to skip"),
    service: JudgeService = Depends(get_judge_service),
):
    """List submissions, optionally filtered by problem_id"""
    submissions = service.list_submissions(
        problem_id=problem_id,
        limit=limit,
        offset=offset,
    )
    
    # Convert to list items (without source_code for security)
    list_items = [
        SubmissionListItem(
            id=sub.id,
            problem_id=sub.problem_id,
            language=sub.language,
            status=sub.status,
            execution_time_ms=sub.execution_time_ms,
            created_at=sub.created_at,
            judged_at=sub.judged_at,
        )
        for sub in submissions
    ]
    
    return SubmissionListResponse(
        submissions=list_items,
        total=len(list_items),  # TODO: Add total count from database
        limit=limit,
        offset=offset,
    )
