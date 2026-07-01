# Testing Guide

This guide explains how to validate the BusinessPilot AI project and how the current test suite fits into the development workflow.

## Purpose

The testing guide provides a straightforward reference for running automated checks, understanding the current coverage, and expanding tests as the project grows.

## Current Test Suite

The repository currently includes:
- [tests/test_basic.py](../tests/test_basic.py) for a basic sanity check,
- [tests/test_evaluation_framework.py](../tests/test_evaluation_framework.py) for evaluation framework behavior.

## Running Tests

From the repository root:

```bash
pytest
```

To generate a coverage report:

```bash
pytest --cov=src --cov-report=term-missing
```

## What Is Being Verified

The existing tests validate that:
- the evaluation framework can run successfully,
- churn evaluation metrics are produced with expected structure,
- the project remains importable and stable for basic development tasks.

## Recommended Testing Practices

- Add unit tests for each new agent method.
- Test API endpoints for both success and error cases.
- Verify that new evaluation metrics produce well-formed outputs.
- Prefer small, focused tests over broad integration-only checks.

## Extending the Tests

When adding a new feature, create tests that cover:
1. the happy path,
2. missing or invalid inputs,
3. edge cases that could affect business logic.

## Troubleshooting Test Failures

If tests fail, confirm that:
- dependencies are installed,
- the Python environment is active,
- the latest repository changes are saved.
