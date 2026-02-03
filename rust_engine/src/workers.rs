use sqlx::{PgPool, Row};
use reqwest::Client;
use crate::models::{Job, ProductViewStat, JobResult};
use libc::{getrusage, rusage, RUSAGE_SELF};
use std::collections::HashMap;
use redis::AsyncCommands;


fn cpu_and_memory() -> (f64, f64) {
    unsafe {
        let mut usage: rusage = std::mem::zeroed();
        getrusage(RUSAGE_SELF, &mut usage);

        let cpu =
            usage.ru_utime.tv_sec as f64
            + usage.ru_utime.tv_usec as f64 / 1_000_000.0
            + usage.ru_stime.tv_sec as f64
            + usage.ru_stime.tv_usec as f64 / 1_000_000.0;

        let memory_mb = usage.ru_maxrss as f64 / 1024.0; // KB → MB

        (cpu, memory_mb)
    }
}

// fn cpu_and_memory() -> (f64, f64) {
//     (0.0, 0.0)
// }


pub async fn run_worker() -> ! {
    tracing::info!("Rust worker started");

    let redis_url =
        std::env::var("REDIS_URL")
            .unwrap_or_else(|_| "redis://redis:6379".to_string());

    let mut con = loop {
        match redis::Client::open(redis_url.clone()) {
            Ok(client) => match client.get_async_connection().await {
                Ok(conn) => {
                    tracing::info!("✅ Redis connected");
                    break conn;
                }
                Err(e) => {
                    tracing::warn!("Redis connection failed: {e}");
                }
            },
            Err(e) => {
                tracing::warn!("Redis client failed: {e}");
            }
        }

        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    };

    let db_url =
        std::env::var("DATABASE_URL")
            .expect("DATABASE_URL missing");

    let pool = loop {
        match PgPool::connect(&db_url).await {
            Ok(p) => {
                tracing::info!("✅ Postgres connected");
                break p;
            }
            Err(e) => {
                tracing::warn!("Postgres not ready: {e}");
                tokio::time::sleep(std::time::Duration::from_secs(1)).await;
            }
        }
    };

    let http = Client::new();

    loop {
        tracing::info!("⏳ Waiting for job (BLPOP)…");

        let result: Result<(String, String), redis::RedisError> =
            con.blpop("score_jobs", 0.0).await;

        let (_key, job_json) = match result {
            Ok(v) => v,
            Err(e) => {
                tracing::error!("Redis BLPOP error: {e}");
                continue;
            }
        };

        let job: Job =
            serde_json::from_str(&job_json)
                .expect("Invalid job JSON");

        tracing::info!("▶️ Processing job {}", job.job_id);

        if let Err(e) =
            run_product_views_job(&pool, &http, job).await
        {
            tracing::error!("Job failed: {:?}", e);
        }
    }
}



pub async fn run_product_views_job(
    pool: &PgPool,
    http: &Client,
    job: Job,
) -> anyhow::Result<()> {

    // --------------------------------------------------
    // 🔥 FETCH DATA (hors CPU mesure)
    // --------------------------------------------------
    let mut query = sqlx::QueryBuilder::new(
        r#"
        SELECT pv.product_id, u.age
        FROM products_productview pv
        JOIN users_user u ON u.id = pv.user_id
        WHERE u.age IS NOT NULL
        "#
    );

    if let Some(limit) = job.payload.limit {
        query.push(" LIMIT ");
        query.push_bind(limit as i64);
    }

    let rows = query
        .build()
        .fetch_all(pool)
        .await?;

    if rows.is_empty() {
        tracing::warn!("No product views found");
        return Ok(());
    }

    // --------------------------------------------------
    // 🔥 CPU-BOUND SECTION
    // --------------------------------------------------
    let (cpu_start, _) = cpu_and_memory();

    #[derive(Default)]
    struct Stats {
        views: u64,
        age_sum: u64,
    }

    let mut stats: HashMap<i64, Stats> = HashMap::new();

    for row in rows.iter() {
        let product_id: i64 = row.get("product_id");
        let age: i32 = row.get("age");

        let s = stats.entry(product_id).or_default();
        s.views += 1;
        s.age_sum += age as u64;
    }

    let views_by_product: Vec<ProductViewStat> = stats
        .into_iter()
        .map(|(product_id, s)| ProductViewStat {
            product_id,
            views: s.views,
            average_age: s.age_sum as f64 / s.views as f64,
        })
        .collect();

    let (cpu_end, mem_end) = cpu_and_memory();
    // --------------------------------------------------

    let result = JobResult {
        engine: "rust".to_string(),
        processed_items: rows.len(),
        products_count: views_by_product.len(),
        cpu_time_ms: (cpu_end - cpu_start) * 1000.0,
        memory_mb_peak: mem_end,
        views_by_product,
    };

    notify_django(http, &job.job_id, result).await?;

    Ok(())
}


async fn notify_django(
    client: &Client,
    job_id: &str,
    result: JobResult,
) -> Result<(), reqwest::Error> {
    let base_url =
        std::env::var("DJANGO_CALLBACK_URL")
            .unwrap_or_else(|_| "http://django:8000/api/v1".to_string());

    let url = format!("{}/jobs/{}/complete/", base_url, job_id);

    client
        .post(url)
        .json(&serde_json::json!({
            "status": "DONE",
            "result": result
        }))
        .send()
        .await?
        .error_for_status()?; // 👈 capture 4xx / 5xx

    Ok(())
}
