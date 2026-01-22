from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from apps.domain.entities.submission import Submission
from apps.domain.enums.judge_status import JudgeStatus
from apps.domain.interfaces.judge_submission_repository import JudgeSubmissionRepository
from apps.domain.interfaces.submission_repository import SubmissionRepository
from apps.infrastructure.db.models.submission import SubmissionModel


class SubmissionSQLAlchemyRepository(SubmissionRepository, JudgeSubmissionRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, submission: Submission) -> Submission:
        model = SubmissionModel(
            id=submission.id,
            problem_id=submission.problem_id,
            language=submission.language,
            source_code=submission.source_code,
            status=submission.status,
            execution_time_ms=submission.execution_time_ms,
            output=submission.output,
        )
        self.session.add(model)
        self.session.commit()
        return submission
    
    def save(self, submission: Submission) -> Submission:
        """Save submission (alias for add)"""
        return self.add(submission)

    def get_by_id(self, submission_id: UUID) -> Submission | None:
        model = (
            self.session
            .query(SubmissionModel)
            .filter(SubmissionModel.id == submission_id)
            .one_or_none()
        )
        if not model:
            return None

        return Submission(
            id=model.id,
            problem_id=model.problem_id,
            language=model.language,
            source_code=model.source_code,
            status=model.status,
            created_at=model.created_at,
            execution_time_ms=model.execution_time_ms,
            output=model.output,
            judged_at=model.judged_at,
            rejudge_count=model.rejudge_count,
        )

    def update(self, submission: Submission) -> Submission:
        model = self.session.get(SubmissionModel, submission.id)
        if not model:
            raise ValueError("Submission not found")

        model.status = submission.status
        model.execution_time_ms = submission.execution_time_ms
        model.output = submission.output
        model.judged_at = submission.judged_at
        model.rejudge_count = submission.rejudge_count

        self.session.commit()
        return submission

    def reset_for_rejudge(self, submission_id: UUID) -> Submission | None:
        model = self.session.get(SubmissionModel, submission_id)
        if not model or model.status == JudgeStatus.RUNNING:
            return None

        model.status = JudgeStatus.PENDING
        model.output = None
        model.execution_time_ms = None
        model.rejudge_count = (model.rejudge_count or 0) + 1
        model.judged_at = None

        self.session.commit()
        return self.get_by_id(submission_id)
    
    def list(self, problem_id: int | None = None, limit: int = 100, offset: int = 0) -> list[Submission]:
        query = self.session.query(SubmissionModel)
        
        if problem_id is not None:
            query = query.filter(SubmissionModel.problem_id == problem_id)
        
        models = query.order_by(SubmissionModel.created_at.desc()).limit(limit).offset(offset).all()
        
        return [
            Submission(
                id=model.id,
                problem_id=model.problem_id,
                language=model.language,
                source_code=model.source_code,
                status=model.status,
                created_at=model.created_at,
                execution_time_ms=model.execution_time_ms,
                output=model.output,
                judged_at=model.judged_at,
                rejudge_count=model.rejudge_count,
            )
            for model in models
        ]
    
    # JudgeSubmissionRepository methods
    def mark_running(self, submission_id: UUID):
        """Mark submission as running"""
        model = self.session.get(SubmissionModel, submission_id)
        if not model:
            raise ValueError("Submission not found")
        
        model.status = JudgeStatus.RUNNING
        self.session.commit()
    
    def mark_failed(self, submission_id: UUID, reason: str):
        """Mark submission as failed with reason"""
        model = self.session.get(SubmissionModel, submission_id)
        if not model:
            raise ValueError("Submission not found")
        
        model.status = JudgeStatus.WRONG_ANSWER
        model.output = reason
        model.judged_at = datetime.utcnow()
        self.session.commit()
    
    def mark_success(self, submission_id: UUID):
        """Mark submission as accepted/successful"""
        model = self.session.get(SubmissionModel, submission_id)
        if not model:
            raise ValueError("Submission not found")
        
        model.status = JudgeStatus.ACCEPTED
        model.judged_at = datetime.utcnow()
        self.session.commit()
    
    def save_result(
        self,
        submission_id: UUID,
        *,
        testcase_id: UUID,
        output: str,
        execution_time_ms: int,
        is_correct: bool,
    ):
        """
        Save testcase result.
        Note: testcase_id is accepted but not stored in submission model.
        This method updates execution_time_ms and output for the submission.
        """
        model = self.session.get(SubmissionModel, submission_id)
        if not model:
            raise ValueError("Submission not found")
        
        # Update execution time (keep the maximum so far)
        if model.execution_time_ms is None or execution_time_ms > model.execution_time_ms:
            model.execution_time_ms = execution_time_ms
        
        # Update output with the latest testcase result
        model.output = output
        
        self.session.commit()