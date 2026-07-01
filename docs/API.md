# API Documentation

This document explains the purpose and usage of the BusinessPilot AI API endpoints. It complements the implementation in [src/services/api.py](../src/services/api.py) and provides a clear reference for local testing and integration.

## Purpose

The API exposes the core product capabilities in a simple HTTP interface:
- create or retrieve customer sessions,
- request churn scoring,
- build retention plans from customer context.

This makes the system easy to test, demo, and integrate into existing business tools.

## Base URL

When running locally:

```bash
http://127.0.0.1:8000
```

## Endpoints

### Health Check

GET /health

Returns service health information.

Example:

```bash
curl http://127.0.0.1:8000/health
```

Example response:

```json
{
  "status": "ok"
}
```

### Create Session

POST /session

Creates a new customer session and stores the supplied customer context.

Request body:

```json
{
  "customer_id": "cust_001",
  "usage": 18.5,
  "support_tickets": 3,
  "contract_months_remaining": 1
}
```

Response:

```json
{
  "status": "success",
  "session_id": "<generated-session-id>"
}
```

### Retrieve Session

GET /session/{session_id}

Returns the stored session record, including customer context and prior interactions.

### Build Retention Plan

POST /plan

Builds a structured retention plan using customer context.

Request body:

```json
{
  "customer_id": "cust_001",
  "usage": 18.5,
  "support_tickets": 3,
  "contract_months_remaining": 1,
  "session_id": "optional-existing-session-id"
}
```

Response:

```json
{
  "status": "success",
  "plan": [
    {
      "id": "capture_context",
      "name": "Capture customer context"
    }
  ],
  "summary": "Plan composed with 5 task(s).",
  "fallback": false
}
```

### Score Customer

POST /score

Scores the customer for churn risk and returns a recommendation payload.

Request body:

```json
{
  "customer_id": "cust_001",
  "usage": 18.5,
  "support_tickets": 3,
  "contract_months_remaining": 1,
  "session_id": "optional-existing-session-id"
}
```

Response:

```json
{
  "status": "success",
  "customer_id": "cust_001",
  "churn_score": 0.7,
  "explanation": {
    "churn_score": 0.7,
    "reasons": ["Low product usage", "Frequent support issues"]
  },
  "recommendations": [
    "Increase onboarding support"
  ],
  "reflection": {
    "status": "ok"
  },
  "evaluation": {
    "score": 0.8
  },
  "logging": {
    "status": "logged"
  }
}
```

## Error Handling

The API returns standard HTTP errors:
- 400 for invalid or incomplete planning requests,
- 404 when a session cannot be found,
- 500 for unexpected server errors.

## Notes

The API is intentionally lightweight and can be extended with authentication, persistence, and richer external integrations over time.
