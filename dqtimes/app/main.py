import os
import io
import json
import dask.dataframe as dd
import pandas as pd
import tempfile
from dask.distributed import Client, LocalCluster
from app import forecast_temp
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import math
import time
import logging
import math
import time
import uuid
import logging
import asyncio
import tempfile
from datetime import datetime
from typing import List, Optional, Dict, Any
from copy import copy as cp
import numpy as np

import dask.dataframe as dd
from dask.distributed import Client, LocalCluster
from celery import Celery
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator, conint, field_validator, Gt, Ge
from typing import Annotated

def tax_acrescimo(lista: list) -> tuple:
    """Placeholder: Retorna taxas de crescimento/decréscimo dummy."""
    print("AVISO: Usando a função placeholder 'tax_acrescimo'.")
    return (0.05, -0.02)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# configura o loggin - registro de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# configura o ambiente do fallback
FORCE_FALLBACK = os.getenv("FORCE_FALLBACK", "false").lower() in ("1", "true", "yes")

# metricas simples em memoria - integrar o prometheus depois aui
_metrics = {
    "fallback_count": 0,
    "requests_csv": 0
}


@app.on_event("startup")
async def startup_event():
    logging.info(f"Dask Dashboard is available at {client.dashboard_link}")

# mapeando rotas publicas com roteamento seguro - usando FileResponse do FastAPI

#/
@app.get("/")
async def root():
    return FileResponse("app/templates/index.html", media_type="text/html")

#/app
@app.get("/app")
async def app_page():
    return FileResponse("app/templates/app.html", media_type="text/html")

#/historico
@app.get("/historico")
async def historico():
    return FileResponse("app/templates/historico.html", media_type="text/html")


#/health - checagem de saude health 
@app.get("/health")
async def health():
    return {"status": "ok"}

#/ready - checagem de saude readiness
@app.get("/ready")
async def readiness():
    try:
        # verificando se o dask esta conectado e o scheduler ta responsivo
        info = client.scheduler_info()
        if info:
            return {"status": "ready"}
        else:
            raise HTTPException(status_code=503, detail="Scheduler not responsive")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Not ready: {str(e)}")


#/metrics - metricas simples - substituir por prometheus depois
@app.get("/metrics")
async def metrics():
    """Endpointe de metricas simples (JSON).
    utilizado para checagens rapidas, mas tem que trocar pelo prometheis depois.
    """
    return _metrics
def binariza(lista: list, arg1: int, arg2: int) -> list:
    """Placeholder: Retorna uma lista binarizada dummy."""
    print("AVISO: Usando a função placeholder realiza para a 'binarização'.")
    return [1 if x > np.mean(lista) else 0 for x in lista]

def inferencia_bayes_bin_general(lista: list, n_binarizacao: int) -> tuple:
    """Placeholder: Retorna uma probabilidade dummy."""
    print("AVISO: Usando a função placeholder 'inferencia_bayes_bin_general'.")
    return (0.6,) 

def media_suave4(lista: list, n_de_prevs: int) -> list:
    """Placeholder: Faltava no código original, mas era chamada."""
    print("AVISO: Usando a função placeholder 'media_suave4'.")
    return media_movel4(lista, n_de_prevs)

def media_suave12(lista: list, n_de_prevs: int) -> list:
    """Placeholder: Faltava no código original, mas era chamada."""
    print("AVISO: Usando a função placeholder 'media_suave12'.")
    return media_movel12(lista, n_de_prevs)

def naive_bayes(lista, n_de_prevs):
    lista_atual = cp(lista)
    previsoes = []
    taxa = tax_acrescimo(lista)
    
    for _ in range(n_de_prevs):
        n_bin = min(max(len(lista_atual) - 1, 2), 6)

        dados_binarizados = binariza(lista_atual, n_bin - 1, n_bin - 1)
        resultado_bayes = inferencia_bayes_bin_general(dados_binarizados, n_bin)
        
        prob_alta = resultado_bayes[0]
        ultimo_valor = lista_atual[-1]

        if prob_alta > 0.5:
            proxima_prev = ultimo_valor + (ultimo_valor * taxa[0])
        else:
            proxima_prev = ultimo_valor + (ultimo_valor * taxa[1])

        previsoes.append(proxima_prev)
        lista_atual.append(proxima_prev)

    return previsoes

def alfa(lista_valores):
    return sum(lista_valores) / len(lista_valores) if lista_valores else 0

