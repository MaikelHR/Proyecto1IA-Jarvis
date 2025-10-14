"""
Quick test to verify model loading paths
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("=" * 60)
print("🔍 VERIFICACIÓN DE PATHS")
print("=" * 60)

# Test 1: Verificar estructura de directorios
print("\n1. Estructura de directorios:")
print(f"   Backend dir: {backend_dir}")
print(f"   Existe: {backend_dir.exists()}")

data_dir = backend_dir / "data" / "raw"
print(f"\n   Data dir: {data_dir}")
print(f"   Existe: {data_dir.exists()}")

reports_dir = backend_dir / "reports"
print(f"\n   Reports dir: {reports_dir}")
print(f"   Existe: {reports_dir.exists()}")

# Test 2: Listar archivos CSV
print("\n2. Archivos CSV encontrados:")
if data_dir.exists():
    csv_files = list(data_dir.glob("*.csv"))
    for csv in csv_files:
        print(f"   ✓ {csv.name}")
else:
    print("   ✗ Directorio no existe")

# Test 3: Listar modelos PKL
print("\n3. Modelos PKL encontrados:")
if reports_dir.exists():
    pkl_files = list(reports_dir.glob("*_model.pkl"))
    for pkl in pkl_files:
        print(f"   ✓ {pkl.name}")
else:
    print("   ✗ Directorio no existe")

# Test 4: Intentar importar dataset_registry
print("\n4. Test de importación:")
try:
    from src.dataset_registry import iter_datasets, DatasetInfo
    print("   ✓ dataset_registry importado correctamente")
    
    print("\n5. Datasets registrados:")
    for dataset_info in iter_datasets():
        print(f"   ✓ {dataset_info.name}")
        print(f"      - Archivo: {dataset_info.filename}")
        print(f"      - Path completo: {dataset_info.path}")
        print(f"      - Existe: {dataset_info.path.exists()}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Intentar cargar ModelService
print("\n6. Test de ModelService:")
try:
    from api.services.model_service import ModelService
    print("   ✓ ModelService importado correctamente")
    
    service = ModelService()
    models = service.get_available_models()
    print(f"\n   Modelos cargados: {len(models)}")
    for model_key in models:
        info = service.get_model_info(model_key)
        print(f"   ✓ {model_key} -> {info.name if info else 'N/A'}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 60)
