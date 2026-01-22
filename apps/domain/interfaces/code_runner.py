# apps/domain/interfaces/code_runner.py
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class RunResult:
    output: str
    execution_time_ms: int


class CodeRunner(ABC):
    @abstractmethod
    def run(self, *, source_code: str, input_data: str) -> RunResult:
        pass
