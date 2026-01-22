# apps/services/judge_service.py
from uuid import UUID, uuid4
from datetime import datetime

from apps.domain.entities.submission import Submission
from apps.domain.enums.judge_status import JudgeStatus


class JudgeService:
    def __init__(
        self,
        *,
        submission_repo,
        testcase_repo,
        runner,
    ):
        self.submission_repo = submission_repo
        self.testcase_repo = testcase_repo
        self.runner = runner

    def run_submission(self, submission_id: UUID) -> None:
        submission = self.submission_repo.get_by_id(submission_id)
        if not submission:
            raise ValueError("Submission not found")

        self.submission_repo.mark_running(submission_id)

        testcases = self.testcase_repo.list_by_problem_id(
            submission.problem_id
        )

        for tc in testcases:
            result = self.runner.run(
                source_code=submission.source_code,   # 👈 KOD MANA SHU YERDAN
                input_data=tc.input_data,
            )

            is_correct = result.output.strip() == tc.expected_output.strip()

            self.submission_repo.save_result(
                submission_id=submission_id,
                testcase_id=tc.id,
                output=result.output,
                execution_time_ms=result.execution_time_ms,
                is_correct=is_correct,
            )

            if not is_correct:
                self.submission_repo.mark_failed(
                    submission_id,
                    reason=f"Wrong answer on testcase {tc.id}",
                )
                return

        self.submission_repo.mark_success(submission_id)
    
    def list_submissions(
        self,
        problem_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Submission]:
        """List submissions, optionally filtered by problem_id"""
        return self.submission_repo.list(
            problem_id=problem_id,
            limit=limit,
            offset=offset,
        )
    
    def create_submission(
        self,
        *,
        problem_id: int,
        language: str,
        source_code: str,
    ) -> Submission:
        """Create a new submission"""
        submission = Submission(
            id=uuid4(),
            problem_id=problem_id,
            language=language,
            source_code=source_code,
            status=JudgeStatus.PENDING,
            created_at=datetime.utcnow(),
        )
        return self.submission_repo.save(submission)
    
    def rejudge(self, submission_id: UUID) -> Submission | None:
        """Reset submission for rejudging"""
        return self.submission_repo.reset_for_rejudge(submission_id)
