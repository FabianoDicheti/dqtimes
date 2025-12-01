# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:07:24 2024

@author: Fabiano Dicheti
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import time

def moving_averages(lst):
    result = {}
    periods = [3, 4, 5, 6, 7, 14, 30]
    # Converte a lista para um array NumPy e substitui valores não numéricos por 0
    lst = np.array(lst, dtype=float)
    np.nan_to_num(lst, copy=False)
    for period in periods:
        if len(lst) >= period:
            result[f'MA_{period}'] = np.convolve(lst, np.ones(period)/period, mode='valid')
        else:
            result[f'MA_{period}'] = np.array([])
    return result


def holt_winters(lst):
    result = {}
    periods = [3, 4, 5, 6, 7, 14, 30]
    for period in periods:
        if len(lst) >= period:
            model = ExponentialSmoothing(lst, trend='add', seasonal='add', seasonal_periods=period)
            fit = model.fit()
            result[f'HW_{period}'] = fit.fittedvalues
        else:
            result[f'HW_{period}'] = np.array([])
    return result

def process_dataframe(df, n):
    start_time = time.time()
    ma_results = []
    hw_results = []

    for i in range(n):
        for _, row in df.iterrows():
            lst = row.tolist()[1:]  # Remove o primeiro item
            ma_results.append(moving_averages(lst))
            hw_results.append(holt_winters(lst))

    total_time = time.time() - start_time
    print(f'Total execution time: {total_time} seconds')
    return ma_results, hw_results

# Exemplo de uso
df = pd.read_csv('./cp_h.csv')
ma_results, hw_results = process_dataframe(df, 1)
