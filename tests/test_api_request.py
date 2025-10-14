"""
Probar la API directamente con requests para ver el error exacto.
"""

import requests
import json

print("=" * 80)
print(" PRUEBA DE LA API CON REQUESTS")
print("=" * 80)
print()

# Datos de prueba con nombres en minúsculas (snake_case)
data = {
    "features": {
        "customer_id": "1234-ABCDE",
        "gender": "Male",
        "senior_citizen": 0,
        "partner": "No",
        "dependents": "No",
        "tenure": 3,
        "phone_service": "Yes",
        "multiple_lines": "No",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "No",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "Yes",
        "streaming_movies": "Yes",
        "contract": "Month-to-month",
        "paperless_billing": "Yes",
        "payment_method": "Electronic check",
        "monthly_charges": 85.0,
        "total_charges": 255.0
    }
}

print("1. Datos a enviar:")
print(json.dumps(data, indent=2))
print()

print("2. Enviando request a la API...")
print("   URL: http://localhost:8000/predictions/telco_churn")
print()

try:
    response = requests.post(
        "http://localhost:8000/predictions/telco_churn",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"3. Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ PREDICCIÓN EXITOSA")
        print()
        print("Respuesta:")
        print(json.dumps(result, indent=2))
    else:
        print("❌ ERROR EN LA PREDICCIÓN")
        print()
        print("Respuesta de error:")
        try:
            error_detail = response.json()
            print(json.dumps(error_detail, indent=2))
        except:
            print(response.text)
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se puede conectar a la API")
    print()
    print("Asegúrate de que la API esté corriendo:")
    print("   .\\start_api_with_env.ps1")
    
except Exception as e:
    print(f"❌ ERROR INESPERADO: {e}")
    import traceback
    traceback.print_exc()
