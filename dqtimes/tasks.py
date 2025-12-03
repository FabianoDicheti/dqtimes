from celery_app import celery
import random
import time

@celery.task
def previsao_task(serie, nome_ref, periodos):
    time.sleep(2)
    resultados = [round(random.uniform(0, 100), 2) for _ in range(periodos)]
    return {
        "serie": serie,
        "nome_ref": nome_ref,
        "resultados": resultados
    }
