# Documentação dos Endpoints FastAPI - DQTimes

## 📋 Visão Geral

Este documento detalha a implementação dos endpoints FastAPI para o serviço de projeções de séries temporais DQTimes, conforme especificado nas issues #114 e #115.

## 🔧 Configuração Base

```python
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from typing import List, Optional, Dict, Any
import json
from pydantic import BaseModel, Field, validator
from datetime import datetime
import pandas as pd
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DQTimes API",
    description="API de Projeção de Séries Temporais",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

---

## 📌 Issue #114: Documentar Endpoints FastAPI (Parte 1: Collection)

### 1️⃣ Lista de Endpoints de Upload, Histórico, Login e Previsões

#### A. Endpoint de Upload de Dados

```python
class UploadResponse(BaseModel):
    """Modelo de resposta para upload de dados"""
    file_id: str = Field(..., description="ID único do arquivo carregado")
    filename: str = Field(..., description="Nome do arquivo original")
    size: int = Field(..., description="Tamanho do arquivo em bytes")
    upload_time: datetime = Field(..., description="Timestamp do upload")
    status: str = Field(..., description="Status do processamento")

@app.post("/upload/csv", 
          response_model=UploadResponse,
          summary="Upload de arquivo CSV",
          description="Realiza o upload de um arquivo CSV com dados de série temporal")
async def upload_csv(
    file: UploadFile = File(..., description="Arquivo CSV com dados históricos"),
    description: Optional[str] = Form(None, description="Descrição opcional do dataset")
):
    """
    Endpoint para fazer upload de arquivos CSV com séries temporais.
    
    - **file**: Arquivo CSV obrigatório
    - **description**: Descrição opcional do dataset
    
    Returns:
        Informações sobre o arquivo carregado
    """
    # Implementação
    pass

@app.post("/upload/json",
          response_model=UploadResponse,
          summary="Upload de dados JSON",
          description="Recebe dados de série temporal em formato JSON")
async def upload_json(
    data: List[float] = Form(..., description="Lista de valores numéricos"),
    metadata: Optional[Dict[str, Any]] = Form(None, description="Metadados opcionais")
):
    """
    Endpoint para enviar dados em formato JSON.
    
    - **data**: Lista de valores numéricos obrigatória
    - **metadata**: Metadados opcionais sobre os dados
    """
    # Implementação
    pass
```

#### B. Endpoint de Histórico

```python
class HistoryItem(BaseModel):
    """Modelo para item do histórico"""
    id: str = Field(..., description="ID único da operação")
    operation_type: str = Field(..., description="Tipo de operação realizada")
    timestamp: datetime = Field(..., description="Data/hora da operação")
    user_id: Optional[str] = Field(None, description="ID do usuário")
    parameters: Dict[str, Any] = Field(..., description="Parâmetros utilizados")
    result_summary: Dict[str, Any] = Field(..., description="Resumo dos resultados")

class HistoryResponse(BaseModel):
    """Modelo de resposta para histórico"""
    total_items: int = Field(..., description="Total de itens no histórico")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    items: List[HistoryItem] = Field(..., description="Lista de itens do histórico")

@app.get("/history",
         response_model=HistoryResponse,
         summary="Consultar histórico de operações",
         description="Retorna o histórico de operações realizadas")
async def get_history(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    start_date: Optional[datetime] = Query(None, description="Data inicial"),
    end_date: Optional[datetime] = Query(None, description="Data final"),
    operation_type: Optional[str] = Query(None, description="Filtrar por tipo de operação")
):
    """
    Recupera o histórico de operações com paginação e filtros.
    
    - **page**: Número da página (padrão: 1)
    - **page_size**: Quantidade de itens por página (padrão: 10, máx: 100)
    - **start_date**: Filtrar por data inicial
    - **end_date**: Filtrar por data final
    - **operation_type**: Filtrar por tipo de operação
    """
    # Implementação
    pass

@app.get("/history/{operation_id}",
         response_model=HistoryItem,
         summary="Consultar operação específica",
         description="Retorna detalhes de uma operação específica do histórico")
async def get_history_item(
    operation_id: str = Path(..., description="ID da operação")
):
    """
    Recupera detalhes de uma operação específica.
    
    - **operation_id**: ID único da operação
    """
    # Implementação
    pass
```

#### C. Endpoint de Login/Autenticação

```python
class LoginRequest(BaseModel):
    """Modelo para requisição de login"""
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")

class LoginResponse(BaseModel):
    """Modelo para resposta de login"""
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    user_id: str = Field(..., description="ID do usuário autenticado")
    username: str = Field(..., description="Nome do usuário")

