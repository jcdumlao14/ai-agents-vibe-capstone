from src.evaluation.framework import EvaluationFramework


def test_evaluation_framework_runs():
    framework = EvaluationFramework()
    customer = {
        "customer_id": "test_123",
        "usage": 12.5,
        "support_tickets": 3,
        "contract_months_remaining": 1,
        "industry": "enterprise",
    }
    metrics = framework.evaluate_customer_run(customer, expected_score=0.85)

    assert metrics.latency_seconds is not None
    assert metrics.tool_calls == 1
    assert metrics.token_usage is not None
    assert metrics.cost_estimate is not None
    assert "expected_retention_rate" in metrics.business_kpis
    assert metrics.business_kpis["customer_health"] in {"high", "medium", "low"}
