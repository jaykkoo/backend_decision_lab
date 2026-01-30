import pytest
from benchmarks.services import run_benchmark

@pytest.mark.django_db
def test_benchmark_runs(benchmark_ruleset):
    result = run_benchmark(
        ruleset_id=benchmark_ruleset.id,
        dataset_size=5,
    )

    assert "django" in result
    assert "rust" in result