@app.post("/auth/login",
          response_model=LoginResponse,
          summary="Autenticação de usuário",
          description="Realiza o login e retorna um token de acesso")
async def login(
    credentials: LoginRequest
):
    """
    Autentica o usuário e retorna um token JWT.
    
    - **username**: Nome de usuário (3-50 caracteres)
    - **password**: Senha (mínimo 8 caracteres)
    
    Returns:
        Token de acesso e informações do usuário
    """
    # Implementação
    pass

@app.post("/auth/logout",
          summary="Logout de usuário",
          description="Invalida o token de acesso atual")
async def logout(
    authorization: str = Header(..., description="Token Bearer")
):
    """
    Realiza o logout invalidando o token atual.
    
    - **authorization**: Token Bearer no header
    """
    # Implementação
    pass

@app.post("/auth/refresh",
          response_model=LoginResponse,
          summary="Renovar token de acesso",
          description="Gera um novo token de acesso")
async def refresh_token(
    refresh_token: str = Form(..., description="Token de atualização")
):
    """
    Renova o token de acesso usando um refresh token.
    
    - **refresh_token**: Token de atualização válido
    """
    # Implementação
    pass
```

#### D. Endpoint de Previsões

```python
class ForecastRequest(BaseModel):
    """Modelo para requisição de previsão"""
    data: List[float] = Field(..., min_items=10, description="Série temporal histórica")
    n_projections: int = Field(..., ge=1, le=365, description="Número de projeções")
    method: Optional[str] = Field("auto", description="Método de previsão")
    confidence_level: Optional[float] = Field(0.95, ge=0.5, le=0.99, description="Nível de confiança")

class ForecastResponse(BaseModel):
    """Modelo para resposta de previsão"""
    projections: List[float] = Field(..., description="Valores projetados")
    confidence_intervals: List[Dict[str, float]] = Field(..., description="Intervalos de confiança")
    method_used: str = Field(..., description="Método utilizado")
    metrics: Dict[str, float] = Field(..., description="Métricas de qualidade")
    probability_increase: float = Field(..., ge=0, le=1, description="Probabilidade de aumento")

@app.post("/forecast/single",
          response_model=ForecastResponse,
          summary="Previsão de série única",
          description="Realiza previsão para uma série temporal")
async def forecast_single(
    request: ForecastRequest
):
    """
    Gera previsões para uma série temporal única.
    
    - **data**: Lista com no mínimo 10 valores históricos
    - **n_projections**: Quantidade de projeções (1-365)
    - **method**: Método de previsão (auto, holt_winters, moving_average)
    - **confidence_level**: Nível de confiança (0.5-0.99)
    """
    # Implementação
    pass

@app.post("/forecast/batch",
          summary="Previsão em lote",
          description="Realiza previsões para múltiplas séries")
async def forecast_batch(
    file: UploadFile = File(..., description="Arquivo CSV com múltiplas séries"),
    n_projections: int = Form(..., ge=1, le=365, description="Número de projeções"),
    parallel_processing: bool = Form(True, description="Usar processamento paralelo")
):
    """
    Gera previsões para múltiplas séries temporais.
    
    - **file**: Arquivo CSV com múltiplas séries
    - **n_projections**: Quantidade de projeções para cada série
    - **parallel_processing**: Ativar processamento paralelo
    """
    # Implementação
    pass
```

### 2️⃣ Exemplos de Requisições Válidas e Inválidas

#### Requisições Válidas ✅

```python
# Exemplo 1: Upload de CSV válido
curl -X POST "http://localhost:8000/upload/csv" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dados.csv" \
  -F "description=Dados de vendas 2024"

# Resposta esperada:
{
  "file_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "filename": "dados.csv",
  "size": 2048,
  "upload_time": "2024-11-17T21:30:00",
  "status": "processed"
}

# Exemplo 2: Previsão válida
curl -X POST "http://localhost:8000/forecast/single" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 120, 130, 115, 140, 160, 155, 170, 180, 190],
    "n_projections": 5,
    "method": "holt_winters",
    "confidence_level": 0.95
  }'

# Resposta esperada:
{
  "projections": [195.2, 201.5, 208.3, 215.7, 223.8],
  "confidence_intervals": [
    {"lower": 185.3, "upper": 205.1},
    {"lower": 188.7, "upper": 214.3},
    {"lower": 192.5, "upper": 224.1},
    {"lower": 196.8, "upper": 234.6},
    {"lower": 201.5, "upper": 246.1}
  ],
  "method_used": "holt_winters",
  "metrics": {
    "mse": 12.5,
    "rmse": 3.54,
    "mape": 2.3
  },
  "probability_increase": 0.82
}

