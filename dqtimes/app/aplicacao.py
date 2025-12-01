import ctypes
import numpy as np
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determinar caminho das bibliotecas de forma robusta
lib_dir = os.path.join(os.path.dirname(__file__), 'libs')

# Flag para indicar se CUDA está disponível
USE_CUDA = False

# Tentar carregar as bibliotecas CUDA
try:
    cuda_lib = ctypes.CDLL(os.path.join(lib_dir, 'medias_moveis.so'))
    hw_cuda_lib = ctypes.CDLL(os.path.join(lib_dir, 'holt_winters.so'))
    interpolador1d_lib = ctypes.CDLL(os.path.join(lib_dir, 'interpolador1d.so'))
    utilitarios_lib = ctypes.CDLL(os.path.join(lib_dir, 'utilitarios.so'))
    USE_CUDA = True
    logger.info("CUDA libraries loaded successfully")
except (OSError, FileNotFoundError) as e:
    logger.warning(f"CUDA libraries not found ({e}), using Python fallback implementations")
    USE_CUDA = False

# Define os tipos de ponteiros
float_pointer = ctypes.POINTER(ctypes.c_float)
float_pointer_pointer = ctypes.POINTER(float_pointer)

# ============ FALLBACK IMPLEMENTATIONS (Pure Python) ============

def python_moving_average(values, period):
    """Implementação Python de média móvel simples"""
    result = []
    for i in range(len(values)):
        if i < period - 1:
            result.append(np.mean(values[:i+1]))
        else:
            result.append(np.mean(values[i-period+1:i+1]))
    return result

def python_holt_winters_simple(values, period):
    """Implementação simplificada de Holt-Winters"""
    alpha = 0.2
    beta = 0.1

    if len(values) < period:
        return values.copy()

    result = [values[0]]
    level = values[0]
    trend = 0

    for i in range(1, len(values)):
        last_level = level
        level = alpha * values[i] + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        result.append(level + trend)

    return result

def python_split_list(data, second_member_size):
    """Divide lista em base e testemunha"""
    split_idx = len(data) - second_member_size
    return data[:split_idx], data[split_idx:]

def python_mse(actual, predicted):
    """Calcula Mean Squared Error"""
    min_len = min(len(actual), len(predicted))
    actual = actual[:min_len]
    predicted = predicted[:min_len]
    return float(np.mean((np.array(actual) - np.array(predicted)) ** 2))

def python_binarize(data, lookback):
    """Binariza dados (1 se subiu, 0 se desceu)"""
    result = []
    for i in range(1, len(data)):
        result.append(1 if data[i] > data[i-1] else 0)
    return result

def python_bayes_probability(binary_data, lookback):
    """Calcula probabilidade bayesiana de aumento"""
    if len(binary_data) < lookback:
        lookback = len(binary_data)

    recent = binary_data[-lookback:] if lookback > 0 else binary_data
    increases = sum(recent)
    total = len(recent)

    if total == 0:
        return 0.5

    # Prior bayesiano simples
    alpha = 1  # Prior
    beta = 1
    return (increases + alpha) / (total + alpha + beta)

# ============ END FALLBACK IMPLEMENTATIONS ============

# Define os tipos de argumentos e resultados para as funções das bibliotecas (apenas se CUDA disponível)
if USE_CUDA:
    cuda_lib.moving_average.argtypes = [float_pointer, float_pointer_pointer, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    cuda_lib.moving_average.restype = None

    hw_cuda_lib.holt_winters_smoothing.argtypes = [float_pointer, float_pointer_pointer, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    hw_cuda_lib.holt_winters_smoothing.restype = None

    interpolador1d_lib.run_interpolation_kernel.argtypes = [float_pointer, float_pointer, float_pointer, float_pointer, float_pointer, ctypes.c_int]
    interpolador1d_lib.run_interpolation_kernel.restype = None

    utilitarios_lib.split_list.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
    utilitarios_lib.split_list.restype = None

    utilitarios_lib.compara_testemunha.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int]
    utilitarios_lib.compara_testemunha.restype = ctypes.c_double

    utilitarios_lib.binariza.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    utilitarios_lib.binariza.restype = None

    utilitarios_lib.inferencia_bayes_bin_general.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]
    utilitarios_lib.inferencia_bayes_bin_general.restype = ctypes.c_double

    utilitarios_lib.tax_acrescimo.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
    utilitarios_lib.tax_acrescimo.restype = None

# Funções de exemplo (com fallback para Python se CUDA não disponível)
def cuda_medias_moveis(values, periods):
    if not USE_CUDA:
        # Usar implementação Python
        return [python_moving_average(values, period) for period in periods]

    num_values = len(values)
    num_periods = len(periods)

    values_array = np.array(values, dtype=np.float32)
    values_ctypes = values_array.ctypes.data_as(float_pointer)

    periods_array = np.array(periods, dtype=np.int32)
    periods_ctypes = periods_array.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

    averages = np.zeros((num_periods, num_values), dtype=np.float32)
    averages_pointers = (float_pointer * num_periods)()
    for i in range(num_periods):
        averages_pointers[i] = averages[i].ctypes.data_as(float_pointer)

    cuda_lib.moving_average(values_ctypes, averages_pointers, num_values, periods_ctypes, num_periods)

    return averages.tolist()

