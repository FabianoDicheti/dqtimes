# Import only the forecast function, not CUDA libs
from .aplicacao import forecast_temp

# Optional CUDA libs import (may not be available)
try:
    from .aplicacao import USE_CUDA
    if USE_CUDA:
        from .aplicacao import (
            cuda_lib,
            hw_cuda_lib,
            interpolador1d_lib,
            utilitarios_lib
        )
except (ImportError, AttributeError):
    # CUDA not available, using Python fallback
    USE_CUDA = False