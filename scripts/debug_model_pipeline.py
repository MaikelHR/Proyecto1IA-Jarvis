"""
Investigar a fondo qué está pasando con el pipeline del modelo.
"""

import pickle
import pandas as pd
import json
from sklearn.pipeline import Pipeline

print("=" * 80)
print(" ANÁLISIS PROFUNDO DEL MODELO WINE_QUALITY")
print("=" * 80)
print()

# Cargar modelo
with open('reports/winequality_model.pkl', 'rb') as f:
    model = pickle.load(f)

print(f"Tipo de modelo: {type(model)}")
print()

# Ver estructura del pipeline
if isinstance(model, Pipeline):
    print("Pasos del pipeline:")
    for i, (name, step) in enumerate(model.steps, 1):
        print(f"  {i}. {name}: {type(step).__name__}")
    print()
    
    # Ver el transformador de columnas
    if hasattr(model, 'named_steps'):
        if 'columntransformer' in model.named_steps:
            ct = model.named_steps['columntransformer']
            print("ColumnTransformer:")
            print(f"  Tipo: {type(ct)}")
            
            if hasattr(ct, 'transformers_'):
                print(f"  Transformers: {len(ct.transformers_)}")
                for name, transformer, cols in ct.transformers_:
                    print(f"    • {name}: {cols}")
            print()

# Intentar crear DataFrame y ver qué pasa
print("=" * 80)
print(" PRUEBA DE CONVERSIÓN")
print("=" * 80)
print()

features = {
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

print("Features originales:")
print(json.dumps(features, indent=2))
print()

df = pd.DataFrame([features])
print("DataFrame creado:")
print(df.dtypes)
print()
print(df)
print()

# Ver qué columnas tiene el DataFrame
print(f"Columnas en DataFrame: {df.columns.tolist()}")
print(f"Columnas esperadas:    {list(model.feature_names_in_)}")
print()

# Ver diferencias
df_cols = set(df.columns)
model_cols = set(model.feature_names_in_)

missing = model_cols - df_cols
extra = df_cols - model_cols

if missing:
    print(f"❌ Faltan en DataFrame: {missing}")
if extra:
    print(f"⚠️  Columnas extra: {extra}")
if not missing and not extra:
    print("✅ Las columnas coinciden perfectamente")

print()
print("=" * 80)
print(" INTENTANDO PREDICCIÓN")
print("=" * 80)
print()

try:
    # Asegurarse que las columnas estén en el orden correcto
    df_ordered = df[model.feature_names_in_]
    print("DataFrame reordenado:")
    print(df_ordered.columns.tolist())
    print()
    
    prediction = model.predict(df_ordered)
    print(f"✅ PREDICCIÓN EXITOSA: {prediction[0]}")
    
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(df_ordered)[0]
        print(f"   Confianza: {max(proba):.2%}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()
    import traceback
    traceback.print_exc()
