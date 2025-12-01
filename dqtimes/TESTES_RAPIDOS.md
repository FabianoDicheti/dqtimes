# ⚡ Testes Rápidos - API DQTimes

## 🔥 Cola de Comandos (PowerShell)

### Teste Completo Automatizado
```powershell
python test_quick.py
```

---

## 🎯 Testes Manuais (Copiar e Colar)

### 1️⃣ Health Check (sem autenticação)
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/health"
```

**Resultado esperado:**
```
status    : healthy
timestamp : 2025-12-01T03:00:00
version   : 2.0.0
uptime    : running
```

---

### 2️⃣ Login Completo
```powershell
# Fazer login
$body = @{username="admin"; password="Admin@123"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:8080/auth/login" -Method Post -Body $body -ContentType "application/json"

# Mostrar resultado
Write-Host "✓ Login OK!" -ForegroundColor Green
Write-Host "Token: $($response.access_token.Substring(0,50))..." -ForegroundColor Cyan
Write-Host "Usuário: $($response.username)" -ForegroundColor Cyan
Write-Host "Expira em: $($response.expires_in) segundos" -ForegroundColor Cyan

# Salvar token para próximos comandos
$token = $response.access_token
```

---

### 3️⃣ Fazer Previsão (requer token)
```powershell
# Preparar headers
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# Dados para previsão
$forecast = @{
    data = @(10.0, 12.0, 13.0, 15.0, 17.0, 20.0, 22.0, 25.0, 27.0, 30.0)
    n_projections = 5
    method = "auto"
    confidence_level = 0.95
} | ConvertTo-Json

# Fazer previsão
$result = Invoke-RestMethod -Uri "http://localhost:8080/forecast/single" -Method Post -Body $forecast -Headers $headers

# Mostrar resultado
Write-Host "✓ Previsão concluída!" -ForegroundColor Green
Write-Host "Método usado: $($result.method_used)" -ForegroundColor Cyan
Write-Host "Projeções: $($result.projections -join ', ')" -ForegroundColor Yellow
Write-Host "Tempo de execução: $($result.execution_time)s" -ForegroundColor Cyan
```

---

### 4️⃣ Teste Completo em Sequência (All-in-One)
```powershell
# 1. Health Check
Write-Host "`n[1/3] Health Check..." -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "http://localhost:8080/health"
Write-Host "✓ API está $($health.status)" -ForegroundColor Green

# 2. Login
Write-Host "`n[2/3] Login..." -ForegroundColor Yellow
$loginBody = @{username="admin"; password="Admin@123"} | ConvertTo-Json
$login = Invoke-RestMethod -Uri "http://localhost:8080/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
$token = $login.access_token
Write-Host "✓ Login realizado! Token obtido." -ForegroundColor Green

# 3. Forecast
Write-Host "`n[3/3] Fazendo previsão..." -ForegroundColor Yellow
$headers = @{Authorization="Bearer $token"; "Content-Type"="application/json"}
$forecastBody = @{
    data=@(10,12,13,15,17,20,22,25,27,30)
    n_projections=5
    method="auto"
} | ConvertTo-Json

$forecast = Invoke-RestMethod -Uri "http://localhost:8080/forecast/single" -Method Post -Body $forecastBody -Headers $headers
Write-Host "✓ Previsão concluída!" -ForegroundColor Green
Write-Host "`nProjeções: $($forecast.projections -join ', ')" -ForegroundColor Cyan
Write-Host "Probabilidade de aumento: $([math]::Round($forecast.probability_increase * 100, 2))%" -ForegroundColor Cyan

Write-Host "`n🎉 Todos os testes passaram!" -ForegroundColor Green
```

---

## 📊 Visualizar Dados Bonitos

### Ver resultado do forecast formatado
```powershell
$forecast.projections | ForEach-Object -Begin {$i=1} -Process {
    Write-Host "Projeção $i : $([math]::Round($_, 2))" -ForegroundColor Cyan
    $i++
}
```

### Ver intervalos de confiança
```powershell
$forecast.confidence_intervals | ForEach-Object -Begin {$i=1} -Process {
    $lower = [math]::Round($_.lower, 2)
    $upper = [math]::Round($_.upper, 2)
    Write-Host "Intervalo $i : [$lower - $upper]" -ForegroundColor Yellow
    $i++
}
```

### Ver métricas
```powershell
Write-Host "`nMétricas de Qualidade:" -ForegroundColor Cyan
$forecast.metrics.GetEnumerator() | ForEach-Object {
    Write-Host "  $($_.Key): $([math]::Round($_.Value, 4))" -ForegroundColor White
}
```

---

## 🐛 Troubleshooting

### Erro: "Connection refused"
```powershell
# Verificar se a API está rodando
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
```

**Solução:** Rodar a API primeiro
```powershell
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080 --reload
```

---

### Erro: "Token inválido"
```powershell
# Fazer login novamente
$body = @{username="admin"; password="Admin@123"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:8080/auth/login" -Method Post -Body $body -ContentType "application/json"
$token = $response.access_token
```

---

### Erro: 404 Not Found
Verifique se está usando os endpoints corretos:
- ✅ `/auth/login` (correto)
- ❌ `/login` (errado)
- ✅ `/forecast/single` (correto)
- ❌ `/forecast` (errado)

---

## 📝 Resumo dos Endpoints

| Endpoint | Método | Autenticação | Descrição |
|----------|--------|--------------|-----------|
| `/health` | GET | ❌ Não | Status da API |
| `/auth/login` | POST | ❌ Não | Login |
| `/auth/logout` | POST | ✅ Sim | Logout |
| `/auth/refresh` | POST | ✅ Sim | Renovar token |
| `/forecast/single` | POST | ✅ Sim | Fazer previsão |
| `/upload/csv` | POST | ✅ Sim | Upload CSV |
| `/upload/json` | POST | ✅ Sim | Upload JSON |
| `/history` | GET | ✅ Sim | Ver histórico |
| `/docs` | GET | ❌ Não | Documentação |

---

## 🎯 Exemplos de Dados para Teste

### Série crescente
```powershell
@(10, 12, 15, 18, 22, 26, 31, 36, 42, 48)
```

### Série com sazonalidade
```powershell
@(100, 120, 80, 110, 130, 90, 115, 135, 95, 120)
```

### Série decrescente
```powershell
@(100, 95, 89, 85, 80, 76, 72, 68, 65, 62)
```

### Série estável
```powershell
@(50, 51, 49, 50, 52, 49, 51, 50, 48, 51)
```

---

**🚀 Pronto para testar!**

Execute:
```powershell
python test_quick.py
```

Ou use os comandos manuais acima! ⚡
