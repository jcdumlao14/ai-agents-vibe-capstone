# Architecture Guide

This guide provides a concise architectural reference for the BusinessPilot AI capstone project and explains how the existing components work together.

## Purpose

The architecture guide helps readers understand the system’s structure, the role of each agent, and how the API service orchestrates business workflows.

## High-Level Design

BusinessPilot AI follows a modular architecture with clear separation between:
- user-facing API services,
- orchestration agents,
- supporting business logic,
- evaluation and memory utilities.

This structure keeps the workflow understandable while allowing future extension to cloud services, external models, or richer tooling.

## Main Layers

### 1. API Layer

The FastAPI application in [src/services/api.py](../src/services/api.py) exposes the main endpoints for health checks, session management, churn scoring, and plan generation.

### 2. Agent Layer

The agent layer in [src/agents](../src/agents) contains specialized components:
- MainAgent orchestrates the overall flow.
- PlannerAgent builds a structured retention plan.
- MemoryAgent persists session context.
- Supporting agents handle reasoning, reflection, evaluation, logging, and tool calls.

### 3. Data and Model Layer

The [src/models](../src/models), [src/data](../src/data), and [src/evaluation](../src/evaluation) modules host the business logic, predictive modeling hooks, and evaluation utilities.

### 4. Configuration and Infrastructure

Configuration and environment guidance live in [configs](../configs) and [deployment](../deployment), supporting future deployment and operational use.

## Request Flow

A typical scoring request follows this path:

1. The API receives the customer context.
2. The request is routed to the main orchestration flow.
3. The tool agent performs the underlying scoring step.
4. The reasoning and reflection agents generate business guidance.
5. The evaluation and logging agents record the outcome.
6. The API returns the completed response.

## Design Principles

- Modularity: each agent has a focused responsibility.
- Extensibility: new agents and endpoints can be added without restructuring the system.
- Traceability: requests and sessions can be tracked through the memory layer.
- Practicality: the implementation remains lightweight while reflecting enterprise-style design patterns.

## Future Evolution

The current repository is a strong foundation for later improvements such as:
- authentication and authorization,
- persistent storage instead of in-memory sessions,
- real model integration,
- external tool and workflow connectors,
- deployment automation and observability.
