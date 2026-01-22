from fastapi import Depends
from sqlalchemy.orm import Session

from apps.domain.interfaces.code_runner import CodeRunner
from apps.domain.interfaces.submission_repository import SubmissionRepository
from apps.domain.interfaces.testcase_repository import TestCaseRepository
from apps.infrastructure.db.session import SessionLocal
from apps.infrastructure.repositories.submission_sqlalchemy import (
    SubmissionSQLAlchemyRepository,
)
from apps.infrastructure.repositories.testcase_sqlalchemy import TestCaseSQLAlchemyRepository
from apps.infrastructure.runners.python_runner import PythonRunner
from apps.services.judge_service import JudgeService
from apps.services.testcase_generation_service import TestCaseGenerationService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_judge_service(db=Depends(get_db)) -> JudgeService:
    submission_repo: SubmissionRepository = SubmissionSQLAlchemyRepository(db)
    testcase_repo: TestCaseRepository = TestCaseSQLAlchemyRepository(db)
    runner: CodeRunner = PythonRunner()

    return JudgeService(
        submission_repo=submission_repo,
        testcase_repo=testcase_repo,
        runner=runner,
    )

def get_testcase_generation_service(db=Depends(get_db)):
    repo = TestCaseSQLAlchemyRepository(db)
    return TestCaseGenerationService(repo)