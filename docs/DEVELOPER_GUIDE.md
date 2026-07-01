# Developer Guide

This guide is intended for contributors who want to extend the BusinessPilot AI codebase. It explains the development workflow, project structure, and the main extension points.

## Purpose

The guide helps developers understand how the current implementation is organized and where to add new features without disrupting the existing architecture.

## Development Environment

The project targets Python 3.11 and uses the dependencies listed in [requirements.txt](../requirements.txt) and [pyproject.toml](../pyproject.toml).

Recommended setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Repository Layout

- [src/agents](../src/agents) contains the orchestration agents.
- [src/services](../src/services) contains the API and MCP server entry points.
- [src/models](../src/models) contains model-related logic.
- [src/data](../src/data) contains data preprocessing and feature utilities.
- [src/evaluation](../src/evaluation) contains scoring and evaluation utilities.
- [tests](../tests) contains automated tests.

## Core Components

### Main Agent

The [src/agents/main_agent.py](../src/agents/main_agent.py) orchestrates the overall churn analysis workflow by calling supporting agents and assembling the final response.

### Planner Agent

The [src/agents/planner_agent.py](../src/agents/planner_agent.py) builds a structured task plan from customer context.

### Memory Agent

The [src/agents/memory_agent.py](../src/agents/memory_agent.py) stores session state and interaction history in memory.

### API Layer

The [src/services/api.py](../src/services/api.py) exposes the application through FastAPI endpoints.

## Typical Development Workflow

1. Create or update a feature in the relevant module.
2. Add or adjust tests in [tests](../tests).
3. Run the test suite.
4. Start the local API server for manual validation.

## Running the Project

Start the API:

```bash
uvicorn src.services.api:app --host 0.0.0.0 --port 8000
```

Run tests:

```bash
pytest
```

## Extending the System

### Add a New Agent

Create a new class under [src/agents](../src/agents) and invoke it from [src/agents/main_agent.py](../src/agents/main_agent.py) or another orchestration component.

### Add a New Endpoint

Extend [src/services/api.py](../src/services/api.py) with a new route and associated request model.

### Add a New Evaluation Metric

Update [src/evaluation/framework.py](../src/evaluation/framework.py) to include the metric and expose it through the evaluation flow.

## Coding Conventions

- Keep modules focused and reusable.
- Preserve the existing naming conventions for agents and services.
- Use clear, descriptive method names.
- Prefer small, testable functions.

## Troubleshooting

If the API does not start, verify that:
- Python 3.11 is installed,
- dependencies are installed,
- the repository root is used when launching Uvicorn.
