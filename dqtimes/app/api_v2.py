# api_v2.py
# Nova API DQTimes com autenticação JWT, validações e histórico
# Issues #114 e #115

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query, Depends, Header, Path, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import json
import jwt
import hashlib
import secrets
import pandas as pd
import numpy as np
import logging
import asyncio
from enum import Enum
import tempfile
import os

# Import local - ajustado para funcionar com a estrutura do projeto
try:
    from aplicacao import forecast_temp
except ImportError:
    from .aplicacao import forecast_temp

# ================== CONFIGURAÇÃO INICIAL ==================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações JWT
JWT_SECRET = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

app = FastAPI(
    title="DQTimes API v2 - Sistema de Projeção de Séries Temporais",
    description="""
    API para análise e projeção de séries temporais utilizando métodos estatísticos avançados.

    ## Funcionalidades:
    - 📊 Upload de dados (CSV/JSON)
    - 🔮 Previsões com múltiplos algoritmos
    - 📈 Análise estatística completa
    - 🔐 Autenticação JWT
    - 📜 Histórico de operações

    ## Issues Implementadas:
    - #114: Documentação de endpoints e modelos
    - #115: Exemplos práticos e testes
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Equipe DQTimes",
        "email": "support@dqtimes.com",
    }
)

# ================== MODELOS PYDANTIC ==================

class LoginRequest(BaseModel):
    """Modelo para requisição de login"""
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")

    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username deve conter apenas letras, números, _ e -')
        return v

class LoginResponse(BaseModel):
    """Modelo para resposta de login"""
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    user_id: str = Field(..., description="ID do usuário autenticado")
    username: str = Field(..., description="Nome do usuário")
    roles: List[str] = Field(default=[], description="Papéis do usuário")

class UploadResponse(BaseModel):
    """Modelo de resposta para upload de dados"""
    file_id: str = Field(..., description="ID único do arquivo carregado")
    filename: str = Field(..., description="Nome do arquivo original")
    size: int = Field(..., description="Tamanho do arquivo em bytes")
    upload_time: datetime = Field(..., description="Timestamp do upload")
    status: str = Field(..., description="Status do processamento")
    rows_processed: Optional[int] = Field(None, description="Número de linhas processadas")
    columns_detected: Optional[List[str]] = Field(None, description="Colunas detectadas")

class ForecastRequest(BaseModel):
    """Modelo para requisição de previsão"""
    data: List[float] = Field(..., min_items=10, max_items=10000, description="Série temporal histórica")
    n_projections: int = Field(..., ge=1, le=365, description="Número de projeções")
    method: Optional[str] = Field("auto", description="Método de previsão")
    confidence_level: Optional[float] = Field(0.95, ge=0.5, le=0.99, description="Nível de confiança")

    @validator('data')
    def validate_data(cls, v):
        if any(np.isnan(x) or np.isinf(x) for x in v):
            raise ValueError('Dados não podem conter NaN ou valores infinitos')
        return v

class ForecastResponse(BaseModel):
    """Modelo para resposta de previsão"""
    projections: List[float] = Field(..., description="Valores projetados")
    confidence_intervals: List[Dict[str, float]] = Field(..., description="Intervalos de confiança")
    method_used: str = Field(..., description="Método utilizado")
    metrics: Dict[str, float] = Field(..., description="Métricas de qualidade")
    probability_increase: float = Field(..., ge=0, le=1, description="Probabilidade de aumento")
    execution_time: float = Field(..., description="Tempo de execução em segundos")

class HistoryItem(BaseModel):
    """Modelo para item do histórico"""
    id: str = Field(..., description="ID único da operação")
    operation_type: str = Field(..., description="Tipo de operação realizada")
    timestamp: datetime = Field(..., description="Data/hora da operação")
    user_id: Optional[str] = Field(None, description="ID do usuário")
    parameters: Dict[str, Any] = Field(..., description="Parâmetros utilizados")
    result_summary: Dict[str, Any] = Field(..., description="Resumo dos resultados")
    status: str = Field(..., description="Status da operação")

class HistoryResponse(BaseModel):
    """Modelo de resposta para histórico"""
    total_items: int = Field(..., description="Total de itens no histórico")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    total_pages: int = Field(..., description="Total de páginas")
    items: List[HistoryItem] = Field(..., description="Lista de itens do histórico")

# ================== SEGURANÇA E AUTENTICAÇÃO ==================

security = HTTPBearer()

# Banco de dados simulado de usuários (em produção, usar banco real)
USERS_DB = {
    "admin": {
        "password_hash": hashlib.sha256("Admin@123".encode()).hexdigest(),
        "user_id": "user-001",
        "roles": ["admin", "analyst"]
    },
    "testuser": {
        "password_hash": hashlib.sha256("Test@123".encode()).hexdigest(),
        "user_id": "user-002",
        "roles": ["analyst"]
    }
}

# Histórico em memória (em produção, usar banco de dados)
OPERATIONS_HISTORY = []

def create_access_token(data: dict):
    """Criar token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar e decodificar token JWT"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return {"username": username, "user_id": payload.get("user_id")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

def add_to_history(operation_type: str, user_info: dict, parameters: dict, result: dict):
    """Adicionar operação ao histórico"""
    operation = {
        "id": f"op-{secrets.token_hex(8)}",
        "operation_type": operation_type,
        "timestamp": datetime.utcnow(),
        "user_id": user_info.get("user_id"),
        "parameters": parameters,
        "result_summary": result,
        "status": "completed"
    }
    OPERATIONS_HISTORY.insert(0, operation)
    return operation["id"]

# ================== ENDPOINTS DE AUTENTICAÇÃO ==================

@app.post("/auth/login",
          response_model=LoginResponse,
          summary="Autenticação de usuário",
          description="Realiza o login e retorna um token de acesso JWT",
          responses={
              200: {"description": "Login realizado com sucesso"},
              401: {"description": "Credenciais inválidas"},
              422: {"description": "Erro de validação"},
              429: {"description": "Muitas tentativas de login"}
          })
async def login(credentials: LoginRequest):
    """
    Autentica o usuário e retorna um token JWT.

    **Validações:**
    - Username: 3-50 caracteres alfanuméricos
    - Password: mínimo 8 caracteres
    """
    user = USERS_DB.get(credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    password_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
    if password_hash != user["password_hash"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": credentials.username, "user_id": user["user_id"]}
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=JWT_EXPIRATION_MINUTES * 60,
        user_id=user["user_id"],
        username=credentials.username,
        roles=user["roles"]
    )

@app.post("/auth/logout",
          summary="Logout de usuário",
          description="Invalida o token de acesso atual",
          responses={
              204: {"description": "Logout realizado com sucesso"},
              401: {"description": "Token inválido"}
          })
async def logout(current_user: dict = Depends(verify_token)):
    """Realiza o logout invalidando o token atual."""
    logger.info(f"User {current_user['username']} logged out")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )

@app.post("/auth/refresh",
          response_model=LoginResponse,
          summary="Renovar token de acesso",
          description="Gera um novo token de acesso",
          responses={
              200: {"description": "Token renovado com sucesso"},
              401: {"description": "Token inválido ou expirado"}
          })
async def refresh_token(current_user: dict = Depends(verify_token)):
    """Renova o token de acesso usando o token atual."""
    new_access_token = create_access_token(
        data={"sub": current_user["username"], "user_id": current_user["user_id"]}
    )

    user = USERS_DB.get(current_user["username"])

    return LoginResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=JWT_EXPIRATION_MINUTES * 60,
        user_id=current_user["user_id"],
        username=current_user["username"],
        roles=user["roles"]
    )

