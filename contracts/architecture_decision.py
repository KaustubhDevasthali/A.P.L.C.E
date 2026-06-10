from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ArchitectureDecision:
    summary: str
    selected_approach: str
    affected_components: list[str] = field(default_factory=list)
    files_to_inspect: list[str] = field(default_factory=list)
    design_constraints: list[str] = field(default_factory=list)
    rejected_alternatives: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "selected_approach": self.selected_approach,
            "affected_components": self.affected_components,
            "files_to_inspect": self.files_to_inspect,
            "design_constraints": self.design_constraints,
            "rejected_alternatives": self.rejected_alternatives,
            "risks": self.risks,
            "confidence": self.confidence
        }