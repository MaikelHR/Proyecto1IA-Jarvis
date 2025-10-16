"""
Analizar el modelo de Telco Churn para entender por qué siempre predice "No"
"""
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Cargar el modelo
model_path = Path("reports/telco_churn_model.pkl")

if not model_path.exists():
    print(f"❌ Modelo no encontrado en: {model_path}")
    exit(1)

with open(model_path, "rb") as f:
    pipeline = pickle.load(f)

print("="*70)
print("📊 ANÁLISIS DEL MODELO TELCO CHURN")
print("="*70)

# Información del pipeline
print(f"\n🔧 Pipeline steps:")
for i, (name, transformer) in enumerate(pipeline.steps):
    print(f"   {i+1}. {name}: {type(transformer).__name__}")

# Obtener el modelo final
model = pipeline.named_steps.get('model') or pipeline.steps[-1][1]
print(f"\n🤖 Modelo final: {type(model).__name__}")

# Verificar si tiene feature_importances
if hasattr(model, 'feature_importances_'):
    print(f"\n📈 Feature importances shape: {model.feature_importances_.shape}")
    print(f"   Top 5 features más importantes:")
    
    # Necesitamos los nombres de las features después del preprocesamiento
    preprocessor = pipeline.named_steps.get('preprocessor')
    if preprocessor:
        # Intentar obtener nombres de features
        try:
            if hasattr(preprocessor, 'get_feature_names_out'):
                feature_names = preprocessor.get_feature_names_out()
            else:
                feature_names = [f"feature_{i}" for i in range(len(model.feature_importances_))]
            
            importances = sorted(
                zip(feature_names, model.feature_importances_),
                key=lambda x: x[1],
                reverse=True
            )
            
            for name, importance in importances[:10]:
                print(f"      {name:40s}: {importance:.4f}")
        except Exception as e:
            print(f"   ⚠️  No se pudieron obtener nombres: {e}")

# Verificar clases
if hasattr(model, 'classes_'):
    print(f"\n🏷️  Clases del modelo: {model.classes_}")

# Hacer predicciones de prueba con casos extremos
print(f"\n{'='*70}")
print("🧪 PRUEBAS CON CASOS EXTREMOS")
print('='*70)

# Cargar datos reales
df = pd.read_csv("data/raw/telco_churn.csv")

# Normalizar nombres de columnas
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# Caso 1: Cliente que SÍ hizo churn en los datos reales
churned = df[df['churn'] == 'Yes'].iloc[0:5]
print(f"\n1️⃣  Cliente que SÍ abandonó (del dataset real):")

for idx in range(min(5, len(churned))):
    row = churned.iloc[idx]
    features = row.drop(['churn', 'customerid']).to_dict()
    
    # Limpiar el dict para la predicción
    features_clean = {k: v for k, v in features.items() if pd.notna(v)}
    
    try:
        df_test = pd.DataFrame([features_clean])
        prediction = pipeline.predict(df_test)[0]
        proba = pipeline.predict_proba(df_test)[0] if hasattr(pipeline, 'predict_proba') else None
        
        print(f"   Predicción: {prediction}", end="")
        if proba is not None:
            print(f" (probabilidades: No={proba[0]:.3f}, Yes={proba[1]:.3f})")
        else:
            print()
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Caso 2: Cliente que NO hizo churn
not_churned = df[df['churn'] == 'No'].iloc[0:5]
print(f"\n2️⃣  Cliente que NO abandonó (del dataset real):")

for idx in range(min(5, len(not_churned))):
    row = not_churned.iloc[idx]
    features = row.drop(['churn', 'customerid']).to_dict()
    
    # Limpiar el dict para la predicción
    features_clean = {k: v for k, v in features.items() if pd.notna(v)}
    
    try:
        df_test = pd.DataFrame([features_clean])
        prediction = pipeline.predict(df_test)[0]
        proba = pipeline.predict_proba(df_test)[0] if hasattr(pipeline, 'predict_proba') else None
        
        print(f"   Predicción: {prediction}", end="")
        if proba is not None:
            print(f" (probabilidades: No={proba[0]:.3f}, Yes={proba[1]:.3f})")
        else:
            print()
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n{'='*70}")
print("🎯 CONCLUSIONES")
print('='*70)

# Hacer predicción sobre todo el dataset de test
from sklearn.model_selection import train_test_split

X = df.drop(['churn', 'customerid'], axis=1)
y = df['churn']

_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

try:
    y_pred = pipeline.predict(X_test)
    
    unique_predictions = np.unique(y_pred)
    print(f"\nPredicciones únicas en test set: {unique_predictions}")
    
    from collections import Counter
    pred_counts = Counter(y_pred)
    print(f"\nDistribución de predicciones:")
    for pred, count in pred_counts.items():
        pct = (count / len(y_pred)) * 100
        print(f"   {pred}: {count} ({pct:.1f}%)")
    
    if len(unique_predictions) == 1:
        print(f"\n❌ PROBLEMA CONFIRMADO: El modelo solo predice '{unique_predictions[0]}'")
        print("   Este es un problema de entrenamiento del modelo.")
    else:
        print(f"\n✅ El modelo hace {len(unique_predictions)} predicciones diferentes")
        
        # Calcular accuracy
        from sklearn.metrics import accuracy_score, classification_report
        acc = accuracy_score(y_test, y_pred)
        print(f"\n📊 Accuracy en test set: {acc:.3f}")
        
        print(f"\n📊 Classification Report:")
        print(classification_report(y_test, y_pred))
        
except Exception as e:
    print(f"\n❌ Error al hacer predicciones: {e}")
    import traceback
    traceback.print_exc()
