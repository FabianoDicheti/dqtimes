# 📋 Endpoints da API DQTimes

## URL Base
```
http://localhost:8080
```

---

## 🔐 Autenticação

### Login
```http
POST /auth/login
```

**Body:**
```json
{
  "username": "admin",
  "password": "Admin@123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_id": "user-001",
  "username": "admin",
  "roles": ["admin", "analyst"]
}
```

### Logout
```http
POST /auth/logout
Headers: Authorization: Bearer {token}
```

### Renovar Token
```http
POST /auth/refresh
Headers: Authorization: Bearer {token}
```

---

## 📊 Upload de Dados

### Upload CSV
```http
POST /upload/csv
Headers: Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Form Data:**
```
file: arquivo.csv
```

### Upload JSON
```http
POST /upload/json
Headers: Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "data": [10, 12, 15, 18, 20, 22, 25, 28, 30, 33],
  "metadata": {
    "name": "Vendas Mensais",
    "frequency": "monthly"
  }
}
```

---

## 🔮 Previsões

### Fazer Previsão
```http
POST /forecast/single
Headers: Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "data": [10.0, 12.0, 13.0, 15.0, 17.0, 20.0, 22.0, 25.0, 27.0, 30.0],
  "n_projections": 5,
  "method": "auto",
  "confidence_level": 0.95
}
```

**Resposta:**
```json
{
  "projections": [32.5, 35.2, 37.8, 40.1, 42.6],
  "confidence_intervals": [
    {"lower": 30.1, "upper": 34.9},
    {"lower": 32.5, "upper": 37.9}
  ],
  "method_used": "arima",
  "metrics": {
    "mae": 1.2,
    "rmse": 1.5,
    "mape": 4.2
  },
  "probability_increase": 0.87,
  "execution_time": 0.234
}
```

### Métodos Disponíveis:
- `auto` - Seleção automática do melhor método
- `arima` - ARIMA
- `exponential_smoothing` - Suavização Exponencial
- `prophet` - Prophet (Facebook)
- `linear_regression` - Regressão Linear

---

## 📜 Histórico

### Listar Histórico
```http
GET /history?page=1&page_size=10
Headers: Authorization: Bearer {token}
```

**Parâmetros:**
- `page` (opcional): Número da página (padrão: 1)
- `page_size` (opcional): Itens por página (padrão: 10)

**Resposta:**
```json
{
  "total_items": 45,
  "page": 1,
  "page_size": 10,
  "total_pages": 5,
  "items": [
    {
      "id": "op-a1b2c3d4",
      "operation_type": "forecast",
      "timestamp": "2025-12-01T03:00:00",
      "user_id": "user-001",
      "parameters": {...},
      "result_summary": {...},
      "status": "completed"
    }
  ]
}
```

---

## ℹ️ Informações

### Health Check
```http
GET /health
```

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-01T03:00:00",
  "version": "2.0.0",
  "uptime": "running"
}
```

### Documentação Interativa
```
GET /docs
```

### Documentação ReDoc
```
GET /redoc
```

---

## 👤 Usuários de Teste

### Admin
```
Username: admin
Password: Admin@123
Roles: admin, analyst
```

### Testuser
```
Username: testuser
Password: Test@123
Roles: analyst
```

---

## ⚠️ Códigos de Erro

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 204 | Sucesso sem conteúdo |
| 400 | Requisição inválida |
| 401 | Não autenticado |
| 403 | Sem permissão |
| 404 | Não encontrado |
| 422 | Erro de validação |
| 429 | Muitas requisições |
| 500 | Erro interno |

---

## 📝 Exemplo Completo (PowerShell)

```powershell
# 1. Login
$login = @{
    username = "admin"
    password = "Admin@123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8080/auth/login" -Method Post -Body $login -ContentType "application/json"
$token = $response.access_token

# 2. Fazer previsão
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$forecast = @{
    data = @(10, 12, 15, 18, 20, 22, 25, 28, 30, 33)
    n_projections = 5
    method = "auto"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8080/forecast/single" -Method Post -Body $forecast -Headers $headers

Write-Host "Projeções: $($result.projections)"
```

---

## 📝 Exemplo Completo (cURL)

```bash
# 1. Login
curl -X POST "http://localhost:8080/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin@123"}'

# 2. Fazer previsão (substitua SEU_TOKEN)
curl -X POST "http://localhost:8080/forecast/single" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [10, 12, 15, 18, 20, 22, 25, 28, 30, 33],
    "n_projections": 5,
    "method": "auto"
  }'
```

---

**🚀 Acesse `/docs` para testar interativamente!**
