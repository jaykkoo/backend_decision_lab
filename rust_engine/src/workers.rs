use std::{env, time::Instant};
use redis::AsyncCommands;
use sqlx::{PgPool, Row};
use reqwest::Client;
use tokio::time::{sleep, Duration};
use crate::models::{Job, JobResult};


pub async fn run_worker() -> ! {
    tracing::info!("Worker initializing…");

    loop {
        if let Err(e) = run_worker_once().await {
            tracing::error!("Worker iteration failed: {e}");
            sleep(Duration::from_secs(1)).await;
        }
    }
}


async fn run_worker_once() -> anyhow::Result<()> {
    // 🔌 Redis
    let redis_url =
        env::var("REDIS_URL").unwrap_or_else(|_| "redis://redis:6379".to_string());

    let client = redis::Client::open(redis_url)?;
    let mut con = client.get_async_connection().await?;

    // 🔌 PostgreSQL
    let database_url = env::var("DATABASE_URL")?;
    let pool = PgPool::connect(&database_url).await?;

    let http = Client::new();

    let result: Option<(String, String)> =
        con.blpop("score_jobs", 0.0).await?;

    let (_key, job_json) = match result {
        Some(v) => v,
        None => {
            sleep(Duration::from_millis(500)).await;
            return Ok(());
        }
    };

    let job: Job = serde_json::from_str(&job_json)?;

    tracing::info!(job_id = %job.job_id, "▶️ Processing job");

    let start = Instant::now(); 
    let rows = sqlx::query(
        r#"
        SELECT age
        FROM users_user
        WHERE age IS NOT NULL
        LIMIT $1
        "#
    )
    .bind(job.payload.limit as i64)
    .fetch_all(&pool)
    .await?;
     
    let ages: Vec<i32> = rows
        .iter()
        .filter_map(|row| row.try_get::<i32, _>("age").ok())
        .collect();
    if ages.is_empty() {
        tracing::warn!("No ages returned"); 
        return Ok(()); 
    } 
    let sum: i64 = ages.iter().map(|&a| a as i64).sum(); 
    let average = sum as f64 / ages.len() as f64; 
    let execution_time_ms = start.elapsed().as_secs_f64() * 1000.0; 
    let result = JobResult { 
        engine: "rust".to_string(), 
        processed_items: ages.len(), 
        average_age: average, 
        execution_time_ms, 
    };

    notify_django(&http, &job.job_id, result).await?;

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
