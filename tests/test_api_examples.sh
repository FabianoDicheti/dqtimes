# test_api_examples.sh
#!/bin/bash

# ========================================
# Script de Testes e Exemplos da API DQTimes
# Issues: #27_ref5_ref7_8_2h e #27b_ref5_ref7_8_1h
# ========================================

# Configuração
BASE_URL="http://localhost:8000"
TOKEN=""
REFRESH_TOKEN=""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir cabeçalho
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Função para imprimir sucesso
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Função para imprimir erro
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Função para fazer pretty print JSON
pretty_json() {
    python3 -m json.tool
}

# ========================================
# TESTES DOS ENDPOINTS
# ========================================

print_header "INICIANDO TESTES DA API DQTIMES"

# -------------------------------
# 1. TESTE DE LOGIN
# -------------------------------
print_header "1. TESTE DE LOGIN"

echo "1.1. Login com credenciais válidas:"
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123"
  }')

echo "$RESPONSE" | pretty_json
TOKEN=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

if [ ! -z "$TOKEN" ]; then
    print_success "Login realizado com sucesso! Token obtido."
else
    print_error "Falha no login!"
    exit 1
fi

echo -e "\n1.2. Login com credenciais inválidas (deve falhar):"
curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_invalido",
    "password": "senha123"
  }' | pretty_json

echo -e "\n1.3. Login com validação de parâmetros (deve falhar):"
curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ab",
    "password": "123"
  }' | pretty_json

# -------------------------------
# 2. TESTE DE UPLOAD
# -------------------------------
print_header "2. TESTE DE UPLOAD"

echo "2.1. Upload de JSON válido:"
curl -s -X POST "$BASE_URL/upload/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'data=[100, 110, 120, 130, 140, 150, 160, 170, 180, 190]&metadata={"source": "teste", "period": "daily"}' | pretty_json

echo -e "\n2.2. Upload de JSON com dados insuficientes (deve falhar):"
curl -s -X POST "$BASE_URL/upload/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'data=[100, 110]' | pretty_json

echo -e "\n2.3. Upload sem autenticação (deve falhar):"
curl -s -X POST "$BASE_URL/upload/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'data=[100, 110, 120, 130, 140, 150, 160, 170, 180, 190]' | pretty_json

# Criar arquivo CSV de teste
echo "2.4. Criando arquivo CSV de teste:"
cat > /tmp/test_data.csv << EOF
month,sales,forecast
Jan,100,105
Feb,110,115
Mar,120,125
Apr,130,135
May,140,145
Jun,150,155
Jul,160,165
Aug,170,175
Sep,180,185
Oct,190,195
EOF

echo "2.5. Upload de arquivo CSV:"
curl -s -X POST "$BASE_URL/upload/csv" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test_data.csv" \
  -F "description=Dados de vendas mensais 2024" | pretty_json

# -------------------------------
# 3. TESTE DE PREVISÃO
# -------------------------------
print_header "3. TESTE DE PREVISÃO"

echo "3.1. Previsão com dados válidos:"
curl -s -X POST "$BASE_URL/forecast/single" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 110, 120, 115, 125, 130, 135, 140, 145, 150],
    "n_projections": 5,
    "method": "auto",
    "confidence_level": 0.95
  }' | pretty_json

echo -e "\n3.2. Previsão com dados insuficientes (deve falhar):"
curl -s -X POST "$BASE_URL/forecast/single" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 110, 120],
    "n_projections": 3
  }' | pretty_json

echo -e "\n3.3. Previsão com parâmetros inválidos (deve falhar):"
curl -s -X POST "$BASE_URL/forecast/single" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 110, 120, 115, 125, 130, 135, 140, 145, 150],
    "n_projections": 500,
    "confidence_level": 1.5
  }' | pretty_json

# Criar arquivo CSV para batch
echo -e "\n3.4. Criando arquivo CSV para previsão em lote:"
cat > /tmp/batch_data.csv << EOF
series1,series2,series3
100,200,150
110,210,160
120,220,170
130,215,165
140,225,175
150,235,185
160,245,195
170,250,200
180,260,210
190,270,220
EOF

