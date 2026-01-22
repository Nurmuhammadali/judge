from apps.domain.interfaces.code_runner import CodeRunner, RunResult


class FakeRunner(CodeRunner):
    def __init__(self, outputs: list[str]):
        self.outputs = outputs
        self.call_index = 0

    def run(self, *, source_code: str, input_data: str) -> RunResult:
        output = self.outputs[self.call_index]
        self.call_index += 1
        return RunResult(output=output, execution_time_ms=5)
