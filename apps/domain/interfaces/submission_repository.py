from typing import Protocol
from uuid import UUID

from apps.domain.entities.submission import Submission


class SubmissionRepository(Protocol):
    """
    Repository interface for Submission entity.
    Infrastructure layer will implement this.
    """

    def save(self, submission: Submission) -> Submission:
        ...

    def get_by_id(self, submission_id: UUID) -> Submission | None:
        ...

    def update(self, submission: Submission) -> Submission:
        ...

    def reset_for_rejudge(self, submission_id: UUID) -> Submission | None:
        ...
    
    def list(self, problem_id: int | None = None, limit: int = 100, offset: int = 0) -> list[Submission]:
        ...