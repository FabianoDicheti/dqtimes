# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 08:20:42 2024

@author: Fabiano Dicheti
"""

def naive_bayes(lista, n_de_prevs):
    from copy import copy as cp

    lista1 = cp(lista)
    prevs = []
    contador = 1
    taxa = tax_acrescimo(lista)
    while contador <= n_de_prevs:
        n_binarizacao = min(max(len(lista1) - 1, 2), 6)
        a = binariza(lista1, n_binarizacao - 1, n_binarizacao - 1)
        b = inferencia_bayes_bin_general(a, n_binarizacao)
        alta = b[0]

        ultimo = lista1[-1]

        if alta > 0.5:
            prev = ultimo + (ultimo * taxa[0])
        else:
            prev = ultimo + (ultimo * taxa[1])

        prevs.append(prev)
        lista1.append(prev)
        contador += 1

    return prevs



############################### interpolaçãao 2D, receber uma lista de índices e uma lista de valores e retornar as duas completas
############################### se o valor estiver na ultima coluna, o valor da interpolacao deve ser o valor da projecao e nao a replica da ultima


import numpy as np
import datetime

def alfa(lista_valores):
    return sum(lista_valores) / len(lista_valores)

def interpolador(lista_ano, lista_valores):
    ano_atual = datetime.date.today().year

    anos_completos = list(range(lista_ano[0], ano_atual + 1))

    anos_faltantes = sorted(set(anos_completos) - set(lista_ano))

    valores_interpolados = np.interp(anos_faltantes, lista_ano, lista_valores)
    fator_alfa = alfa(lista_valores)
    valores_interpolados = [(valor / fator_alfa) - ((valor * fator_alfa) / 100) for valor in valores_interpolados]

    if len(valores_interpolados) >= 2 and valores_interpolados[-1] == valores_interpolados[-2]:
        valores_interpolados[-1] = (valores_interpolados[-1] / fator_alfa) - ((valores_interpolados[-1] * (2 * fator_alfa)) / 100)

    anos_total = lista_ano + anos_faltantes
    valores_total = lista_valores + valores_interpolados

    ordenados = sorted(zip(anos_total, valores_total), key=lambda x: x[0])
    anos_ordenados, valores_ordenados = zip(*ordenados)

    valores_ordenados = [round(valor, 4) for valor in valores_ordenados]

    return list(anos_ordenados), list(valores_ordenados)

# Exemplo de uso
lista_ano = [2018, 2019, 2021]
lista_valores = [10, 12, 16]
print(interpolador(lista_ano, lista_valores))







# 3 definir interpolacao
def interpolador(lista_ano, lista_valores):
    data = datetime.date.today()
    ano_atual = data.year
    ano_completo = np.arange(lista_ano[0], ano_atual+1, 1)
    a = alfa(lista_valores)
    anos_faltantes = list(set(ano_completo)-set(lista_ano))
    anos_faltantes.sort()
                                        
    valores_inter = np.interp(anos_faltantes, lista_ano, lista_valores)
    valores_inter = [(i/a)-((i*a)/100) for i in valores_inter]
    i = len(valores_inter)-1
    x = valores_inter[i]
    y = valores_inter[i-1]
    if x == y:
        valores_inter[-1] = (valores_inter[-1]/a)-((valores_inter[-1]*(2*a))/100)
    else:
        x = x
            
    
    matriz = [lista_ano + anos_faltantes, lista_valores + [*valores_inter]]
    M = np.asarray(matriz)
    ordem = M[:, M[0].argsort()]    

    ano_total = [int(i) for i in ordem[0]]
    valor_total = [round(j,4) for j in ordem[1]]

    return ano_total, valor_total


def previsao1(lista,ano1):
    ano = cp(ano1)
    nova_lista = cp(lista)
    if(len(lista)==0):
        return [0,0]
    if np.std(nova_lista)<=1:
        return [nova_lista[-1], nova_lista[-1]]

    if len(lista)<=3:
        aumento_lista = lista[0]
        aumento_ano = ano[0]

        lista.insert(0, aumento_lista)
        ano.insert(0, aumento_ano)
        if ano[0] == ano[1] or ano[1] == ano[2]:
            for i in range(len(ano)):
                ano[i] = ano[0]+(i)


        if ano[0] >= 2000:
            ano.insert(0, 2000)
            posicao_0 = lista[0]
            lista.insert(0, posicao_0)

            nova_ano, nova_lista = interpolador(ano, lista)
            Valfa = alfa(nova_lista)
            primeiro = nova_lista[-1] * (1 + (1-Valfa))
            segundo = primeiro * (1 + (1-Valfa))
            return [primeiro, segundo]
        else:
            return [0,0]


    if ano[0] == ano[1] or ano[1] == ano[2]:
        for i in range(len(ano)):
            ano[i] = ano[0]+(i)
        nova_ano = ano

    else:
        nova_ano, nova_lista = interpolador(ano, lista)

    coeficiente1 = nova_lista[-1] - nova_lista[-3]
    coeficiente2 = nova_lista[-2] - nova_lista[-4]
    prev1 = 0
    prev2 = 0
    if coeficiente1 == coeficiente2:
        delta = nova_lista[-1] - nova_lista[-2]
        prev1 = nova_lista[-1] + delta
        prev2 = prev1 + delta
    else:
        if np.std(nova_lista)<=1:
            prev1, prev2 = nova_lista[-1], nova_lista[-1]
        else:
            prev1, prev2 = naive_bayes(nova_lista, 2)

    ano = []
    return [round(prev1,3), round(prev2,3)]




def media_movel3(lista, n_de_prevs):
    '''
    Média móvel de 3 períodos

    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas
    '''
    from copy import copy as cp
    a3 = 3
    i3 = 1
    
    lista3 = cp(lista)

    while len(lista3) < 3:
      lista3 = lista3+lista3
    
    previsoes_media_movel3 = []
    final = lista3[(len(lista3)-a3):]
    while i3 <= n_de_prevs:
        x = (final[0]+final[1]+final[2])/a3
        previsoes_media_movel3.append(x)
        lista3.append(x)
        final = lista3[(len(lista3)-a3):]
        i3 +=1
    return(previsoes_media_movel3)



def media_movel4(lista, n_de_prevs):
    '''Média móvel de 4 períodos

    cada previsão é feita com base nos 4 períodos anteriores, cada previsão é concatenada no final da base de dados antes de ser emitida a nova previsão

    lista = array com os dados históricos/série temporal

    n_de_prevs = quantas previsões devem ser feitas
    '''
    
    from copy import copy as cp
    i = 1
    a = 4
    lista4 = cp(lista)
    L = len(lista4)

    while len(lista4) < 4:
      lista4 = lista4+lista4
    
    previsoes_media_movel4 = []
    final4 = lista4[(len(lista4)-a):]
    while i <= n_de_prevs:
        x = (final4[0]+final4[1]+final4[2]+final4[3])/a
        previsoes_media_movel4.append(x)
        lista4.append(x)
        final4 = lista4[(len(lista4)-a):]
        i +=1
    return(previsoes_media_movel4)    
    

def media_movel12(lista, n_de_prevs):
    '''Média móvel de 12 períodos

    cada previsão é feita com base nos 12 períodos anteriores, caso a base de dados seja inferior a 12 períodos, a lista é repetida de modo que os últimos elementos serão a lista inicial

    lista = array com os dados históricos/série temporal

    n_de_prevs = quantas previsões devem ser feitas
    '''
    from copy import copy as cp
    a = 12
    i = 1
    lista12 = cp(lista)
    previsoes_media_movel12 = []
    
    while len(lista12) < 12:
      lista12 = lista12+lista12
    
    final12 = lista12[(len(lista12)-a):]
    while i <= n_de_prevs:
        x = sum(final12[:])
        w = (x)/a
        previsoes_media_movel12.append(w)
        lista12.append(w)
        final12 = lista12[(len(lista12)-a):]
        i +=1
    return(previsoes_media_movel12)


def media_movel30(lista, n_de_prevs):
    '''
    Média móvel de 30 períodos

    cada previsão é feita com base nos 30 períodos anteriores, caso a base de dados seja inferior a 30 períodos, a lista é repetida de modo que os últimos elementos serão a lista inicial

    lista = array com os dados históricos/série temporal

    n_de_prevs = quantas previsões devem ser feitas
    '''
    from copy import copy as cp
    a = 30
    i = 1
    lista30 = cp(lista)
    while len(lista30)<30:
      lista30 = lista30+lista30

    previsoes_media_movel30 = []

    final30 = lista30[(len(lista30)-a):]
    while i <= n_de_prevs:
        x = sum(final30[:])
        w = (x)/a
        previsoes_media_movel30.append(w)
        lista30.append(w)
        final30 = lista30[(len(lista30)-a):]
        i +=1
    return(previsoes_media_movel30)



def media_suave3(lista, n_de_prevs):
    '''
    Média móvel de 3 períodos com suavização exponencial

    calcula a média móvel de 3 em 3 períodos, o último valor da série recebe um peso exponencialmente maior do penúltimo, e o penúltimo um peso exp. maior em relação ao anterior.
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas
    '''
    
    
    from copy import copy as cp
    as3 = 3
    is3 = 1
    listas3 = cp(lista)   
    
    while len(listas3)<3:
      listas3 = listas3+listas3
      
    previsoes_media_suave3 = []
    final = listas3[(len(listas3)-as3):]
    while is3 <= n_de_prevs:
        x = [final[0],final[1],final[2]]
        w = [2, 4, 16]
        yl = []
        for i in range(len(x)):
            y = (x[i]*w[i])/22
            yl.append(y)
        z = sum(yl)

        previsoes_media_suave3.append(z)
        listas3.append(z)
        final = listas3[(len(listas3)-as3):]
        is3 +=1
    return(previsoes_media_suave3)




def sazonal_aditivo(lista, n_de_prevs):
    '''
    
    Média sazonal aditiva
    
    Dá peso adicional aos maiores valores que são apresentado ao longo do tempo e menor peso aos menores.
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas
    '''
    
    from copy import copy as cp
    listasa = cp(lista)
    lista2 = cp(lista)

    while len(lista2)<10:
      lista2 = lista2+lista2
      
    contador = 0
    sazonalidade = []
    pre_prev = media_suave3(lista2,n_de_prevs)
    prevs = []
    
    while contador <= (n_de_prevs-1):
        soma = 0
        media = []
        for i in listasa:
            soma += i 
            media = soma/len(listasa)
                     
        cast1 = (listasa[0]-(media))/5
        listasa.append(cast1)
        sazonalidade.append(cast1)
        listasa.append(cast1)
        listasa.pop(0)
        contador += 1
  
    for l in range(len(sazonalidade)):
        difere = pre_prev[l]+sazonalidade[l]
        prevs.append(difere)


    return(prevs)


def sazonal_multiplicativo(lista, n_de_prevs):
    
    '''Média sazonal multiplicativa

    Dá peso com diferença exponencial entre os maiores valores ao longo do tempo em relação aos menores.
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas
    '''
        
    from copy import copy as cp
    listasm = cp(lista)
    lista2m = cp(lista)

    while len(listasm)<10:
      listasm = lista2m+lista2m

    contador = 0
    sazonalidade = []
    pre_prev = media_suave3(lista2m,n_de_prevs)
    prevs = []
    
    while contador <= (n_de_prevs-1):
        soma = 0
        media = []
        for i in listasm:
            soma += i 
            media = soma/len(listasm)
                     
        cast1 = (listasm[0]-(media))/10
        listasm.append(cast1)
        sazonalidade.append(cast1)
        listasm.append(cast1)
        listasm.pop(0)
        contador += 1
  
    for l in range(len(sazonalidade)):
        difere = pre_prev[l]*(1+sazonalidade[l])
        prevs.append(difere)


    return(prevs)


def media_mov_dupla3(lista, n_de_prevs):
    '''
    média móvel dupla de 3 períodos
    
    calcula as previsões derivadas da média móvel de 3 períodos
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas

    '''
    from copy import copy as cp
    listammd3 = cp(lista)
    xis3 = cp(n_de_prevs)

    while len(listammd3)<4:
      listammd3 = listammd3+listammd3

    mmd31 = media_movel3(listammd3,xis3)
    mmd32 = media_movel3(mmd31,xis3)
    return(mmd32)



def media_mov_dupla4(lista, n_de_prevs):
    '''
    média móvel dupla de 4 períodos

    calcula as previsões derivadas da média móvel de 4 períodos
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas
    '''
    from copy import copy as cp
    listammd4 = cp(lista)

    while len(listammd4)<5:
      listammd4 = listammd4+listammd4

    xis4 = cp(n_de_prevs)
    mmd41 = media_movel4(listammd4,xis4)
    mmd42 = media_movel4(mmd41,xis4)
    return(mmd42)




def suave_dupla3(lista, n_de_prevs):
    '''
    suavização dupla de 3 períodos
    
    calcula a suavização de 3 períodos derivadas de uma suavização de também 3 períodos
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas
    '''
    from copy import copy as cp
    listdupla = cp(lista)

    while len(listdupla)<10:
      listdupla = listdupla+listdupla

    npdup = cp(n_de_prevs)
    
    sud3 = media_suave3(listdupla, npdup)
    sud3b = media_suave3(sud3,npdup)
    return(sud3b)


def suave_dupla4(lista, n_de_prevs):
    '''
    suavização dupla de 4 períodos

    calcula a suavização de 4 períodos derivadas de uma suavização de também 4 períodos
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas
    '''
    from copy import copy as cp
    listdupla4 = cp(lista)

    while len(listdupla4)<5:
      listdupla4 = listdupla4+listdupla4
   
    npdup = cp(n_de_prevs)
    sud4 = media_suave4(listdupla4, npdup)
    sud4b = media_suave4(sud4,npdup)
    return(sud4b)


def holt_winter7(lista, n_de_prevs):
    
    '''
    
    método aditivo de Holt Winter
    usa a sazonalidade e uma medida de tendência, produzindo uma previsão aditivada.
    
    '''
    
    
    from copy import copy as cp

    listahw7 = cp(lista)
    coluna = cp(lista)
    contador = 0
    prevs = []
    diferenca = (listahw7[(len(listahw7)-1)]-listahw7[0])
    tendencia = diferenca /(len(listahw7))
    
    somafix = 0
    for k in listahw7:
            somafix += k 
            mediafix = somafix/len(listahw7)
    
    while contador <= (n_de_prevs-1):
        soma = 0
        media = []
        for i in listahw7:
            soma += i 
            media = soma/len(listahw7)
               
       
        cast1 = media+tendencia+(listahw7[0]-media)
        listahw7.append(cast1)
        prevs.append(cast1)
        coluna.append(cast1)
        listahw7.pop(0)
        contador += 1
    
    sazon = []
    for z in coluna:
        sazon.append(z-mediafix)
            
    indice_sazonalidade = sazon[0:len(prevs)]
    
    beta = 0.1
    prev_discontada = []
    for x in range(len(prevs)):
        difere = prevs[x]-(beta*indice_sazonalidade[x])
        prev_discontada.append(difere)
    

    alpha = 0.1 
    prev_suav = []
    for h in range(len(prev_discontada)):
        mult = (prev_discontada[h]+(prev_discontada[h] - (2*((mediafix*tendencia)*alpha))))/2
        prev_suav.append(mult)

    return(prev_suav)


def pre_arima (lista):
    from copy import copy as cp

    yps = cp(lista)
    beta1 = 0.75
    beta2 = 0.18
    coluna = []
    coluna.append(yps[0])
    hist_erro = []
    contador = 0
    
    while contador <= 1:  
        
        for y in range(len(yps)):
            
            erro = (yps[y]-coluna[y])
            yprev = (yps[y]*beta1)+(erro*beta2)
            coluna.append(yprev)
            hist_erro.append(erro)
            
            contador += 1 

    return(coluna[(len(coluna)-1):])
    
def arima (lista, n_de_prevs):
    '''
    arima
    modelo auto-regressivo de médias móveis integtradas (ARIMA).
    '''
    
    from copy import copy as cp
    lista0 = cp(lista)
    contador = 1
    while contador <= n_de_prevs:
        anexo = pre_arima(lista0)
        lista0.append(anexo[0])
        contador += 1
    
    return(lista0[(len(lista0)-n_de_prevs):])


def media_mista(lista, n_de_prevs):
    '''
    média móvel mista
    
    calcula as previsões derivadas da combinação de diferentes médias móveis
    
    lista = array com os dados históricos/série temporal
    
    n_de_prevs = quantas previsões devem ser feitas

    '''
    from copy import copy as cp
    listamis = cp(lista)
    xismis = cp(n_de_prevs)

    while len(listamis)<30:
      listamis = listamis+listamis

    mmis = media_suave12(listamis,xismis)
    mmis2 = media_mov_dupla4(mmis,xismis)
    mmis3 = media_suave12(mmis2,xismis)
    mmis4 = media_suave4(mmis3,xismis)
    return(mmis4)   