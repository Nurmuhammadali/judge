from apps.domain.interfaces.code_runner import CodeRunner, RunResult


class FakeRunner(CodeRunner):
    def __init__(self, outputs):
        self.outputs = outputs
        self.index = 0

    def run(self, *, source_code: str, input_data: str) -> RunResult:
        output = self.outputs[self.index]
        self.index += 1
        return RunResult(output=output, execution_time_ms=10)
