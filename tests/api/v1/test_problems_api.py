from unittest.mock import MagicMock


def test_create_problem_api(client, mocker):
    # Arrange: mock ProblemService
    mock_service = MagicMock()
    fake_problem = {
        "id": 1,
        "title": "Two Sum",
        "description": "Find two numbers that add up to target",
        "input_description": "n and array",
        "output_description": "indices",
        "constraints": None,
        "time_limit_sec": 2,
        "memory_limit_mb": 256,
        "created_at": "2024-01-01T00:00:00Z",
    }
    mock_service.create_problem.return_value = fake_problem

    # Patch dependency creation in route module
    mocker.patch(
        "api.v1.problems.ProblemService",
        return_value=mock_service,
    )

    payload = {
        "title": "Two Sum",
        "description": "Find two numbers that add up to target",
        "input_description": "n and array",
        "output_description": "indices",
        "constraints": None,
        "time_limit_sec": 2,
        "memory_limit_mb": 256,
    }

    # Act
    resp = client.post("/api/v1/problems", json=payload)

    # Assert
    assert resp.status_code == 200 or resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    mock_service.create_problem.assert_called_once_with(**payload)


def test_list_problems_api(client, mocker):
    # Arrange
    mock_service = MagicMock()
    fake_list = [
        {
            "id": 1,
            "title": "Two Sum",
            "description": "...",
            "input_description": "...",
            "output_description": "...",
            "constraints": None,
            "time_limit_sec": 2,
            "memory_limit_mb": 256,
            "created_at": "2024-01-01T00:00:00Z",
        },
        {
            "id": 2,
            "title": "Reverse String",
            "description": "...",
            "input_description": "...",
            "output_description": "...",
            "constraints": None,
            "time_limit_sec": 1,
            "memory_limit_mb": 64,
            "created_at": "2024-01-02T00:00:00Z",
        },
    ]
    mock_service.list_problems.return_value = fake_list

    mocker.patch(
        "api.v1.problems.ProblemService",
        return_value=mock_service,
    )

    # Act
    resp = client.get("/api/v1/problems")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) == 2
    mock_service.list_problems.assert_called_once()


def test_create_problem_validates_required_fields(client, mocker):
    # Even with service mocked, FastAPI should validate body
    mock_service = MagicMock()
    mocker.patch("api.v1.problems.ProblemService", return_value=mock_service)

    # Missing required field 'title'
    payload = {
        "description": "desc",
        "input_description": "in",
        "output_description": "out",
    }

    resp = client.post("/api/v1/problems", json=payload)
    assert resp.status_code == 422


def test_create_problem_passes_db_dependency(client, mocker):
    # Verify that repository/service is constructed (constructor called)
    mock_service_cls = mocker.patch("api.v1.problems.ProblemService")
    mock_instance = MagicMock()
    mock_instance.create_problem.return_value = {"id": 1}
    mock_service_cls.return_value = mock_instance

    # Also spy on repository class so it's constructed
    mock_repo_cls = mocker.patch("api.v1.problems.ProblemSQLAlchemyRepository")

    payload = {
        "title": "A",
        "description": "B",
        "input_description": "C",
        "output_description": "D",
    }

    resp = client.post("/api/v1/problems", json=payload)
    assert resp.status_code in (200, 201)

    # Ensure ProblemService was instantiated with a ProblemSQLAlchemyRepository
    assert mock_service_cls.called
    args, kwargs = mock_service_cls.call_args
    assert len(args) == 1
    assert args[0] is mock_repo_cls.return_value


def test_list_problems_empty(client, mocker):
    mock_service = MagicMock()
    mock_service.list_problems.return_value = []
    mocker.patch("api.v1.problems.ProblemService", return_value=mock_service)

    resp = client.get("/api/v1/problems")
    assert resp.status_code == 200
    assert resp.json() == []
