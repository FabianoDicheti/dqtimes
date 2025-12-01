# 🚀 DQTimes API - Guia Rápido

## Como Rodar (3 passos)

### 1️⃣ Ativar o ambiente virtual

```powershell
.\venv\Scripts\activate
```

### 2️⃣ Ir para o diretório dqtimes

```powershell
cd dqtimes
```

### 3️⃣ Escolha UMA das opções:

**OPÇÃO A - Usar script automático (Mais fácil):**

```powershell
.\run.bat
```

**OPÇÃO B - Comando manual:**

```powershell
uvicorn app.api_v2:app --host 0.0.0.0 --port 8080 --reload
```

---

## 🌐 Acessar a API

Depois que iniciar, abra no navegador:

- **Documentação Interativa:** http://localhost:8080/docs
- **API:** http://localhost:8080

### 🔑 Endpoints Principais:

- `POST /auth/login` - Login (admin / Admin@123)
- `POST /forecast/single` - Fazer previsão
- `GET /health` - Status da API
- `GET /docs` - Documentação completa

Ver todos: `dqtimes/ENDPOINTS.md`

---

## 🧪 Testar a API

Em outro terminal (com venv ativado):

```powershell
cd dqtimes
python test_quick.py
```

---

## ❓ Problemas??

### Erro: Porta em uso

Se der erro de porta, use outra porta:

```powershell
uvicorn app.api_v2:app --host 0.0.0.0 --port 8081 --reload
```

### Erro: Módulo não encontrado

Certifique-se de estar no diretório correto:

```powershell
cd C:\Users\acer\Desktop\commitsbostafabianica\dqtimes
```

---

## 📖 Documentação Completa

Leia o arquivo: `TUTORIAL_COMO_RODAR.md`

---

## 🛑 Parar o Servidor

Pressione `CTRL + C` no terminal

---

**Pronto! É só isso! 🎉**
