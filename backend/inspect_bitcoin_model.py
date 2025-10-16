"""Inspect Bitcoin model internals."""

import pickle
from pathlib import Path
import numpy as np
import pandas as pd

# Load model
model_path = Path("reports/bitcoin_price_training_model.pkl")
model = pickle.load(open(model_path, 'rb'))

print("="*70)
print("🔍 ANÁLISIS DEL MODELO DE BITCOIN")
print("="*70)

# Check model type
print(f"\n📋 Tipo de modelo: {type(model)}")

# Get feature names
if hasattr(model, 'feature_names_in_'):
    print(f"\n📊 Features esperados ({len(model.feature_names_in_)}):")
    for i, feat in enumerate(model.feature_names_in_, 1):
        print(f"  {i}. {feat}")

# Check if it's a pipeline
from sklearn.pipeline import Pipeline
if isinstance(model, Pipeline):
    print(f"\n🔧 Pipeline steps:")
    for name, step in model.steps:
        print(f"  - {name}: {type(step).__name__}")
    
    # Get the final estimator
    final_estimator = model.steps[-1][1]
    print(f"\n🎯 Estimador final: {type(final_estimator).__name__}")
    
    # Check if it has coefficients
    if hasattr(final_estimator, 'coef_'):
        coef = final_estimator.coef_
        print(f"\n📈 Coeficientes del modelo:")
        print(f"  Shape: {coef.shape}")
        print(f"  Valores:")
        for i, (feat, c) in enumerate(zip(model.feature_names_in_, coef)):
            print(f"    {feat:20s}: {c:12.6f}")
    
    # Check intercept
    if hasattr(final_estimator, 'intercept_'):
        print(f"\n📍 Intercept: {final_estimator.intercept_}")

# Test prediction with different inputs
print("\n" + "="*70)
print("🧪 PRUEBA DE PREDICCIÓN")
print("="*70)

test_cases = [
    {
        "name": "Caso Bajo",
        "data": {
            'open': 2500.00,
            'high': 2550.00,
            'low': 2450.00,
            'volume': 500_000_000,
            'market_cap': 40_000_000_000,
            'lag_1': 2480.00,
            'lag_7': 2400.00,
            'rolling_mean_7': 2450.00
        }
    },
    {
        "name": "Caso Alto",
        "data": {
            'open': 45000.00,
            'high': 48000.00,
            'low': 44000.00,
            'volume': 3_500_000_000,
            'market_cap': 850_000_000_000,
            'lag_1': 44500.00,
            'lag_7': 42000.00,
            'rolling_mean_7': 43500.00
        }
    },
    {
        "name": "Caso Medio",
        "data": {
            'open': 8500.00,
            'high': 8800.00,
            'low': 8300.00,
            'volume': 1_200_000_000,
            'market_cap': 150_000_000_000,
            'lag_1': 8450.00,
            'lag_7': 8200.00,
            'rolling_mean_7': 8400.00
        }
    }
]

predictions = []
for case in test_cases:
    df = pd.DataFrame([case['data']])
    pred = model.predict(df)[0]
    predictions.append(pred)
    print(f"\n{case['name']}:")
    print(f"  Predicción: ${pred:,.2f}")

print("\n" + "="*70)
print("📊 COMPARACIÓN DE PREDICCIONES")
print("="*70)
print(f"Bajo:  ${predictions[0]:,.2f}")
print(f"Medio: ${predictions[1]:,.2f}")
print(f"Alto:  ${predictions[2]:,.2f}")

# Check if they're all the same
if len(set([round(p, 2) for p in predictions])) == 1:
    print("\n⚠️  PROBLEMA: Todas las predicciones son IDÉNTICAS!")
    print("   El modelo NO está respondiendo a cambios en las variables.")
    print("\n💡 Posibles causas:")
    print("   1. El modelo está predeciendo una constante (coeficientes ~ 0)")
    print("   2. El preprocessing normaliza todo a los mismos valores")
    print("   3. El modelo está roto o mal entrenado")
else:
    print("\n✅ Las predicciones varían correctamente")
    print(f"   Rango: ${min(predictions):,.2f} - ${max(predictions):,.2f}")
