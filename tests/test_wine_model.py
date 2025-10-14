"""Ver columnas del modelo de vinos."""

import pickle
import pandas as pd
import json

print("=" * 80)
print(" MODELO: WINE QUALITY")
print("=" * 80)
print()

# Cargar modelo
with open('reports/winequality_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("Columnas que espera el modelo:")
if hasattr(model, 'feature_names_in_'):
    for i, col in enumerate(model.feature_names_in_, 1):
        print(f"  {i:2d}. {col}")
    print()
    print(f"Total: {len(model.feature_names_in_)} columnas")
else:
    print("  No tiene feature_names_in_")

print()
print("=" * 80)
print(" CSV ORIGINAL")
print("=" * 80)
print()

df = pd.read_csv('data/raw/winequality.csv')
print(f"Columnas en CSV: {len(df.columns)}")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print()
print("=" * 80)
print(" DATOS DE PRUEBA")
print("=" * 80)
print()

# Crear datos de prueba
# Mapeo especial de columnas
column_mapping = {
    'p_h': 'pH',
    'fixed_acidity': 'fixed acidity',
    'volatile_acidity': 'volatile acidity',
    'citric_acid': 'citric acid',
    'residual_sugar': 'residual sugar',
    'free_sulfur_dioxide': 'free sulfur dioxide',
    'total_sulfur_dioxide': 'total sulfur dioxide',
}

features = {}
for col in model.feature_names_in_:
    # Usar mapeo si existe, sino usar el nombre directamente
    csv_col = column_mapping.get(col, col)
    
    if csv_col in df.columns:
        value = df[csv_col].iloc[0]
        # Si es numérico, convertir a float, si no, dejar como string
        if isinstance(value, (int, float)):
            features[col] = float(value)
        else:
            features[col] = str(value)

print("JSON para Swagger:")
print()
print(json.dumps({"features": features}, indent=2))

print()
print("=" * 80)
print(" PRUEBA DIRECTA")
print("=" * 80)
print()

# Probar predicción
df_test = pd.DataFrame([features])
prediction = model.predict(df_test)
print(f"✅ Predicción: {prediction[0]}")

if hasattr(model, 'predict_proba'):
    proba = model.predict_proba(df_test)[0]
    print(f"   Probabilidades: {proba}")
    print(f"   Confianza: {max(proba):.2%}")
