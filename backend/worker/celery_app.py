from celery import Celery

app = Celery(
    "dqtmes",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=["tasks"]
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Sao_Paulo"
)