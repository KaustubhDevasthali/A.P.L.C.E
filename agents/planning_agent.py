from contracts.agent_result import AgentResult
from contracts.execution_plan import PlanStep, ExecutionPlan
from contracts.task_specs import TaskSpecs
from agents.base_agent import BaseAgent

class PlanningAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "PlanningAgent"
    
    def run(self, task_specs: TaskSpecs, requirement_output: dict) -> AgentResult:
        schema = {
            "type": "object",
            "properties": {
                "goal": {"type": "string"},
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "step_id": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "owner_agent": {"type": "string"},
                            "expected_output": {"type": "string"},
                            "dependencies": {"type": "array", "items": {"type": "string"}},
                            "risks": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["step_id", "title", "description", "owner_agent", "expected_output"]
                    }
                },
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "risks": {"type": "array", "items": {"type": "string"}},
                "required_tools": {"type": "array", "items": {"type": "string"}},
                "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}
            },
            "required": ["goal", "steps", "assumptions", "risks", "required_tools", "confidence"]
        }

        prompt = f"""
                You are a senior planning agent for an agentic software engineering system.

                Create an execution plan from the structured task specifications.

                Task ID: {task_specs.task_id}
                Title: {task_specs.title}
                Raw Request: {task_specs.raw_request}
                Requirement Output: {requirement_output}
                Constraints: {task_specs.constraints}

                Rules:
                - Do not write code.
                - Do not invent repository details.
                - Create clear, ordered implementation steps.
                - Assign each step to the most appropriate downstream agent.
                - Include risks and dependencies.
                - Return structured JSON only.  

            """
        
        output = self.llm_provider.generate_json(prompt, schema, 
                                                 system= "You convert structured task specifications into ordered execution plans.")
        
        steps = [
            PlanStep(
                step_id=step["step_id"],
                title=step["title"],
                description=step["description"],
                owner_agent=step["owner_agent"],
                executed_output=step["expected_output"],
                dependencies=step.get("dependencies", []),
                risks=step.get("risks", []),
            )
            for step in output["steps"]
        ]

        plan = ExecutionPlan(
            goal=output["goal"],
            steps=steps,
            assumptions=output.get("assumptions", []),
            risks=output.get("risks", []),
            required_tools=output.get("required_tools", []),
            confidence=float(output.get("confidence", 0.0)),
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS" if plan.confidence >= 0.6 else "BLOCKED",
            summary=plan.goal,
            output=plan.to_dict(),
            risks=plan.risks,
            confidence=plan.confidence,

        )