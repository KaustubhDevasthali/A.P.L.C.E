from contracts.agent_result import AgentResult
from contracts.task_specs import TaskSpecs
from agents.base_agent import BaseAgent

class RequirementAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "RequirementAgent"
    
    def run(self, task_specs: TaskSpecs) -> AgentResult:
        schema = {
            "type": "object",
            "properties": {
                "goal": {"type": "string"},
                "scope":{"type": "array", "items": {"type": "string"}},
                "out_of_scope": {"type": "array", "items": {"type": "string"}},
                "acceptance_criteria": {"type": "array", "items": {"type": "string"}},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "open_questions": {"type": "array", "items": {"type": "string"}},
                "risk_flags": {"type": "array", "items": {"type": "string"}},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": [
                "goal",
                "scope",
                "out_of_scope",
                "acceptance_criteria",
                "assumptions",
                "open_questions",
                "risk_flags",
                "confidence"
            ]
        }

        prompt = f"""
            You are Senior Requirement Analysis Engineer. Your task is to take a raw user request for a software engineering task and convert it into a structured set of requirements that can be easily consumed by downstream agents responsible for design, implementation, testing, etc.

            Convert the raw user input into implementation ready requirements.

            Task ID: {task_specs.task_id}
            Title: {task_specs.title}
            Raw Request: {task_specs.raw_request}
            Constraints: {task_specs.constraints}

            Return structured JSON only.

            """
        
        output = self.llm_provider.generate_json(prompt, schema, 
                                                 system="You convert vague user requests into precise engineering task specifications.")
        
        confidence = float(output.get("confidence", 0.0))

        Status = "SUCCESS"

        if (output.get("open_questions") and confidence < 0.6):
            Status = "BLOCKED"

        return AgentResult(
            agent_name=self.name,
            status=Status,
            summary=output.get("goal", ""),
            output=output,
            risks=output.get("risk_flags", []),
            confidence=confidence
        )