# User Guide

This guide explains how end users and reviewers can interact with BusinessPilot AI in its current form.

## Purpose

The user guide lowers the barrier to entry by showing how the system behaves in practical scenarios and how to use the exposed API without needing to understand the internal agent architecture.

## What the System Does

BusinessPilot AI helps analyze customer churn risk and recommend retention actions. The product experience is currently centered around:
- customer context submission,
- churn scoring,
- retention planning,
- session-based follow-up.

## Typical Workflow

1. Submit customer information through the API.
2. Request a churn score for that customer.
3. Review the explanation and recommendations.
4. Optionally create or reuse a session for continued interaction.

## Example: Score a Customer

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "usage": 18.5,
    "support_tickets": 3,
    "contract_months_remaining": 1
  }'
```

The response includes a churn score, explanation, and recommendation list.

## Example: Create a Session

```bash
curl -X POST http://127.0.0.1:8000/session \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "usage": 18.5,
    "support_tickets": 3,
    "contract_months_remaining": 1
  }'
```

## Interpreting Results

- Higher churn scores suggest stronger risk.
- Explanations surface common drivers such as low usage or frequent support issues.
- Recommendations are intended as starting points for retention workflows.

## Best Practices

- Include as much customer context as possible.
- Reuse session IDs when reviewing a customer over multiple steps.
- Treat the generated output as operational guidance rather than a final decision.
