import pytest
from rulesets.models import RuleSet
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def benchmark_ruleset(db):
    user = User.objects.create_user(username="bench")
    return RuleSet.objects.create(
        name="benchmark_ruleset",
        rules={
            "rules": [],
            "output": {
                "decision_thresholds": {
                    "reject": 30,
                    "review": 60,
                    "accept": 80,
                }
            },
        },
        created_by=user,
    )
