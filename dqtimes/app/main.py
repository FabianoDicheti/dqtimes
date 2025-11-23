import os
import io
import asyncio
import json
import dask.dataframe as dd
import tempfile
from dask.distributed import Client, LocalCluster
from app import forecast_temp
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
import math
import time

# Iniciar um cluster local e um cliente Dask
cluster = LocalCluster()
client = Client(cluster)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print(f"Dask Dashboard is available at {client.dashboard_link}")


@app.post("/projecao_lista/")
async def upload_file(
    lista_historico: str = Form(...),
    quantidade_projecoes: int = Form(...),
):

    lista_original = json.loads(lista_historico)  # Convertendo para lista

    n = quantidade_projecoes 

    # Chamando a função de previsão
    resultado = forecast_temp(lista_original, n)

    return {
        "projecoes": resultado
    }

@app.post("/projecao_dataframe/")
async def upload_file(
    csv_dataframe: UploadFile = File(...),
    quantidade_projecoes: int = Form(...),
    header: bool = Form(...),
    index_col: bool = Form(...),
    page: int = Query(1, ge=1),  # Número da página, deve ser >= 1
    page_size: int = Query(10, ge=1),  # Tamanho da página, deve ser >= 1
):
    n = quantidade_projecoes

    # Salvar o conteúdo do arquivo em um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(await csv_dataframe.read())
        tmp_file_path = tmp_file.name

    ddf = dd.read_csv(tmp_file_path, header=0 if header else None)

    if index_col:
        ddf = ddf.drop(ddf.columns[0], axis=1)

    # Calcular o número total de linhas e o número total de páginas
    total_rows = len(ddf)
    total_pages = math.ceil(total_rows / page_size)

    # Verificar se o número da página é válido
    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page number out of range")

    # Calcular o índice inicial e final para a paginação
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Aplicar a paginação ao DataFrame
    ddf_paginated = ddf.loc[start_index:end_index]

    start_time = time.time()
    lista_df = []

    for part in ddf_paginated.to_delayed():
        # Converter a partição para um pandas DataFrame e iterar sobre as linhas
        for index, row in part.compute().iterrows():
            lista_df.append(row.tolist())

    # Aplica a função de projeção à lista de listas
    
    resultado = []
    for lista in lista_df:
        projection = forecast_temp(lista, n)
        resultado.append(projection)

    end_time = time.time()
    execution_time = end_time - start_time 

    return {
        "execution_time": execution_time,
        "total_pages": total_pages,
        "current_page": page,
        "projecoes": resultado
    }
