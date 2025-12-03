// Arquivo: src/algorithms/linear_regression.rs
//! Implementação simples de regressão linear usando mínimos quadrados


pub fn fit_linear_regression(x: &[f64], y: &[f64]) -> Option<(f64, f64)> {
if x.len() != y.len() || x.is_empty() {
return None;
}
let n = x.len() as f64;
let sum_x: f64 = x.iter().sum();
let sum_y: f64 = y.iter().sum();
let sum_xy: f64 = x.iter().zip(y.iter()).map(|(a,b)| a*b).sum();
let sum_x2: f64 = x.iter().map(|v| v*v).sum();


let denom = n * sum_x2 - sum_x * sum_x;
if denom.abs() < 1e-12 {
return None;
}
let slope = (n * sum_xy - sum_x * sum_y) / denom;
let intercept = (sum_y - slope * sum_x) / n;
Some((slope, intercept))
}


pub fn predict_from_linear(slope: f64, intercept: f64, x: f64) -> f64 {
slope * x + intercept
}
```


---


### 5) `src/algorithms/mod.rs`


```rust
pub mod linear_regression;


pub use linear_regression::*;