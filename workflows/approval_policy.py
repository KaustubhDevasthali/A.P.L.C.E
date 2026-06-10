from contracts.approval import ApprovalMode


class ApprovalPolicy:
    def __init__(self) -> None:
        self.agent_modes: dict[str, ApprovalMode] = {
            "RequirementAgent": "MANDATORY",
            "PlanningAgent": "MANDATORY",
            "ArchitectureAgent": "MANDATORY",
            "ImplementationAgent": "MANDATORY",
            "TestingAgent": "BLOCK_ON_RISK",
            "SecurityAgent": "MANDATORY",
            "ReviewAgent": "MANDATORY",
            "DeploymentAgent": "MANDATORY",
            "EvaluationAgent": "OPTIONAL",
        }

    def mode_for(self, agent_name: str) -> ApprovalMode:
        return self.agent_modes.get(agent_name, "MANDATORY")