from app.celery_app import celery_app
from app import forecast_temp
import time

@celery_app.task(name="app.tasks.task_dummy")
def task_dummy(data: dict):
    """
    Task dummy para validar a execução do Celery.
    
    Args:
        data: Dicionário com dados de entrada
        
    Returns:
        dict: Resultado da task dummy
    """
    # Simula algum processamento
    time.sleep(2)
    
    return {
        "status": "completed",
        "message": "Task dummy executada com sucesso",
        "input_data": data,
        "output": {
            "processed": True,
            "timestamp": time.time()
        }
    }

@celery_app.task(name="app.tasks.projection_task")
def projection_task(lista_historico: list, quantidade_projecoes: int):
    """
    Task assíncrona para realizar projeções de dados.
    
    Args:
        lista_historico: Lista de valores históricos
        quantidade_projecoes: Número de projeções a serem feitas
        
    Returns:
        dict: Resultado da projeção
    """
    try:
        # Chama a função de prejeção existente
        resultado = forecast_temp(lista_historico, quantidade_projecoes)
        
        return {
            "status": "completed",
            "resultado": resultado,
            "input_data": {
                "lista_historico": lista_historico,
                "quantidade_projecoes": quantidade_projecoes
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

@celery_app.task(name="app.tasks.task_long_running")
def task_long_running(iterations: int = 10):
    """
    Task que simula uma operação longa para testar o round-trip.
    
    Args:
        iterations: Número de iterações
        
    Returns:
        dict: Resultado da operação
    """
    result = []
    for i in range(iterations):
        result.append(i ** 2)
        time.sleep(0.5)  # Simula processamento
    
    return {
        "status": "completed",
        "iterations": iterations,
        "result": result,
        "message": f"Processou {iterations} iterações com sucesso"
    }

