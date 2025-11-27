# Celery Setup - DQTimes

## Dependências

Redis, Celery, FastAPI

## Instalação Local

```bash
pip install -r requirements.txt
```

## Iniciar Redis

```bash
redis-server
```

## Iniciar Celery Worker

```bash
celery -A app.celery_app worker --loglevel=info --queues=forecast_queue,default
```

## Iniciar Flower (Monitor)

```bash
celery -A app.celery_app flower --port=5555
```

Acesse: http://localhost:5555

## Parar Workers

```bash
pkill -f "celery worker"
```

## Docker Compose

```bash
docker-compose up -d
docker-compose down
```

## Testar

```python
from app.tasks import health_check
result = health_check.delay()
print(result.get())
```

## Filas

- `forecast_queue`: tarefas de previsão
- `default`: tarefas gerais

## Variáveis de Ambiente

- `CELERY_BROKER_URL`: redis://localhost:6379/0
- `CELERY_RESULT_BACKEND`: redis://localhost:6379/0
