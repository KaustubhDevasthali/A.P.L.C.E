from typing import Any

from providers.base import LLMProvider

class MockRequirementProvider(LLMProvider):
    def generate(self, prompt: str, *, system: str | None = None) -> str:
        return "This is a mock response."

    def generate_json(self, prompt: str, schema: dict[str, Any], *, system: str | None = None) -> dict[str, Any]:
        return {
            "goal": "Clarify and structure the requested engineering task.",
            "scope": [
                "Understand the raw user request",
                "Convert it into implementation ready requirements",
                "Identify missing details and risks"
            ],
            "out_of_scope": [
                "Writing code",
                "Changing repository files or structure",
                "Running tests or commands"
            ],
            "acceptance_criteria":[
                "Structured requirements that are clear, actionable, and testable",
                "Constraints and risks are identified and documented",
                "The output is in a format that can be easily consumed by downstream agents",
                "Ambiguities are explicitly identified and documented"
            ],
            "assumptions": [
                "The user wants an implementation-ready engineering task specification",
            ],
            "open_questions": [
                "Which repository or module should be modified ?",
                "Are there existing architectural or design constraints to consider ?"
            ],
            "risk_flags": [
                "Original request may be too vague or ambiguous",
                "Potential for missing critical details that could impact implementation",
                "Risk of misinterpreting the user's intent without further clarification"
            ],
            "confidence": 0.78
        }
    
