"""
Probar predicción directamente con el modelo para entender el problema.
"""

import pickle
import pandas as pd
import json

print("=" * 80)
print(" PRUEBA DIRECTA DEL MODELO TELCO_CHURN")
print("=" * 80)
print()

# 1. Cargar el modelo
print("1. Cargando modelo...")
with open('reports/telco_churn_model.pkl', 'rb') as f:
    model = pickle.load(f)
print(f"   ✓ Modelo cargado: {type(model)}")
print()

# 2. Ver qué columnas espera
print("2. Columnas que espera el modelo:")
if hasattr(model, 'feature_names_in_'):
    print(f"   Total: {len(model.feature_names_in_)} columnas")
    for col in model.feature_names_in_:
        print(f"   • {col}")
else:
    print("   ⚠️  El modelo no tiene feature_names_in_")
print()

# 3. Crear datos de prueba EXACTOS
print("3. Creando datos de prueba...")

# Opción A: Nombres en minúsculas (lo que el modelo espera)
features_snake = {
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

df = pd.DataFrame([features_snake])

print(f"   DataFrame creado con {len(df.columns)} columnas:")
for col in df.columns:
    print(f"   • {col} = {df[col].iloc[0]}")
print()

# 4. Intentar hacer predicción
print("4. Intentando predicción...")
try:
    prediction = model.predict(df)
    print(f"   ✅ PREDICCIÓN EXITOSA: {prediction[0]}")
    
    # Intentar obtener probabilidad
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(df)
        print(f"   Probabilidades: {proba[0]}")
        print(f"   Confianza: {max(proba[0]):.2%}")
    
    print()
    print("=" * 80)
    print(" RESULTADO FINAL")
    print("=" * 80)
    print()
    print(f"Predicción: {'Abandonará' if prediction[0] == 1 else 'Se quedará'}")
    print()
    print("✅ EL MODELO FUNCIONA CORRECTAMENTE")
    print()
    print("JSON para usar en Swagger:")
    print(json.dumps({"features": features_snake}, indent=2))
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    print()
    print("Detalles del error:")
    import traceback
    traceback.print_exc()