# Exemplo 3: Consulta de histórico válida
curl -X GET "http://localhost:8000/history?page=1&page_size=5&operation_type=forecast"

# Resposta esperada:
{
  "total_items": 42,
  "page": 1,
  "page_size": 5,
  "items": [
    {
      "id": "op-001",
      "operation_type": "forecast",
      "timestamp": "2024-11-17T20:15:00",
      "user_id": "user-123",
      "parameters": {
        "n_projections": 10,
        "method": "auto"
      },
      "result_summary": {
        "projections_count": 10,
        "probability_increase": 0.75
      }
    }
  ]
}
```

#### Requisições Inválidas ❌

```python
# Exemplo 1: Upload sem arquivo
curl -X POST "http://localhost:8000/upload/csv"

# Erro esperado:
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

# Exemplo 2: Previsão com dados insuficientes
curl -X POST "http://localhost:8000/forecast/single" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 120],  # Menos de 10 valores
    "n_projections": 5
  }'

# Erro esperado:
{
  "detail": [
    {
      "loc": ["body", "data"],
      "msg": "ensure this value has at least 10 items",
      "type": "value_error.list.min_items",
      "ctx": {"limit_value": 10}
    }
  ]
}

# Exemplo 3: Login com credenciais inválidas
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ab",  # Menos de 3 caracteres
    "password": "123"   # Menos de 8 caracteres
  }'

# Erro esperado:
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "ensure this value has at least 3 characters",
      "type": "value_error.str.min_length",
      "ctx": {"limit_value": 3}
    },
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.str.min_length",
      "ctx": {"limit_value": 8}
    }
  ]
}

# Exemplo 4: Parâmetros de paginação inválidos
curl -X GET "http://localhost:8000/history?page=0&page_size=150"

# Erro esperado:
{
  "detail": [
    {
      "loc": ["query", "page"],
      "msg": "ensure this value is greater than or equal to 1",
      "type": "value_error.number.not_ge",
      "ctx": {"limit_value": 1}
    },
    {
      "loc": ["query", "page_size"],
      "msg": "ensure this value is less than or equal to 100",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 100}
    }
  ]
}
```

### 3️⃣ Detalhamento de Parâmetros Obrigatórios e Opcionais

```python
# Classe para documentação detalhada de parâmetros
class ParameterDocumentation:
    """
    Documentação completa dos parâmetros de cada endpoint
    """
    
    UPLOAD_CSV = {
        "obrigatórios": {
            "file": {
                "tipo": "UploadFile",
                "descrição": "Arquivo CSV com dados de série temporal",
                "formato": "CSV com headers",
                "tamanho_máximo": "10MB"
            }
        },
        "opcionais": {
            "description": {
                "tipo": "str",
                "descrição": "Descrição do dataset",
                "padrão": None,
                "tamanho_máximo": 500
            }
        }
    }
    
    FORECAST_SINGLE = {
        "obrigatórios": {
            "data": {
                "tipo": "List[float]",
                "descrição": "Série temporal histórica",
                "mínimo_items": 10,
                "máximo_items": 10000
            },
            "n_projections": {
                "tipo": "int",
                "descrição": "Número de projeções futuras",
                "mínimo": 1,
                "máximo": 365
            }
        },
        "opcionais": {
            "method": {
                "tipo": "str",
                "descrição": "Método de previsão",
                "opções": ["auto", "holt_winters", "moving_average", "arima"],
                "padrão": "auto"
            },
            "confidence_level": {
                "tipo": "float",
                "descrição": "Nível de confiança para intervalos",
                "mínimo": 0.5,
                "máximo": 0.99,
                "padrão": 0.95
            }
        }
    }
    
    HISTORY = {
        "obrigatórios": {},  # Nenhum parâmetro obrigatório
        "opcionais": {
            "page": {
                "tipo": "int",
                "descrição": "Número da página",
                "mínimo": 1,
                "padrão": 1
            },
            "page_size": {
                "tipo": "int",
                "descrição": "Itens por página",
                "mínimo": 1,
                "máximo": 100,
                "padrão": 10
            },
            "start_date": {
                "tipo": "datetime",
                "descrição": "Data inicial do filtro",
                "formato": "ISO 8601",
                "padrão": None
            },
            "end_date": {
                "tipo": "datetime",
                "descrição": "Data final do filtro",
                "formato": "ISO 8601",
                "padrão": None
            },
            "operation_type": {
                "tipo": "str",
                "descrição": "Tipo de operação",
                "opções": ["upload", "forecast", "batch", "export"],
                "padrão": None
            }
        }
    }
    
    LOGIN = {
        "obrigatórios": {
            "username": {
                "tipo": "str",
                "descrição": "Nome de usuário",
                "mínimo_caracteres": 3,
                "máximo_caracteres": 50,
                "formato": "alfanumérico com _ e -"
            },
            "password": {
                "tipo": "str",
                "descrição": "Senha do usuário",
                "mínimo_caracteres": 8,
                "deve_conter": ["letras", "números", "caractere especial"]
            }
        },
        "opcionais": {}
    }

