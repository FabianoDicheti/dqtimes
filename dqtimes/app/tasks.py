from app.celery_app import celery_app
from app.aplicacao import forecast_temp
import time

@celery_app.task(name='app.tasks.forecast_task', bind=True)
def forecast_task(self, lista_historico, quantidade_projecoes):
    resultado = forecast_temp(lista_historico, quantidade_projecoes)
    return {
        "task_id": self.request.id,
        "projecoes": resultado
    }

@celery_app.task(name='app.tasks.process_dataframe_task', bind=True)
def process_dataframe_task(self, csv_content, quantidade_projecoes):
    return {
        "task_id": self.request.id,
        "status": "processed"
    }

@celery_app.task(name='app.tasks.dummy_task', bind=True)
def dummy_task(self, wait_seconds=5):
    time.sleep(wait_seconds)
    return {
        "task_id": self.request.id,
        "message": f"Task completed after {wait_seconds} seconds",
        "status": "success"
    }

@celery_app.task(name='app.tasks.health_check')
def health_check():
    return {"status": "healthy"}
