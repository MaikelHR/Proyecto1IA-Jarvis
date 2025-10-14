"""Script de prueba para la API de Jarvis."""

import requests
import json

# Base URL de la API
BASE_URL = "http://localhost:8000"

def test_health():
    """Probar endpoint de salud."""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_list_datasets():
    """Probar listado de datasets."""
    print("=" * 60)
    print("TEST 2: Listar Datasets Disponibles")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/predictions/datasets")
    print(f"Status: {response.status_code}")
    datasets = response.json()
    print(f"Datasets encontrados: {len(datasets)}")
    
    for dataset in datasets:
        print(f"\n- {dataset['key']}: {dataset['name']}")
        print(f"  Tipo: {dataset['task']}")
        print(f"  Comandos: {dataset['voice_commands'][0]}")
    print()


def test_prediction_telco_churn():
    """Probar predicción de Churn Telco."""
    print("=" * 60)
    print("TEST 3: Predicción de Churn Telco")
    print("=" * 60)
    
    data = {
        "features": {
            "gender": "Female",
            "senior_citizen": 0,
            "partner": "Yes",
            "dependents": "No",
            "tenure": 12,
            "phone_service": "Yes",
            "multiple_lines": "No",
            "internet_service": "Fiber optic",
            "online_security": "No",
            "online_backup": "No",
            "device_protection": "No",
            "tech_support": "No",
            "streaming_tv": "No",
            "streaming_movies": "No",
            "contract": "Month-to-month",
            "paperless_billing": "Yes",
            "payment_method": "Electronic check",
            "monthly_charges": 70.5,
            "total_charges": 846.0
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/predictions/telco_churn",
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()


def test_prediction_wine_quality():
    """Probar predicción de calidad de vino."""
    print("=" * 60)
    print("TEST 4: Predicción de Calidad de Vino")
    print("=" * 60)
    
    data = {
        "features": {
            "fixed_acidity": 7.4,
            "volatile_acidity": 0.7,
            "citric_acid": 0,
            "residual_sugar": 1.9,
            "chlorides": 0.076,
            "free_sulfur_dioxide": 11,
            "total_sulfur_dioxide": 34,
            "density": 0.9978,
            "ph": 3.51,
            "sulphates": 0.56,
            "alcohol": 9.4
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/predictions/wine_quality",
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()


def test_voice_command():
    """Probar reconocimiento de comando de voz."""
    print("=" * 60)
    print("TEST 5: Análisis de Comando de Voz")
    print("=" * 60)
    
    commands = [
        "Jarvis predice el precio de Bitcoin",
        "Analiza riesgo de churn",
        "Evalúa la calidad del vino",
        "Calcula mi grasa corporal"
    ]
    
    for command in commands:
        response = requests.post(
            f"{BASE_URL}/voice/parse",
            params={"text": command}
        )
        result = response.json()
        print(f"Comando: '{command}'")
        print(f"  Reconocido: {result['command_recognized']}")
        print(f"  Dataset: {result.get('dataset_key', 'N/A')}")
        print()


if __name__ == "__main__":
    print("\n🤖 JARVIS IA - Test Suite\n")
    
    try:
        test_health()
        test_list_datasets()
        test_prediction_telco_churn()
        test_prediction_wine_quality()
        test_voice_command()
        
        print("=" * 60)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar a la API")
        print("Asegúrate de que el servidor esté corriendo:")
        print("  python run_api.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")
