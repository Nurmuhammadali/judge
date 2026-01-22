from uuid import uuid4
from datetime import datetime

from apps.domain.entities.submission import Submission
from apps.domain.enums.judge_status import JudgeStatus
from apps.domain.entities.testcase import TestCase

from apps.infrastructure.repositories.submission_sqlalchemy import (
    SubmissionSQLAlchemyRepository,
)
from apps.infrastructure.repositories.testcase_sqlalchemy import (
    TestCaseSQLAlchemyRepository,
)
from apps.services.judge_service import JudgeService

from tests.integration.fakes.fake_runner import FakeRunner


def test_judge_service_accepted(db):
    submission_repo = SubmissionSQLAlchemyRepository(db)
    testcase_repo = TestCaseSQLAlchemyRepository(db)

    # Testcase'lar
    testcase_repo.bulk_create([
        TestCase(
            id=0,
            problem_id=1,
            input_data="1\n",
            expected_output="1\n",
        ),
        TestCase(
            id=0,
            problem_id=1,
            input_data="2\n",
            expected_output="2\n",
        ),
    ])

    submission = Submission(
        id=uuid4(),
        problem_id=1,
        language="python",
        source_code="print(input())",
        status=JudgeStatus.PENDING,
        created_at=datetime.utcnow(),
    )

    submission_repo.add(submission)

    runner = FakeRunner(outputs=["1\n", "2\n"])
    service = JudgeService(submission_repo, testcase_repo, runner)

    service.run_submission(submission.id)

    result = submission_repo.get_by_id(submission.id)

    assert result.status == JudgeStatus.ACCEPTED
    assert result.execution_time_ms == 20


def test_judge_service_wrong_answer(db):
    submission_repo = SubmissionSQLAlchemyRepository(db)
    testcase_repo = TestCaseSQLAlchemyRepository(db)

    testcase_repo.bulk_create([
        TestCase(
            id=0,
            problem_id=1,
            input_data="1\n",
            expected_output="1\n",
        ),
    ])

    submission = Submission(
        id=uuid4(),
        problem_id=1,
        language="python",
        source_code="print(input())",
        status=JudgeStatus.PENDING,
        created_at=datetime.utcnow(),
    )

    submission_repo.add(submission)

    runner = FakeRunner(outputs=["999\n"])
    service = JudgeService(submission_repo, testcase_repo, runner)

    service.run_submission(submission.id)

    result = submission_repo.get_by_id(submission.id)

    assert result.status == JudgeStatus.WRONG_ANSWER
