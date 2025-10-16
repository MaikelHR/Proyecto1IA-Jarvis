"""
Script para probar que las predicciones CAMBIAN con diferentes inputs
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_model_variability(model_key, test_cases):
    """Prueba que un modelo dé diferentes predicciones con diferentes inputs"""
    print(f"\n{'='*70}")
    print(f"🔍 PROBANDO MODELO: {model_key}")
    print('='*70)
    
    predictions = []
    
    for i, features in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/predictions/{model_key}",
                json={"features": features},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get('prediction')
                predictions.append(prediction)
                
                print(f"\n📊 Test Case {i}:")
                print(f"   Input: {json.dumps(features, indent=6)}")
                print(f"   ✅ Predicción: {prediction}")
            else:
                print(f"\n❌ Test Case {i} FALLÓ:")
                print(f"   Status: {response.status_code}")
                print(f"   Error: {response.json()}")
                predictions.append(None)
                
        except Exception as e:
            print(f"\n❌ Test Case {i} ERROR: {e}")
            predictions.append(None)
    
    # Análisis de variabilidad
    print(f"\n{'='*70}")
    valid_predictions = [p for p in predictions if p is not None]
    
    if len(valid_predictions) < 2:
        print("⚠️  NO SE PUDIERON OBTENER SUFICIENTES PREDICCIONES")
        return False
    
    unique_predictions = len(set(map(str, valid_predictions)))
    
    if unique_predictions == 1:
        print(f"❌ PROBLEMA: Todas las predicciones son IGUALES: {valid_predictions[0]}")
        print("   → El modelo NO está respondiendo a cambios en el input")
        return False
    else:
        print(f"✅ BIEN: Se obtuvieron {unique_predictions} predicciones DIFERENTES")
        print(f"   Predicciones: {valid_predictions}")
        return True


# ============================================================================
# TEST 1: BODY FAT (Regresión - debería variar mucho)
# ============================================================================
print("\n" + "="*70)
print("TEST 1: BODY FAT - Porcentaje de grasa corporal")
print("="*70)
print("Probando con diferentes pesos y abdómenes...")

body_fat_tests = [
    {
        "Density": 1.0708,
        "Age": 23,
        "Weight": 154.25,  # Peso bajo
        "Height": 67.75,
        "Neck": 36.2,
        "Chest": 93.1,
        "Abdomen": 85.2,   # Abdomen normal
        "Hip": 94.5,
        "Thigh": 59.0,
        "Knee": 37.3,
        "Ankle": 21.9,
        "Biceps": 32.0,
        "Forearm": 27.4,
        "Wrist": 17.1
    },
    {
        "Density": 1.0328,  # Densidad menor (más grasa)
        "Age": 45,
        "Weight": 220.0,    # Peso alto
        "Height": 67.75,
        "Neck": 40.0,
        "Chest": 115.0,
        "Abdomen": 110.0,   # Abdomen grande
        "Hip": 110.0,
        "Thigh": 65.0,
        "Knee": 42.0,
        "Ankle": 24.0,
        "Biceps": 38.0,
        "Forearm": 30.0,
        "Wrist": 19.0
    },
    {
        "Density": 1.0900,  # Densidad alta (poca grasa)
        "Age": 20,
        "Weight": 140.0,    # Peso bajo
        "Height": 70.0,
        "Neck": 34.0,
        "Chest": 85.0,
        "Abdomen": 75.0,    # Abdomen pequeño
        "Hip": 88.0,
        "Thigh": 55.0,
        "Knee": 35.0,
        "Ankle": 20.0,
        "Biceps": 28.0,
        "Forearm": 25.0,
        "Wrist": 16.0
    }
]

body_fat_ok = test_model_variability("body_fat", body_fat_tests)


# ============================================================================
# TEST 2: TELCO CHURN (Clasificación - debería dar 0 o 1)
# ============================================================================
print("\n\n" + "="*70)
print("TEST 2: TELCO CHURN - Probabilidad de abandono")
print("="*70)
print("Probando con diferentes perfiles de cliente...")

telco_tests = [
    {
        # Cliente de BAJO RIESGO (servicio largo, contrato anual)
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "Yes",
        "tenure": 60,  # 5 años de servicio
        "PhoneService": "Yes",
        "MultipleLines": "Yes",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "Yes",
        "DeviceProtection": "Yes",
        "TechSupport": "Yes",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Two year",  # Contrato largo
        "PaperlessBilling": "No",
        "PaymentMethod": "Bank transfer (automatic)",
        "MonthlyCharges": 85.0,
        "TotalCharges": 5100.0
    },
    {
        # Cliente de ALTO RIESGO (nuevo, mes a mes, pocos servicios)
        "gender": "Female",
        "SeniorCitizen": 1,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 1,  # Cliente nuevo
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",  # Sin compromiso
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 70.0,
        "TotalCharges": 70.0
    },
    {
        # Cliente de RIESGO MEDIO
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 24,  # 2 años
        "PhoneService": "Yes",
        "MultipleLines": "Yes",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "No",
        "DeviceProtection": "Yes",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "No",
        "Contract": "One year",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Credit card (automatic)",
        "MonthlyCharges": 75.0,
        "TotalCharges": 1800.0
    }
]

telco_ok = test_model_variability("telco_churn", telco_tests)


# ============================================================================
# TEST 3: WINE QUALITY (Clasificación multiclase - debería dar 3-9)
# ============================================================================
print("\n\n" + "="*70)
print("TEST 3: WINE QUALITY - Calidad del vino")
print("="*70)
print("Probando con diferentes composiciones químicas...")

wine_tests = [
    {
        # Vino de BAJA CALIDAD (mucha acidez volátil, poco alcohol)
        "type": "red",
        "fixed acidity": 11.0,
        "volatile acidity": 1.2,  # Alta (malo)
        "citric acid": 0.1,
        "residual sugar": 2.0,
        "chlorides": 0.15,  # Alto (malo)
        "free sulfur dioxide": 10.0,
        "total sulfur dioxide": 80.0,
        "density": 1.000,
        "pH": 3.8,
        "sulphates": 0.4,
        "alcohol": 9.0  # Bajo
    },
    {
        # Vino de ALTA CALIDAD (balanceado, buen alcohol)
        "type": "red",
        "fixed acidity": 7.5,
        "volatile acidity": 0.3,  # Baja (bueno)
        "citric acid": 0.35,
        "residual sugar": 2.5,
        "chlorides": 0.06,  # Bajo (bueno)
        "free sulfur dioxide": 25.0,
        "total sulfur dioxide": 100.0,
        "density": 0.996,
        "pH": 3.2,
        "sulphates": 0.7,
        "alcohol": 12.5  # Alto
    },
    {
        # Vino MEDIO
        "type": "white",
        "fixed acidity": 7.0,
        "volatile acidity": 0.5,
        "citric acid": 0.3,
        "residual sugar": 8.0,
        "chlorides": 0.08,
        "free sulfur dioxide": 40.0,
        "total sulfur dioxide": 150.0,
        "density": 0.998,
        "pH": 3.0,
        "sulphates": 0.5,
        "alcohol": 10.5
    }
]

wine_ok = test_model_variability("wine_quality", wine_tests)


# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n\n" + "="*70)
print("📊 RESUMEN DE PRUEBAS DE VARIABILIDAD")
print("="*70)

results = {
    "Body Fat (Regresión)": body_fat_ok,
    "Telco Churn (Clasificación)": telco_ok,
    "Wine Quality (Multiclase)": wine_ok
}

print("\nResultados:")
for model, ok in results.items():
    status = "✅ FUNCIONA CORRECTAMENTE" if ok else "❌ PROBLEMA DETECTADO"
    print(f"  {model:30s}: {status}")

failed = [m for m, ok in results.items() if not ok]

if failed:
    print(f"\n❌ ATENCIÓN: {len(failed)} modelo(s) con problemas:")
    for model in failed:
        print(f"   - {model}")
    print("\n🔍 POSIBLES CAUSAS:")
    print("   1. Modelo siempre predice la media/moda (no aprendió patrones)")
    print("   2. Pipeline de preprocesamiento descarta features importantes")
    print("   3. Datos de entrenamiento no tienen suficiente variabilidad")
    print("   4. Modelo no fue entrenado correctamente")
else:
    print("\n✅ TODOS LOS MODELOS RESPONDEN A CAMBIOS EN EL INPUT")

print("="*70)