echo "3.5. Previsão em lote:"
curl -s -X POST "$BASE_URL/forecast/batch" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/batch_data.csv" \
  -F "n_projections=3" \
  -F "parallel_processing=true" | pretty_json

# -------------------------------
# 4. TESTE DE HISTÓRICO
# -------------------------------
print_header "4. TESTE DE HISTÓRICO"

echo "4.1. Listar histórico com paginação:"
curl -s -X GET "$BASE_URL/history?page=1&page_size=5" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

echo -e "\n4.2. Histórico com filtro por tipo de operação:"
curl -s -X GET "$BASE_URL/history?operation_type=forecast&page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

echo -e "\n4.3. Histórico com filtro de data:"
START_DATE="2024-11-01T00:00:00"
END_DATE="2024-11-30T23:59:59"
curl -s -X GET "$BASE_URL/history?start_date=$START_DATE&end_date=$END_DATE" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

echo -e "\n4.4. Paginação inválida (deve falhar):"
curl -s -X GET "$BASE_URL/history?page=0&page_size=200" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

echo -e "\n4.5. Buscar operação específica (pegando o primeiro ID do histórico):"
OPERATION_ID=$(curl -s -X GET "$BASE_URL/history?page=1&page_size=1" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['items'][0]['id']) if data.get('items') else print('none')")

if [ "$OPERATION_ID" != "none" ] && [ ! -z "$OPERATION_ID" ]; then
    echo "Buscando detalhes da operação: $OPERATION_ID"
    curl -s -X GET "$BASE_URL/history/$OPERATION_ID" \
      -H "Authorization: Bearer $TOKEN" | pretty_json
else
    echo "Nenhuma operação encontrada no histórico"
fi

# -------------------------------
# 5. TESTE DE REFRESH TOKEN
# -------------------------------
print_header "5. TESTE DE REFRESH TOKEN"

echo "5.1. Renovar token de acesso:"
curl -s -X POST "$BASE_URL/auth/refresh" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "refresh_token=dummy_refresh_token" | pretty_json

# -------------------------------
# 6. TESTE DE LOGOUT
# -------------------------------
print_header "6. TESTE DE LOGOUT"

echo "6.1. Realizar logout:"
curl -s -X POST "$BASE_URL/auth/logout" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

echo -e "\n6.2. Tentar acessar endpoint após logout (deve falhar):"
curl -s -X GET "$BASE_URL/history" \
  -H "Authorization: Bearer $TOKEN" | pretty_json

# -------------------------------
# 7. TESTE DE HEALTH CHECK
# -------------------------------
print_header "7. TESTE DE HEALTH CHECK"

echo "7.1. Verificar status da API:"
curl -s -X GET "$BASE_URL/health" | pretty_json

# -------------------------------
# 8. TESTE DO ENDPOINT ROOT
# -------------------------------
print_header "8. TESTE DO ENDPOINT ROOT"

echo "8.1. Informações da API:"
curl -s -X GET "$BASE_URL/" | pretty_json

# -------------------------------
# LIMPEZA
# -------------------------------
print_header "LIMPEZA"

rm -f /tmp/test_data.csv
rm -f /tmp/batch_data.csv
print_success "Arquivos temporários removidos"

# -------------------------------
# RESUMO
# -------------------------------
print_header "RESUMO DOS TESTES"

echo "Testes executados:"
echo "✓ Login e autenticação"
echo "✓ Upload de dados (JSON e CSV)"
echo "✓ Previsões (simples e em lote)"
echo "✓ Histórico de operações"
echo "✓ Refresh token"
echo "✓ Logout"
echo "✓ Health check"
echo "✓ Endpoint root"

print_success "Testes concluídos!"

echo -e "\n${YELLOW}Documentação disponível em:${NC}"
echo "- Swagger UI: $BASE_URL/docs"
echo "- ReDoc: $BASE_URL/redoc"
