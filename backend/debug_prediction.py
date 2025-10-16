"""Debug prediction step by step."""

import pickle
from pathlib import Path
import numpy as np
import pandas as pd

# Load model
model_path = Path("reports/bitcoin_price_training_model.pkl")
model = pickle.load(open(model_path, 'rb'))

# Prepare test data
test_low = pd.DataFrame([{
    'open': 2500.00,
    'high': 2550.00,
    'low': 2450.00,
    'volume': 500_000_000,
    'market_cap': 40_000_000_000,
    'lag_1': 2480.00,
    'lag_7': 2400.00,
    'rolling_mean_7': 2450.00
}])

test_high = pd.DataFrame([{
    'open': 45000.00,
    'high': 48000.00,
    'low': 44000.00,
    'volume': 3_500_000_000,
    'market_cap': 850_000_000_000,
    'lag_1': 44500.00,
    'lag_7': 42000.00,
    'rolling_mean_7': 43500.00
}])

print("="*70)
print("🔍 DEBUG PREDICCIÓN PASO A PASO")
print("="*70)

# Step 1: Preprocessing
preprocessor = model.named_steps['preprocessor']
X_low_transformed = preprocessor.transform(test_low)
X_high_transformed = preprocessor.transform(test_high)

print("\n📊 PASO 1: Preprocessing")
print(f"Bajo transformado:  {X_low_transformed}")
print(f"Alto transformado:  {X_high_transformed}")

# Step 2: Model prediction
estimator = model.named_steps['model']

# Get base prediction
base_pred = estimator.init_.predict(X_low_transformed)
print(f"\n📍 PASO 2: Predicción base (init)")
print(f"Base prediction: {base_pred}")

# Get full prediction
pred_low = estimator.predict(X_low_transformed)
pred_high = estimator.predict(X_high_transformed)

print(f"\n🎯 PASO 3: Predicción final")
print(f"Predicción baja:  ${pred_low[0]:,.2f}")
print(f"Predicción alta:  ${pred_high[0]:,.2f}")

# Use the pipeline
print(f"\n📦 PASO 4: Predicción con pipeline completo")
pred_low_pipeline = model.predict(test_low)
pred_high_pipeline = model.predict(test_high)
print(f"Predicción baja:  ${pred_low_pipeline[0]:,.2f}")
print(f"Predicción alta:  ${pred_high_pipeline[0]:,.2f}")

# Check if there's an inverse transformation issue
print("\n" + "="*70)
print("🔍 VERIFICACIÓN DE SCALER")
print("="*70)

# Get the scaler
num_transformer = preprocessor.named_transformers_['num']
scaler = num_transformer.named_steps['scaler']

print(f"Scaler mean: {scaler.mean_}")
print(f"Scaler scale: {scaler.scale_}")

# Manually transform and predict
print("\n🧪 Transformación manual:")
print(f"Open bajo (2500) → {(2500 - scaler.mean_[0]) / scaler.scale_[0]:.4f}")
print(f"Open alto (45000) → {(45000 - scaler.mean_[0]) / scaler.scale_[0]:.4f}")
