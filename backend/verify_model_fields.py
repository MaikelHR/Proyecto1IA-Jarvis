"""Verify all model field names match expected format."""

import pickle
from pathlib import Path

models_to_check = {
    'bitcoin_price': 'bitcoin_price_training_model.pkl',
    'avocado_prices': 'avocado_model.pkl',
    'body_fat': 'bodyfat_model.pkl',
    'car_prices': 'car_prices_model.pkl',
    'telco_churn': 'telco_churn_model.pkl',
    'wine_quality': 'winequality_model.pkl',
    'stroke_risk': 'healthcare_stroke_data_model.pkl',
    'hepatitis_c': 'hepatitis_c_data_model.pkl',
    'cirrhosis_status': 'cirrhosis_model.pkl'
}

print("="*80)
print("🔍 VERIFICACIÓN DE CAMPOS DE MODELOS")
print("="*80)

for model_name, model_file in models_to_check.items():
    model_path = Path(f"reports/{model_file}")
    
    if not model_path.exists():
        print(f"\n❌ {model_name}: Archivo no encontrado ({model_file})")
        continue
    
    try:
        model = pickle.load(open(model_path, 'rb'))
        
        if hasattr(model, 'feature_names_in_'):
            features = model.feature_names_in_
        else:
            features = "No disponible (no es Pipeline sklearn)"
        
        print(f"\n✅ {model_name}:")
        print(f"   Archivo: {model_file}")
        if isinstance(features, str):
            print(f"   Features: {features}")
        else:
            print(f"   Features ({len(features)}):")
            for feat in features:
                # Check if field name has uppercase or mixed case
                if feat != feat.lower():
                    print(f"      ⚠️  {feat} (contiene mayúsculas)")
                else:
                    print(f"      ✓ {feat}")
    except Exception as e:
        print(f"\n❌ {model_name}: Error al cargar - {e}")

print("\n" + "="*80)
print("RESUMEN")
print("="*80)
print("Todos los campos deben estar en snake_case (minúsculas con guiones bajos)")
print("Ejemplo: 'car_name', 'monthly_charges', 'fixed_acidity'")
