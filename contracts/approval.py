from dataclasses import dataclass, field
from typing import Any, Literal

ApprovalStatus = Literal[
    "APPROVED",
    "REJECTED",
    "CHANGES_REQUESTED",
    "AUTO_APPROVED"
]


ApprovalMode = Literal [
    "MANDATORY",
    "OPTIONAL",
    "AUTO",
    "BLOCK_ON_RISK"
]

@dataclass(frozen=True)
class ApprovalDecision:
    agent_name: str
    mode: ApprovalMode
    status: ApprovalStatus
    reviewer: str
    comments: str | None = None
    required_changes: list[str] = field(default_factory=list)
    approved_output: dict[str, Any] | None = None