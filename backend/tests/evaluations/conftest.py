import pytest
from django.contrib.auth import get_user_model
from rulesets.models import RuleSet

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="password"
    )

@pytest.fixture
def ruleset(user):
    return RuleSet.objects.create(
        name="evaluation_ruleset",
        rules={
            "rules": [
                {
                    "id": "R1",
                    "if": {
                        "field": "monthly_volume",
                        "operator": ">=",
                        "value": 10000,
                    },
                    "then": {"score": 20},
                }
            ],
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
