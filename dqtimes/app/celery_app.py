from celery import Celery
import os

# Configuração do Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Cria a instância do Celery
celery_app = Celery(
    "dqtimes",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks"]
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,  # Importante para rastrear status
    task_time_limit=300,  # 5 minutos de timeout
    result_expires=3600,  # Expira resultados após 1 hora
)

# Configuração de roteamento de tasks
celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "celery"},
}

