# 📘 Troubleshooting – Plataforma de Previsão de Séries Temporais

Esta documentação reúne os principais procedimentos de diagnóstico para o backend da plataforma de previsão, incluindo análise de logs, rastreio via request-id, investigação de problemas de desempenho, erros de upload, falhas nas bibliotecas CUDA/C++, e problemas com o processamento distribuído via Dask.

Escopo: Serviços FastAPI, Dask, Workers e bibliotecas nativas (.so)

## 🧩 1. Componentes Envolvidos no Diagnóstico

### Antes de iniciar o troubleshooting, identifique qual componente pode estar envolvido:

|Componente | Função |
| --------- | :---------: |
|FastAPI | Processamento das requisições REST e orquestração |
|Middleware de logging | Geração de logs de acesso/erro com request-id |
|Dask / LocalCluster | Processamento distribuído de dataframes |
|Bibliotecas nativas (.so) | Execução acelerada em C/CUDA |
|Lógica de projeção | forecast_temp / médias móveis / Holt-Winters |
|Upload de arquivos | CSV, listas, paginação, limpeza temporária |

## 🕵️ 2. Como usar o Request-ID para rastrear requisições

### Cada requisição recebe automaticamente um request-id (UUID), incluído em:

* Log de acesso
* Log de erro
* response.headers["X-Request-ID"]
* request.state.request_id

### 🔍 Exemplo de log
```
2025-11-29 15:41:01 | INFO | 7f404c32-3ff8-4b14-8acd | ACESSO | Rota=/projecao_lista/ | Status=200 | Latência=12.40ms
```

## 📌 Como usar no diagnóstico

1. Pegue o valor do header X-Request-ID da requisição problemática.
2. Busque esse ID nos arquivos:

```
logs/access.log
logs/error.log
```

Você verá:
* rota
* status
* tempo total
* exceção (se existir)

## 📁 3. Onde encontrar os logs

Os logs ficam em:

```
/logs/access.log
/logs/error.log
```

### 🔄 Rotação automática

* Rotação diária
* Mantém 7 dias
* Arquivos antigos são renomeados automaticamente (ex.: access.log.2025-11-28)

## 🧪 4. Checklists de Diagnóstico por Sintoma

A seguir estão checklists práticos para os cenários mais comuns.

### 🚫 4.1. A API está retornando erro 500
 ✔ **Passo a passo**

1. Capture o request-id do header.
2. Busque esse ID no arquivo error.log.
3. Verifique o traceback completo registrado automaticamente.

**Principais causas prováveis**

* Dados inválidos (JSON mal formatado)
* Períodos de projeção mal especificados
* Biblioteca nativa (.so) ausente ou não carregada
* Problemas com Dask (morte de worker)
* Falha ao processar CSV

🔧 **Como validar bibliotecas nativas**
No terminal, dentro do container:
```
ldd app/libs/medias_moveis.so
```

Se aparecer "not found", instalar dependências ausentes.

### 📉 4.2. Lentidão ou alta latência nas rotas
✔ **Checklist**

* Verifique a latência nos logs de acesso
* Avalie se houve upload de CSV grande
* Veja se o cluster Dask iniciou corretamente:
```
Dask Dashboard is available at http://127.0.0.1:8787
```

**Possíveis causas**
* CSV com milhões de linhas
*Falta de memória ao fazer .compute()
* Paginação com page_size muito grande
* Código nativo lento

📊 **Ações recomendadas**
* Reduzir page_size
* Aumentar limite de memória
* Validar uso de CPU/GPU

### 🗂 4.3. Paginação retornando "Page number out of range"
✔ **Diagnóstico**

O total de linhas é obtido por:
```
total_rows = len(ddf)
```

O len(ddf) só funciona corretamente se:
* O CSV possui índice único
* Não há particionamento inconsistente

🛠 **Soluções**

* Validar se o CSV possui header consistente
* Verificar se index_col=True está correto
* Testar paginação com:
```
page=1&page_size=20
```

### 🧾 4.4. Upload de CSV falha ou retorna erro 422
✔ **Verifique:**
* Se o arquivo é realmente CSV
* Se o frontend está enviando multipart/form-data
* Se o parâmetro header está coerente (true/false)
* Se o CSV usa separador de vírgula

🔧 **Teste direto via curl**
```
curl -X POST http://localhost:8000/projecao_dataframe/ \
  -F "csv_dataframe=@dados.csv" \
  -F "header=true" \
  -F "index_col=false" \
  -F "quantidade_projecoes=5"
```

### 📉 4.5. Algoritmo de previsão retornando valores estranhos
✔ **Diagnóstico**
Verifique se a lista contém:
* NaN
* strings
* None
* valores negativos quando não deveriam
* n_projecoes > tamanho da série

🔬 **Validar execução das libs nativas**
Erros comuns no log:
```
OSError: cannot load shared object file
```

### ⚠️ 4.6. Erros relacionados ao Dask
✔ **Sinais de falha**
* API retorna rapidamente “erro interno”
* Log mostra:
```
distributed.worker - WARNING - Compute Failed
```
✔ **Soluções**
* Reiniciar o cluster:
```
cluster = LocalCluster()
client = Client(cluster)
```
* Reduzir quantidade de threads:
```
LocalCluster(threads_per_worker=1)
```
* Aumentar memória do container

## 🛠 5. Troubleshooting avançado
### 🧩 5.1. Debug das bibliotecas .so
```
nm -D app/libs/medias_moveis.so
```

Se não listar as funções → erro de compilação.

### 🔧 5.2. Validação da assinatura das funções ctypes

Verificar:
* argtypes correspondem exatamente ao esperado
* restype está correto

Erros típicos:
* Segfault silencioso → ponteiros incompatíveis
* Retornos vazios → restype incorreto

### 🔍 5.3. Ativar logs DEBUG
logging_config.py:
```
logger.setLevel(logging.DEBUG)
```

FastAPI:
```
uvicorn main:app --reload --log-level debug
```
## 📑 6. Checklist de Saúde da Aplicação
🔵 **FastAPI**
* Endpoints respondendo (/docs)
* Logs sendo gerados
* Request-id presente

🔵 **Dask**
* Dashboard acessível
* Workers ativos
* Sem warnings de memória

🔵 **Bibliotecas C/CUDA**
* Arquivos .so presentes
* ldd sem “not found”
* Modelos retornando valores coerentes

🔵 **Logging**
* access.log e error.log atualizados
* Rotação funcionando
* Pasta logs/ com permissão de escrita

## 📚 7. Recursos adicionais
* Documentação FastAPI Middleware
* Guia oficial do Dask Distributed
* Referência ctypes / carregamento dinâmico
* Python logging — TimedRotatingFileHandler