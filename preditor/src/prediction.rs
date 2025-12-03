// Arquivo: src/prediction.rs
//! API pública de previsão: tipos, traits e wrappers (stubs)


use serde::{Deserialize, Serialize};
use std::collections::HashMap;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TimeSeries {
pub values: Vec<f64>,
pub timestamps: Option<Vec<i64>>,
}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PredictionParams {
pub horizon: usize,
pub freq_seconds: Option<i64>,
pub confidence: Option<f64>,
pub extras: Option<HashMap<String, String>>,
}


impl Default for PredictionParams {
fn default() -> Self {
PredictionParams {
horizon: 1,
freq_seconds: None,
confidence: Some(0.95),
extras: None,
}
}
}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ForecastResult {
pub forecast: Vec<f64>,
pub timestamps: Option<Vec<i64>>,
pub lower: Option<Vec<f64>>,
pub upper: Option<Vec<f64>>,
pub meta: Option<HashMap<String, String>>,
}


impl ForecastResult {
pub fn new(forecast: Vec<f64>) -> Self {
}