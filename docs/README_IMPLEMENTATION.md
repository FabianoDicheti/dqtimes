# 🚀 Guia de Implementação - API DQTimes

## 📋 Visão Geral

Este documento fornece instruções completas para implementar e testar a API DQTimes com base nas issues #27_ref5_ref7_8_2h e #27b_ref5_ref7_8_1h.

## 📦 Arquivos Criados

1. **`api_documentation.md`** - Documentação completa dos endpoints
2. **`api_implementation.py`** - Implementação completa da API FastAPI
3. **`test_api_examples.sh`** - Script de testes automatizados
4. **`postman_collection.json`** - Coleção Postman para testes
5. **`README_IMPLEMENTATION.md`** - Este arquivo

## 🔧 Pré-requisitos

```bash
# Python 3.8+
python3 --version

# Instalar dependências
pip install fastapi uvicorn pandas numpy dask distributed python-multipart pyjwt
```

## 🚀 Como Executar

### 1. Preparar o Ambiente

```bash
# Navegar para o diretório do projeto
cd /home/claude/bostafabianica/dqtimes

# Criar ambiente virtual (opcional mas recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
pip install pyjwt  # Adicional para autenticação
```

### 2. Iniciar a API

```bash
# Método 1: Executar diretamente
python api_implementation.py

# Método 2: Usar uvicorn
uvicorn api_implementation:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

### 3. Executar Testes

#### Usando o Script Bash

```bash
# Dar permissão de execução
chmod +x test_api_examples.sh

# Executar testes
./test_api_examples.sh
```

#### Usando Postman

1. Abrir Postman
2. Importar arquivo `postman_collection.json`
3. Configurar variável `base_url` se necessário
4. Executar a coleção

#### Usando cURL

```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin@123"}'

# Salvar o token retornado
TOKEN="seu_token_aqui"

# Fazer previsão
curl -X POST "http://localhost:8000/forecast/single" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
    "n_projections": 5,
    "method": "auto"
  }'
```

## 📊 Estrutura dos Endpoints

### Autenticação
- `POST /auth/login` - Login e obtenção de token
- `POST /auth/logout` - Logout
- `POST /auth/refresh` - Renovar token

### Upload de Dados
- `POST /upload/csv` - Upload de arquivo CSV
- `POST /upload/json` - Upload de dados JSON

### Previsões
- `POST /forecast/single` - Previsão de série única
- `POST /forecast/batch` - Previsão em lote

### Histórico
- `GET /history` - Listar histórico com paginação
- `GET /history/{id}` - Detalhes de operação específica

### Utilitários
- `GET /health` - Health check
- `GET /` - Informações da API

## 🔑 Credenciais de Teste

```json
{
  "admin": {
    "username": "admin",
    "password": "Admin@123",
    "roles": ["admin", "analyst"]
  },
  "testuser": {
    "username": "testuser",
    "password": "Test@123",
    "roles": ["analyst"]
  }
}
```

## 📝 Exemplos de Requisições

### 1. Login

```json
POST /auth/login
{
  "username": "admin",
  "password": "Admin@123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_id": "user-001",
  "username": "admin",
  "roles": ["admin", "analyst"]
}
```

### 2. Upload de Dados JSON

```json
POST /upload/json
Headers: Authorization: Bearer {token}
{
  "data": "[100, 110, 120, 130, 140, 150, 160, 170, 180, 190]",
  "metadata": "{\"source\": \"vendas\", \"period\": \"mensal\"}"
}

Response:
{
  "file_id": "json-a1b2c3d4",
  "filename": "json_upload",
  "size": 124,
  "upload_time": "2024-11-17T21:45:00Z",
  "status": "processed",
  "rows_processed": 10
}
```

### 3. Previsão

```json
POST /forecast/single
Headers: Authorization: Bearer {token}
{
  "data": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
  "n_projections": 5,
  "method": "auto",
  "confidence_level": 0.95
}

