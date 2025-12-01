# Script para rodar a API DQTimes
# Uso: .\run.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DQTimes API - Iniciando..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está no ambiente virtual
if ($env:VIRTUAL_ENV) {
    Write-Host "[OK] Ambiente virtual ativado" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Ambiente virtual NAO detectado" -ForegroundColor Yellow
    Write-Host "Tentando ativar..." -ForegroundColor Yellow
    & "..\venv\Scripts\activate.ps1"
}

Write-Host ""
Write-Host "Iniciando servidor na porta 8080..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Acesse:" -ForegroundColor Cyan
Write-Host "  - Documentacao: http://localhost:8080/docs" -ForegroundColor White
Write-Host "  - API: http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Rodar a aplicação
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080 --reload
