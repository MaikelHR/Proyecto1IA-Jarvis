"""
Comparar los modelos de Telco Churn (funciona) vs Wine Quality (falla).
"""

import pickle
import pandas as pd
from sklearn.pipeline import Pipeline

print("=" * 80)
print(" COMPARACIÓN: TELCO_CHURN (✓) vs WINE_QUALITY (✗)")
print("=" * 80)
print()

# Cargar ambos modelos
print("1. Cargando modelos...")
with open('reports/telco_churn_model.pkl', 'rb') as f:
    telco_model = pickle.load(f)

with open('reports/winequality_model.pkl', 'rb') as f:
    wine_model = pickle.load(f)

print(f"   Telco: {type(telco_model)}")
print(f"   Wine:  {type(wine_model)}")
print()

# Comparar estructuras
print("2. Estructura del pipeline:")
print()
print("   TELCO_CHURN:")
if isinstance(telco_model, Pipeline):
    for i, (name, step) in enumerate(telco_model.steps, 1):
        print(f"      {i}. {name}: {type(step).__name__}")

print()
print("   WINE_QUALITY:")
if isinstance(wine_model, Pipeline):
    for i, (name, step) in enumerate(wine_model.steps, 1):
        print(f"      {i}. {name}: {type(step).__name__}")

print()

# Comparar columnas
print("3. Columnas esperadas:")
print()
print(f"   TELCO_CHURN ({len(telco_model.feature_names_in_)} columnas):")
print(f"      {telco_model.feature_names_in_[:5]}...")

print()
print(f"   WINE_QUALITY ({len(wine_model.feature_names_in_)} columnas):")
print(f"      {wine_model.feature_names_in_[:5]}...")

print()

# Probar con datos correctos
print("4. Probando predicciones directas:")
print()

# TELCO
telco_data = {
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

try:
    df_telco = pd.DataFrame([telco_data])
    pred_telco = telco_model.predict(df_telco)
    print(f"   TELCO_CHURN: ✓ Predicción = {pred_telco[0]}")
except Exception as e:
    print(f"   TELCO_CHURN: ✗ Error = {e}")

# WINE
wine_data = {
    "type": "white",
    "fixed_acidity": 7.0,
    "volatile_acidity": 0.27,
    "citric_acid": 0.36,
    "residual_sugar": 20.7,
    "chlorides": 0.045,
    "free_sulfur_dioxide": 45.0,
    "total_sulfur_dioxide": 170.0,
    "density": 1.001,
    "p_h": 3.0,
    "sulphates": 0.45,
    "alcohol": 8.8
}

try:
    df_wine = pd.DataFrame([wine_data])
    pred_wine = wine_model.predict(df_wine)
    print(f"   WINE_QUALITY: ✓ Predicción = {pred_wine[0]}")
except Exception as e:
    print(f"   WINE_QUALITY: ✗ Error = {e}")

print()

# Verificar si hay algún problema con el transformador
print("5. Detalles del ColumnTransformer:")
print()

if isinstance(wine_model, Pipeline) and 'preprocessor' in wine_model.named_steps:
    ct = wine_model.named_steps['preprocessor']
    print(f"   Tipo: {type(ct)}")
    
    if hasattr(ct, 'transformers_'):
        print(f"   Transformers:")
        for name, transformer, cols in ct.transformers_:
            print(f"      • {name}: {len(cols) if isinstance(cols, (list, tuple)) else '?'} columnas")
            if isinstance(cols, (list, tuple)) and len(cols) < 20:
                print(f"        Columnas: {cols}")
