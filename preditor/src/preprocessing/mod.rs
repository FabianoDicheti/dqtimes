pub fn difference(values: &[f64], lag: usize) -> Vec<f64> {
if lag == 0 || values.len() <= lag { return vec![]; }
values.iter().skip(lag).zip(values.iter()).map(|(a,b)| a - b).collect()
}