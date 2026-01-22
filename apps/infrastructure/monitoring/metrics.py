from prometheus_client import Counter, Histogram

submission_total = Counter(
    "judge_submissions_total",
    "Total judge submissions",
    ["status", "language"],
)

execution_time_ms = Histogram(
    "judge_execution_time_ms",
    "Submission execution time (ms)",
    buckets=(5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000),
)

runner_errors_total = Counter(
    "judge_runner_errors_total",
    "Runner execution errors total",
)