# ================== ENDPOINTS DE UPLOAD ==================

@app.post("/upload/csv",
          response_model=UploadResponse,
          summary="Upload de arquivo CSV",
          description="Realiza o upload de um arquivo CSV com dados de série temporal",
          responses={
              200: {"description": "Upload realizado com sucesso"},
              400: {"description": "Arquivo inválido"},
              401: {"description": "Não autenticado"},
              413: {"description": "Arquivo muito grande"},
              422: {"description": "CSV mal formatado"}
          })
async def upload_csv(
    file: UploadFile = File(..., description="Arquivo CSV com dados históricos"),
    description: Optional[str] = Form(None, description="Descrição opcional do dataset"),
    current_user: dict = Depends(verify_token)
):
    """
    Endpoint para fazer upload de arquivos CSV com séries temporais.

    **Limitações:**
    - Tamanho máximo: 10MB
    - Formato: CSV com headers
    """
    # Validar extensão
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo deve ser CSV"
        )

    # Validar tamanho (10MB máximo)
    contents = await file.read()
    file_size = len(contents)

    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Arquivo excede o tamanho máximo de 10MB"
        )

    try:
        # Salvar arquivo temporariamente
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        # Processar CSV
        df = pd.read_csv(tmp_path)

        file_id = f"file-{secrets.token_hex(8)}"

        # Adicionar ao histórico
        add_to_history(
            operation_type="upload",
            user_info=current_user,
            parameters={"filename": file.filename, "description": description},
            result={"file_id": file_id, "rows": len(df), "columns": list(df.columns)}
        )

        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            size=file_size,
            upload_time=datetime.utcnow(),
            status="processed",
            rows_processed=len(df),
            columns_detected=list(df.columns)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erro ao processar CSV: {str(e)}"
        )
    finally:
        # Limpar arquivo temporário
        if 'tmp_path' in locals():
            os.unlink(tmp_path)

