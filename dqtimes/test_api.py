#!/usr/bin/env python
"""
Script de teste para a API DQTimes v2
Testa os principais endpoints para garantir que tudo funciona
"""

import requests
import json
import time

# Configurações
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

# Cores para output (funciona no Windows também)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}[OK] {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR] {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.END}")

def test_health_check():
    """Testa o endpoint de health check"""
    print_info("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            print_success("Health check OK")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_root():
    """Testa o endpoint root"""
    print_info("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Root endpoint OK - API: {data.get('name', 'Unknown')}")
            return True
        else:
            print_error(f"Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Root endpoint error: {e}")
        return False

def test_login():
    """Testa o endpoint de login"""
    print_info("Testing login endpoint...")
    try:
        credentials = {
            "username": "admin",
            "password": "Admin@123"
        }
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=credentials,
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print_success(f"Login successful - Token received (length: {len(token)})")
                return token
            else:
                print_error("Login failed: No token in response")
                return None
        else:
            print_error(f"Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None

def test_login_invalid():
    """Testa login com credenciais inválidas"""
    print_info("Testing login with invalid credentials...")
    try:
        credentials = {
            "username": "invalid",
            "password": "wrong"
        }
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=credentials,
            timeout=TIMEOUT
        )

        # 401 = Invalid credentials, 422 = Validation error (também aceitável)
        if response.status_code in [401, 422]:
            print_success(f"Invalid login correctly rejected ({response.status_code})")
            return True
        else:
            print_error(f"Expected 401 or 422, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Invalid login test error: {e}")
        return False

def test_forecast(token):
    """Testa o endpoint de previsão"""
    print_info("Testing forecast endpoint...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        forecast_data = {
            "data": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
            "n_projections": 5,
            "method": "auto",
            "confidence_level": 0.95
        }

        response = requests.post(
            f"{BASE_URL}/forecast/single",
            json=forecast_data,
            headers=headers,
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            data = response.json()
            projections = data.get("projections", [])
            probability = data.get("probability_increase", 0)
            print_success(f"Forecast successful - {len(projections)} projections generated")
            print_info(f"  Projections: {projections}")
            print_info(f"  Probability of increase: {probability:.2%}")
            print_info(f"  Execution time: {data.get('execution_time', 0):.3f}s")
            return True
        else:
            print_error(f"Forecast failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Forecast error: {e}")
        return False

def test_forecast_without_auth():
    """Testa forecast sem autenticação"""
    print_info("Testing forecast without authentication...")
    try:
        forecast_data = {
            "data": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
            "n_projections": 5
        }

        response = requests.post(
            f"{BASE_URL}/forecast/single",
            json=forecast_data,
            timeout=TIMEOUT
        )

        # 401 = Unauthorized (sem token), 403 = Forbidden (token inválido)
        if response.status_code in [401, 403]:
            print_success(f"Forecast without auth correctly rejected ({response.status_code})")
            return True
        else:
            print_error(f"Expected 401 or 403, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Forecast without auth test error: {e}")
        return False

def test_history(token):
    """Testa o endpoint de histórico"""
    print_info("Testing history endpoint...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/history?page=1&page_size=10",
            headers=headers,
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            data = response.json()
            total_items = data.get("total_items", 0)
            items = data.get("items", [])
            print_success(f"History retrieved - {total_items} total items, {len(items)} on this page")
            if items:
                print_info(f"  Latest operation: {items[0].get('operation_type', 'unknown')}")
            return True
        else:
            print_error(f"History failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"History error: {e}")
        return False

def test_validation_error():
    """Testa validação de dados inválidos"""
    print_info("Testing validation with invalid data...")
    try:
        # Tentar fazer login sem autenticação primeiro para pegar o token
        credentials = {"username": "admin", "password": "Admin@123"}
        login_response = requests.post(f"{BASE_URL}/auth/login", json=credentials, timeout=TIMEOUT)
        token = login_response.json().get("access_token")

        headers = {"Authorization": f"Bearer {token}"}
        # Dados insuficientes (menos de 10 valores)
        forecast_data = {
            "data": [100, 110, 120],  # Apenas 3 valores
            "n_projections": 5
        }

        response = requests.post(
            f"{BASE_URL}/forecast/single",
            json=forecast_data,
            headers=headers,
            timeout=TIMEOUT
        )

        if response.status_code == 422:
            print_success("Invalid data correctly rejected (422)")
            return True
        else:
            print_error(f"Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Validation test error: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("DQTimes API v2 - Test Suite")
    print("="*60 + "\n")

    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }

    # Aguardar API iniciar
    print_info("Waiting for API to be ready...")
    time.sleep(2)

    # Testes básicos
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root),
        ("Login (Valid)", test_login),
        ("Login (Invalid)", test_login_invalid),
        ("Forecast (No Auth)", test_forecast_without_auth),
        ("Validation Error", test_validation_error),
    ]

    token = None
    for test_name, test_func in tests:
        results["total"] += 1
        print(f"\n--- Test {results['total']}: {test_name} ---")
        try:
            if test_name == "Login (Valid)":
                result = test_func()
                if result:
                    token = result
                    results["passed"] += 1
                else:
                    results["failed"] += 1
            else:
                if test_func():
                    results["passed"] += 1
                else:
                    results["failed"] += 1
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results["failed"] += 1

    # Testes que precisam de autenticação
    if token:
        auth_tests = [
            ("Forecast (Authenticated)", lambda: test_forecast(token)),
            ("History", lambda: test_history(token)),
        ]

        for test_name, test_func in auth_tests:
            results["total"] += 1
            print(f"\n--- Test {results['total']}: {test_name} ---")
            try:
                if test_func():
                    results["passed"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                print_error(f"Test crashed: {e}")
                results["failed"] += 1

    # Resumo
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    print(f"\nTotal Tests: {results['total']}")
    print_success(f"Passed: {results['passed']}")
    if results['failed'] > 0:
        print_error(f"Failed: {results['failed']}")
    else:
        print_success("Failed: 0")

    success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")

    if results['failed'] == 0:
        print_success("\n*** All tests passed! API is working correctly! ***")
    else:
        print_warning(f"\n*** {results['failed']} test(s) failed. Please review the errors above. ***")

    print("\n" + "="*60 + "\n")

    return results['failed'] == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print_warning("\nTests interrupted by user")
        exit(1)
    except Exception as e:
        print_error(f"\nTest suite crashed: {e}")
        exit(1)
