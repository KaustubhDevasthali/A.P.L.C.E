import yaml
from pathlib import Path

from agents.requirement_agent import RequirementAgent
from agents.planning_agent import PlanningAgent
from agents.architecture_agent import ArchitectureAgent


from contracts.task_specs import TaskSpecs
from contracts.approval import ApprovalDecision
from contracts.workflow_context import WorkflowContext
from providers.mock_providers import MockPlanningProvider, MockRequirementProvider
from workflows import approval_gate, approval_policy

def print_result(agent_result):
    print("Agent:", agent_result.agent_name)
    print("Status:", agent_result.status)
    print("Confidence:", agent_result.confidence)
    print("Summary:", agent_result.summary)
    print("Output:")
    for key, value in agent_result.output.items():
        print(f"- {key}: {value}")

def require_approval(result):
    mode = approval_policy.mode_for(result.agent_name)
    decision = approval_gate.review(result, mode)

    if decision.status == "REJECTED":
        stop_workflow()

    if decision.status == "CHANGES_REQUESTED":
        pause_or_revise()

    if decision.status in ["APPROVED", "AUTO_APPROVED"]:
        continue_workflow()


def stop_workflow(workflow_context: WorkflowContext, approval: ApprovalDecision) -> None:
    workflow_context.status = "TERMINATED"
    workflow_context.end_time = utcnow()
    # workflow_context.audit_log.append(
    #     AuditEntry(
    #         event_type="WORKFLOW_TERMINATED",
    #         stage=workflow_context.current_stage,
    #         message=approval.comments,
    #     )
    # )

def resume_workflow(workflow_context: WorkflowContext) -> None:
    workflow_context.status = "RUNNING"
    # workflow_context.audit_log.append(
    #     AuditEntry(
    #         event_type="WORKFLOW_RESUMED",
    #         stage=workflow_context.current_stage,
    #         message="Workflow resumed after requested changes.",
    #     )
    # )

def pause_or_revise(workflow_context: WorkflowContext, approval: ApprovalDecision) -> None:
    workflow_context.status = "WAITING_FOR_REVIEW_UPDATES"
    # workflow_context.audit_log.append(
    #     AuditEntry(
    #         event_type="CHANGES_REQUESTED",
    #         stage=workflow_context.current_stage,
    #         message=approval.comments,
    #     )
    # )

    workflow_context.pending_feedback = (
        approval.required_changes
    )

def continue_workflow(workflow_context: WorkflowContext) -> None:
    workflow_context.current_stage_index += 1

    # workflow_context.audit_log.append(
    #     AuditEntry(
    #         event_type="WORKFLOW_CONTINUED",
    #         stage=workflow_context.current_stage,
    #         message="Output approved. Continuing workflow.",
    #     )
    # )


def load_task(path: str) -> TaskSpecs:
    data = yaml.safe_load(Path(path).read_text())
    
    return TaskSpecs(
        task_id=data["task_id"],
        title=data["title"],
        raw_request=data["raw_request"],
        repo_path=data.get("repo_path"),
        constraints=data.get("constraints", []),
        metadata=data.get("metadata", {})
    )

def main() -> None:
    task = load_task("benchmarks/tasks/sample_requirement.yaml")

    # Requirement Agent

    requirement_provider = MockRequirementProvider()
    requirement_agent = RequirementAgent(requirement_provider)
    requirement_result = requirement_agent.run(task)
    print_result(requirement_result)
    
    # Approval Gate
    if requirement_result.status == "FAILED":
        print("Stopping workflow because requirement analysis failed.")
        return
    
    # Planning Agent

    planning_provider = MockPlanningProvider()
    planning_agent = PlanningAgent(planning_provider)
    # Requirement agent output - structured requirements are passed to the planning agent.
    planning_result = planning_agent.run(task, requirement_result.output)
    print_result(planning_result)

    if planning_result.status == "FAILED":
        print("Stopping workflow because planning failed.")
        return
    
    architecture_agent = ArchitectureAgent(planning_provider)
    architecture_result = architecture_agent.run(
        task, requirement_result.output, planning_result.output
    )

    print_result(architecture_result)
    
if __name__ == "__main__":
    main()