def cuda_holt_winters(values, periods):
    if not USE_CUDA:
        # Usar implementação Python
        return [python_holt_winters_simple(values, period) for period in periods]

    num_values = len(values)
    num_periods = len(periods)

    values_array = np.array(values, dtype=np.float32)
    values_ctypes = values_array.ctypes.data_as(float_pointer)

    periods_array = np.array(periods, dtype=np.int32)
    periods_ctypes = periods_array.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

    projections = np.zeros((num_periods, num_values), dtype=np.float32)
    projections_pointers = (float_pointer * num_periods)()
    for i in range(num_periods):
        projections_pointers[i] = projections[i].ctypes.data_as(float_pointer)

    hw_cuda_lib.holt_winters_smoothing(values_ctypes, projections_pointers, num_values, periods_ctypes, num_periods)

    return projections.tolist()

def cuda_interpolacao1d(indices, valores):
    n = len(indices)

    indices_array = np.array(indices, dtype=np.float32)
    valores_array = np.array(valores, dtype=np.float32)
    indices_ctypes = indices_array.ctypes.data_as(float_pointer)
    valores_ctypes = valores_array.ctypes.data_as(float_pointer)

    result_multivariate = np.zeros(n, dtype=np.float32)
    result_gaussian = np.zeros(n, dtype=np.float32)
    result_polynomial = np.zeros(n, dtype=np.float32)
    result_multivariate_ctypes = result_multivariate.ctypes.data_as(float_pointer)
    result_gaussian_ctypes = result_gaussian.ctypes.data_as(float_pointer)
    result_polynomial_ctypes = result_polynomial.ctypes.data_as(float_pointer)

    interpolador1d_lib.run_interpolation_kernel(indices_ctypes, valores_ctypes, result_multivariate_ctypes, result_gaussian_ctypes, result_polynomial_ctypes, n)

    return result_multivariate.tolist(), result_gaussian.tolist(), result_polynomial.tolist()


def forecast_temp(data, n_projecoes):
    periods = [3, 4, 5, 6, 7, 14, 30]
    segundo_membro = int(len(data) * 0.3)

    # Split data into base and testemunha (test set)
    if USE_CUDA:
        data_ctypes = (ctypes.c_float * len(data))(*data)
        base_ctypes = (ctypes.c_float * (len(data) - segundo_membro))()
        testemunha_ctypes = (ctypes.c_float * segundo_membro)()
        utilitarios_lib.split_list(data_ctypes, len(data), segundo_membro, base_ctypes, testemunha_ctypes)

        base = [base_ctypes[i] for i in range(len(data) - segundo_membro)]
        testemunha = [testemunha_ctypes[i] for i in range(segundo_membro)]
    else:
        base, testemunha = python_split_list(data, segundo_membro)

    # Calculate projections with multiple methods
    moving_averages = cuda_medias_moveis(base, periods)
    holt_winters_projections = cuda_holt_winters(base, periods)

    # Find best method by comparing with test set
    errors = []
    for i, period in enumerate(periods):
        if USE_CUDA:
            min_len = min(len(testemunha), len(holt_winters_projections[i]))
            proj_ctypes = (ctypes.c_float * min_len)(*holt_winters_projections[i][:min_len])
            testemunha_ctypes = (ctypes.c_float * min_len)(*testemunha[:min_len])
            mse_hw = utilitarios_lib.compara_testemunha(testemunha_ctypes, proj_ctypes, min_len)

            min_len = min(len(testemunha), len(moving_averages[i]))
            avg_ctypes = (ctypes.c_float * min_len)(*moving_averages[i][:min_len])
            testemunha_ctypes = (ctypes.c_float * min_len)(*testemunha[:min_len])
            mse_ma = utilitarios_lib.compara_testemunha(testemunha_ctypes, avg_ctypes, min_len)
        else:
            mse_hw = python_mse(testemunha, holt_winters_projections[i])
            mse_ma = python_mse(testemunha, moving_averages[i])

        errors.append((mse_hw, period, 'HW'))
        errors.append((mse_ma, period, 'MA'))

    # Select best method
    _, best_period, best_method = min(errors)

    # Generate final projection with best method
    if best_method == 'HW':
        final_projection = cuda_holt_winters(data, [best_period])
    else:
        final_projection = cuda_medias_moveis(data, [best_period])

    # Calculate probability of increase using Bayesian inference
    if USE_CUDA:
        data_ctypes = (ctypes.c_float * len(data))(*data)
        binarios_ctypes = (ctypes.c_int * len(data))()
        utilitarios_lib.binariza(data_ctypes, len(data), n_projecoes, n_projecoes, binarios_ctypes)
        binarios = [binarios_ctypes[i] for i in range(len(data))]
        probabilidade_subir = utilitarios_lib.inferencia_bayes_bin_general(binarios_ctypes, len(data), n_projecoes)
    else:
        binarios = python_binarize(data, n_projecoes)
        probabilidade_subir = python_bayes_probability(binarios, n_projecoes)

    return {
        "final_projection": final_projection,
        "moving_averages": moving_averages,
        "holt_winters_projections": holt_winters_projections,
        "probabilidade_subir": probabilidade_subir
    }


# Exemplo de uso
# data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# n_projecoes = 3
# proj, probab = forecast_temp(data, n_projecoes)
# print("Projeção:", proj)
# print("Probabilidade de aumento:", probab)
