import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_round_trip():
    print("=== Test Round-Trip: Request API -> Enfileira -> Executa -> Retorna ID ===\n")
    
    print("1. Testando task dummy...")
    response = requests.post(f"{BASE_URL}/tasks/dummy?wait_seconds=3")
    if response.status_code == 200:
        task_data = response.json()
        task_id = task_data["task_id"]
        print(f"   Task criada: {task_id}")
        print(f"   Status inicial: {task_data['status']}")
        
        print("\n2. Verificando status (pending/running)...")
        for i in range(5):
            time.sleep(1)
            status_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
            status_data = status_response.json()
            print(f"   [{i+1}s] Status: {status_data['status']}")
            
            if status_data['status'] == 'completed':
                print(f"\n3. Task completada!")
                print(f"   Resultado: {json.dumps(status_data['result'], indent=2)}")
                break
        else:
            print("\n   Task ainda em execução...")
    else:
        print(f"   Erro: {response.status_code}")
    
    print("\n" + "="*70)
    print("\n4. Testando task de forecast...")
    
    forecast_request = {
        "lista_historico": [10, 15, 20, 25, 30],
        "quantidade_projecoes": 3
    }
    
    response = requests.post(f"{BASE_URL}/tasks/forecast", json=forecast_request)
    if response.status_code == 200:
        task_data = response.json()
        task_id = task_data["task_id"]
        print(f"   Task criada: {task_id}")
        
        time.sleep(2)
        status_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        status_data = status_response.json()
        print(f"   Status final: {status_data['status']}")
        if status_data.get('result'):
            print(f"   Resultado: {json.dumps(status_data['result'], indent=2)}")
    else:
        print(f"   Erro: {response.status_code}")

if __name__ == "__main__":
    try:
        test_round_trip()
    except requests.exceptions.ConnectionError:
        print("Erro: Servidor não está rodando em http://localhost:8000")
        print("\nPara testar:")
        print("1. Inicie Redis: redis-server")
        print("2. Inicie Celery: celery -A app.celery_app worker --loglevel=info")
        print("3. Inicie FastAPI: uvicorn app.main:app --reload")
