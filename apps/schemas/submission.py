from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from apps.domain.enums.judge_status import JudgeStatus
from apps.domain.enums.language import Language


class SubmissionCreate(BaseModel):
    problem_id: int = Field(..., gt=0)
    language: Language
    source_code: str = Field(..., min_length=1)


class SubmissionResponse(BaseModel):
    id: UUID
    status: JudgeStatus

    class Config:
        from_attributes = True


class SubmissionListItem(BaseModel):
    """Submission list item - user uchun ko'rsatish"""
    id: UUID
    problem_id: int
    language: str
    status: JudgeStatus
    execution_time_ms: int | None = None
    created_at: datetime
    judged_at: datetime | None = None

    class Config:
        from_attributes = True


class SubmissionListResponse(BaseModel):
    """Submission list response"""
    submissions: list[SubmissionListItem]
    total: int
    limit: int
    offset: int
