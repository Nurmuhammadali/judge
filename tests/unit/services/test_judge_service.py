from uuid import uuid4

from apps.domain.entities.submission import Submission
from apps.domain.enums.judge_status import JudgeStatus
from apps.domain.entities.testcase import TestCase
from apps.services.judge_service import JudgeService

from tests.unit.fakes.fake_submission_repo import FakeSubmissionRepository
from tests.unit.fakes.fake_testcase_repo import FakeTestCaseRepository
from tests.unit.fakes.fake_runner import FakeRunner


def test_submission_accepted():
    submission_repo = FakeSubmissionRepository()
    testcase_repo = FakeTestCaseRepository(
        testcases=[
            TestCase(
                id=1,
                problem_id=1,
                input_data="1\n",
                expected_output="1\n",
            ),
            TestCase(
                id=2,
                problem_id=1,
                input_data="2\n",
                expected_output="2\n",
            ),
        ]
    )

    runner = FakeRunner(outputs=["1\n", "2\n"])

    service = JudgeService(
        submission_repo=submission_repo,
        testcase_repo=testcase_repo,
        runner=runner,
    )

    submission = Submission(
        id=uuid4(),
        problem_id=1,
        language="python",
        source_code="print(input())",
        status=JudgeStatus.PENDING,
        created_at=None,
    )

    submission_repo.add(submission)

    service.run_submission(submission.id)

    result = submission_repo.get_by_id(submission.id)

    assert result.status == JudgeStatus.ACCEPTED
    assert result.execution_time_ms == 10



def test_submission_wrong_answer():
    submission_repo = FakeSubmissionRepository()
    testcase_repo = FakeTestCaseRepository(
        testcases=[
            TestCase(
                id=1,
                problem_id=1,
                input_data="1\n",
                expected_output="1\n",
                type=TestCaseType.HIDDEN,
            ),
        ]
    )

    runner = FakeRunner(outputs=["999\n"])

    service = JudgeService(
        submission_repo=submission_repo,
        testcase_repo=testcase_repo,
        runner=runner,
    )

    submission = Submission(
        id=uuid4(),
        problem_id=1,
        language="python",
        source_code="print(input())",
        status=JudgeStatus.PENDING,
        created_at=None,
    )

    submission_repo.add(submission)
    service.run_submission(submission.id)

    result = submission_repo.get_by_id(submission.id)

    assert result.status == JudgeStatus.WRONG_ANSWER
