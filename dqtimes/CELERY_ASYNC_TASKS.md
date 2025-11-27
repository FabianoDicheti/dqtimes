# Celery Async Tasks - DQTimes

## Endpoints

### POST /tasks/forecast
Enfileira task de previsão

```bash
curl -X POST "http://localhost:8000/tasks/forecast" \
  -H "Content-Type: application/json" \
  -d '{"lista_historico": [10, 15, 20, 25, 30], "quantidade_projecoes": 3}'
```

Resposta:
```json
{
  "task_id": "abc-123-xyz",
  "status": "pending"
}
```

### POST /tasks/dummy
Task dummy para validação

```bash
curl -X POST "http://localhost:8000/tasks/dummy?wait_seconds=5"
```

### GET /tasks/{task_id}
Verifica status da task

```bash
curl "http://localhost:8000/tasks/{task_id}"
```

Resposta:
```json
{
  "task_id": "abc-123-xyz",
  "status": "completed|pending|running|failed",
  "result": {...},
  "error": null
}
```

## Status possíveis
- `pending`: Task enfileirada
- `running`: Em execução
- `completed`: Concluída com sucesso
- `failed`: Erro na execução

## Teste Round-Trip

```bash
python test_celery_roundtrip.py
```

## Iniciar ambiente

```bash
redis-server
celery -A app.celery_app worker --loglevel=info
uvicorn app.main:app --reload
```
