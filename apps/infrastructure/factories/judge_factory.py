# infrastructure/factories/judge_factory.py

from apps.infrastructure.db.session import SessionLocal
from apps.infrastructure.repositories.submission_sqlalchemy import (
    SubmissionSQLAlchemyRepository,
)
from apps.infrastructure.repositories.testcase_sqlalchemy import (
    TestCaseSQLAlchemyRepository,
)
from apps.infrastructure.runners.python_runner import PythonRunner
from apps.services.judge_service import JudgeService


def get_judge_service_for_worker() -> JudgeService:
    session = SessionLocal()

    submission_repo = SubmissionSQLAlchemyRepository(session)
    testcase_repo = TestCaseSQLAlchemyRepository(session)
    runner = PythonRunner()

    return JudgeService(
        submission_repo=submission_repo,
        testcase_repo=testcase_repo,
        runner=runner,
    ), session
