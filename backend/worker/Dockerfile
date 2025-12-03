FROM python:3.11-slim

WORKDIR /app

# Agora o requirements.txt está DENTRO da pasta worker → sem ../, sem erro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install celery[redis] prometheus-client celery-prometheus-exporter

COPY libs ./libs
COPY celery_app.py .
COPY tasks.py .

ENV PYTHONPATH=/app/libs:/app

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info", "--concurrency=6"]