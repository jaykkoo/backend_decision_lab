// fn main() {
//     panic!("THIS IS THE REAL BINARY");
// }


use axum::{routing::get, Router};
use tokio::net::TcpListener;
use tracing_subscriber::{fmt, EnvFilter};

mod workers;
mod models;

#[tokio::main]
async fn main() {
    // 🔧 Logger (UNE SEULE FOIS, avant tout)
    fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into()),
        )
        .init();

    tracing::info!("🚀 rust_engine starting");

    let mode = std::env::var("MODE")
        .unwrap_or_else(|_| "api".to_string());

    // =====================
    // WORKER MODE
    // =====================
    if mode == "worker" {
        tracing::info!("Running in WORKER mode");

        // ⛔ DOIT BLOQUER À VIE
        workers::run_worker().await;

        unreachable!("run_worker never returns");
    }

    // =====================
    // API MODE
    // =====================
    tracing::info!("Running in API mode");

    let app = Router::new()
        .route("/health", get(|| async { "ok" }));

    let listener = TcpListener::bind("0.0.0.0:8080")
        .await
        .expect("Failed to bind");

    axum::serve(listener, app)
        .await
        .expect("Server failed");
}
