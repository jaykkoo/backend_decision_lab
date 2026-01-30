import pytest
from unittest.mock import patch
import evaluations.services as services


@pytest.mark.django_db
def test_fallback_to_django_if_rust_fails(ruleset, user):
    with patch.object(
        services,
        "_evaluate_with_rust",
        side_effect=Exception("Rust down"),
    ):
        result = services.evaluate_ruleset(
            ruleset_id=ruleset.id,
            engine="rust",
            input_data={"monthly_volume": 12000},
            user=user,
        )

    assert result["engine"] == "django"
