from dataclasses import dataclass


@dataclass(frozen=True)
class TestCase:
    id: int
    problem_id: int
    input_data: str
    expected_output: str
