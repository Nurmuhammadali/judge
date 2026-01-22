# domain/interfaces/judge_submission_repository.py
from abc import ABC, abstractmethod
from uuid import UUID

from apps.domain.enums.judge_status import JudgeStatus


class JudgeSubmissionRepository(ABC):
    @abstractmethod
    def mark_running(self, submission_id: UUID): ...

    @abstractmethod
    def mark_failed(
        self,
        submission_id: UUID,
        reason: str,
        status: JudgeStatus = JudgeStatus.WRONG_ANSWER,
    ): ...

    @abstractmethod
    def mark_success(self, submission_id: UUID): ...

    @abstractmethod
    def save_result(
        self,
        submission_id: UUID,
        *,
        testcase_id: UUID,
        output: str,
        execution_time_ms: int,
        is_correct: bool,
    ): ...
