# Tutorial: Como Rodar a API DQTimes

## O que você já fez (correto!)

1. Criou o ambiente virtual
2. Instalou as dependências

## Passo a Passo Completo

### 1. Ativar o Ambiente Virtual

```powershell
.\venv\Scripts\activate
```

**Você verá** `(venv)` no início da linha do terminal.

---

### 2. Navegar para o diretório correto

```powershell
cd dqtimes
```

---

### 3. Rodar a aplicação com porta diferente

O erro aconteceu porque a porta 8000 já está em uso. Existem 3 formas de resolver:

#### **OPÇÃO A - Usar porta 8080 (Recomendado)**

```powershell
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080 --reload
```

#### **OPÇÃO B - Usar porta 8001**

```powershell
uvicorn app.api_v2:app --host 0.0.0.0 --port 8001 --reload
```

#### **OPÇÃO C - Encontrar e matar o processo na porta 8000**

```powershell
# Encontrar o processo
netstat -ano | findstr :8000

# Matar o processo (substitua PID pelo número que apareceu)
taskkill /PID <número_do_processo> /F

# Depois rodar normalmente
uvicorn app.api_v2:app --reload
```

---

### 4. Acessar a API

Depois que a aplicação iniciar, você verá algo assim:

```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Abra o navegador em:**

- **Documentação Interativa (Swagger):** http://localhost:8080/docs
- **Documentação Alternativa (ReDoc):** http://localhost:8080/redoc
- **API Base:** http://localhost:8080

---

## Comandos Úteis

### Rodar sem reload (mais estável)

```powershell
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080
```

### Rodar em modo de produção com múltiplos workers

```powershell
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080 --workers 4
```

### Parar o servidor

Pressione `CTRL + C` no terminal

---

## Testando a API

### 1. Teste de Health Check

Abra outro PowerShell e execute:

```powershell
curl http://localhost:8080/health
```

### 2. Fazer Login (obter token)

```powershell
curl -X POST "http://localhost:8080/login" -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"Admin@123\"}"
```

### 3. Fazer uma previsão

Primeiro obtenha o token, depois:

```powershell
curl -X POST "http://localhost:8080/forecast" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI" ^
  -H "Content-Type: application/json" ^
  -d "{\"data\":[10,12,13,15,17,20,22,25,27,30],\"n_projections\":5,\"method\":\"auto\"}"
```

---

## Troubleshooting (Resolução de Problemas)

### Erro: Porta em uso

```
ERROR: [WinError 10013] Foi feita uma tentativa de acesso a um soquete...
```

**Solução:** Use uma porta diferente (8080, 8001, 3000, etc.)

### Erro: Módulo não encontrado

```
ModuleNotFoundError: No module named 'aplicacao'
```

**Solução:** Certifique-se de estar no diretório `dqtimes`:

```powershell
cd C:\Users\acer\Desktop\commitsbostafabianica\dqtimes
```

### Erro: CUDA not found

Isso é apenas um WARNING, não um erro. A aplicação funcionará normalmente usando CPU.

### Warnings do Pydantic

Os warnings sobre `@validator` são apenas deprecation warnings. A aplicação funciona normalmente.

---

## Estrutura do Projeto

```
commitsbostafabianica/
├── venv/                    # Ambiente virtual
├── dqtimes/
│   ├── .env                 # Configurações (criado)
│   ├── .env.example         # Exemplo de configurações
│   ├── requirements.txt     # Dependências
│   └── app/
│       ├── api_v2.py       # API principal
│       ├── aplicacao.py    # Lógica de forecast
│       └── ...
└── TUTORIAL_COMO_RODAR.md   # Este arquivo
```

---

## Resumo Rápido

**TL;DR - Comandos para rodar:**

```powershell
# 1. Ativar venv
.\venv\Scripts\activate

# 2. Ir para o diretório
cd dqtimes

# 3. Rodar a API
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080 --reload

# 4. Abrir no navegador
# http://localhost:8080/docs
```

---

## Próximos Passos

1. Explore a documentação em `/docs`
2. Teste os endpoints interativamente
3. Leia a documentação da API
4. Configure as variáveis de ambiente conforme necessário
5. Integre com seu frontend/aplicação

---

**Pronto! Sua API está rodando! 🚀**
