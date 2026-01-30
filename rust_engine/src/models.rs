use serde::{Deserialize, Serialize};


#[derive(Debug, Deserialize)]
pub struct Job {
    pub job_id: String,
    pub payload: JobPayload,
}

#[derive(Debug, Deserialize)]
pub struct JobPayload {
    pub engine: String,
    pub limit: usize,
}

#[derive(Debug, Serialize)]
pub struct JobResult {
    pub engine: String,              // "rust"
    pub processed_items: usize,      // ex: 10000
    pub average_age: f64,            // résultat métier
    pub execution_time_ms: f64,      // temps total
}
