from contracts.agent_result import AgentResult
from contracts.approval import ApprovalMode, ApprovalDecision

class ApprovalGate:
    def review(self, result: AgentResult, mode: ApprovalMode = "MANDATORY") -> ApprovalDecision:
        if mode == "AUTO_APPROVE":
            return ApprovalDecision(
                    agent_name=result.agent_name,
                    mode=mode,
                    status="AUTO_APPROVED",
                    reviewer="system",
                    comments="Auto-approved by workflow policy.",
                    approved_output=result.output,
                )
        
        if mode == "BLOCK_ON_RISK" and not result.risks:
            return ApprovalDecision(
                agent_name=result.agent_name,
                mode=mode,
                status="AUTO_APPROVED",
                reviewer="system",
                comments="Auto-approved because no risks were reported.",
                approved_output=result.output,
            )
        
        print("\n" + "=" * 80)
        print(f"Review required for: {result.agent_name}")
        print("=" * 80)
        print("Summary:", result.summary)
        print("Confidence:", result.confidence)
        print("Risks:", result.risks)
        print("\nOutput:")
        
        for key, value in result.output.items():
            print(f"{key}: {value}")
        
        print("\nChoose:")
        print("1. Approve")
        print("2. Request changes")
        print("3. Reject")
        
        choice = input("Decision: ").strip()
        if choice == "1":
            return ApprovalDecision(
                agent_name=result.agent_name,
                mode=mode,
                status="APPROVED",
                reviewer="human",
                comments="Approved from CLI review.",
                approved_output=result.output,
            )
        if choice == "2":
            changes = input("Required changes: ").strip()
            return ApprovalDecision(
                agent_name=result.agent_name,
                mode=mode,
                status="CHANGES_REQUESTED",
                reviewer="human",
                comments="Changes requested from CLI review.",
                required_changes=[changes],
            )

        return ApprovalDecision(
            agent_name=result.agent_name,
            mode=mode,
            status="REJECTED",
            reviewer="human",
            comments="Rejected from CLI review.",
        )