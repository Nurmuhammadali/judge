from uuid import UUID

from apps.infrastructure.db.session import SessionLocal
from apps.infrastructure.repositories.submission_sqlalchemy import SubmissionSQLAlchemyRepository
from apps.infrastructure.repositories.testcase_sqlalchemy import TestCaseSQLAlchemyRepository
from apps.infrastructure.runners.factory import RunnerFactory
from apps.services.judge_service import JudgeService
from core.celery_app import celery_app


@celery_app.task(
    name="apps.tasks.judge_tasks.run_submission_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=3,
    retry_kwargs={"max_retries": 3},
)
def run_submission_task(self, submission_id: str):
    db = SessionLocal()

    try:
        submission_repo = SubmissionSQLAlchemyRepository(db)
        testcase_repo = TestCaseSQLAlchemyRepository(db)
        
        # Get submission first to determine language
        submission = submission_repo.get_by_id(UUID(submission_id))
        if not submission:
            raise ValueError(f"Submission {submission_id} not found")
        
        # Create appropriate runner based on submission language
        runner = RunnerFactory.create(submission.language)

        service = JudgeService(
            submission_repo=submission_repo,
            testcase_repo=testcase_repo,
            runner=runner,
        )

        service.run_submission(UUID(submission_id))
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

