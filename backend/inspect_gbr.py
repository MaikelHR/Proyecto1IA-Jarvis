"""Inspect GradientBoostingRegressor internals."""

import pickle
from pathlib import Path

# Load model
model_path = Path("reports/bitcoin_price_training_model.pkl")
model = pickle.load(open(model_path, 'rb'))

print("="*70)
print("🔍 ANÁLISIS DEL GRADIENT BOOSTING REGRESSOR")
print("="*70)

# Get estimator
estimator = model.named_steps['model']

print(f"\nTipo: {type(estimator)}")
print(f"Número de estimators: {estimator.n_estimators}")
print(f"Learning rate: {estimator.learning_rate}")
print(f"Max depth: {estimator.max_depth}")

# Check if it's fitted
if hasattr(estimator, 'estimators_'):
    print(f"\n✅ Modelo está entrenado (fitted)")
    print(f"   Número de árboles construidos: {len(estimator.estimators_)}")
    
    # Check init estimator
    if hasattr(estimator, 'init_'):
        print(f"   Init estimator: {type(estimator.init_)}")
        print(f"   Init value: {estimator.init_.constant_}")
        
        # THIS IS THE PROBLEM!
        if len(estimator.estimators_) == 0:
            print("\n⚠️  PROBLEMA: No hay árboles entrenados!")
            print("   El modelo solo predice el valor inicial constante.")
else:
    print("\n❌ Modelo NO está entrenado")

# Check training data info
print(f"\n📊 Features usados en entrenamiento: {len(estimator.feature_names_in_)}")
print(f"   {estimator.feature_names_in_}")

# Check loss function
print(f"\n📉 Función de pérdida: {estimator.loss}")

# Check train score
if hasattr(estimator, 'train_score_'):
    print(f"\n📈 Train scores shape: {estimator.train_score_.shape}")
    print(f"   Primeros 10: {estimator.train_score_[:10]}")
    print(f"   Últimos 10: {estimator.train_score_[-10:]}")
