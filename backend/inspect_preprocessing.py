"""Inspect Bitcoin model preprocessing."""

import pickle
from pathlib import Path
import numpy as np
import pandas as pd

# Load model
model_path = Path("reports/bitcoin_price_training_model.pkl")
model = pickle.load(open(model_path, 'rb'))

print("="*70)
print("🔍 ANÁLISIS DEL PREPROCESSING")
print("="*70)

# Get preprocessor
preprocessor = model.named_steps['preprocessor']
print(f"\n📋 Tipo de preprocessor: {type(preprocessor)}")
print(f"\n🔧 Transformers:")
for name, transformer, columns in preprocessor.transformers_:
    print(f"\n  {name}:")
    print(f"    Transformer: {type(transformer).__name__}")
    print(f"    Columns: {columns}")
    
    # Check if it's a pipeline
    from sklearn.pipeline import Pipeline
    if isinstance(transformer, Pipeline):
        print(f"    Steps:")
        for step_name, step in transformer.steps:
            print(f"      - {step_name}: {type(step).__name__}")
            # If it's a scaler, check its properties
            if hasattr(step, 'mean_'):
                print(f"        Mean: {step.mean_}")
            if hasattr(step, 'scale_'):
                print(f"        Scale: {step.scale_}")

# Test transformation
print("\n" + "="*70)
print("🧪 PRUEBA DE TRANSFORMACIÓN")
print("="*70)

test_data = pd.DataFrame([{
    'open': 2500.00,
    'high': 2550.00,
    'low': 2450.00,
    'volume': 500_000_000,
    'market_cap': 40_000_000_000,
    'lag_1': 2480.00,
    'lag_7': 2400.00,
    'rolling_mean_7': 2450.00
}])

print("\n📥 Datos originales:")
print(test_data)

# Transform
X_transformed = preprocessor.transform(test_data)
print(f"\n📊 Datos transformados:")
print(f"  Shape: {X_transformed.shape}")
print(f"  Values: {X_transformed}")

# Test with different data
test_data2 = pd.DataFrame([{
    'open': 45000.00,
    'high': 48000.00,
    'low': 44000.00,
    'volume': 3_500_000_000,
    'market_cap': 850_000_000_000,
    'lag_1': 44500.00,
    'lag_7': 42000.00,
    'rolling_mean_7': 43500.00
}])

print("\n📥 Datos originales 2:")
print(test_data2)

X_transformed2 = preprocessor.transform(test_data2)
print(f"\n📊 Datos transformados 2:")
print(f"  Shape: {X_transformed2.shape}")
print(f"  Values: {X_transformed2}")

# Compare
print("\n" + "="*70)
print("📊 COMPARACIÓN")
print("="*70)
print(f"Datos 1: {X_transformed}")
print(f"Datos 2: {X_transformed2}")

if np.allclose(X_transformed, X_transformed2):
    print("\n⚠️  PROBLEMA: Los datos transformados son IDÉNTICOS!")
    print("   El preprocessor está normalizando todo a los mismos valores.")
else:
    print("\n✅ Los datos transformados son diferentes")

# Get final estimator and predict
print("\n" + "="*70)
print("🎯 PREDICCIÓN CON MODELO")
print("="*70)

estimator = model.named_steps['model']
pred1 = estimator.predict(X_transformed)
pred2 = estimator.predict(X_transformed2)

print(f"Predicción 1: ${pred1[0]:,.2f}")
print(f"Predicción 2: ${pred2[0]:,.2f}")

if np.isclose(pred1[0], pred2[0]):
    print("\n⚠️  Las predicciones son idénticas incluso con datos diferentes!")
else:
    print("\n✅ Las predicciones varían correctamente")
