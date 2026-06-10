from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Literal

from contracts.agent_result import AgentResult
from contracts.approval import ApprovalDecision
from contracts.task_specs import TaskSpecs


class WorkflowStatus(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    WAITING_FOR_REVIEW = "WAITING_FOR_REVIEW"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"


@dataclass
class WorkflowContext:
    execution_id: str
    task: TaskSpecs
    status: WorkflowStatus
    current_stage: str
    outputs: dict[str, AgentResult]
    approval_history: list[ApprovalDecision]
    pending_feedback: list[str]
    audit_log: list[str]
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime