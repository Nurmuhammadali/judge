from dataclasses import dataclass
from datetime import datetime


@dataclass
class Problem:
    id: int
    title: str
    description: str
    input_description: str
    output_description: str
    constraints: str | None
    time_limit_sec: int
    memory_limit_mb: int
    created_at: datetime
