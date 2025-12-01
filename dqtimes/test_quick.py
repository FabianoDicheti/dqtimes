#!/usr/bin/env python3
"""
Script de teste rápido para a API DQTimes
Uso: python test_quick.py
"""

import requests
import json
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:8080"
TEST_USER = "admin"
TEST_PASS = "Admin@123"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def test_health():
    """Teste 1: Health check"""
    print_header("Teste 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"API está online! Status: {response.status_code}")
            print(f"   Resposta: {response.json()}")
            return True
        else:
            print_error(f"API retornou status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API!")
        print("   Certifique-se de que a API está rodando em http://localhost:8080")
        return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_login():
    """Teste 2: Login"""
    print_header("Teste 2: Login")
    try:
        payload = {
            "username": TEST_USER,
            "password": TEST_PASS
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print_success("Login realizado com sucesso!")
            print(f"   Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"   Usuário: {data.get('username', 'N/A')}")
            print(f"   Expira em: {data.get('expires_in', 'N/A')} segundos")
            return data.get('access_token')
        else:
            print_error(f"Login falhou! Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return None
    except Exception as e:
        print_error(f"Erro no login: {e}")
        return None

def test_forecast(token):
    """Teste 3: Forecast"""
    print_header("Teste 3: Previsão (Forecast)")

    if not token:
        print_error("Token não disponível. Pulando teste de forecast.")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "data": [10.0, 12.0, 13.0, 15.0, 17.0, 20.0, 22.0, 25.0, 27.0, 30.0],
            "n_projections": 5,
            "method": "auto"
        }

        print("   Enviando dados para previsão...")
        print(f"   Dados históricos: {payload['data']}")
        print(f"   Projeções solicitadas: {payload['n_projections']}")

        response = requests.post(
            f"{BASE_URL}/forecast/single",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print_success("Previsão realizada com sucesso!")
            print(f"   Método usado: {data.get('method_used', 'N/A')}")
            print(f"   Projeções: {data.get('projections', [])}")
            print(f"   Confiança: {data.get('confidence_interval', {})}")
            return True
        else:
            print_error(f"Forecast falhou! Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print_error(f"Erro no forecast: {e}")
        return False

def test_docs():
    """Teste 4: Documentação"""
    print_header("Teste 4: Documentação")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_success("Documentação acessível!")
            print(f"   Acesse: {BASE_URL}/docs")
            return True
        else:
            print_error(f"Documentação retornou status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro ao acessar documentação: {e}")
        return False

def main():
    """Executar todos os testes"""
    print("\n" + "🚀 "*20)
    print("  TESTE RÁPIDO DA API DQTimes")
    print("🚀 "*20)
    print(f"\n⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")

    results = []

    # Teste 1: Health
    results.append(("Health Check", test_health()))

    # Teste 2: Login
    token = test_login()
    results.append(("Login", token is not None))

    # Teste 3: Forecast
    results.append(("Forecast", test_forecast(token)))

    # Teste 4: Docs
    results.append(("Documentação", test_docs()))

    # Resumo
    print_header("RESUMO DOS TESTES")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        color = "green" if result else "red"
        print(f"  {status}: {name}")

    print(f"\n📊 Resultado: {passed}/{total} testes passaram")

    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! A API está funcionando perfeitamente!")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique os erros acima.")

    print(f"\n⏰ Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário.")
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
