# A.P.L.C.E
Agentic Project Life Cycle Engine A provider-agnostic agent system that takes a software task and routes it through specialized agents throughout the life cycle.

A complete SDLC with agents, contracts, workflow states, benchmarks and evaluation built in it.

Agents 

    Requirement Agent
    Planning Agent
    Architecture Agent
    Implementation Agent
    Testing Agent
    Security Agent
    Review Agent
    Deployment Architecture Agent
    Evaluation Agent

# Tech Stack 

    Backend: Python
    API: FastAPI
    CLI: Typer/Click
    LLM Abstraction: Custom Provider Interface
    Repo Execution: Local Sandbox
    Testing Framework: pytest
    Storage: SQLite/Postgres
    Task Input Format: YAML/JSON
    Report Output Formar: Markdown + JSON


# Core Concept 

Each agent receives input in following format -

    Task Context
    Previous Agent Output(s), if any
    Relevant Files, if any
    Available Tools
    Rules
    Memory

Each agent will then return result 

    Status
    Summary
    Decisions
    Files Created/Changed
    Risks, if any
    Recommendations, if any
    Confidence


# Agents

## Requirement Agent
