from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class PlanStep:
    step_id: str
    title: str
    description: str
    owner_agent: str
    executed_output: str
    dependencies: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class ExecutionPlan:
    goal: str
    steps: list[PlanStep] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    required_tools: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "steps": [step.__dict__ for step in self.steps],
            "assumptions": self.assumptions,
            "risks": self.risks,
            "required_tools": self.required_tools,
            "confidence": self.confidence
        }