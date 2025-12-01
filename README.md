# 🚀 DQTimes - Sistema de Projeção de Séries Temporais

API moderna para análise e previsão de séries temporais utilizando métodos estatísticos avançados e aceleração CUDA.

## 📋 Sobre o Projeto

DQTimes é um sistema de projeção de séries temporais que combina:
- 🔮 Algoritmos de previsão (Moving Average, Holt-Winters)
- ⚡ Aceleração CUDA para processamento de alto desempenho
- 🔐 Autenticação JWT
- 📊 API REST moderna com FastAPI
- 📈 Análise estatística completa

## 🆕 Nova API v2

A API v2 foi desenvolvida para atender as issues **#114** e **#115**:
- ✅ **Issue #114**: Documentação completa de endpoints
- ✅ **Issue #115**: Exemplos práticos e ferramentas de teste

### Principais Recursos

- **Autenticação JWT**: Sistema seguro de tokens
- **Upload de Dados**: Suporte para CSV e JSON
- **Previsões Avançadas**: Single e batch processing
- **Histórico de Operações**: Rastreamento completo
- **Documentação Automática**: Swagger/ReDoc integrados
- **Validação de Dados**: Pydantic models
- **Fallback Python**: Funciona sem CUDA

## 🛠️ Instalação

### Pré-requisitos

- Python 3.8+
- PostgreSQL (opcional, para produção)
- CUDA toolkit (opcional, para aceleração GPU)

### 1. Clonar o Repositório

```bash
git clone <seu-repositorio>
cd dqtimes/dqtimes
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## 🚀 Executando a API

### Método 1: Python Direto

```bash
python app/api_v2.py
```

### Método 2: Uvicorn

```bash
uvicorn app.api_v2:app --reload --host 0.0.0.0 --port 8000
```

### Método 3: Docker (Recomendado)

```bash
docker build -t dqtimes-api .
docker run -p 8000:8000 dqtimes-api
```

## 📚 Documentação

Após iniciar a API, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Documentação Completa**: [docs/api_documentation.md](docs/api_documentation.md)
- **Guia de Implementação**: [docs/README_IMPLEMENTATION.md](docs/README_IMPLEMENTATION.md)

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

## 📊 Exemplos de Uso

### 1. Autenticação

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123"
  }'
```

### 2. Fazer Previsão

```bash
TOKEN="seu_token_aqui"

curl -X POST "http://localhost:8000/forecast/single" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
    "n_projections": 5,
    "method": "auto",
    "confidence_level": 0.95
  }'
```

### 3. Upload de Dados CSV

```bash
curl -X POST "http://localhost:8000/upload/csv" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@dados.csv" \
  -F "description=Dados de vendas 2024"
```

### 4. Consultar Histórico

```bash
curl -X GET "http://localhost:8000/history?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN"
```

## 🧪 Testes

### Script de Testes Bash

```bash
chmod +x tests/test_api_examples.sh
./tests/test_api_examples.sh
```

### Postman Collection

1. Importe `postman_collection.json` no Postman
2. Configure a variável `base_url` (padrão: http://localhost:8000)
3. Execute a coleção

## 🏗️ Estrutura do Projeto

```
dqtimes/
├── app/
│   ├── api_v2.py              # Nova API com autenticação
│   ├── aplicacao.py           # Lógica de previsão (CUDA/Python)
│   ├── main.py                # API antiga (compatibilidade)
│   ├── libs/                  # Bibliotecas CUDA compiladas
│   └── ...
├── docs/                      # Documentação completa
│   ├── api_documentation.md
│   └── README_IMPLEMENTATION.md
├── tests/                     # Scripts de teste
│   └── test_api_examples.sh
├── requirements.txt           # Dependências Python
├── .env.example               # Template de configuração
├── Dockerfile                 # Containerização
└── postman_collection.json    # Coleção Postman

```

## 🔧 Endpoints Disponíveis

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

## ⚙️ Configuração

As principais configurações estão no arquivo `.env`:

```bash
# API
API_HOST=0.0.0.0
API_PORT=8000

# JWT
JWT_SECRET_KEY=sua_chave_secreta
JWT_EXPIRATION_MINUTES=60

# Processamento
USE_CUDA=auto  # auto, true, false
PARALLEL_PROCESSING=true

# Limites
MAX_FILE_SIZE_MB=10
MAX_PROJECTIONS=365
```

## 🐳 Docker

### Build

```bash
docker build -t dqtimes-api .
```

### Run

```bash
docker run -d \
  -p 8000:8000 \
  -e JWT_SECRET_KEY=sua_chave_secreta \
  --name dqtimes \
  dqtimes-api
```

### Docker Compose

```bash
docker-compose up -d
```

## 🔒 Segurança

- ✅ Autenticação JWT com expiração
- ✅ Validação de dados com Pydantic
- ✅ Limitação de tamanho de arquivos
- ✅ Rate limiting (configurável)
- ✅ Logs de auditoria
- ✅ CORS configurável

## 📈 Métricas

A API retorna métricas detalhadas:

- **MSE**: Mean Squared Error
- **RMSE**: Root Mean Squared Error
- **MAPE**: Mean Absolute Percentage Error
- **R²**: Coeficiente de determinação
- **Execution Time**: Tempo de processamento
- **Probability Increase**: Probabilidade de aumento

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

[Adicione sua licença aqui]

## 👥 Equipe

- **Desenvolvido por**: Claude (Anthropic)
- **Issues**: #114, #115
- **Data**: 2024-11-30

## 🔗 Links Úteis

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [JWT.io](https://jwt.io/)
- [Postman](https://www.postman.com/)

## 🆘 Suporte

Para problemas e dúvidas:

1. Consulte a [documentação completa](docs/api_documentation.md)
2. Verifique as [issues do GitHub](../../issues)
3. Execute os testes: `./tests/test_api_examples.sh`

## 📋 Changelog

### v2.0.0 (2024-11-30)
- ✨ Nova API com autenticação JWT
- ✨ Upload de CSV e JSON
- ✨ Previsões single e batch
- ✨ Histórico de operações
- ✨ Documentação completa (Issues #114 e #115)
- ✨ Fallback Python para ambientes sem CUDA
- ✨ Coleção Postman
- ✨ Scripts de teste automatizados

### v1.0.0
- 🎉 Versão inicial com endpoints básicos
- ⚡ Suporte a CUDA
- 📊 Algoritmos de previsão

---

**Nota**: Para ver a documentação original do projeto, consulte [README_ORIGINAL.md](README_ORIGINAL.md)
