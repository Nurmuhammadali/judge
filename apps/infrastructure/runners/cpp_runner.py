from apps.domain.interfaces.code_runner import CodeRunner, RunResult
from apps.infrastructure.runners.docker_runner import DockerRunner


class CppRunner(CodeRunner):
    """
    C++17 runner using Docker sandbox.
    """

    def __init__(self):
        self.docker = DockerRunner()

    def run(self, *, source_code: str, input_data: str) -> RunResult:
        output, exec_time = self.docker.run_cpp(
            source_code=source_code,
            input_data=input_data,
        )
        return RunResult(
            output=output,
            execution_time_ms=exec_time,
        )
