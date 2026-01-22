from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apps.domain.enums.judge_status import JudgeStatus


@dataclass
class Submission:
    id: UUID
    problem_id: int
    language: str
    source_code: str
    status: JudgeStatus
    created_at: datetime
    execution_time_ms: int | None = None
    output: str | None = None
    judged_at: datetime | None = None
    rejudge_count: int = 0
