"""Check training data for Bitcoin."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.dataset_registry import get_dataset
from src.modeling import _prepare_time_series_features

dataset = get_dataset('bitcoin_price')
df = dataset.load_dataframe()

print("="*70)
print("🔍 ANÁLISIS DE DATOS DE ENTRENAMIENTO")
print("="*70)

print(f"\n📊 Dataset original:")
print(f"   Shape: {df.shape}")
print(f"   Columnas: {df.columns.tolist()}")

print(f"\n🎯 Target ('close') stats:")
print(df['close'].describe())

# Prepare features
X, y = _prepare_time_series_features(df, dataset)

print(f"\n📊 Después de preparar features:")
print(f"   X shape: {X.shape}")
print(f"   y shape: {y.shape}")
print(f"   X columns: {X.columns.tolist()}")

print(f"\n🎯 Target (y) después de lag:")
print(y.describe())

# Check correlation between features and target
print(f"\n📈 Correlación de features con target:")
correlations = X.join(y).corr()['close'].sort_values(ascending=False)
print(correlations)

# Check a few samples
print(f"\n📋 Primeras 5 filas de X:")
print(X.head())

print(f"\n📋 Primeras 5 valores de y:")
print(y.head())

# Check if there's variance in the data
print(f"\n📊 Varianza de cada feature:")
print(X.var())

# Split as the model does
split_index = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

print(f"\n✂️  Split:")
print(f"   Train: {len(X_train)} filas")
print(f"   Test: {len(X_test)} filas")

print(f"\n🎯 y_train stats:")
print(y_train.describe())

print(f"\n🎯 y_test stats:")
print(y_test.describe())

# Check if test data is very different from train
print(f"\n⚠️  Diferencia train vs test:")
print(f"   Train mean: ${y_train.mean():.2f}")
print(f"   Test mean: ${y_test.mean():.2f}")
print(f"   Train max: ${y_train.max():.2f}")
print(f"   Test max: ${y_test.max():.2f}")
