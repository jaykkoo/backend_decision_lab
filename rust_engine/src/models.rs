// src/models.rs
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct Job {
    pub job_id: String,
    pub payload: JobPayload,
}

#[derive(Debug, Deserialize)]
pub struct JobPayload {
    pub engine: String,
    pub limit: Option<usize>,
}

#[derive(Serialize)]
pub struct ProductViewStat {
    pub product_id: i64,
    pub views: u64,
    pub average_age: f64,
}

#[derive(Serialize)]
pub struct JobResult {
    pub engine: String,
    pub processed_items: usize,
    pub products_count: usize,
    pub cpu_time_ms: f64,
    pub memory_mb_peak: f64,
    pub views_by_product: Vec<ProductViewStat>,
}
