from uuid import UUID
from unittest.mock import MagicMock

from apps.domain.enums.judge_status import JudgeStatus


def test_create_submission_api(client, mocker):
    # 🔧 Mock JudgeService
    fake_submission = MagicMock()
    fake_submission.id = UUID("11111111-1111-1111-1111-111111111111")
    fake_submission.status = JudgeStatus.PENDING

    mock_service = MagicMock()
    mock_service.create_submission.return_value = fake_submission

    # 🔧 Dependency override
    mocker.patch(
        "api.v1.submissions.get_judge_service",
        return_value=mock_service,
    )

    payload = {
        "problem_id": 1,
        "language": "python",
        "source_code": "print(input())",
    }

    response = client.post("/api/v1/submissions", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == str(fake_submission.id)
    assert data["status"] == "PENDING"

    mock_service.create_submission.assert_called_once()


def test_rejudge_submission_api(client, mocker):
    fake_submission = MagicMock()
    fake_submission.id = UUID("22222222-2222-2222-2222-222222222222")
    fake_submission.status = JudgeStatus.PENDING

    mock_service = MagicMock()
    mock_service.rejudge.return_value = fake_submission

    mocker.patch(
        "api.v1.submissions.get_judge_service",
        return_value=mock_service,
    )

    mock_task = mocker.patch(
        "api.v1.submissions.run_submission_task.delay"
    )

    response = client.post(
        f"/api/v1/submissions/{fake_submission.id}/rejudge"
    )

    assert response.status_code == 202

    mock_service.rejudge.assert_called_once()
    mock_task.assert_called_once_with(str(fake_submission.id))
