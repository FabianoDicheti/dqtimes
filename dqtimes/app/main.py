import os
import io
import asyncio
import json
import dask.dataframe as dd
import tempfile
from dask.distributed import Client, LocalCluster
from app import forecast_temp
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import math
import time

from .auth import router as auth_router

cluster = LocalCluster()
client = Client(cluster)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.on_event("startup")
async def startup_event():
    print(f"Dask Dashboard is available at {client.dashboard_link}")


@app.post("/projecao_lista/")
async def upload_file(
    lista_historico: str = Form(...),
    quantidade_projecoes: int = Form(...),
):

    lista_original = json.loads(lista_historico)

    n = quantidade_projecoes 

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
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    n = quantidade_projecoes

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(await csv_dataframe.read())
        tmp_file_path = tmp_file.name

    ddf = dd.read_csv(tmp_file_path, header=0 if header else None)

    if index_col:
        ddf = ddf.drop(ddf.columns[0], axis=1)

    total_rows = len(ddf)
    total_pages = math.ceil(total_rows / page_size)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page number out of range")

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    ddf_paginated = ddf.loc[start_index:end_index]

    start_time = time.time()
    lista_df = []

    for part in ddf_paginated.to_delayed():
        for index, row in part.compute().iterrows():
            lista_df.append(row.tolist())

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