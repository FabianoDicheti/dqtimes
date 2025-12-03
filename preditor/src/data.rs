use crate::error::ForecastError;
use std::fs::File;
use std::io::{BufRead, BufReader};


/// Lê um arquivo simples de valores (uma coluna) e retorna uma TimeSeries mínima
pub fn read_values_from_file(path: &str) -> Result<Vec<f64>, ForecastError> {
let f = File::open(path)?;
let reader = BufReader::new(f);
let mut vals = Vec::new();
for line in reader.lines() {
let l = line?;
if l.trim().is_empty() { continue; }
match l.trim().parse::<f64>() {
Ok(v) => vals.push(v),
Err(_) => return Err(ForecastError::Parse(format!("invalid float: {}", l))),
}
}
Ok(vals)
}