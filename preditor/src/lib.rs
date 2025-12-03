pub mod prediction;
pub mod algorithms;
pub mod error;
pub mod data;
pub mod metrics;
pub mod preprocessing;
pub mod scripts;


// Re-exportações públicas úteis
pub use prediction::{TimeSeries, PredictionParams, ForecastResult, PredictiveModel};
```


---


### 3) `src/prediction.rs`


```rust
// A