"""Retrain Bitcoin model."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.dataset_registry import get_dataset
from src.data_analysis import summarize_dataset
from src.modeling import train_dataset, save_model_result

print("="*70)
print("🔄 REENTRENANDO MODELO DE BITCOIN")
print("="*70)

# Get dataset
dataset = get_dataset('bitcoin_price')
print(f"\n📊 Dataset: {dataset.name}")
print(f"📁 Archivo: {dataset.filename}")

# Summarize
print("\n1️⃣ Generando resumen del dataset...")
summary_path = summarize_dataset(dataset)
print(f"✅ Resumen guardado en: {summary_path}")

# Train
print("\n2️⃣ Entrenando modelo...")
result = train_dataset(dataset)
print(f"✅ Modelo entrenado")
print(f"   Resultado: {result}")

# Save
print("\n3️⃣ Guardando modelo y métricas...")
metrics_path = save_model_result(result)
print(f"✅ Métricas guardadas en: {metrics_path}")

print("\n" + "="*70)
print("✅ REENTRENAMIENTO COMPLETADO")
print("="*70)
