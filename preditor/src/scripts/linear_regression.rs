use forecast_crate::{TimeSeries, PredictionParams, predict_linear_regression};
use std::env;


fn main() {
let args: Vec<String> = env::args().collect();
let path = args.get(1).map(|s| s.as_str()).unwrap_or("data/teste.txt");
let horizon = args.get(2).and_then(|s| s.parse::<usize>().ok()).unwrap_or(3);


let content = std::fs::read_to_string(path).expect("cannot read file");
let values: Vec<f64> = content.lines().filter_map(|l| l.trim().parse().ok()).collect();
let ts = TimeSeries { values, timestamps: None };
let params = PredictionParams { horizon, ..Default::default() };
let res = predict_linear_regression(&ts, &params);
println!("Forecast: {:?}
Meta: {:?}", res.forecast, res.meta);
}