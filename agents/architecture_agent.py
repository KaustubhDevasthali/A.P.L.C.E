from agents.base_agent import BaseAgent
from contracts.agent_result import AgentResult
from contracts.architecture_decision import ArchitectureDecision
from contracts.task_specs import TaskSpecs

class ArchitectureAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "ArchitectureAgent"
    
    def run(self, task_specs: TaskSpecs, requirement_output: dict, planning_output: dict) -> AgentResult:
        schema = {
            "type": "object",
            "properties": {
                "summary": { "type" : "string" },
                "selected_approach": { "type": "string" },
                "affected_components": { "type" : "array", "items": { "type" : "string" } },
                "files_to_inspect": { "type" : "array", "items": { "type" : "string" } },
                "design_constraints": { "type" : "array", "items": { "type" : "string" } },
                "rejected_alternatives": { "type" : "array", "items": { "type" : "string" } },
                "risks": { "type" : "array", "items": { "type" : "string" } },
                "confidence": { "type" : "number" }
            },
            "required": [
                "summary",
                "selected_approach",
                "affected_components",
                "files_to_inspect",
                "design_constraints",
                "rejected_alternatives",
                "risks",
                "confidence"
            ]
        }

        prompt= f"""

        You are a senior architecture agent for an agentic software engineering system.

        Create an architecture decision from approved requirements and execution plan

        Task ID: {task_specs.task_id}
        Title: {task_specs.title}
        Raw Request: {task_specs.raw_request}
        Requirement Output: {requirement_output}
        Planning Output: {planning_output}
        Constraints: {task_specs.constraints}

        Rules:
            - Do not write implementation code
            - Do not invent repository files that have not been confirmed
            - Focus on design, integration points, constraints and risks
            - Identify components that should be inspected before implementation
            - Reject unnecessary scope and over-engineering
            - Return Structured JSON only
        """

        output = self.llm_provider.generate_json(prompt, schema, system="You convert software requirements and plans into architecture decisions")

        decision = ArchitectureDecision(
            summary=output["summary"],
            selected_approach=output.get("selected_approach", []),
            affected_components=output.get("affected_components", []),
            design_constraints=output.get("design_constraints", []),
            files_to_inspect=output.get("files_to_inspect", []),
            rejected_alternatives=output.get("rejected_alternatives", []),
            risks=output.get("risks", []),
            confidence=float(output.get("confidence", 0.0))
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS" if decision.confidence > 0.6 else "BLOCKED",
            summary=decision.summary,
            output=decision.to_dict(),
            risks=decision.risks,
            confidence=decision.confidence
        )