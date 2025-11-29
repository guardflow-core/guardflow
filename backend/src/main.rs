use axum::{
    routing::{get, post},
    Router,
    Json,
};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use tower_http::cors::CorsLayer;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();
    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health_check))
        .route("/api/scan", post(create_scan))
        .layer(CorsLayer::permissive());
        
    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000").await.unwrap();
    tracing::info!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> Json<Value> {
    Json(json!({ "message": "Welcome to GuardFlow API" }))
}

async fn health_check() -> Json<Value> {
    Json(json!({ "status": "healthy", "version": "0.1.0" }))
}

#[derive(Deserialize)]
struct ScanRequest {
    model_url: String,
    #[allow(dead_code)]
    scan_type: String,
}

#[derive(Serialize)]
struct ScanResponse {
    id: String,
    score: u8,
    status: String,
    details: Value,
}

async fn create_scan(Json(payload): Json<ScanRequest>) -> Json<ScanResponse> {
    let score = if payload.model_url.contains("high-risk") { 45 } else { 92 };
    let response = ScanResponse {
        id: uuid::Uuid::new_v4().to_string(),
        score,
        status: "completed".to_string(),
        details: json!({
            "bias_detected": score < 80,
            "fairness_metric": "0.95",
            "timestamp": chrono::Utc::now().to_string()
        }),
    };
    Json(response)
}
