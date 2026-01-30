import time
import httpx
from celery import shared_task
from users.models import User
from django.conf import settings
from django.db.models import Avg

@shared_task(bind=True)
def compute_average_age(self, job_id, limit):
    import time
    start = time.perf_counter()

    qs = User.objects.exclude(age=None).values_list("age", flat=True)[:limit]

    ages = list(qs)
    if not ages:
        raise ValueError("No users found")

    total = sum(ages)
    average = total / len(ages)

    execution_time_ms = (time.perf_counter() - start) * 1000

    result = {
        "engine": "celery",
        "average_age": average,
        "processed_items": len(ages),
        "execution_time_ms": execution_time_ms,
    }

    try:
        import httpx
        from django.conf import settings

        r = httpx.post(
            f"{settings.API_BASE_URL}/jobs/{job_id}/complete/",
            json={"status": "DONE", "result": result},
            timeout=5.0,
        )
        r.raise_for_status()
    except Exception as e:
        print("❌ CALLBACK FAILED:", e)
        raise

    return result

