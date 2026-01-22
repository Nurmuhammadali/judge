# apps/infrastructure/runners/python_runner.py
from apps.domain.interfaces.code_runner import CodeRunner, RunResult
from apps.infrastructure.runners.docker_runner import DockerRunner


class PythonRunner(CodeRunner):
    def __init__(self):
        self.docker_runner = DockerRunner()

    def run(self, *, source_code: str, input_data: str) -> RunResult:
        output, exec_time = self.docker_runner.run_python(
            source_code=source_code,
            input_data=input_data,
        )
        return RunResult(
            output=output,
            execution_time_ms=exec_time,
        )