# Middleware para validação de parâmetros
@app.middleware("http")
async def validate_parameters(request, call_next):
    """
    Middleware para validação adicional de parâmetros
    """
    try:
        response = await call_next(request)
        return response
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=422,
            content={
                "detail": str(e),
                "type": "validation_error"
            }
        )
```

---

## 📌 Issue #115: Documentar Endpoints FastAPI (Parte 2: Exemplos Práticos)

### 1️⃣ Incluir Exemplos cURL/Postman

#### Coleção Postman

```json
{
  "info": {
    "name": "DQTimes API Collection",
    "description": "Coleção de endpoints para a API DQTimes",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Autenticação",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"usuario_teste\",\n  \"password\": \"Senha@123\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth", "login"]
            }
          }
        },
        {
          "name": "Refresh Token",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/x-www-form-urlencoded"
              }
            ],
            "body": {
              "mode": "urlencoded",
              "urlencoded": [
                {
                  "key": "refresh_token",
                  "value": "{{refresh_token}}"
                }
              ]
            },
            "url": {
              "raw": "{{base_url}}/auth/refresh",
              "host": ["{{base_url}}"],
              "path": ["auth", "refresh"]
            }
          }
        }
      ]
    },
    {
      "name": "Upload de Dados",
      "item": [
        {
          "name": "Upload CSV",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "file",
                  "type": "file",
                  "src": "/path/to/data.csv"
                },
                {
                  "key": "description",
                  "value": "Dataset de vendas mensais",
                  "type": "text"
                }
              ]
            },
            "url": {
              "raw": "{{base_url}}/upload/csv",
              "host": ["{{base_url}}"],
              "path": ["upload", "csv"]
            }
          }
        },
        {
          "name": "Upload JSON",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              },
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"data\": [100, 120, 135, 142, 158, 165, 172, 188, 195, 203],\n  \"metadata\": {\n    \"source\": \"vendas\",\n    \"period\": \"mensal\",\n    \"unit\": \"unidades\"\n  }\n}"
            },
            "url": {
              "raw": "{{base_url}}/upload/json",
              "host": ["{{base_url}}"],
              "path": ["upload", "json"]
            }
          }
        }
      ]
    },
    {
      "name": "Previsões",
      "item": [
        {
          "name": "Previsão Simples",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              },
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"data\": [100, 110, 105, 120, 125, 130, 128, 135, 140, 145],\n  \"n_projections\": 6,\n  \"method\": \"auto\",\n  \"confidence_level\": 0.95\n}"
            },
            "url": {
              "raw": "{{base_url}}/forecast/single",
              "host": ["{{base_url}}"],
              "path": ["forecast", "single"]
            }
          }
        },
        {
          "name": "Previsão em Lote",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "file",
                  "type": "file",
                  "src": "/path/to/multiple_series.csv"
                },
                {
                  "key": "n_projections",
                  "value": "12",
                  "type": "text"
                },
                {
                  "key": "parallel_processing",
                  "value": "true",
                  "type": "text"
                }
              ]
            },
            "url": {
              "raw": "{{base_url}}/forecast/batch",
              "host": ["{{base_url}}"],
              "path": ["forecast", "batch"]
            }
          }
        }
      ]
    },
    {
      "name": "Histórico",
      "item": [
        {
          "name": "Listar Histórico",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/history?page=1&page_size=10&operation_type=forecast",
              "host": ["{{base_url}}"],
              "path": ["history"],
              "query": [
                {
                  "key": "page",
                  "value": "1"
                },
                {
                  "key": "page_size",
                  "value": "10"
                },
                {
                  "key": "operation_type",
                  "value": "forecast"
                },
                {
                  "key": "start_date",
                  "value": "2024-11-01T00:00:00",
                  "disabled": true
                },
                {
                  "key": "end_date",
                  "value": "2024-11-30T23:59:59",
                  "disabled": true
                }
              ]
            }
          }
        },
        {
          "name": "Detalhes de Operação",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/history/{{operation_id}}",
              "host": ["{{base_url}}"],
              "path": ["history", "{{operation_id}}"]
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    },
    {
      "key": "access_token",
      "value": ""
    },
    {
      "key": "refresh_token",
      "value": ""
    },
    {
      "key": "operation_id",
      "value": ""
    }
  ]
}
```

#### Exemplos cURL Completos

```bash
#!/bin/bash

