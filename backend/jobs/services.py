import json
import redis
from django.conf import settings
from django.db import connection

import json
import redis
from django.conf import settings
from .tasks import compute_product_views_analytics


def enqueue_job(job):
    engine = job.payload["engine"]
    limit = job.payload["limit"]

    if engine == "celery":
        # 🐍 Celery worker
        compute_product_views_analytics.delay(str(job.id), limit)

    elif engine == "rust":
        # 🦀 Rust worker (Redis queue)
        r = redis.Redis.from_url(settings.REDIS_URL)
        r.lpush(
            "score_jobs",
            json.dumps({
                "job_id": str(job.id),
                "payload": job.payload,
            })
        )
    else:
        raise ValueError(f"Unknown engine: {engine}")


def get_latency_by_volume():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
              processed_items,
              engine,
              percentile_cont(0.95)
                WITHIN GROUP (ORDER BY execution_time_ms) AS p95,
              percentile_cont(0.99)
                WITHIN GROUP (ORDER BY execution_time_ms) AS p99
            FROM jobs_jobrun
            GROUP BY processed_items, engine
            ORDER BY processed_items;
        """)
        rows = cursor.fetchall()

    return rows
