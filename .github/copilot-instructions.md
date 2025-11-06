# DQTimes - AI Coding Agent Instructions

## Project Overview
DQTimes is a high-performance time series forecasting system migrated from Rust to Python, utilizing a **hybrid architecture** combining Python/FastAPI with CUDA-accelerated C++ libraries for computational performance.

**Core Architecture**: 3-tier microservices stack
- **Frontend**: React + Vite (port 5173 dev, containerized with Docker)
- **Backend Service Layer**: FastAPI (`server/app.py` - port 8000)
- **Compute Engine**: FastAPI + Dask (`dqtimes/app/main.py` - port 80, Dask dashboard 8787)

## Critical Technical Patterns

### Hybrid Python-CUDA Architecture
The project's **most unique aspect** is the CUDA/C++ integration pattern:

**Compilation Requirements** (see `dqtimes/README.md`):
```bash
# C++ to Python module (using pybind11)
c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) utils.cpp -o utilitarios$(python3-config --extension-suffix)

# CUDA to shared library
nvcc -arch=sm_75 -o medias_moveis.so -shared -Xcompiler -fPIC medias_moveis.cu
```

**Integration Pattern** (`dqtimes/app/aplicacao.py`):
- Load `.so` files via `ctypes.CDLL()`
- Define function signatures with `argtypes` and `restype`
- Convert Python lists to ctypes arrays: `(ctypes.c_float * len(data))(*data)`
- All CUDA libs in `dqtimes/app/libs/`: `medias_moveis.cu`, `holt_winters.cu`, `interpolador1d.cu`, etc.

### Time Series Forecasting Pipeline
**Main Entry Point**: `forecast_temp()` in `dqtimes/app/aplicacao.py`

**Workflow**:
1. **Split data** into base/test sets (70/30 split via `utilitarios_lib.split_list`)
2. **Compute predictions** using CUDA kernels for multiple periods [3,4,5,6,7,14,30]
   - Moving averages (`cuda_medias_moveis`)
   - Holt-Winters smoothing (`cuda_holt_winters`)
3. **Evaluate MSE** against test set using `utilitarios_lib.compara_testemunha`
4. **Select best model** (lowest MSE) and method (HW vs MA)
5. **Bayesian inference** for trend probability via `utilitarios_lib.inferencia_bayes_bin_general`

### API Endpoints Architecture

**Compute Service** (`dqtimes/app/main.py`):
- `POST /projecao_lista/` - Direct list forecasting (JSON array input)
- `POST /projecao_dataframe/` - CSV batch processing with Dask parallel execution
  - Uses `dask.distributed.Client` with LocalCluster
  - Dashboard at `:8787` for monitoring
  - Pagination support: `page`, `page_size` query params
  - Returns: `execution_time`, `total_pages`, `current_page`, `projecoes`

**Service Layer** (`server/app.py`):
- Uses Pydantic models from `models.py` for request/response validation
- Service classes in `services/` directory pattern

## Development Workflows

### Running the Application
**Docker-based deployment** (TensorFlow GPU base image):
```bash
# Build from dqtimes/Dockerfile
docker build -t dqtimes-compute ./dqtimes
docker run -p 80:80 -p 8787:8787 dqtimes-compute

# Frontend (Vite dev server)
npm run dev  # Port 5173

# Backend service
cd server && uvicorn app:app --reload --port 8000
```

**Environment**: `tensorflow/tensorflow:2.14.0-gpu` base with pybind11, dask[distributed], dask[dataframe]

### Testing CUDA Functions
Pattern in `dqtimes/README.md`:
```python
import ctypes
import numpy as np

cuda_lib = ctypes.CDLL('./sumArrayGPU.so')
cuda_lib.my_cuda_function.argtypes = [ctypes.POINTER(ctypes.c_int), ...]
# Use PyCUDA for GPU memory allocation
```

## Project-Specific Conventions

### File Structure Logic
- **`dqtimes/app/libs/`**: All CUDA `.cu` files + compiled `.so` libraries (both checked in)
- **`dqtimes/app/aplicacao.py`**: Main CUDA library wrapper/orchestrator
- **`dqtimes/app/libs/py_utils.py`**: Pure Python utility fallbacks (binariza, split_list, etc.)
- **`dqtimes/app/libs/modelos_preditivos.py`**: High-level forecasting algorithms (naive_bayes, interpolador)

### Data Processing Patterns
**Dask Usage** (`dqtimes/app/main.py`):
- Always use `dd.read_csv()` for large files
- Iterate partitions via `.to_delayed()` and `.compute()`
- Temporary file pattern for uploads: `tempfile.NamedTemporaryFile(delete=False, suffix=".csv")`

**Type Conversions** (critical for ctypes):
- Python list → ctypes array: `(ctypes.c_float * len(data))(*data)`
- Extract from ctypes: `[arr[i] for i in range(length)]`
- Pointer types: Use `ctypes.POINTER(ctypes.c_float)` for function signatures

### Frontend Integration
- React 19 with Vite + SWC
- Component structure: `src/components/{feature}/{Feature}.jsx` + `{feature}.css`
- No routing configured yet (single Login page in `App.jsx`)
- Form validation pattern in `Login.jsx`: useState + useCallback hooks, regex validation, error state management

## Common Pitfalls

1. **CUDA Library Loading**: Must use absolute/relative paths from execution context (`app/libs/medias_moveis.so` when running from project root)
2. **Ctypes Array Lengths**: Always pass explicit length parameters - ctypes doesn't know array bounds
3. **Dask Dashboard**: Always exposed on `:8787` - check `client.dashboard_link` in startup logs
4. **TensorFlow Dependency**: Base image is tensorflow-gpu but not actively used - required for CUDA runtime
5. **Port Conflicts**: Compute (80), Service (8000), Frontend (5173), Dask (8787) - ensure all available

## Key Files Reference
- **Main API**: `dqtimes/app/main.py` (FastAPI + Dask)
- **CUDA Orchestrator**: `dqtimes/app/aplicacao.py`
- **Core Algorithm**: `forecast_temp()` function (lines 98-152 in aplicacao.py)
- **Compilation Guide**: `dqtimes/README.md` (C++/CUDA build commands)
- **Docker Config**: `dqtimes/Dockerfile` (TensorFlow GPU base)
- **Service Template**: `server/services/example_service.py`

## Known Limitations
- No docker-compose.yml exists despite extensive documentation in README.md
- `server/services/time_series.py` is empty placeholder
- No integration tests between CUDA libs and Python wrappers
- Frontend has no API integration yet - login is UI-only simulation
