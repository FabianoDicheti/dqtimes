"""
Script de teste para validar a integração Celery + FastAPI.

Execute este script após iniciar:
1. Redis: redis-server
2. FastAPI: uvicorn app.main:app --reload
3. Celery Worker: celery -A app.celery_app worker --loglevel=info
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Testa o endpoint de health check."""
    print("\n=== Testando Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_task_dummy():
    """Testa a task dummy - round-trip completo."""
    print("\n=== Testando Task Dummy (Round-Trip) ===")
    
    # 1. Enfileirar a task
    print("1. Enfileirando task...")
    response = requests.post(
        f"{BASE_URL}/task/dummy",
        json={"test": "dummy data", "timestamp": time.time()}
    )
    
    if response.status_code != 200:
        print(f"Erro ao enfileirar task: {response.status_code}")
        return False
    
    task_data = response.json()
    task_id = task_data["task_id"]
    print(f"Task ID: {task_id}")
    print(f"Response: {json.dumps(task_data, indent=2)}")
    
    # 2. Aguardar e verificar status
    print("\n2. Verificando status da task...")
    max_attempts = 10
    for attempt in range(max_attempts):
        time.sleep(1)
        status_response = requests.get(f"{BASE_URL}/task/{task_id}")
        status_data = status_response.json()
        
        print(f"Tentativa {attempt + 1}: Status = {status_data['status']}")
        
        if status_data["status"] == "completed":
            print("\n✓ Task concluída com sucesso!")
            print(f"Resultado: {json.dumps(status_data.get('result', {}), indent=2)}")
            return True
        elif status_data["status"] == "failed":
            print(f"\n✗ Task falhou: {status_data.get('error', 'Erro desconhecido')}")
            return False
    
    print(f"\n✗ Timeout: Task não completou em {max_attempts} segundos")
    return False


def test_projection_task():
    """Testa a task de projeção assíncrona."""
    print("\n=== Testando Task de Projeção ===")
    
    # Preparar dados
    lista_historico = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    quantidade_projecoes = 3
    
    # Enfileirar task
    print(f"Enfileirando task com {len(lista_historico)} valores históricos...")
    response = requests.post(
        f"{BASE_URL}/task/projection",
        data={
            "lista_historico": json.dumps(lista_historico),
            "quantidade_projecoes": quantidade_projecoes
        }
    )
    
    if response.status_code != 200:
        print(f"Erro ao enfileirar task: {response.status_code}")
        return False
    
    task_data = response.json()
    task_id = task_data["task_id"]
    print(f"Task ID: {task_id}")
    
    # Verificar status
    print("Aguardando conclusão...")
    for attempt in range(20):  # Mais tempo para processamento complexo
        time.sleep(1)
        status_response = requests.get(f"{BASE_URL}/task/{task_id}")
        status_data = status_response.json()
        
        print(f"Tentativa {attempt + 1}: {status_data['status']}")
        
        if status_data["status"] == "completed":
            print("\n✓ Projeção concluída com sucesso!")
            if "result" in status_data:
                result = status_data["result"]
                print(f"Probabilidade de Subir: {result.get('probabilidade_subir', 'N/A')}")
            return True
        elif status_data["status"] == "failed":
            print(f"\n✗ Projeção falhou")
            return False
    
    return False


def test_long_running_task():
    """Testa a task long-running."""
    print("\n=== Testando Task Long-Running ===")
    
    iterations = 5
    print(f"Enfileirando task com {iterations} iterações...")
    
    response = requests.post(
        f"{BASE_URL}/task/long-running",
        data={"iterations": iterations}
    )
    
    if response.status_code != 200:
        print(f"Erro: {response.status_code}")
        return False
    
    task_data = response.json()
    task_id = task_data["task_id"]
    print(f"Task ID: {task_id}")
    
    # Monitorar progresso
    print("Monitorando progresso...")
    for attempt in range(15):
        time.sleep(1)
        status_response = requests.get(f"{BASE_URL}/task/{task_id}")
        status_data = status_response.json()
        
        print(f"Tentativa {attempt + 1}: {status_data['status']}")
        
        if status_data["status"] == "completed":
            print("\n✓ Task long-running concluída!")
            return True
    
    return False


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("TESTE DE INTEGRAÇÃO CELERY + FASTAPI")
    print("=" * 60)
    
    # Verificar se a API está rodando
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.ConnectionError:
        print("\n✗ Erro: API não está rodando em http://localhost:8000")
        print("  Inicie o servidor com: uvicorn app.main:app --reload")
        return
    except requests.exceptions.Timeout:
        print("\n✗ Erro: Timeout ao conectar com a API")
        return
    
    results = []
    
    # Testar health check
    results.append(("Health Check", test_health_check()))
    
    # Testar task dummy
    results.append(("Task Dummy (Round-Trip)", test_task_dummy()))
    
    # Testar projeção
    results.append(("Task de Projeção", test_projection_task()))
    
    # Testar long-running
    results.append(("Task Long-Running", test_long_running_task()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} testes passaram")
    print("=" * 60)


if __name__ == "__main__":
    main()