# Arquivo: api_examples.sh
# Exemplos de uso da API DQTimes com cURL

BASE_URL="http://localhost:8000"
TOKEN=""

# Função auxiliar para pretty print JSON
pretty_json() {
    python -m json.tool
}

# 1. Login e obtenção de token
echo "=== AUTENTICAÇÃO ==="
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123"
  }')

echo "$RESPONSE" | pretty_json
TOKEN=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "Token obtido: $TOKEN"

# 2. Upload de arquivo CSV
echo -e "\n=== UPLOAD DE CSV ==="
curl -X POST "$BASE_URL/upload/csv" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./data/sales_data.csv" \
  -F "description=Dados de vendas Q4 2024" | pretty_json

# 3. Upload de dados JSON
echo -e "\n=== UPLOAD DE JSON ==="
curl -X POST "$BASE_URL/upload/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 112, 124, 136, 148, 160, 172, 184, 196, 208],
    "metadata": {
      "source": "manual_input",
      "description": "Dados de teste"
    }
  }' | pretty_json

# 4. Previsão simples
echo -e "\n=== PREVISÃO SIMPLES ==="
curl -X POST "$BASE_URL/forecast/single" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [10, 12, 13, 15, 14, 16, 18, 17, 19, 21, 20, 22],
    "n_projections": 3,
    "method": "holt_winters",
    "confidence_level": 0.95
  }' | pretty_json

# 5. Previsão em lote
echo -e "\n=== PREVISÃO EM LOTE ==="
curl -X POST "$BASE_URL/forecast/batch" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./data/multiple_series.csv" \
  -F "n_projections=6" \
  -F "parallel_processing=true" | pretty_json

# 6. Consultar histórico com filtros
echo -e "\n=== HISTÓRICO COM FILTROS ==="
curl -X GET "$BASE_URL/history?page=1&page_size=5&operation_type=forecast" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

# 7. Consultar operação específica
echo -e "\n=== DETALHES DE OPERAÇÃO ==="
OPERATION_ID="op-12345"
curl -X GET "$BASE_URL/history/$OPERATION_ID" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

# 8. Renovar token
echo -e "\n=== RENOVAR TOKEN ==="
curl -X POST "$BASE_URL/auth/refresh" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "refresh_token=$REFRESH_TOKEN" | pretty_json

# 9. Logout
echo -e "\n=== LOGOUT ==="
curl -X POST "$BASE_URL/auth/logout" \
  -H "Authorization: Bearer $TOKEN" | pretty_json
```

### 2️⃣ Mostrar Resposta JSON de Sucesso e Erro

```python
# Arquivo: response_examples.py