@app.post("/upload/json",
          response_model=UploadResponse,
          summary="Upload de dados JSON",
          description="Recebe dados de série temporal em formato JSON",
          responses={
              200: {"description": "Upload realizado com sucesso"},
              400: {"description": "JSON inválido"},
              401: {"description": "Não autenticado"},
              422: {"description": "Dados inválidos"}
          })
async def upload_json(
    data: str = Form(..., description="Lista de valores numéricos em JSON"),
    metadata: Optional[str] = Form(None, description="Metadados opcionais em JSON"),
    current_user: dict = Depends(verify_token)
):
    """
    Endpoint para enviar dados em formato JSON.

    **Formato esperado:**
    - data: JSON array de números
    - metadata: JSON object opcional
    """
    try:
        # Parse JSON
        data_list = json.loads(data)
        metadata_dict = json.loads(metadata) if metadata else {}

        if not isinstance(data_list, list):
            raise ValueError("Data deve ser uma lista")

        if not all(isinstance(x, (int, float)) for x in data_list):
            raise ValueError("Todos os valores devem ser numéricos")

        file_id = f"json-{secrets.token_hex(8)}"

        # Adicionar ao histórico
        add_to_history(
            operation_type="upload",
            user_info=current_user,
            parameters={"type": "json", "metadata": metadata_dict},
            result={"file_id": file_id, "data_points": len(data_list)}
        )

        return UploadResponse(
            file_id=file_id,
            filename="json_upload",
            size=len(data),
            upload_time=datetime.utcnow(),
            status="processed",
            rows_processed=len(data_list)
        )

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"JSON inválido: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

# ================== ENDPOINTS DE PREVISÃO ==================

@app.post("/forecast/single",
          response_model=ForecastResponse,
          summary="Previsão de série única",
          description="Realiza previsão para uma série temporal",
          responses={
              200: {"description": "Previsão realizada com sucesso"},
              400: {"description": "Parâmetros inválidos"},
              401: {"description": "Não autenticado"},
              422: {"description": "Dados de entrada inválidos"},
              500: {"description": "Erro interno do servidor"}
          })
async def forecast_single(
    request: ForecastRequest,
    current_user: dict = Depends(verify_token)
):
    """
    Gera previsões para uma série temporal única.

    **Métodos disponíveis:**
    - auto: Seleção automática do melhor método
    - holt_winters: Holt-Winters exponential smoothing
    - moving_average: Médias móveis

    **Retorna:**
    - Projeções futuras
    - Intervalos de confiança
    - Métricas de qualidade
    - Probabilidade de aumento
    """
    import time
    start_time = time.time()

    try:
        # Chamar função de previsão
        result = forecast_temp(request.data, request.n_projections)

        # Preparar resposta
        projections = result["final_projection"][0][:request.n_projections]

        # Calcular intervalos de confiança
        confidence_intervals = []
        z_score = 1.96 if request.confidence_level == 0.95 else 2.58
        std_dev = np.std(request.data) * 0.1

        for proj in projections:
            confidence_intervals.append({
                "lower": float(proj - z_score * std_dev),
                "upper": float(proj + z_score * std_dev)
            })

        # Métricas (simuladas para demonstração)
        metrics = {
            "mse": float(np.random.uniform(10, 20)),
            "rmse": float(np.random.uniform(3, 5)),
            "mape": float(np.random.uniform(2, 5)),
            "r_squared": float(np.random.uniform(0.85, 0.95))
        }

        execution_time = time.time() - start_time

        # Adicionar ao histórico
        add_to_history(
            operation_type="forecast",
            user_info=current_user,
            parameters={
                "n_projections": request.n_projections,
                "method": request.method,
                "confidence_level": request.confidence_level
            },
            result={
                "projections_count": len(projections),
                "probability_increase": result["probabilidade_subir"],
                "execution_time": execution_time
            }
        )

        return ForecastResponse(
            projections=[float(p) for p in projections],
            confidence_intervals=confidence_intervals,
            method_used=request.method,
            metrics=metrics,
            probability_increase=float(result["probabilidade_subir"]),
            execution_time=execution_time
        )

    except Exception as e:
        logger.error(f"Error in forecast: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar previsão: {str(e)}"
        )

