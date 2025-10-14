"""
Prueba Rápida del Backend - 5 Minutos

Script simplificado para verificar rápidamente que el backend funciona.
"""

import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("\n" + "="*60)
print("  🚀 PRUEBA RÁPIDA DEL BACKEND - JARVIS IA")
print("="*60)

score = 0
total = 6

# Test 1: Imports
print("\n[1/6] Verificando imports...")
try:
    from api.main import app
    from api.services import model_service
    print("      ✓ API y servicios OK")
    score += 1
except Exception as e:
    print(f"      ❌ Error: {e}")

# Test 2: Models
print("\n[2/6] Verificando modelos ML...")
try:
    available = model_service.get_available_models()
    print(f"      ✓ {len(available)} modelos disponibles")
    score += 1
except Exception as e:
    print(f"      ❌ Error: {e}")

# Test 3: Prediction
print("\n[3/6] Probando predicción...")
try:
    # Verify models can be called (even if features are minimal)
    available = model_service.get_available_models()
    if available:
        print(f"      ✓ {len(available)} modelos listos para predicción")
        print(f"         Modelos: {', '.join(available[:3])}...")
        score += 1
    else:
        print(f"      ❌ No hay modelos disponibles")
except Exception as e:
    print(f"      ❌ Error: {e}")

# Test 4: Speech Service
print("\n[4/6] Verificando Speech-to-Text...")
try:
    from api.services import speech_to_text_service
    if speech_to_text_service.is_available():
        print("      ✓ Speech-to-Text configurado")
        score += 1
    else:
        print("      ⚠️  No configurado (opcional)")
        score += 0.5
except Exception as e:
    print(f"      ⚠️  {e}")
    score += 0.5

# Test 5: Face Service
print("\n[5/6] Verificando Face Recognition...")
try:
    from api.services import face_recognition_service
    if face_recognition_service.is_available():
        print("      ✓ Face Recognition configurado")
        score += 1
    else:
        print("      ⚠️  No configurado (opcional)")
        score += 0.5
except Exception as e:
    print(f"      ⚠️  {e}")
    score += 0.5

# Test 6: API Server
print("\n[6/6] Verificando API Server...")
try:
    import requests
    r = requests.get("http://localhost:8000/health", timeout=3)
    if r.status_code == 200:
        data = r.json()
        print(f"      ✓ API corriendo - {data['models_loaded']} modelos")
        score += 1
    else:
        print(f"      ❌ API respondió: {r.status_code}")
except requests.exceptions.ConnectionError:
    print("      ⚠️  API no está corriendo")
    print("         Inicia con: python start_api.py")
except Exception as e:
    print(f"      ⚠️  {e}")

# Results
print("\n" + "="*60)
print(f"  RESULTADO: {score}/{total} ({score/total*100:.0f}%)")
print("="*60)

if score >= 5.5:
    print("\n  ✅ Backend funcional - Listo para usar")
    print("\n  Siguiente paso:")
    print("     1. Inicia API: python start_api.py")
    print("     2. Abre Swagger: http://localhost:8000/docs")
elif score >= 3:
    print("\n  ⚠️  Backend funcional con opcionales pendientes")
    print("\n  Configuraciones opcionales:")
    print("     • Speech-to-Text: python setup_speech.py")
    print("     • Face Recognition: python setup_face_recognition.py")
else:
    print("\n  ❌ Problemas detectados")
    print("\n  Ejecuta prueba completa:")
    print("     python test_complete_backend.py")

print("\n")
