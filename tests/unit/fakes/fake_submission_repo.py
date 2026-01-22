from uuid import UUID
from apps.domain.entities.submission import Submission
from apps.domain.enums.judge_status import JudgeStatus


class FakeSubmissionRepository:
    def __init__(self):
        self.storage: dict[UUID, Submission] = {}

    def add(self, submission: Submission) -> Submission:
        self.storage[submission.id] = submission
        return submission

    def get_by_id(self, submission_id: UUID) -> Submission | None:
        return self.storage.get(submission_id)

    def update(self, submission: Submission) -> Submission:
        self.storage[submission.id] = submission
        return submission

    def reset_for_rejudge(self, submission_id: UUID):
        submission = self.storage.get(submission_id)
        if not submission:
            return None

        submission.status = JudgeStatus.PENDING
        submission.output = None
        submission.execution_time_ms = None
        return submission
