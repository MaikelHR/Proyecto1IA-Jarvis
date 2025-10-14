"""Ver qué columnas espera el modelo de telco_churn."""

import pickle
import pandas as pd

# Cargar el modelo
with open('reports/telco_churn_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("=" * 80)
print(" COLUMNAS QUE ESPERA EL MODELO DE TELCO_CHURN")
print("=" * 80)
print()

# Ver las columnas que espera el modelo
if hasattr(model, 'feature_names_in_'):
    print("Columnas esperadas por el modelo:")
    print()
    for i, col in enumerate(model.feature_names_in_, 1):
        print(f"{i:2d}. {col}")
    print()
    print(f"Total: {len(model.feature_names_in_)} columnas")
else:
    print("El modelo no tiene información de feature_names_in_")
    print("Tipo de modelo:", type(model))

print()
print("=" * 80)

# Leer el CSV original para comparar
df = pd.read_csv('data/raw/telco_churn.csv')
print(" COLUMNAS EN EL CSV ORIGINAL")
print("=" * 80)
print()

for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print()
print(f"Total: {len(df.columns)} columnas")
print()

# Ver si hay diferencias
if hasattr(model, 'feature_names_in_'):
    model_cols = set(model.feature_names_in_)
    csv_cols = set(df.columns) - {'Churn'}  # Excluir la columna target
    
    print("=" * 80)
    print(" ANÁLISIS DE DIFERENCIAS")
    print("=" * 80)
    print()
    
    only_in_model = model_cols - csv_cols
    only_in_csv = csv_cols - model_cols
    
    if only_in_model:
        print("❌ Columnas que el modelo espera pero NO están en CSV:")
        for col in sorted(only_in_model):
            print(f"   • {col}")
        print()
    
    if only_in_csv:
        print("⚠️  Columnas en CSV que el modelo NO espera:")
        for col in sorted(only_in_csv):
            print(f"   • {col}")
        print()
    
    if not only_in_model and not only_in_csv:
        print("✅ Las columnas coinciden perfectamente")
