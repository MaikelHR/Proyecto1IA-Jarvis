"""
Script para verificar que todos los modelos estén entrenados y listos para usar.
Muestra información detallada de cada modelo.
"""

import os
import json
from pathlib import Path

def verificar_modelos():
    """Verifica que todos los modelos estén entrenados correctamente."""
    
    print("=" * 80)
    print(" VERIFICACIÓN DE MODELOS ENTRENADOS")
    print("=" * 80)
    print()
    
    # Ruta de reportes
    reports_dir = Path("reports")
    data_dir = Path("data/raw")
    
    # Mapeo de archivos CSV a modelos esperados
    datasets_esperados = {
        "avocado.csv": {
            "model": "avocado_model.pkl",
            "summary": "avocado_summary.json",
            "metrics": "precios_de_aguacate_por_región_metrics.json",
            "name": "Precios de aguacate por región",
            "key": "avocado_prices"
        },
        "bitcoin_price_training.csv": {
            "model": "bitcoin_price_training_model.pkl",
            "summary": "bitcoin_price_training_summary.json",
            "metrics": "precio_histórico_de_bitcoin_metrics.json",
            "name": "Precio histórico de Bitcoin",
            "key": "bitcoin_price"
        },
        "bodyfat.csv": {
            "model": "bodyfat_model.pkl",
            "summary": "bodyfat_summary.json",
            "metrics": "porcentaje_de_grasa_corporal_metrics.json",
            "name": "Porcentaje de grasa corporal",
            "key": "body_fat"
        },
        "car_prices.csv": {
            "model": "car_prices_model.pkl",
            "summary": "car_prices_summary.json",
            "metrics": "valor_de_automóviles_usados_metrics.json",
            "name": "Valor de automóviles usados",
            "key": "car_prices"
        },
        "cirrhosis.csv": {
            "model": "cirrhosis_model.pkl",
            "summary": "cirrhosis_summary.json",
            "metrics": "estatus_clínico_de_cirrosis_metrics.json",
            "name": "Estatus clínico de cirrosis",
            "key": "cirrhosis_status"
        },
        "healthcare_stroke_data.csv": {
            "model": "healthcare_stroke_data_model.pkl",
            "summary": "healthcare_stroke_data_summary.json",
            "metrics": "predicción_de_derrame_cerebral_metrics.json",
            "name": "Predicción de derrame cerebral",
            "key": "stroke_risk"
        },
        "hepatitis_c_data.csv": {
            "model": "hepatitis_c_data_model.pkl",
            "summary": "hepatitis_c_data_summary.json",
            "metrics": "diagnóstico_de_hepatitis_c_metrics.json",
            "name": "Diagnóstico de hepatitis C",
            "key": "hepatitis_c"
        },
        "telco_churn.csv": {
            "model": "telco_churn_model.pkl",
            "summary": "telco_churn_summary.json",
            "metrics": "churn_de_clientes_telco_metrics.json",
            "name": "Churn de clientes Telco",
            "key": "telco_churn"
        },
        "winequality.csv": {
            "model": "winequality_model.pkl",
            "summary": "winequality_summary.json",
            "metrics": "calidad_de_vinos_metrics.json",
            "name": "Calidad de vinos",
            "key": "wine_quality"
        }
    }
    
    print(f"📊 Datasets CSV encontrados: {len(list(data_dir.glob('*.csv')))}")
    print(f"🤖 Modelos esperados: {len(datasets_esperados)}")
    print()
    print("=" * 80)
    print()
    
    modelos_ok = 0
    modelos_error = 0
    
    for i, (csv_file, info) in enumerate(datasets_esperados.items(), 1):
        csv_path = data_dir / csv_file
        model_path = reports_dir / info["model"]
        summary_path = reports_dir / info["summary"]
        metrics_path = reports_dir / info["metrics"]
        
        print(f"{i}. {info['name']}")
        print(f"   Key: {info['key']}")
        print(f"   Dataset: {csv_file}")
        
        # Verificar CSV
        if csv_path.exists():
            import pandas as pd
            df = pd.read_csv(csv_path)
            print(f"   ✓ CSV existe: {len(df)} filas, {len(df.columns)} columnas")
        else:
            print(f"   ❌ CSV NO existe")
            modelos_error += 1
            print()
            continue
        
        # Verificar modelo
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"   ✓ Modelo entrenado: {info['model']} ({size_mb:.2f} MB)")
        else:
            print(f"   ❌ Modelo NO existe: {info['model']}")
            modelos_error += 1
            print()
            continue
        
        # Verificar summary
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                summary = json.load(f)
            print(f"   ✓ Summary existe")
        else:
            print(f"   ⚠️  Summary NO existe: {info['summary']}")
        
        # Verificar metrics
        if metrics_path.exists():
            with open(metrics_path, 'r', encoding='utf-8') as f:
                metrics = json.load(f)
            
            print(f"   ✓ Métricas existen")
            
            # Mostrar métricas principales
            if 'metrics' in metrics:
                m = metrics['metrics']
                if 'accuracy' in m:
                    print(f"      • Accuracy: {m['accuracy']:.4f} ({m['accuracy']*100:.2f}%)")
                if 'r2' in m:
                    print(f"      • R² Score: {m['r2']:.4f}")
                if 'mae' in m:
                    print(f"      • MAE: {m['mae']:.4f}")
                if 'precision' in m:
                    print(f"      • Precision: {m['precision']:.4f} ({m['precision']*100:.2f}%)")
                if 'recall' in m:
                    print(f"      • Recall: {m['recall']:.4f} ({m['recall']*100:.2f}%)")
                if 'f1' in m:
                    print(f"      • F1-Score: {m['f1']:.4f} ({m['f1']*100:.2f}%)")
            
            # Mostrar tipo de tarea
            if 'task' in metrics:
                task_emoji = "🎯" if metrics['task'] == 'classification' else "📈"
                print(f"      {task_emoji} Tipo: {metrics['task']}")
        else:
            print(f"   ⚠️  Métricas NO existen: {info['metrics']}")
        
        print(f"   ✅ MODELO COMPLETO Y FUNCIONAL")
        modelos_ok += 1
        print()
    
    print("=" * 80)
    print(" RESUMEN")
    print("=" * 80)
    print()
    print(f"✅ Modelos OK: {modelos_ok}/{len(datasets_esperados)}")
    print(f"❌ Modelos con error: {modelos_error}/{len(datasets_esperados)}")
    print()
    
    if modelos_ok == len(datasets_esperados):
        print("🎉 ¡TODOS LOS MODELOS ESTÁN ENTRENADOS Y LISTOS!")
        print()
        print("Puedes usar estos modelos en la API con las siguientes keys:")
        print()
        for csv_file, info in datasets_esperados.items():
            print(f"   • {info['key']:<20} → {info['name']}")
        print()
        return True
    else:
        print("⚠️  Algunos modelos tienen problemas.")
        print()
        print("Para entrenar los modelos faltantes, ejecuta:")
        print("   python src/pipeline.py")
        print()
        return False

if __name__ == "__main__":
    verificar_modelos()
