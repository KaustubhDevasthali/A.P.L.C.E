from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class TaskSpecs:
    task_id: str
    title: str
    raw_request: str
    repo_path: str | None = None
    constraints: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)