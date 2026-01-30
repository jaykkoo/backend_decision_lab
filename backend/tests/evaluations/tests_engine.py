from evaluations.services import _evaluate_with_django

def test_rule_is_applied(ruleset):
    result = _evaluate_with_django(
        ruleset,
        {"monthly_volume": 12000},
    )

    assert result["score"] == 20
    assert result["decision"] == "reject"
    assert result["engine"] == "django"
