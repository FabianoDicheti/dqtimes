@echo off
REM Script para rodar a API DQTimes (Windows CMD)

echo ========================================
echo   DQTimes API - Iniciando...
echo ========================================
echo.

REM Ativar ambiente virtual
call ..\venv\Scripts\activate.bat

echo.
echo Iniciando servidor na porta 8080...
echo.
echo Acesse:
echo   - Documentacao: http://localhost:8080/docs
echo   - API: http://localhost:8080
echo.
echo Pressione CTRL+C para parar o servidor
echo.

REM Rodar a aplicação
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080 --reload
