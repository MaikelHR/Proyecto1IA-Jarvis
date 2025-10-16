"""
Probar Telco con la API y ver las probabilidades
"""
import requests
import json

BASE_URL = "http://localhost:8000"

test_cases = [
    {
        "name": "Cliente de BAJO RIESGO (debería predecir NO)",
        "features": {
            "gender": "Male",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "Yes",
            "tenure": 72,  # 6 años de servicio
            "PhoneService": "Yes",
            "MultipleLines": "Yes",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "Yes",
            "OnlineBackup": "Yes",
            "DeviceProtection": "Yes",
            "TechSupport": "Yes",
            "StreamingTV": "Yes",
            "StreamingMovies": "Yes",
            "Contract": "Two year",
            "PaperlessBilling": "No",
            "PaymentMethod": "Bank transfer (automatic)",
            "MonthlyCharges": 95.0,
            "TotalCharges": 6840.0
        }
    },
    {
        "name": "Cliente de ALTO RIESGO (debería predecir YES)",
        "features": {
            "gender": "Female",
            "SeniorCitizen": 1,
            "Partner": "No",
            "Dependents": "No",
            "tenure": 1,  # Cliente nuevo
            "PhoneService": "No",
            "MultipleLines": "No phone service",
            "InternetService": "DSL",
            "OnlineSecurity": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 29.85,
            "TotalCharges": 29.85
        }
    },
    {
        "name": "Cliente de RIESGO EXTREMO (debería predecir YES)",
        "features": {
            "gender": "Male",
            "SeniorCitizen": 1,
            "Partner": "No",
            "Dependents": "No",
            "tenure": 2,  # Muy nuevo
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 70.7,
            "TotalCharges": 151.65
        }
    }
]

print("="*80)
print("🧪 PRUEBA DETALLADA DE TELCO CHURN")
print("="*80)

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. {test['name']}")
    print("-" * 80)
    
    # Imprimir algunas features clave
    f = test['features']
    print(f"   tenure: {f['tenure']} meses | Contract: {f['Contract']}")
    print(f"   MonthlyCharges: ${f['MonthlyCharges']} | TotalCharges: ${f['TotalCharges']}")
    print(f"   Services: Security={f['OnlineSecurity']}, Backup={f['OnlineBackup']}, Tech={f['TechSupport']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predictions/telco_churn",
            json={"features": test['features']},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get('prediction')
            confidence = result.get('confidence')
            
            print(f"\n   ✅ Predicción: {prediction}")
            if confidence is not None:
                print(f"   📊 Confianza: {confidence:.1%}")
                
                # Calcular probabilidad inversa
                if prediction == "No":
                    prob_no = confidence
                    prob_yes = 1 - confidence
                else:
                    prob_yes = confidence
                    prob_no = 1 - confidence
                
                print(f"   📊 Probabilidades:")
                print(f"      - NO (queda):   {prob_no:.1%}")
                print(f"      - YES (abandona): {prob_yes:.1%}")
        else:
            print(f"\n   ❌ Error {response.status_code}: {response.json()}")
            
    except Exception as e:
        print(f"\n   ❌ Excepción: {e}")

print("\n" + "="*80)
print("🎯 ANÁLISIS")
print("="*80)
print("""
Si todas las predicciones son "No" con confianza similar (~73%), 
el modelo está prediciendo siempre la clase mayoritaria.

Esto indica que:
1. El modelo no aprendió patrones útiles del dataset
2. Puede estar sobre-regularizado
3. O tiene un problema en el entrenamiento

Solución posible: Re-entrenar el modelo con mejores hiperparámetros
o verificar que las features se estén procesando correctamente.
""")
