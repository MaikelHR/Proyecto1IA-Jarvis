"""
Script para obtener las columnas exactas que espera cada modelo entrenado.
Genera los ejemplos JSON correctos en snake_case para cada uno de los 9 modelos.
"""
import joblib
import json
from pathlib import Path

def get_model_columns(model_path):
    """Obtiene las columnas que espera un modelo."""
    try:
        model = joblib.load(model_path)
        
        # Si es un Pipeline, obtener el transformador
        if hasattr(model, 'named_steps'):
            if 'preprocessor' in model.named_steps:
                preprocessor = model.named_steps['preprocessor']
                
                # Obtener columnas numéricas y categóricas
                if hasattr(preprocessor, 'transformers_'):
                    num_cols = []
                    cat_cols = []
                    
                    for name, transformer, cols in preprocessor.transformers_:
                        if name == 'num':
                            num_cols = list(cols)
                        elif name == 'cat':
                            cat_cols = list(cols)
                    
                    return num_cols + cat_cols
                    
        return None
    except Exception as e:
        print(f"Error al cargar {model_path}: {e}")
        return None

def get_csv_sample_data(csv_path, columns):
    """Obtiene una fila de ejemplo del CSV con las columnas especificadas."""
    import pandas as pd
    
    try:
        df = pd.read_csv(csv_path)
        
        # Tomar la primera fila
        sample = df.iloc[0]
        
        # Crear diccionario con las columnas del modelo
        result = {}
        for col in columns:
            # Buscar la columna en el CSV (ignorando case y espacios)
            found = False
            for csv_col in df.columns:
                # Normalizar nombres para comparación
                normalized_csv = csv_col.lower().replace(' ', '_').replace('-', '_')
                normalized_model = col.lower().replace(' ', '_').replace('-', '_')
                
                if normalized_csv == normalized_model:
                    value = sample[csv_col]
                    # Convertir a tipos nativos de Python
                    if pd.isna(value):
                        result[col] = None
                    elif isinstance(value, (pd.Int64Dtype, pd.Int32Dtype)):
                        result[col] = int(value)
                    elif isinstance(value, (pd.Float64Dtype, pd.Float32Dtype)):
                        result[col] = float(value)
                    else:
                        result[col] = str(value) if not isinstance(value, (int, float)) else value
                    found = True
                    break
            
            if not found:
                # Si no se encuentra, usar un valor por defecto según el nombre
                if any(x in col.lower() for x in ['id', 'number', 'count', 'age', 'year']):
                    result[col] = 0
                elif any(x in col.lower() for x in ['price', 'rate', 'amount', 'volume', 'acidity', 'density']):
                    result[col] = 0.0
                else:
                    result[col] = "example"
        
        return result
    except Exception as e:
        print(f"Error al leer CSV {csv_path}: {e}")
        return None

# Definir los datasets con sus archivos
datasets = {
    'bitcoin_price': {
        'model': 'reports/precio_histórico_de_bitcoin_metrics.json',
        'csv': 'data/raw/bitcoin_price_training.csv',
        'description': 'Predicción del precio histórico de Bitcoin'
    },
    'avocado_prices': {
        'model': 'reports/precios_de_aguacate_por_región_metrics.json',
        'csv': 'data/raw/avocado.csv',
        'description': 'Predicción de precios de aguacate por región'
    },
    'body_fat': {
        'model': 'reports/porcentaje_de_grasa_corporal_metrics.json',
        'csv': 'data/raw/bodyfat.csv',
        'description': 'Predicción del porcentaje de grasa corporal'
    },
    'car_prices': {
        'model': 'reports/valor_de_automóviles_usados_metrics.json',
        'csv': 'data/raw/car_prices.csv',
        'description': 'Predicción del valor de automóviles usados'
    },
    'telco_churn': {
        'model': 'reports/churn_de_clientes_telco_metrics.json',
        'csv': 'data/raw/telco_churn.csv',
        'description': 'Predicción de churn de clientes de telecomunicaciones'
    },
    'wine_quality': {
        'model': 'reports/calidad_de_vinos_metrics.json',
        'csv': 'data/raw/winequality.csv',
        'description': 'Predicción de la calidad de vinos'
    },
    'stroke_risk': {
        'model': 'reports/predicción_de_derrame_cerebral_metrics.json',
        'csv': 'data/raw/healthcare_stroke_data.csv',
        'description': 'Predicción del riesgo de derrame cerebral'
    },
    'hepatitis_c': {
        'model': 'reports/diagnóstico_de_hepatitis_c_metrics.json',
        'csv': 'data/raw/hepatitis_c_data.csv',
        'description': 'Diagnóstico de hepatitis C'
    },
    'cirrhosis_status': {
        'model': 'reports/estatus_clínico_de_cirrosis_metrics.json',
        'csv': 'data/raw/cirrhosis.csv',
        'description': 'Predicción del estatus clínico de cirrosis'
    }
}

print("=" * 80)
print("OBTENIENDO COLUMNAS Y EJEMPLOS PARA LOS 9 MODELOS")
print("=" * 80)

all_examples = {}

for dataset_key, info in datasets.items():
    print(f"\n{'='*80}")
    print(f"📊 Dataset: {dataset_key}")
    print(f"📝 Descripción: {info['description']}")
    print(f"{'='*80}")
    
    # Cargar las métricas para obtener la ruta del modelo
    try:
        with open(info['model'], 'r', encoding='utf-8') as f:
            metrics = json.load(f)
            model_path = metrics.get('model_path')
            
            if model_path and Path(model_path).exists():
                print(f"✅ Modelo encontrado: {model_path}")
                
                # Obtener columnas del modelo
                columns = get_model_columns(model_path)
                
                if columns:
                    print(f"\n📋 Columnas esperadas por el modelo ({len(columns)}):")
                    for i, col in enumerate(columns, 1):
                        print(f"   {i}. {col}")
                    
                    # Obtener datos de ejemplo del CSV
                    if Path(info['csv']).exists():
                        sample_data = get_csv_sample_data(info['csv'], columns)
                        
                        if sample_data:
                            print(f"\n💡 Ejemplo JSON para predicción:")
                            example_json = {
                                "features": sample_data
                            }
                            print(json.dumps(example_json, indent=2, ensure_ascii=False))
                            
                            # Guardar para documentación
                            all_examples[dataset_key] = {
                                'description': info['description'],
                                'columns': columns,
                                'example': example_json
                            }
                    else:
                        print(f"⚠️  CSV no encontrado: {info['csv']}")
                else:
                    print("❌ No se pudieron obtener las columnas del modelo")
            else:
                print(f"❌ Modelo no encontrado: {model_path}")
    except Exception as e:
        print(f"❌ Error al procesar {dataset_key}: {e}")

# Guardar todos los ejemplos en un archivo JSON
output_file = 'ejemplos_modelos_actualizados.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_examples, f, indent=2, ensure_ascii=False)

print(f"\n{'='*80}")
print(f"✅ Ejemplos guardados en: {output_file}")
print(f"{'='*80}")
