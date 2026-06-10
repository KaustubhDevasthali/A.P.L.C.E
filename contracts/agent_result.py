from dataclasses import dataclass, field
from typing import Any, Literal

AgentStatus = Literal["SUCCESS", "FAILED", "IN_PROGRESS", "BLOCKED", "CANCELED"]

@dataclass(frozen=True)
class AgentResult:
    agent_name: str
    status: AgentStatus
    summary: str
    output: dict[str, Any] = field(default_factory=dict)
    risks: list[str] = field(default_factory=list)
    confidence: float = 0.0