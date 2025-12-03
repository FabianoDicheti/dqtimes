# forecast_crate


Estrutura mínima de exemplo para previsão em Rust com compatibilidade futura com Python (pyo3).


## Como compilar (Rust)


```bash
cargo build
```


## Como rodar o script de exemplo


```bash
cargo run --bin scripts/linear_regression -- data/teste.txt 5
```


## Bindings Python (opcional)


Ative a feature `python-binding` e use `maturin` para construir a roda:


```bash
cargo build --release --features python-binding
# ou use maturin build --release --features python-binding
```
```


---


## Onde colocar cada arquivo (resumo)


- `Cargo.toml` — raiz do projeto
- `src/lib.rs` — `src/lib.rs`
- `src/prediction.rs` — `src/prediction.rs`
- `src/algorithms/linear_regression.rs` — `src/algorithms/linear_regression.rs`
- `src/algorithms/mod.rs` — `src/algorithms/mod.rs`
- `src/data.rs` — `src/data.rs`
- `src/error.rs` — `src/error.rs`
- `src/metrics/mod.rs` — `src/metrics/mod.rs`
- `src/preprocessing/mod.rs` — `src/preprocessing/mod.rs`
- `src/scripts/linear_regression.rs` — `src/scripts/linear_regression.rs`
- `src/scripts/mod.rs` — `src/scripts/mod.rs`
- `data/teste.txt` — exemplo de dados
- `lab/teste.txt` — (seu arquivo de laboratório)
- `README.md` — raiz


---


## Instruções rápidas para rodar e testar


1. Copie os arquivos para os caminhos indicados.
2. `cargo build` — compila em Rust.
3. `cargo run --bin scripts/linear_regression -- data/teste.txt 5` — executa o script exemplo (ainda que bin target não esteja configurado; ver nota abaixo).


**Nota sobre bins**: O exemplo `src/scripts/linear_regression.rs` foi escrito como um bin script de exemplo. Para deixá-lo como bin executável pelo `cargo run --bin`, você pode mover o arquivo para `src/bin/linear_regression.rs` ou adicionar um `[[bin]]` entry em `Cargo.toml`. Se preferir eu já deixo pronto para `src/bin`.