class MockPlanningProvider(LLMProvider):
    def generate(self, prompt: str, *, system: str | None = None) -> str:
        return "Mock response"

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any],
        *,
        system: str | None = None,
    ) -> dict[str, Any]:
        lower_prompt = prompt.lower()
        
        if "architecture decision" in lower_prompt or "architecture agent" in lower_prompt:
            return {
                "summary": "Use a minimal JWT authentication architecture integrated through the existing API routing and middleware/dependency structure.",
                "selected_approach": (
                    "Add a dedicated authentication module responsible for credential validation, "
                    "JWT creation, and JWT verification. Protected routes should depend on a reusable "
                    "authentication guard or middleware rather than duplicating token validation logic inside handlers."
                ),
                "affected_components": [
                    "API routing layer",
                    "Authentication service/module",
                    "Configuration/environment loading",
                    "Protected route handlers",
                    "Test suite",
                ],
                "files_to_inspect": [
                    "Application entrypoint",
                    "Route definitions",
                    "Existing middleware/dependency configuration",
                    "Configuration/settings module",
                    "Existing test fixtures",
                ],
                "design_constraints": [
                    "JWT secrets must come from environment/configuration, not source code.",
                    "Token validation must reject missing, malformed, invalid, and expired tokens.",
                    "Authentication logic should be reusable across protected routes.",
                    "OAuth, refresh tokens, social login, and password reset are out of scope.",
                    "Implementation should follow existing routing and testing patterns.",
                ],
                "rejected_alternatives": [
                    "Embedding JWT validation directly inside every protected route handler.",
                    "Adding OAuth or social-login abstractions.",
                    "Introducing refresh-token persistence before it is required.",
                    "Creating a large user-management subsystem if the task only requires authentication.",
                ],
                "risks": [
                    "The existing repository structure is not yet inspected, so integration points are assumed.",
                    "The user store and credential validation mechanism are unspecified.",
                    "Protected routes are not explicitly listed.",
                    "Token expiry policy is not yet defined.",
                ],
                "confidence": 0.82,
            }
        
        if "execution plan" in lower_prompt or "planning agent" in lower_prompt:
            return {
                "goal": "Plan the implementation of JWT-based authentication for the API.",
                "steps": [
                    {
                        "step_id": "PLAN-001",
                        "title": "Inspect existing API structure",
                        "description": "Identify routing, middleware, configuration, dependency, and testing patterns before making implementation decisions.",
                        "owner_agent": "ArchitectureAgent",
                        "expected_output": "Repository structure findings and recommended auth integration points.",
                        "dependencies": [],
                        "risks": [
                            "Existing architecture may not have clear middleware or dependency patterns."
                        ],
                    },
                    {
                        "step_id": "PLAN-002",
                        "title": "Design JWT authentication approach",
                        "description": "Define how login, token creation, token validation, protected-route enforcement, and configuration should work.",
                        "owner_agent": "ArchitectureAgent",
                        "expected_output": "Authentication design proposal aligned with project conventions.",
                        "dependencies": ["PLAN-001"],
                        "risks": [
                            "Token expiry, user store, and protected-route scope may be underspecified."
                        ],
                    },
                    {
                        "step_id": "PLAN-003",
                        "title": "Implement authentication components",
                        "description": "Add login handling, JWT generation, JWT validation, and protected-route enforcement.",
                        "owner_agent": "ImplementationAgent",
                        "expected_output": "Code changes implementing JWT authentication.",
                        "dependencies": ["PLAN-002"],
                        "risks": [
                            "Implementation may introduce insecure token handling if configuration is not handled correctly."
                        ],
                    },
                    {
                        "step_id": "PLAN-004",
                        "title": "Add authentication tests",
                        "description": "Add tests for successful login, missing token, invalid token, expired token, and protected-route access.",
                        "owner_agent": "TestingAgent",
                        "expected_output": "Automated tests covering JWT authentication behavior.",
                        "dependencies": ["PLAN-003"],
                        "risks": [
                            "Tests may need fixtures or fake users that do not yet exist."
                        ],
                    },
                    {
                        "step_id": "PLAN-005",
                        "title": "Review security posture",
                        "description": "Check for hardcoded secrets, weak signing configuration, missing expiration validation, and unsafe error leakage.",
                        "owner_agent": "SecurityAgent",
                        "expected_output": "Security review findings and required fixes.",
                        "dependencies": ["PLAN-003", "PLAN-004"],
                        "risks": [
                            "Security issues may remain if token validation behavior is incomplete."
                        ],
                    },
                    {
                        "step_id": "PLAN-006",
                        "title": "Prepare deployment readiness notes",
                        "description": "Document required environment variables, migration impact, rollback notes, and operational considerations.",
                        "owner_agent": "DeploymentAgent",
                        "expected_output": "Deployment checklist and rollback notes.",
                        "dependencies": ["PLAN-005"],
                        "risks": [
                            "Missing environment configuration could break deployment."
                        ],
                    },
                ],
                "assumptions": [
                    "The repository has an existing API structure.",
                    "JWT authentication is required instead of OAuth.",
                    "A user validation mechanism either exists or will be added minimally.",
                ],
                "risks": [
                    "Protected routes are not explicitly listed.",
                    "Token expiry policy is not specified.",
                    "User credential validation source is unclear.",
                ],
                "required_tools": [
                    "repo_search",
                    "file_reader",
                    "file_writer",
                    "test_runner",
                    "static_analyzer",
                    "git_diff",
                ],
                "confidence": 0.84,
            }
        
        if "jwt" in lower_prompt or "authentication" in lower_prompt:
            return {
                "goal": "Implement JWT-based authentication for the API.",
                "scope": [
                    "Add a login endpoint that validates user credentials.",
                    "Generate a signed JWT after successful login.",
                    "Add middleware or dependency logic to validate JWTs on protected routes.",
                    "Reject requests with missing, invalid, or expired tokens.",
                    "Add tests for successful login, missing token, invalid token, and expired token cases.",
                ],
                "out_of_scope": [
                    "OAuth or social login.",
                    "Refresh token rotation.",
                    "Password reset flow.",
                    "User registration unless already required by the existing API.",
                ],
                "acceptance_criteria": [
                    "A valid user can log in and receive a JWT.",
                    "Protected routes require a valid bearer token.",
                    "Requests without a token return 401.",
                    "Requests with invalid or expired tokens return 401.",
                    "JWT secrets are loaded from configuration or environment variables, not hardcoded.",
                    "Authentication tests pass.",
                ],
                "assumptions": [
                    "The API already has or can use an existing user store.",
                    "The project allows adding a JWT library dependency.",
                    "Bearer token authentication is acceptable for protected routes.",
                ],
                "open_questions": [
                    "What user store should credentials be validated against?",
                    "What token expiry duration should be used?",
                    "Which routes should be protected?",
                ],
                "risk_flags": [
                    "Hardcoded JWT secrets would create a security risk.",
                    "Weak token validation could allow unauthorized access.",
                    "Unclear protected-route scope may cause incomplete implementation.",
                ],
                "confidence": 0.86,
            }

        return {
            "goal": "Clarify and structure the requested engineering task.",
            "scope": [
                "Understand the raw user request",
                "Convert it into implementation-ready requirements",
                "Identify missing details and risks",
            ],
            "out_of_scope": [
                "Writing production code",
                "Changing repository files",
                "Running tests",
            ],
            "acceptance_criteria": [
                "Structured requirements are produced",
                "Constraints are preserved",
                "Ambiguities are explicitly listed",
            ],
            "assumptions": [
                "The user wants an implementation-ready engineering task specification."
            ],
            "open_questions": [
                "Which repository or module should be modified?",
                "Are there existing architecture rules to follow?",
            ],
            "risk_flags": [
                "Original request may be too vague for direct implementation."
            ],
            "confidence": 0.78,
        }