class ResponseExamples:
    """
    Exemplos de respostas JSON para documentação
    """
    
    # RESPOSTAS DE SUCESSO
    SUCCESS_RESPONSES = {
        "upload_csv": {
            "status_code": 200,
            "body": {
                "file_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "filename": "sales_data.csv",
                "size": 4096,
                "upload_time": "2024-11-17T21:45:00Z",
                "status": "processed",
                "rows_processed": 150,
                "columns_detected": ["date", "value", "category"]
            }
        },
        
        "forecast_single": {
            "status_code": 200,
            "body": {
                "projections": [210.5, 215.3, 220.7, 226.4, 232.5],
                "confidence_intervals": [
                    {"lower": 200.2, "upper": 220.8},
                    {"lower": 202.1, "upper": 228.5},
                    {"lower": 204.3, "upper": 237.1},
                    {"lower": 206.8, "upper": 246.0},
                    {"lower": 209.5, "upper": 255.5}
                ],
                "method_used": "holt_winters",
                "metrics": {
                    "mse": 15.7,
                    "rmse": 3.96,
                    "mape": 2.8,
                    "r_squared": 0.92
                },
                "probability_increase": 0.78,
                "execution_time": 0.125
            }
        },
        
        "login": {
            "status_code": 200,
            "body": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "user_id": "user-12345",
                "username": "admin",
                "roles": ["admin", "analyst"]
            }
        },
        
        "history": {
            "status_code": 200,
            "body": {
                "total_items": 156,
                "page": 1,
                "page_size": 10,
                "total_pages": 16,
                "items": [
                    {
                        "id": "op-98765",
                        "operation_type": "forecast",
                        "timestamp": "2024-11-17T20:30:00Z",
                        "user_id": "user-12345",
                        "parameters": {
                            "n_projections": 10,
                            "method": "auto",
                            "confidence_level": 0.95
                        },
                        "result_summary": {
                            "projections_count": 10,
                            "probability_increase": 0.72,
                            "execution_time": 0.235
                        },
                        "status": "completed"
                    }
                ]
            }
        }
    }
    
    # RESPOSTAS DE ERRO
    ERROR_RESPONSES = {
        "validation_error": {
            "status_code": 422,
            "body": {
                "detail": [
                    {
                        "loc": ["body", "data"],
                        "msg": "ensure this value has at least 10 items",
                        "type": "value_error.list.min_items",
                        "ctx": {"limit_value": 10}
                    }
                ]
            }
        },
        
        "authentication_error": {
            "status_code": 401,
            "body": {
                "detail": "Invalid authentication credentials",
                "type": "authentication_error",
                "code": "INVALID_CREDENTIALS"
            }
        },
        
        "authorization_error": {
            "status_code": 403,
            "body": {
                "detail": "Not enough permissions to perform this action",
                "type": "authorization_error",
                "code": "INSUFFICIENT_PERMISSIONS",
                "required_role": "admin"
            }
        },
        
        "not_found_error": {
            "status_code": 404,
            "body": {
                "detail": "Resource not found",
                "type": "not_found_error",
                "code": "RESOURCE_NOT_FOUND",
                "resource_id": "op-99999"
            }
        },
        
        "server_error": {
            "status_code": 500,
            "body": {
                "detail": "Internal server error occurred",
                "type": "internal_error",
                "code": "INTERNAL_SERVER_ERROR",
                "request_id": "req-abc123",
                "timestamp": "2024-11-17T21:50:00Z"
            }
        },
        
        "rate_limit_error": {
            "status_code": 429,
            "body": {
                "detail": "Rate limit exceeded",
                "type": "rate_limit_error",
                "code": "RATE_LIMIT_EXCEEDED",
                "retry_after": 60,
                "limit": 100,
                "window": "1h"
            }
        },
        
        "file_size_error": {
            "status_code": 413,
            "body": {
                "detail": "File size exceeds maximum allowed",
                "type": "file_error",
                "code": "FILE_TOO_LARGE",
                "max_size_mb": 10,
                "uploaded_size_mb": 15.5
            }
        }
    }
```

### 3️⃣ Anotar Códigos de Status Esperados

```python
from enum import Enum
from typing import Dict, List

class StatusCodes(str, Enum):
    """Códigos de status HTTP utilizados pela API"""
    
    # 2xx - Sucesso
    OK = "200 OK"
    CREATED = "201 Created"
    ACCEPTED = "202 Accepted"
    NO_CONTENT = "204 No Content"
    
    # 4xx - Erros do Cliente
    BAD_REQUEST = "400 Bad Request"
    UNAUTHORIZED = "401 Unauthorized"
    FORBIDDEN = "403 Forbidden"
    NOT_FOUND = "404 Not Found"
    METHOD_NOT_ALLOWED = "405 Method Not Allowed"
    CONFLICT = "409 Conflict"
    PAYLOAD_TOO_LARGE = "413 Payload Too Large"
    UNPROCESSABLE_ENTITY = "422 Unprocessable Entity"
    TOO_MANY_REQUESTS = "429 Too Many Requests"
    
    # 5xx - Erros do Servidor
    INTERNAL_SERVER_ERROR = "500 Internal Server Error"
    NOT_IMPLEMENTED = "501 Not Implemented"
    SERVICE_UNAVAILABLE = "503 Service Unavailable"
    GATEWAY_TIMEOUT = "504 Gateway Timeout"

