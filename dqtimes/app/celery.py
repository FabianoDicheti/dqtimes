
from celery import Celery
import os


redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379/0')


app = Celery('backend', broker=redis_url, backend=redis_url)


app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_transport_options={'visibility_timeout': 3600},
    task_retry_backoff=True,
    task_retry_backoff_max=600,
    task_default_retry_delay=10,
    task_default_max_retries=5
)

# Task de teste simples
@app.task(bind=True)
def test_task(self):
    print("Celery está funcionando e conectado ao Redis!")
    return "OK"
