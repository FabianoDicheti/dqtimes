# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 08:17:59 2024

@author: Fabiano Dicheti
"""

import numpy as np
import datetime
from copy import copy as cp


def split_list(lista, segundo_membro):
    """
    Divide uma lista em duas sub-listas: a primeira contendo os elementos iniciais da lista
    e a segunda contendo os últimos 'segundo_membro' elementos.

    Parâmetros:
        lista (list): A lista original a ser dividida.
        segundo_membro (int): O número de elementos na segunda sub-lista.

    Retorna:
        list: Uma lista contendo duas sub-listas, a primeira com os elementos iniciais
        e a segunda com os últimos 'segundo_membro' elementos.
    """
    # Validação dos parâmetros de entrada
    if not isinstance(segundo_membro, int) or segundo_membro < 0 or segundo_membro > len(lista):
        raise ValueError("O parâmetro 'segundo_membro' deve ser um inteiro não negativo menor ou igual ao tamanho da lista.")

    # Divisão da lista
    base = lista[:-segundo_membro] if segundo_membro != 0 else lista[:]
    testemunha = lista[-segundo_membro:]

    return [base, testemunha]

# Exemplo de uso
lista_exemplo = [1, 2, 3, 4, 5]
print(split_list(lista_exemplo, 2))  # Saída: [[1, 2, 3], [4, 5]]


def compara_testemunha(testemunha, previsao):
    """
    Compara um array de valores reais com um array de previsões, calculando o erro quadrático
    para cada valor e o erro quadrático médio.

    Parâmetros:
        testemunha (list): Array de valores reais.
        previsao (list): Array de valores previstos.

    Retorna:
        list: Uma lista contendo o erro quadrático para cada valor previsto (formatado com 3 casas decimais)
        e o erro quadrático médio (um único valor).
    """
    # Cálculo do erro quadrático para cada valor
    erros_quadraticos = [(real - previsto) ** 2 for real, previsto in zip(testemunha, previsao)]
    erros_quadraticos_formatados = [f"{erro:.3f}" for erro in erros_quadraticos]

    # Cálculo do erro quadrático médio
    erro_quadratico_medio = sum(erros_quadraticos) / len(erros_quadraticos)
    erro_quadratico_medio_formatado = round(erro_quadratico_medio, 3)

    return [erros_quadraticos_formatados, erro_quadratico_medio_formatado]


def binariza(lista, n_ante, n_poste):
    from copy import copy as cp
    
    # Criação das listas ante e poste
    ante = cp(lista)
    poste = cp(lista)
    
    # Adiciona o último elemento em ante e o primeiro elemento em poste, se necessário
    if n_ante > 0:
        ante.extend([ante[-1]] * (n_ante - 1))
        ante = ante[:-n_ante]
    if n_poste > 0:
        poste.extend([poste[0]] * (n_poste - 1))
        poste = poste[n_poste:]
    
    # Cálculo da diferença e binarização
    binarios = [1 if poste[i] - ante[i] > 0 else 0 for i in range(len(ante))]
    
    return binarios

# Exemplo de uso
#lista_exemplo = [1, 2, 3, 4, 5]
#print(binariza(lista_exemplo, 2, 2))  # Saída para binariza_4
#print(binariza(lista_exemplo, 4, 1))  # Saída para binariza_t_5
       
##################################################################

def inferencia_bayes_bin_general(binarios, n):
    from copy import copy as cp

    if n < 2:
        raise ValueError("O valor de 'n' deve ser maior ou igual a 2.")

    pref = cp(binarios)
    final = pref[-(n-1):]
    quebrar = cp(binarios)
    subsequencias = []

    while len(quebrar) >= n:
        par = quebrar[:n]
        subsequencias.append(par)
        quebrar.pop(0)

    subir = 0.5
    combinacoes = [(i, j) for i in range(2) for j in range(n - 1)]

    resultados = {}

    for i, comb in enumerate(combinacoes):
        valor_final = [int(x) for x in bin(i)[2:].zfill(n - 1)]
        if valor_final == final:
            acres = subsequencias.count(valor_final + [1])
            decre = subsequencias.count(valor_final + [0])
            if acres > 0:
                subir = acres / (acres + decre)
            else:
                subir = 0.001

    resultado = [subir]
    return resultado

from copy import copy as cp
from statistics import mean


def tax_acrescimo(lista):
    coluna = lista[:-1]
    poste = lista[1:]
    
    acrescimo = [poste[x] - coluna[x] for x in range(len(coluna)) if poste[x] - coluna[x] > 0]
    decrescimo = [poste[x] - coluna[x] for x in range(len(coluna)) if poste[x] - coluna[x] <= 0]
    
    media_lista = mean(lista)
    
    if acrescimo:
        acrescimo_medio = mean(acrescimo)
        acrescimo_percentual = acrescimo_medio / media_lista
    else:
        acrescimo_percentual = 0.001

    if decrescimo:
        decrescimo_medio = mean(decrescimo)
        decrescimo_percentual = decrescimo_medio / media_lista
    else:
        decrescimo_percentual = 0.001
    
    return [acrescimo_percentual, decrescimo_percentual]

# Exemplo de uso
lista_exemplo = [1, 2, 3, 4, 5]
print(tax_acrescimo(lista_exemplo))  # Saída: [0.5, -0.16666666666666666]
