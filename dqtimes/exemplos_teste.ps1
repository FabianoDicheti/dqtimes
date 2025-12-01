# Exemplos de Testes da API DQTimes usando PowerShell
# Execute cada bloco separadamente

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Exemplos de Teste - API DQTimes" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Configuração
$baseUrl = "http://localhost:8080"

# ============================================
# 1. TESTE DE HEALTH CHECK
# ============================================
Write-Host "`n[1] Testando Health Check..." -ForegroundColor Yellow

$response = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get
Write-Host "Resposta:" -ForegroundColor Green
$response | ConvertTo-Json -Depth 10

# ============================================
# 2. LOGIN (obter token)
# ============================================
Write-Host "`n[2] Fazendo Login..." -ForegroundColor Yellow

$loginBody = @{
    username = "admin"
    password = "Admin@123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
Write-Host "Login realizado com sucesso!" -ForegroundColor Green
Write-Host "Token: $($loginResponse.access_token.Substring(0,50))..." -ForegroundColor Cyan

# Salvar token para próximos testes
$token = $loginResponse.access_token
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# ============================================
# 3. FAZER UMA PREVISÃO
# ============================================
Write-Host "`n[3] Fazendo Previsão..." -ForegroundColor Yellow

$forecastBody = @{
    data = @(10.0, 12.0, 13.0, 15.0, 17.0, 20.0, 22.0, 25.0, 27.0, 30.0)
    n_projections = 5
    method = "auto"
} | ConvertTo-Json

try {
    $forecastResponse = Invoke-RestMethod -Uri "$baseUrl/forecast/single" -Method Post -Body $forecastBody -Headers $headers
    Write-Host "Previsão realizada!" -ForegroundColor Green
    Write-Host "Projeções:" -ForegroundColor Cyan
    $forecastResponse.projections
    Write-Host "`nMétodo usado: $($forecastResponse.method_used)" -ForegroundColor Cyan
} catch {
    Write-Host "Erro na previsão: $_" -ForegroundColor Red
}

# ============================================
# 4. VERIFICAR MÉTRICAS
# ============================================
Write-Host "`n[4] Verificando Métricas..." -ForegroundColor Yellow

try {
    $metricsResponse = Invoke-RestMethod -Uri "$baseUrl/metrics" -Method Get -Headers $headers
    Write-Host "Métricas obtidas:" -ForegroundColor Green
    $metricsResponse | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Endpoint de métricas não disponível ou requer autenticação" -ForegroundColor Yellow
}

# ============================================
# 5. LISTAR ENDPOINTS DISPONÍVEIS
# ============================================
Write-Host "`n[5] Endpoints Disponíveis:" -ForegroundColor Yellow
Write-Host "  - GET  $baseUrl/health" -ForegroundColor White
Write-Host "  - POST $baseUrl/login" -ForegroundColor White
Write-Host "  - POST $baseUrl/forecast" -ForegroundColor White
Write-Host "  - POST $baseUrl/upload" -ForegroundColor White
Write-Host "  - GET  $baseUrl/docs (Documentação Interativa)" -ForegroundColor White
Write-Host "  - GET  $baseUrl/redoc (Documentação ReDoc)" -ForegroundColor White

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  Testes Concluídos!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# ============================================
# EXEMPLO DE USO COM ARQUIVO CSV
# ============================================
Write-Host "`n[EXTRA] Para upload de arquivo CSV:" -ForegroundColor Yellow
Write-Host @"
`$csvContent = @"
date,value
2024-01-01,100
2024-01-02,105
2024-01-03,110
`"@

`$csvContent | Out-File -FilePath "data.csv" -Encoding UTF8

`$multipartContent = [System.Net.Http.MultipartFormDataContent]::new()
`$fileStream = [System.IO.File]::OpenRead("data.csv")
`$fileContent = [System.Net.Http.StreamContent]::new(`$fileStream)
`$multipartContent.Add(`$fileContent, "file", "data.csv")

`$uploadResponse = Invoke-RestMethod -Uri "`$baseUrl/upload" -Method Post -Body `$multipartContent -Headers @{
    "Authorization" = "Bearer `$token"
}
"@ -ForegroundColor Gray
