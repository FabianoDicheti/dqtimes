pub fn mae(true_vals: &[f64], pred: &[f64]) -> Option<f64> {
if true_vals.len() != pred.len() || true_vals.is_empty() { return None; }
let sum: f64 = true_vals.iter().zip(pred.iter()).map(|(a,b)| (a-b).abs()).sum();
Some(sum / true_vals.len() as f64)
}