def interpolador(lista_ano, lista_valores):
    data = datetime.today()
    ano_atual = data.year

    if not lista_ano:
        return [], []

    ano_inicial = lista_ano[0]
    anos_completos = np.arange(ano_inicial, ano_atual + 1, 1)

    a = alfa(lista_valores)
    if a == 0:
        a = 1

    anos_faltantes = sorted(set(anos_completos) - set(lista_ano))

    valores_interp = np.interp(anos_faltantes, lista_ano, lista_valores)

    valores_interp = [(v / a) - ((v * a) / 100) for v in valores_interp]

    #incrementa os requests
    _metrics["requests_csv"] += 1

    lista_df = []
    start_time = time.time()

    # se forcar o fallback pelo ambiente, ele para de tentar a usar o dask e vai para o pandas
    if FORCE_FALLBACK:
        logging.warning("FORCE_FALLBACK ativo: usando fallback pandas para o processamento de csv")
        pdf = pd.read_csv(tmp_file_path, header=0 if header else None)
        if index_col:
            pdf = pdf.drop(pdf.columns[0], axis=1)

        total_rows = len(pdf)
        total_pages = math.ceil(total_rows / page_size)

        if page > total_pages:
            raise HTTPException(status_code=404, detail="numero de pagina fora do range")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        pdf_slice = pdf.iloc[start_index:end_index]
        for index, row in pdf_slice.iterrows():
            lista_df.append(row.tolist())

        _metrics["fallback_count"] += 1
    else:
        #aqui ele tenta o dask primeiro, mas se falhar manda para o pandas
        try:
            ddf = dd.read_csv(tmp_file_path, header=0 if header else None)
            if index_col:
                ddf = ddf.drop(ddf.columns[0], axis=1)

            total_rows = len(ddf)
            total_pages = math.ceil(total_rows / page_size)

            if page > total_pages:
                raise HTTPException(status_code=404, detail="numero de pagina fora do range")

            start_index = (page - 1) * page_size
            end_index = start_index + page_size

            ddf_paginated = ddf.loc[start_index:end_index]
            for part in ddf_paginated.to_delayed():
                for index, row in part.compute().iterrows():
                    lista_df.append(row.tolist())
        except Exception as e:
            logging.warning(f"processamento em dask falhou, voltando a utilizar pandas: {e}")
            pdf = pd.read_csv(tmp_file_path, header=0 if header else None)
            if index_col:
                pdf = pdf.drop(pdf.columns[0], axis=1)

            total_rows = len(pdf)
            total_pages = math.ceil(total_rows / page_size)

            if page > total_pages:
                raise HTTPException(status_code=404, detail="numero de pagina fora do range")

            start_index = (page - 1) * page_size
            end_index = start_index + page_size

            pdf_slice = pdf.iloc[start_index:end_index]
            for index, row in pdf_slice.iterrows():
                lista_df.append(row.tolist())

            _metrics["fallback_count"] += 1

    # Aplica a função de projeção à lista de listas
    if len(valores_interp) >= 2:
        if valores_interp[-1] == valores_interp[-2]:
            v = valores_interp[-1]
            valores_interp[-1] = (v / a) - ((v * (2 * a)) / 100)

    matriz = [
        lista_ano + anos_faltantes,
        lista_valores + [*valores_interp]
    ]
    M = np.asarray(matriz)

    ordem = M[:, M[0].argsort()]
    anos_totais = [int(i) for i in ordem[0]]
    valores_totais = [round(j, 4) for j in ordem[1]]

    return anos_totais, valores_totais

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
            if Valfa == 1: Valfa = 0.99
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
    if coeficiente1 == coeficiente2:
        delta = nova_lista[-1] - nova_lista[-2]
        prev1 = nova_lista[-1] + delta
        prev2 = prev1 + delta
    else:
        if np.std(nova_lista)<=1:
            prev1, prev2 = nova_lista[-1], nova_lista[-1]
        else:
            prev1, prev2 = naive_bayes(nova_lista, 2)
    return [round(prev1,3), round(prev2,3)]

def media_movel4(lista, n_de_prevs):
    i = 1
    a = 4
    lista4 = cp(lista)
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
    janela = 12
    lista_mm = cp(lista)
    previsoes = []

    while len(lista_mm) < janela:
        lista_mm += lista_mm

    ultimos = lista_mm[-janela:]

    for _ in range(n_de_prevs):
        media = sum(ultimos) / janela
        previsoes.append(media)
        lista_mm.append(media)
        ultimos = lista_mm[-janela:]

    return previsoes