class EndpointStatusCodes:
    """
    Mapeamento de endpoints para códigos de status esperados
    """
    
    ENDPOINTS: Dict[str, Dict[str, List[str]]] = {
        "/auth/login": {
            "POST": {
                "success": [StatusCodes.OK],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # Formato inválido
                    StatusCodes.UNAUTHORIZED,  # Credenciais inválidas
                    StatusCodes.TOO_MANY_REQUESTS,  # Limite de tentativas
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        },
        
        "/auth/logout": {
            "POST": {
                "success": [StatusCodes.NO_CONTENT],
                "errors": [
                    StatusCodes.UNAUTHORIZED,  # Token inválido
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        },
        
        "/auth/refresh": {
            "POST": {
                "success": [StatusCodes.OK],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # Token mal formatado
                    StatusCodes.UNAUTHORIZED,  # Token expirado
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        },
        
        "/upload/csv": {
            "POST": {
                "success": [StatusCodes.OK, StatusCodes.CREATED],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # Arquivo inválido
                    StatusCodes.UNAUTHORIZED,  # Não autenticado
                    StatusCodes.PAYLOAD_TOO_LARGE,  # Arquivo muito grande
                    StatusCodes.UNPROCESSABLE_ENTITY,  # CSV mal formatado
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        },
        
        "/upload/json": {
            "POST": {
                "success": [StatusCodes.OK, StatusCodes.CREATED],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # JSON inválido
                    StatusCodes.UNAUTHORIZED,  # Não autenticado
                    StatusCodes.UNPROCESSABLE_ENTITY,  # Dados inválidos
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        },
        
        "/forecast/single": {
            "POST": {
                "success": [StatusCodes.OK],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # Parâmetros inválidos
                    StatusCodes.UNAUTHORIZED,  # Não autenticado
                    StatusCodes.FORBIDDEN,  # Sem permissão
                    StatusCodes.UNPROCESSABLE_ENTITY,  # Dados insuficientes
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        },
        
        "/forecast/batch": {
            "POST": {
                "success": [StatusCodes.OK, StatusCodes.ACCEPTED],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # Arquivo inválido
                    StatusCodes.UNAUTHORIZED,  # Não autenticado
                    StatusCodes.FORBIDDEN,  # Limite de uso excedido
                    StatusCodes.PAYLOAD_TOO_LARGE,  # Arquivo muito grande
                    StatusCodes.TOO_MANY_REQUESTS,  # Muitas requisições
                    StatusCodes.INTERNAL_SERVER_ERROR,
                    StatusCodes.SERVICE_UNAVAILABLE  # Serviço sobrecarregado
                ]
            }
        },
        
        "/history": {
            "GET": {
                "success": [StatusCodes.OK],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # Parâmetros inválidos
                    StatusCodes.UNAUTHORIZED,  # Não autenticado
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        },
        
        "/history/{operation_id}": {
            "GET": {
                "success": [StatusCodes.OK],
                "errors": [
                    StatusCodes.BAD_REQUEST,  # ID inválido
                    StatusCodes.UNAUTHORIZED,  # Não autenticado
                    StatusCodes.FORBIDDEN,  # Sem permissão para ver
                    StatusCodes.NOT_FOUND,  # Operação não encontrada
                    StatusCodes.INTERNAL_SERVER_ERROR
                ]
            }
        }
    }
    
    @staticmethod
    def get_status_description(code: str) -> str:
        """Retorna descrição detalhada do código de status"""
        descriptions = {
            "200": "Requisição processada com sucesso",
            "201": "Recurso criado com sucesso",
            "202": "Requisição aceita para processamento",
            "204": "Requisição processada sem conteúdo de retorno",
            "400": "Requisição mal formada ou parâmetros inválidos",
            "401": "Autenticação necessária ou inválida",
            "403": "Permissões insuficientes para a operação",
            "404": "Recurso não encontrado",
            "405": "Método HTTP não permitido",
            "409": "Conflito com o estado atual do recurso",
            "413": "Payload excede o tamanho máximo permitido",
            "422": "Entidade não processável - validação falhou",
            "429": "Muitas requisições - limite de taxa excedido",
            "500": "Erro interno do servidor",
            "501": "Funcionalidade não implementada",
            "503": "Serviço temporariamente indisponível",
            "504": "Timeout na comunicação com serviços externos"
        }
        return descriptions.get(code.split()[0], "Código não documentado")

# Decorador para documentar status codes
def document_status_codes(success: List[int], errors: List[int]):
    """
    Decorador para documentar códigos de status em endpoints
    """
    def decorator(func):
        func.success_codes = success
        func.error_codes = errors
        return func
    return decorator

# Exemplo de uso do decorador
@app.post("/forecast/single", 
         response_model=ForecastResponse,
         responses={
             200: {"description": "Previsão realizada com sucesso"},
             400: {"description": "Parâmetros inválidos"},
             401: {"description": "Não autenticado"},
             422: {"description": "Dados de entrada inválidos"},
             500: {"description": "Erro interno do servidor"}
         })
@document_status_codes(
    success=[200],
    errors=[400, 401, 422, 500]
)
async def forecast_single(request: ForecastRequest):
    """Endpoint com documentação completa de status codes"""
    pass
```

## 📊 Testes Automatizados

```python
# Arquivo: test_api_endpoints.py

import pytest
import httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAuthentication:
    """Testes para endpoints de autenticação"""
    
    def test_login_success(self):
        """Testa login com credenciais válidas"""
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "Test@123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        response = client.post("/auth/login", json={
            "username": "invalid",
            "password": "wrong"
        })
        assert response.status_code == 401
        assert "detail" in response.json()
    
    def test_login_validation_error(self):
        """Testa validação de parâmetros no login"""
        response = client.post("/auth/login", json={
            "username": "ab",  # Muito curto
            "password": "123"   # Muito curto
        })
        assert response.status_code == 422
        assert "detail" in response.json()

class TestForecast:
    """Testes para endpoints de previsão"""
    
    def test_forecast_valid_data(self, auth_headers):
        """Testa previsão com dados válidos"""
        response = client.post("/forecast/single", 
            headers=auth_headers,
            json={
                "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "n_projections": 3,
                "method": "auto"
            }
        )
        assert response.status_code == 200
        assert "projections" in response.json()
        assert len(response.json()["projections"]) == 3
    
    def test_forecast_insufficient_data(self, auth_headers):
        """Testa previsão com dados insuficientes"""
        response = client.post("/forecast/single",
            headers=auth_headers,
            json={
                "data": [1, 2, 3],  # Menos de 10 valores
                "n_projections": 3
            }
        )
        assert response.status_code == 422
    
    def test_forecast_invalid_parameters(self, auth_headers):
        """Testa previsão com parâmetros inválidos"""
        response = client.post("/forecast/single",
            headers=auth_headers,
            json={
                "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "n_projections": 500,  # Excede o máximo
                "confidence_level": 1.5  # Fora do intervalo
            }
        )
        assert response.status_code == 422

class TestHistory:
    """Testes para endpoints de histórico"""
    
    def test_history_pagination(self, auth_headers):
        """Testa paginação do histórico"""
        response = client.get("/history?page=1&page_size=5",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) <= 5
    
    def test_history_invalid_pagination(self, auth_headers):
        """Testa paginação com parâmetros inválidos"""
        response = client.get("/history?page=0&page_size=200",
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_history_filters(self, auth_headers):
        """Testa filtros do histórico"""
        response = client.get(
            "/history?operation_type=forecast&start_date=2024-11-01T00:00:00",
            headers=auth_headers
        )
        assert response.status_code == 200
        items = response.json()["items"]
        assert all(item["operation_type"] == "forecast" for item in items)

@pytest.fixture
def auth_headers():
    """Fixture para obter headers de autenticação"""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "Test@123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

## 🚀 Script de Deploy e Configuração

```bash
#!/bin/bash

# Arquivo: deploy_api.sh
# Script de deploy e configuração da API DQTimes

set -e  # Parar em caso de erro

echo "========================================="
echo "   Deploy da API DQTimes"
echo "========================================="

# 1. Verificar dependências
echo "📦 Verificando dependências..."
python --version
pip --version

# 2. Instalar requirements
echo "📦 Instalando dependências Python..."
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
echo "🔧 Configurando variáveis de ambiente..."
cat > .env << EOF
# Configurações da API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false

# Configurações de autenticação
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Configurações de banco de dados
DATABASE_URL=postgresql://user:password@localhost/dqtimes

# Configurações de processamento
MAX_FILE_SIZE_MB=10
MAX_PROJECTIONS=365
PARALLEL_PROCESSING=true
DASK_WORKERS=4

# Configurações de rate limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Configurações de logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/dqtimes/api.log
EOF

# 4. Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p logs
mkdir -p uploads
mkdir -p cache

# 5. Executar migrações (se aplicável)
echo "🗄️ Executando migrações..."
# alembic upgrade head

# 6. Executar testes
echo "🧪 Executando testes..."
pytest tests/ -v

# 7. Iniciar servidor
echo "🚀 Iniciando servidor..."
uvicorn main:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${API_PORT:-8000} \
    --workers ${API_WORKERS:-4} \
    --log-level ${LOG_LEVEL:-info}

echo "✅ API iniciada com sucesso!"
echo "📚 Documentação disponível em: http://localhost:8000/docs"
```

## 📋 Conclusão

Este documento fornece uma implementação completa das issues #114 e #115, incluindo:

✅ **Issue #114 - Documentar endpoints FastAPI (parte 1: collection)**
- Documentação completa de todos os endpoints
- Exemplos de requisições válidas e inválidas
- Detalhamento de parâmetros obrigatórios e opcionais

✅ **Issue #115 - Documentar endpoints FastAPI (parte 2: exemplos práticos)**
- Exemplos cURL e coleção Postman
- Respostas JSON de sucesso e erro
- Códigos de status HTTP esperados

### 🔗 Próximos Passos

1. **Implementar os endpoints** seguindo esta documentação
2. **Adicionar validações** conforme especificado
3. **Implementar testes automatizados** usando o framework pytest
4. **Configurar CI/CD** para deploy automático
5. **Adicionar monitoramento** e observabilidade

### 📚 Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Validation](https://pydantic-docs.helpmanual.io/)
- [JWT Authentication](https://jwt.io/)
- [Postman Learning Center](https://learning.postman.com/)