Response:
{
  "projections": [195.2, 201.5, 208.3, 215.7, 223.8],
  "confidence_intervals": [
    {"lower": 185.3, "upper": 205.1},
    {"lower": 188.7, "upper": 214.3}
  ],
  "method_used": "auto",
  "metrics": {
    "mse": 12.5,
    "rmse": 3.54,
    "mape": 2.3,
    "r_squared": 0.92
  },
  "probability_increase": 0.82,
  "execution_time": 0.125
}
```

## ⚠️ Tratamento de Erros

### Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Requisição mal formada |
| 401 | Não autenticado |
| 403 | Sem permissão |
| 404 | Recurso não encontrado |
| 413 | Payload muito grande |
| 422 | Entidade não processável |
| 429 | Muitas requisições |
| 500 | Erro interno do servidor |

### Exemplo de Erro

```json
{
  "detail": "Token expirado",
  "status_code": 401,
  "timestamp": "2024-11-17T21:50:00Z"
}
```

## 🧪 Validações Implementadas

### Parâmetros de Login
- Username: 3-50 caracteres alfanuméricos
- Password: mínimo 8 caracteres

### Parâmetros de Previsão
- Data: mínimo 10, máximo 10000 valores
- N_projections: 1-365
- Confidence_level: 0.5-0.99

### Parâmetros de Paginação
- Page: >= 1
- Page_size: 1-100

## 📈 Métricas e Monitoramento

A API retorna as seguintes métricas:

- **MSE** - Mean Squared Error
- **RMSE** - Root Mean Squared Error
- **MAPE** - Mean Absolute Percentage Error
- **R²** - Coeficiente de determinação
- **Execution Time** - Tempo de processamento
- **Probability Increase** - Probabilidade de aumento

## 🔒 Segurança

- Autenticação JWT com expiração configurável
- Validação de parâmetros em todos os endpoints
- Rate limiting (pode ser configurado)
- Logs de auditoria para todas as operações

## 📚 Próximos Passos

1. **Integrar com banco de dados real** (substituir armazenamento em memória)
2. **Implementar cache** para otimizar performance
3. **Adicionar mais métodos de previsão** (ARIMA, Prophet, etc.)
4. **Implementar websockets** para processamento assíncrono
5. **Adicionar dashboard de monitoramento**
6. **Configurar CI/CD pipeline**

## 🆘 Troubleshooting

### Problema: ImportError ao importar app.aplicacao

```bash
# Solução: Verificar se os arquivos .so estão no caminho correto
ls dqtimes/app/libs/*.so
```

### Problema: Token JWT inválido

```bash
# Solução: Verificar se JWT_SECRET está configurado
export JWT_SECRET_KEY="sua_chave_secreta_aqui"
```

### Problema: Arquivo muito grande

```bash
# Solução: Ajustar limite em api_implementation.py
# Linha: if file_size > 10 * 1024 * 1024:  # Aumentar valor
```

## 📞 Suporte

Para dúvidas sobre a implementação:
1. Verificar a documentação em `/docs`
2. Consultar `api_documentation.md`
3. Executar testes com `test_api_examples.sh`
4. Revisar logs da aplicação

## ✅ Checklist de Implementação

- [x] Documentação dos endpoints (Issue #114)
- [x] Exemplos de requisições válidas/inválidas
- [x] Detalhamento de parâmetros
- [x] Exemplos cURL/Postman (Issue #115)
- [x] Respostas JSON de sucesso e erro
- [x] Códigos de status HTTP
- [x] Implementação completa da API
- [x] Script de testes automatizados
- [x] Coleção Postman
- [x] Instruções de uso

## 🎉 Conclusão

A implementação está completa e pronta para uso. Todos os requisitos das issues #27_ref5_ref7_8_2h e #27b_ref5_ref7_8_1h foram atendidos com sucesso!
