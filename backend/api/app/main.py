import os
import io
import asyncio
import json
import dask.dataframe as dd
import tempfile
from dask.distributed import Client, LocalCluster
from app import forecast_temp
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.responses import Response
import math
import time

# Prometheus imports
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator
from app.metrics import MetricsMiddleware, track_projection

# Iniciar um cluster local e um cliente Dask
cluster = LocalCluster()
client = Client(cluster)

app = FastAPI(
    title="DQTimes API",
    description="API de projeções temporais com observabilidade",
    version="1.0.0"
)

# Adicionar middleware de métricas customizado
app.add_middleware(MetricsMiddleware)

# Instrumentar FastAPI com Prometheus
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)

instrumentator.instrument(app)


@app.on_event("startup")
async def startup_event():
    print(f"Dask Dashboard is available at {client.dashboard_link}")
    instrumentator.expose(app, endpoint="/metrics")


@app.get("/metrics")
async def metrics():
    """Endpoint para exposição de métricas do Prometheus."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/projecao_lista/")
async def projecao_lista(
    lista_historico: str = Form(...),
    quantidade_projecoes: int = Form(...),
):
    start_time = time.time()
    
    lista_original = json.loads(lista_historico)  # Convertendo para lista
    n = quantidade_projecoes 

    # Chamando a função de previsão
    resultado = forecast_temp(lista_original, n)
    
    # Registrar métricas de negócio
    processing_time = time.time() - start_time
    method_type = "unknown"
    if isinstance(resultado, dict) and "final_projection" in resultado:
        # Tentar identificar o método usado
        method_type = "forecast_temp"
    
    track_projection(
        endpoint="/projecao_lista/",
        method_type=method_type,
        dataset_size=len(lista_original),
        processing_time=processing_time
    )

    return {
        "projecoes": resultado
    }

@app.post("/projecao_dataframe/")
async def projecao_dataframe(
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
    
    # Registrar métricas de negócio
    track_projection(
        endpoint="/projecao_dataframe/",
        method_type="forecast_temp_batch",
        dataset_size=len(lista_df),
        processing_time=execution_time
    )

    return {
        "execution_time": execution_time,
        "total_pages": total_pages,
        "current_page": page,
        "projecoes": resultado
    }
