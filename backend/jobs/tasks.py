import resource
from celery import shared_task
from django.conf import settings
import httpx

from products.models import ProductView


def get_cpu_and_memory():
    usage = resource.getrusage(resource.RUSAGE_SELF)

    cpu_time_sec = usage.ru_utime + usage.ru_stime
    memory_mb = usage.ru_maxrss / 1024  # Linux: KB → MB

    return cpu_time_sec, memory_mb


@shared_task(bind=True)
def compute_product_views_analytics(self, job_id, limit=None):
    """
    Analyse ProductView:
    - nombre de vues par produit
    - âge moyen des viewers
    - mesure CPU + RAM
    """

    # --------------------------------------------------
    # 🔥 FETCH DATA (hors mesure CPU)
    # --------------------------------------------------
    qs = (
        ProductView.objects
        .select_related("user")
        .exclude(user__age=None)
        .values("product_id", "user__age")
    )

    if limit:
        qs = qs[:limit]

    rows = list(qs)

    if not rows:
        raise ValueError("No product views found")

    # --------------------------------------------------
    # 🔥 CPU-BOUND SECTION
    # --------------------------------------------------
    cpu_start, _ = get_cpu_and_memory()

    stats = {}

    for r in rows:
        pid = r["product_id"]
        age = r["user__age"]

        s = stats.setdefault(
            pid,
            {"views": 0, "age_sum": 0}
        )

        s["views"] += 1
        s["age_sum"] += age

    results = [
        {
            "product_id": pid,
            "views": s["views"],
            "average_age": s["age_sum"] / s["views"],
        }
        for pid, s in stats.items()
    ]

    cpu_end, mem_end = get_cpu_and_memory()
    # --------------------------------------------------

    result = {
        "engine": "celery",
        "processed_items": len(rows),
        "products_count": len(results),
        "cpu_time_ms": (cpu_end - cpu_start) * 1000,
        "memory_mb_peak": mem_end,
        "views_by_product": results,
    }

    # --------------------------------------------------
    # 📤 CALLBACK DJANGO
    # --------------------------------------------------
    httpx.post(
        f"{settings.API_BASE_URL}/jobs/{job_id}/complete/",
        json={"status": "DONE", "result": result},
        timeout=5.0,
    )

    return result
