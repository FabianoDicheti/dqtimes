import ctypes
import numpy as np

# Carrega as bibliotecas compartilhadas
cuda_lib = ctypes.CDLL('app/libs/medias_moveis.so')
hw_cuda_lib = ctypes.CDLL('app/libs/holt_winters.so')
interpolador1d_lib = ctypes.CDLL('app/libs/interpolador1d.so')
utilitarios_lib = ctypes.CDLL('app/libs/utilitarios.so')

# Define os tipos de ponteiros
float_pointer = ctypes.POINTER(ctypes.c_float)
float_pointer_pointer = ctypes.POINTER(float_pointer)

# Define os tipos de argumentos e resultados para as funções das bibliotecas
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

# Funções de exemplo
def cuda_medias_moveis(values, periods):
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
    
    data_ctypes = (ctypes.c_float * len(data))(*data)
    segundo_membro = int(len(data) * 0.3)
    base_ctypes = (ctypes.c_float * (len(data) - segundo_membro))()
    testemunha_ctypes = (ctypes.c_float * segundo_membro)()
    utilitarios_lib.split_list(data_ctypes, len(data), segundo_membro, base_ctypes, testemunha_ctypes)
    
    base = [base_ctypes[i] for i in range(len(data) - segundo_membro)]
    testemunha = [testemunha_ctypes[i] for i in range(segundo_membro)]
    
    moving_averages = cuda_medias_moveis(base, periods)
    holt_winters_projections = cuda_holt_winters(base, periods)
    
    errors = []
    for i, period in enumerate(periods):
        min_len = min(len(testemunha), len(holt_winters_projections[i]))
        proj_ctypes = (ctypes.c_float * min_len)(*holt_winters_projections[i][:min_len])
        mse_hw = utilitarios_lib.compara_testemunha(testemunha_ctypes, proj_ctypes, min_len)
        
        min_len = min(len(testemunha), len(moving_averages[i]))
        avg_ctypes = (ctypes.c_float * min_len)(*moving_averages[i][:min_len])
        mse_ma = utilitarios_lib.compara_testemunha(testemunha_ctypes, avg_ctypes, min_len)
        
        errors.append((mse_hw, period, 'HW'))
        errors.append((mse_ma, period, 'MA'))
    
    _, best_period, best_method = min(errors)
    
    if best_method == 'HW':
        final_projection = cuda_holt_winters(data, [best_period])
    else:
        final_projection = cuda_medias_moveis(data, [best_period])
    
    binarios_ctypes = (ctypes.c_int * len(data))()
    utilitarios_lib.binariza(data_ctypes, len(data), n_projecoes, n_projecoes, binarios_ctypes)
    
    binarios = [binarios_ctypes[i] for i in range(len(data))]
    
    probabilidade_subir = utilitarios_lib.inferencia_bayes_bin_general(binarios_ctypes, len(data), n_projecoes)
    
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
