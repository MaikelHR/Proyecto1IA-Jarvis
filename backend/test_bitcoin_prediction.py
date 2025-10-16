"""Test Bitcoin prediction with different values."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from api.services.model_service import model_service

# Test Case 1: Precio BAJO (dentro del rango de entrenamiento)
print("\n" + "="*60)
print("CASO 1: Precio BAJO (era 2014)")
print("="*60)
features_low = {
    "Open": 250.00,
    "High": 265.00,
    "Low": 240.00,
    "Volume": 15000000,
    "Market Cap": 3500000000,
    "lag_1": 245.00,
    "lag_7": 230.00,
    "rolling_mean_7": 240.00
}

print("\n📥 Features enviados:")
for key, value in features_low.items():
    print(f"  {key}: {value}")

prediction_low, confidence_low = model_service.predict("bitcoin_price", features_low)
print(f"\n✅ Predicción: ${prediction_low:,.2f}")

# Test Case 2: Precio ALTO (dentro del rango de entrenamiento)
print("\n" + "="*60)
print("CASO 2: Precio ALTO (pico 2017)")
print("="*60)
features_high = {
    "Open": 2500.00,
    "High": 2550.00,
    "Low": 2450.00,
    "Volume": 800000000,
    "Market Cap": 40000000000,
    "lag_1": 2480.00,
    "lag_7": 2400.00,
    "rolling_mean_7": 2450.00
}

print("\n📥 Features enviados:")
for key, value in features_high.items():
    print(f"  {key}: {value}")

prediction_high, confidence_high = model_service.predict("bitcoin_price", features_high)
print(f"\n✅ Predicción: ${prediction_high:,.2f}")

# Compare
print("\n" + "="*60)
print("COMPARACIÓN")
print("="*60)
print(f"Precio BAJO:  ${prediction_low:,.2f}")
print(f"Precio ALTO:  ${prediction_high:,.2f}")
print(f"Diferencia:   ${abs(prediction_high - prediction_low):,.2f}")
print(f"Factor:       {prediction_high / prediction_low:.2f}x")

if abs(prediction_high - prediction_low) < 1000:
    print("\n⚠️  PROBLEMA: Las predicciones son muy similares!")
else:
    print("\n✅ Las predicciones varían correctamente")
