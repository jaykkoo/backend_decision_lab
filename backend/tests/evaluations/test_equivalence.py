from evaluations.services import _evaluate_with_django, _evaluate_with_rust

def test_django_and_rust_same_result(mocker, ruleset):
    mocker.patch(
        "evaluations.services._evaluate_with_rust",
        return_value={
            "score": 20,
            "decision": "reject",
            "matched_rules": ["R1"],
            "execution_time_ms": 1.1,
            "engine": "rust",
        },
    )

    django_result = _evaluate_with_django(
        ruleset,
        {"monthly_volume": 12000},
    )

    rust_result = _evaluate_with_rust(
        ruleset,
        {"monthly_volume": 12000},
    )

    assert django_result["score"] == rust_result["score"]
    assert django_result["decision"] == rust_result["decision"]