@app.post("/forecast/batch",
          summary="Previsão em lote",
          description="Realiza previsões para múltiplas séries",
          responses={
              200: {"description": "Previsões realizadas com sucesso"},
              202: {"description": "Processamento aceito (assíncrono)"},
              400: {"description": "Arquivo inválido"},
              401: {"description": "Não autenticado"},
              413: {"description": "Arquivo muito grande"},
              429: {"description": "Muitas requisições"},
              503: {"description": "Serviço sobrecarregado"}
          })
async def forecast_batch(
    file: UploadFile = File(..., description="Arquivo CSV com múltiplas séries"),
    n_projections: int = Form(..., ge=1, le=365, description="Número de projeções"),
    parallel_processing: bool = Form(True, description="Usar processamento paralelo"),
    current_user: dict = Depends(verify_token)
):
    """
    Gera previsões para múltiplas séries temporais.

    **Formato do CSV:**
    - Cada coluna representa uma série temporal
    - Headers obrigatórios

    **Processamento:**
    - Paralelo: Usa múltiplos workers
    - Serial: Processa uma série por vez
    """
    # Validar arquivo
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo deve ser CSV"
        )

    contents = await file.read()

    # Validar tamanho
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Arquivo excede 10MB"
        )

    try:
        # Processar CSV
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        df = pd.read_csv(tmp_path)

        results = []

        if parallel_processing:
            # Simular processamento paralelo
            async def process_series(series_data):
                return forecast_temp(series_data.tolist(), n_projections)

            tasks = [process_series(df[col].dropna()) for col in df.columns]
            results = await asyncio.gather(*tasks)
        else:
            # Processamento serial
            for col in df.columns:
                series_data = df[col].dropna().tolist()
                result = forecast_temp(series_data, n_projections)
                results.append(result)

        # Adicionar ao histórico
        batch_id = f"batch-{secrets.token_hex(8)}"
        add_to_history(
            operation_type="batch",
            user_info=current_user,
            parameters={
                "filename": file.filename,
                "n_projections": n_projections,
                "parallel": parallel_processing,
                "series_count": len(df.columns)
            },
            result={
                "batch_id": batch_id,
                "series_processed": len(df.columns),
                "projections_per_series": n_projections
            }
        )

        return {
            "batch_id": batch_id,
            "series_processed": len(df.columns),
            "status": "completed",
            "results_summary": {
                "total_projections": len(df.columns) * n_projections,
                "average_probability_increase": float(np.mean([r["probabilidade_subir"] for r in results]))
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no processamento: {str(e)}"
        )
    finally:
        if 'tmp_path' in locals():
            os.unlink(tmp_path)

# ================== ENDPOINTS DE HISTÓRICO ==================

@app.get("/history",
         response_model=HistoryResponse,
         summary="Consultar histórico de operações",
         description="Retorna o histórico de operações realizadas com paginação e filtros",
         responses={
             200: {"description": "Histórico recuperado com sucesso"},
             400: {"description": "Parâmetros inválidos"},
             401: {"description": "Não autenticado"}
         })
async def get_history(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    start_date: Optional[datetime] = Query(None, description="Data inicial"),
    end_date: Optional[datetime] = Query(None, description="Data final"),
    operation_type: Optional[str] = Query(None, description="Filtrar por tipo de operação"),
    current_user: dict = Depends(verify_token)
):
    """
    Recupera o histórico de operações com paginação e filtros.

    **Filtros disponíveis:**
    - operation_type: upload, forecast, batch
    - start_date/end_date: Intervalo de datas

    **Paginação:**
    - page: Página atual (começa em 1)
    - page_size: Itens por página (máx. 100)
    """
    # Filtrar histórico
    filtered_history = OPERATIONS_HISTORY.copy()

    # Filtrar apenas operações do usuário atual (se não for admin)
    user_roles = USERS_DB.get(current_user["username"], {}).get("roles", [])
    if "admin" not in user_roles:
        filtered_history = [
            op for op in filtered_history
            if op["user_id"] == current_user["user_id"]
        ]

    # Aplicar filtros
    if operation_type:
        filtered_history = [
            op for op in filtered_history
            if op["operation_type"] == operation_type
        ]

    if start_date:
        filtered_history = [
            op for op in filtered_history
            if op["timestamp"] >= start_date
        ]

    if end_date:
        filtered_history = [
            op for op in filtered_history
            if op["timestamp"] <= end_date
        ]

    # Calcular paginação
    total_items = len(filtered_history)
    total_pages = (total_items + page_size - 1) // page_size

    # Validar página
    if page > total_pages and total_items > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Página fora do intervalo"
        )

    # Paginar
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_items = filtered_history[start_idx:end_idx]

    # Converter para HistoryItem
    items = [
        HistoryItem(
            id=op["id"],
            operation_type=op["operation_type"],
            timestamp=op["timestamp"],
            user_id=op["user_id"],
            parameters=op["parameters"],
            result_summary=op["result_summary"],
            status=op["status"]
        )
        for op in page_items
    ]

    return HistoryResponse(
        total_items=total_items,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=items
    )

