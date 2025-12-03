use thiserror::Error;


#[derive(Error, Debug)]
pub enum ForecastError {
#[error("I/O error: {0}")]
Io(#[from] std::io::Error),


#[error("parse error: {0}")]
Parse(String),


#[error("model error: {0}")]
Model(String),
}