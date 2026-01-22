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

    def list(self, problem_id: int | None = None, limit: int = 100, offset: int = 0) -> list[Submission]:
        submissions = list(self.storage.values())
        if problem_id is not None:
            submissions = [sub for sub in submissions if sub.problem_id == problem_id]
        return submissions[offset:offset + limit]

    def mark_running(self, submission_id: UUID):
        submission = self.storage.get(submission_id)
        if not submission:
            raise ValueError("Submission not found")
        submission.status = JudgeStatus.RUNNING

    def mark_failed(
        self,
        submission_id: UUID,
        reason: str,
        status: JudgeStatus = JudgeStatus.WRONG_ANSWER,
    ):
        submission = self.storage.get(submission_id)
        if not submission:
            raise ValueError("Submission not found")
        submission.status = status
        submission.output = reason

    def mark_success(self, submission_id: UUID):
        submission = self.storage.get(submission_id)
        if not submission:
            raise ValueError("Submission not found")
        submission.status = JudgeStatus.ACCEPTED

    def save_result(
        self,
        submission_id: UUID,
        *,
        testcase_id: UUID,
        output: str,
        execution_time_ms: int,
        is_correct: bool,
    ):
        submission = self.storage.get(submission_id)
        if not submission:
            raise ValueError("Submission not found")
        submission.output = output
        if submission.execution_time_ms is None or execution_time_ms > submission.execution_time_ms:
            submission.execution_time_ms = execution_time_ms