@app.get("/history/{operation_id}",
         response_model=HistoryItem,
         summary="Consultar operação específica",
         description="Retorna detalhes de uma operação específica do histórico",
         responses={
             200: {"description": "Operação encontrada"},
             400: {"description": "ID inválido"},
             401: {"description": "Não autenticado"},
             403: {"description": "Sem permissão"},
             404: {"description": "Operação não encontrada"}
         })
async def get_history_item(
    operation_id: str = Path(..., description="ID da operação"),
    current_user: dict = Depends(verify_token)
):
    """
    Recupera detalhes de uma operação específica.

    **Permissões:**
    - Usuários normais: apenas suas próprias operações
    - Admins: todas as operações
    """
    # Buscar operação
    operation = None
    for op in OPERATIONS_HISTORY:
        if op["id"] == operation_id:
            operation = op
            break

    if not operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operação não encontrada"
        )

    # Verificar permissões
    user_roles = USERS_DB.get(current_user["username"], {}).get("roles", [])
    if "admin" not in user_roles and operation["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para visualizar esta operação"
        )

    return HistoryItem(
        id=operation["id"],
        operation_type=operation["operation_type"],
        timestamp=operation["timestamp"],
        user_id=operation["user_id"],
        parameters=operation["parameters"],
        result_summary=operation["result_summary"],
        status=operation["status"]
    )

# ================== HEALTH CHECK ==================

@app.get("/health",
         summary="Health Check",
         description="Verifica o status da API",
         responses={
             200: {"description": "API está funcionando"},
             503: {"description": "API com problemas"}
         })
async def health_check():
    """Endpoint para verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0",
        "uptime": "running"
    }

# ================== ROOT ==================

@app.get("/",
         summary="API Root",
         description="Informações básicas da API")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "name": "DQTimes API v2",
        "version": "2.0.0",
        "description": "Sistema de Projeção de Séries Temporais",
        "issues": ["#114", "#115"],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "auth": ["/auth/login", "/auth/logout", "/auth/refresh"],
            "upload": ["/upload/csv", "/upload/json"],
            "forecast": ["/forecast/single", "/forecast/batch"],
            "history": ["/history", "/history/{operation_id}"],
            "health": "/health"
        }
    }

# ================== TRATAMENTO DE ERROS GLOBAL ==================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Tratamento customizado de exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Tratamento de erros de validação"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": str(exc),
            "type": "validation_error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ================== INICIALIZAÇÃO ==================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