def forecast_temp(historical_data: list, num_projections: int) -> list:
    """
    Esta função é o ponto de entrada que a API usa.
    Atualmente, ela chama 'naive_bayes'. Mude aqui se quiser usar outra.
    """
    if not historical_data:
        return [0.0] * num_projections
    
    return naive_bayes(historical_data, num_projections)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    cluster = LocalCluster()
    client = Client(cluster)
    logger.info(f"Dask Dashboard disponível em: {client.dashboard_link}")
except Exception as e:
    logger.error(f"Falha ao iniciar o cluster Dask: {e}")
    client = None

celery_app = Celery(
    'forecast_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app = FastAPI(title="API de Projeção de Séries Temporais", version="1.0.0")

class ProjecaoListaRequest(BaseModel):
    lista_historico: str = Field(..., description="Lista histórica em formato de string JSON. Ex: '[10, 11, 12]'")
    
    quantidade_projecoes: Annotated[int, Gt(0)] = Field(..., description="Número de projeções futuras a serem geradas.")
    
    @field_validator('lista_historico')
    def validate_lista_historico(cls, v: str) -> str:
        try:
            lista = json.loads(v)
            if not isinstance(lista, list): raise ValueError("O conteúdo do JSON deve ser uma lista.")
            if not lista: raise ValueError("A lista não pode estar vazia.")
            if not all(isinstance(item, (int, float)) for item in lista): raise ValueError("Todos os elementos da lista devem ser números (int ou float).")
            return v
        except json.JSONDecodeError: raise ValueError("Formato de string JSON inválido.")
        except ValueError as e: raise ValueError(str(e))

class ProjecaoDataframeRequest(BaseModel):
    quantidade_projecoes: Annotated[int, Gt(0)] = Field(..., description="Número de projeções futuras a serem geradas.")
    
    header: bool = Field(..., description="Indica se o arquivo CSV possui uma linha de cabeçalho.")
    index_col: bool = Field(..., description="Indica se a primeira coluna do CSV é um índice a ser ignorado.")
    
    page: Annotated[int, Ge(1)] = Field(1, description="Número da página para paginação de resultados.")
    page_size: Annotated[int, Ge(1)] = Field(10, description="Quantidade de linhas por página.")

class ProjecaoResponse(BaseModel):
    projecoes: List[Any]
    status: str = "completed"
    execution_time: Optional[float] = None
    total_pages: Optional[int] = None
    current_page: Optional[int] = None

class TaskSubmissionResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None

@celery_app.task(bind=True)
def process_forecast_lista(self, lista_historico: str, quantidade_projecoes: int):
    try:
        self.update_state(state='PROGRESS', meta={'status': 'Iniciando processamento...'})
        lista_original = json.loads(lista_historico)
        
        resultado = forecast_temp(lista_original, quantidade_projecoes)
        
        return {"projecoes": resultado, "status": "completed"}
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        logger.error(f"Task {self.request.id} falhou: {e}")
        raise e

@celery_app.task(bind=True)
def process_forecast_dataframe(self, file_path: str, quantidade_projecoes: int, header: bool, index_col: bool, page: int, page_size: int):
    try:
        self.update_state(state='PROGRESS', meta={'status': 'Lendo arquivo CSV...'})
        
        ddf = dd.read_csv(file_path, header=0 if header else None, assume_missing=True)
        
        if index_col: 
            ddf = ddf.drop(ddf.columns[0], axis=1)
            
        total_rows = len(ddf)
        total_pages = math.ceil(total_rows / page_size)
        
        if page > total_pages and total_pages > 0: 
            raise ValueError("Número da página fora do intervalo.")
            
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        ddf_paginated = ddf.loc[start_index:end_index - 1]
        
        self.update_state(state='PROGRESS', meta={'status': 'Calculando projeções...'})
        start_time = time.time()
        
        def apply_forecast(df):
            return df.apply(lambda row: forecast_temp(row.dropna().tolist(), quantidade_projecoes), axis=1)
        
        resultado = ddf_paginated.map_partitions(apply_forecast, meta=('object')).compute().tolist()
        
        execution_time = time.time() - start_time
        
        return {
            "projecoes": resultado, "execution_time": execution_time,
            "total_pages": total_pages, "current_page": page, "status": "completed"
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        logger.error(f"Task {self.request.id} falhou: {e}")
        raise e
    finally:
        if os.path.exists(file_path): 
            os.unlink(file_path)

@app.on_event("startup")
async def startup_event():
    print("FastAPI iniciado com sucesso.")
    if not client:
        print("AVISO: Dask não foi iniciado. Processamento de DataFrames pode ser lento.")

@app.post("/projecao_lista/", response_model=ProjecaoResponse, tags=["Projeções"],
          responses={
              status.HTTP_202_ACCEPTED: {"model": TaskSubmissionResponse},
              status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Erro de validação"},
          })
async def projecao_por_lista(
    lista_historico: str = Form(...),
    quantidade_projecoes: int = Form(...),
    async_processing: bool = Form(False, description="Se True, a tarefa será processada em background.")
):
    """
    Recebe uma lista de dados históricos e retorna projeções.
    - Se `async_processing=False` (padrão): Processa imediatamente e retorna o resultado.
    - Se `async_processing=True`: Enfileira a tarefa no Celery e retorna um ID de tarefa (HTTP 202).
    """
    try:
        request_data = ProjecaoListaRequest(lista_historico=lista_historico, quantidade_projecoes=quantidade_projecoes)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    
    if async_processing:
        task = process_forecast_lista.delay(request_data.lista_historico, request_data.quantidade_projecoes)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED, 
            content=TaskSubmissionResponse(task_id=task.id, status="processing", message="Tarefa de projeção de lista foi enfileirada.").dict()
        )
    else:
        start_time = time.time()
        resultado = forecast_temp(json.loads(request_data.lista_historico), request_data.quantidade_projecoes)
        execution_time = time.time() - start_time
        return ProjecaoResponse(projecoes=resultado, execution_time=execution_time)


@app.post("/projecao_dataframe/", response_model=ProjecaoResponse, tags=["Projeções"],
          responses={
              status.HTTP_202_ACCEPTED: {"model": TaskSubmissionResponse},
              status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Erro de validação"},
              status.HTTP_400_BAD_REQUEST: {"description": "Erro no processamento do arquivo"}
          })
async def projecao_por_dataframe(
    csv_dataframe: UploadFile = File(...),
    quantidade_projecoes: int = Form(...),
    header: bool = Form(...),
    index_col: bool = Form(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    async_processing: bool = Form(False, description="Se True, a tarefa será processada em background.")
):
    """
    Recebe um arquivo CSV, processa linha por linha e retorna projeções.
    - Se `async_processing=False` (padrão): Processa imediatamente e retorna o resultado.
    - Se `async_processing=True`: Enfileira a tarefa no Celery e retorna um ID de tarefa (HTTP 202).
    """
    try:
        request_data = ProjecaoDataframeRequest(
            quantidade_projecoes=quantidade_projecoes, header=header, 
            index_col=index_col, page=page, page_size=page_size
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="wb") as tmp_file:
        content = await csv_dataframe.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
        
    if async_processing:
        task = process_forecast_dataframe.delay(
            tmp_file_path, request_data.quantidade_projecoes, request_data.header, 
            request_data.index_col, request_data.page, request_data.page_size
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED, 
            content=TaskSubmissionResponse(task_id=task.id, status="processing", message="Tarefa de projeção de dataframe foi enfileirada.").dict()
        )
    else:
        try:
            result_dict = process_forecast_dataframe.__wrapped__(
                process_forecast_dataframe,
                file_path=tmp_file_path, 
                quantidade_projecoes=request_data.quantidade_projecoes, 
                header=request_data.header, index_col=request_data.index_col, 
                page=request_data.page, page_size=request_data.page_size
            )
            return ProjecaoResponse(**result_dict)
        except Exception as e:
            if os.path.exists(tmp_file_path): 
                os.unlink(tmp_file_path)
            logger.error(f"Erro no processamento síncrono do dataframe: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao processar o arquivo: {e}")


@app.get("/tasks/{task_id}", response_model=TaskStatusResponse, tags=["Gerenciamento de Tarefas"])
async def get_task_status(task_id: str):
    """Verifica o status de uma tarefa assíncrona enfileirada."""
    task_result = celery_app.AsyncResult(task_id)
    
    response_data = {
        "task_id": task_id, 
        "status": task_result.state, 
        "result": None
    }
    
    if task_result.state == 'SUCCESS':
        response_data["result"] = task_result.result
    elif task_result.state == 'FAILURE':
        response_data["result"] = str(task_result.info)
    elif task_result.state == 'PROGRESS':
        response_data["result"] = task_result.info
    elif task_result.state == 'PENDING':
        response_data["result"] = "Tarefa na fila, aguardando para ser executada."
        
    return TaskStatusResponse(**response_data)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code, 
        content={"error_type": "ClientError", "message": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Erro interno não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content={"error_type": "InternalServerError", "message": "Ocorreu um erro inesperado no servidor.", "status_code": 500}
    )
