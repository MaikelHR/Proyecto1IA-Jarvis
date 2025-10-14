"""
Prueba Completa del Backend - Jarvis IA

Este script realiza una verificación exhaustiva de TODAS las funcionalidades:
1. Modelos ML (9 modelos)
2. API REST (endpoints)
3. Speech-to-Text (Google Cloud)
4. Face Recognition (Azure)

Genera un reporte completo de estado.
"""

import os
import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(title: str, color=Colors.BLUE):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"{color}{Colors.BOLD} {title}{Colors.END}")
    print("=" * 70)


def print_success(msg: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")


def print_error(msg: str):
    """Print error message."""
    print(f"{Colors.RED}❌{Colors.END} {msg}")


def print_warning(msg: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️{Colors.END}  {msg}")


def print_info(msg: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ{Colors.END}  {msg}")


# ============================================================================
# TEST 1: VERIFICAR ESTRUCTURA DE ARCHIVOS
# ============================================================================

def test_file_structure():
    """Verify project file structure."""
    print_header("TEST 1: ESTRUCTURA DE ARCHIVOS")
    
    required_files = {
        "main.py": "Script principal",
        "requirements.txt": "Dependencias",
        "api/main.py": "API FastAPI",
        "api/routers/health.py": "Health check",
        "api/routers/predictions.py": "Predicciones ML",
        "api/routers/voice.py": "Speech-to-Text",
        "api/routers/face.py": "Face Recognition",
        "api/services/model_service.py": "Servicio ML",
        "api/services/speech_service.py": "Servicio Speech",
        "api/services/face_service.py": "Servicio Face",
        "api/services/voice_command_service.py": "Comandos de voz",
        "api/services/audio_utils.py": "Audio utils",
        "api/services/video_utils.py": "Video utils",
    }
    
    required_dirs = [
        "data/raw",
        "reports",
        "src",
        "api",
        "api/routers",
        "api/services",
    ]
    
    all_ok = True
    
    print("\n📁 Verificando archivos...")
    for file_path, description in required_files.items():
        full_path = project_root / file_path
        if full_path.exists():
            print_success(f"{file_path:40s} - {description}")
        else:
            print_error(f"{file_path:40s} - FALTA")
            all_ok = False
    
    print("\n📂 Verificando directorios...")
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print_success(f"{dir_path}")
        else:
            print_error(f"{dir_path} - FALTA")
            all_ok = False
    
    return all_ok


# ============================================================================
# TEST 2: VERIFICAR MODELOS ML
# ============================================================================

def test_ml_models():
    """Verify ML models exist and can be loaded."""
    print_header("TEST 2: MODELOS DE MACHINE LEARNING")
    
    expected_models = [
        "bitcoin_price",
        "avocado_prices",
        "body_fat",
        "car_prices",
        "telco_churn",
        "wine_quality",
        "stroke_risk",
        "hepatitis_c",
        "cirrhosis_status",
    ]
    
    reports_dir = project_root / "reports"
    
    print("\n🤖 Verificando modelos entrenados...")
    
    found_models = []
    missing_models = []
    
    for model_name in expected_models:
        # Check for various file patterns
        patterns = [
            f"{model_name}_model.pkl",
            f"{model_name}.pkl",
            f"*{model_name}*.pkl",
        ]
        
        found = False
        for pattern in patterns:
            matches = list(reports_dir.glob(pattern))
            if matches:
                found = True
                model_file = matches[0]
                size_mb = model_file.stat().st_size / (1024 * 1024)
                print_success(f"{model_name:25s} - {model_file.name} ({size_mb:.2f} MB)")
                found_models.append(model_name)
                break
        
        if not found:
            print_error(f"{model_name:25s} - NO ENCONTRADO")
            missing_models.append(model_name)
    
    print(f"\n📊 Resumen: {len(found_models)}/9 modelos encontrados")
    
    if missing_models:
        print_warning(f"Modelos faltantes: {', '.join(missing_models)}")
        print_info("Ejecuta: python main.py")
    
    return len(found_models) >= 9


# ============================================================================
# TEST 3: VERIFICAR DEPENDENCIAS
# ============================================================================

def test_dependencies():
    """Verify Python packages are installed."""
    print_header("TEST 3: DEPENDENCIAS DE PYTHON")
    
    required_packages = {
        "fastapi": "FastAPI framework",
        "uvicorn": "ASGI server",
        "pandas": "Data processing",
        "numpy": "Numerical computing",
        "scikit-learn": "Machine Learning",
        "pydantic": "Data validation",
        "requests": "HTTP library",
        "google.cloud.speech": "Google Cloud Speech-to-Text",
        "pyaudio": "Audio I/O",
        "azure.cognitiveservices.vision.face": "Azure Face API",
        "cv2": "OpenCV",
        "PIL": "Pillow (image processing)",
    }
    
    print("\n📦 Verificando paquetes instalados...")
    
    all_installed = True
    
    for package, description in required_packages.items():
        try:
            if package == "cv2":
                import cv2
            elif package == "PIL":
                from PIL import Image
            elif package == "google.cloud.speech":
                from google.cloud import speech
            elif package == "azure.cognitiveservices.vision.face":
                from azure.cognitiveservices.vision.face import FaceClient
            else:
                __import__(package)
            
            print_success(f"{package:40s} - {description}")
        except ImportError:
            print_error(f"{package:40s} - NO INSTALADO")
            all_installed = False
    
    if not all_installed:
        print_warning("\nInstala las dependencias faltantes:")
        print_info("pip install -r requirements.txt")
    
    return all_installed


# ============================================================================
# TEST 4: VERIFICAR CREDENCIALES
# ============================================================================

def test_credentials():
    """Verify API credentials are configured."""
    print_header("TEST 4: CREDENCIALES DE APIs")
    
    results = {}
    
    # Google Cloud Speech-to-Text
    print("\n🎤 Google Cloud Speech-to-Text:")
    google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_creds:
        creds_path = Path(google_creds)
        if creds_path.exists():
            print_success(f"GOOGLE_APPLICATION_CREDENTIALS: {google_creds}")
            results['speech'] = True
        else:
            print_error(f"Archivo no existe: {google_creds}")
            results['speech'] = False
    else:
        print_warning("GOOGLE_APPLICATION_CREDENTIALS no configurada")
        print_info("Configura: $env:GOOGLE_APPLICATION_CREDENTIALS=\"credentials\\google-credentials.json\"")
        results['speech'] = False
    
    # Azure Face API
    print("\n😊 Azure Face API:")
    azure_key = os.getenv("AZURE_FACE_KEY")
    azure_endpoint = os.getenv("AZURE_FACE_ENDPOINT")
    
    if azure_key:
        masked_key = "*" * 20 + azure_key[-4:] if len(azure_key) > 4 else "****"
        print_success(f"AZURE_FACE_KEY: {masked_key}")
    else:
        print_warning("AZURE_FACE_KEY no configurada")
        print_info("Configura: $env:AZURE_FACE_KEY=\"tu-key\"")
    
    if azure_endpoint:
        print_success(f"AZURE_FACE_ENDPOINT: {azure_endpoint}")
    else:
        print_warning("AZURE_FACE_ENDPOINT no configurada")
        print_info("Configura: $env:AZURE_FACE_ENDPOINT=\"tu-endpoint\"")
    
    results['face'] = bool(azure_key and azure_endpoint)
    
    return results


# ============================================================================
# TEST 5: VERIFICAR API REST
# ============================================================================

def test_api_server():
    """Test if API server can start."""
    print_header("TEST 5: SERVIDOR API REST")
    
    print("\n🔍 Verificando importación de API...")
    
    try:
        from api.main import app
        print_success("API importada correctamente")
        
        # Verify routers
        print("\n📍 Verificando routers:")
        routes = [route.path for route in app.routes]
        
        expected_routes = {
            "/health": "Health check",
            "/predictions/{dataset_key}": "Predicciones ML",
            "/voice/command": "Comando de voz",
            "/voice/upload": "Upload audio",
            "/voice/parse": "Parse comando",
            "/face/status": "Estado Face Recognition",
            "/face/emotion": "Detectar emociones",
            "/face/analyze": "Análisis facial",
        }
        
        for route in expected_routes.keys():
            if any(route in r for r in routes):
                print_success(f"{route:40s} - {expected_routes[route]}")
            else:
                print_warning(f"{route:40s} - No encontrado")
        
        print(f"\n📊 Total endpoints: {len(routes)}")
        
        return True
    
    except Exception as e:
        print_error(f"Error al importar API: {e}")
        return False


# ============================================================================
# TEST 6: PRUEBA CON REQUESTS (API RUNNING)
# ============================================================================

def test_api_endpoints():
    """Test API endpoints (requires API server running)."""
    print_header("TEST 6: ENDPOINTS DE LA API")
    
    print("\n⚠️  NOTA: Este test requiere que la API esté corriendo")
    print("   Inicia la API en otra terminal con: python start_api.py")
    
    try:
        import requests
    except ImportError:
        print_error("requests no está instalado")
        return False
    
    api_url = "http://localhost:8000"
    
    print(f"\n🔄 Intentando conectar con {api_url}...")
    
    try:
        # Test health endpoint
        response = requests.get(f"{api_url}/health", timeout=5)
        
        if response.status_code == 200:
            print_success("API está corriendo!")
            
            data = response.json()
            print(f"\n📊 Estado:")
            print(f"   Status: {data.get('status')}")
            print(f"   Models loaded: {data.get('models_loaded')}")
            print(f"   Speech service: {data.get('speech_service_available')}")
            
            # Test documentation
            print("\n📚 Documentación:")
            print_success("Swagger UI: http://localhost:8000/docs")
            print_success("ReDoc: http://localhost:8000/redoc")
            
            return True
        else:
            print_error(f"API respondió con status {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print_warning("API no está corriendo")
        print_info("Inicia con: python start_api.py")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


# ============================================================================
# TEST 7: VERIFICAR SERVICIOS
# ============================================================================

def test_services():
    """Test service modules can be imported."""
    print_header("TEST 7: SERVICIOS DE BACKEND")
    
    print("\n🔧 Verificando servicios...")
    
    services = {
        "ModelService": ("api.services.model_service", "ModelService"),
        "SpeechService": ("api.services.speech_service", "SpeechToTextService"),
        "FaceService": ("api.services.face_service", "FaceRecognitionService"),
        "VoiceCommandService": ("api.services.voice_command_service", "VoiceCommandService"),
        "AudioRecorder": ("api.services.audio_utils", "AudioRecorder"),
        "VideoCapture": ("api.services.video_utils", "VideoCapture"),
    }
    
    all_ok = True
    
    for service_name, (module_path, class_name) in services.items():
        try:
            module = __import__(module_path, fromlist=[class_name])
            service_class = getattr(module, class_name)
            print_success(f"{service_name:25s} - {module_path}")
        except Exception as e:
            print_error(f"{service_name:25s} - Error: {e}")
            all_ok = False
    
    return all_ok


# ============================================================================
# TEST 8: VERIFICAR DISPOSITIVOS
# ============================================================================

def test_devices():
    """Test audio/video devices."""
    print_header("TEST 8: DISPOSITIVOS (AUDIO/VIDEO)")
    
    # Test audio devices
    print("\n🎤 Dispositivos de audio:")
    try:
        from api.services.audio_utils import get_available_devices
        devices = get_available_devices()
        
        if devices:
            for idx, device in enumerate(devices):
                print_success(f"[{idx}] {device['name']}")
        else:
            print_warning("No se encontraron dispositivos de audio")
    except Exception as e:
        print_error(f"Error al detectar audio: {e}")
    
    # Test video devices
    print("\n📹 Dispositivos de video:")
    try:
        from api.services.video_utils import get_available_cameras
        cameras = get_available_cameras()
        
        if cameras:
            for idx in cameras:
                print_success(f"[{idx}] Cámara {idx}")
        else:
            print_warning("No se encontraron cámaras")
    except Exception as e:
        print_error(f"Error al detectar cámaras: {e}")


# ============================================================================
# GENERATE REPORT
# ============================================================================

def generate_report(results: dict):
    """Generate final report."""
    print_header("📊 REPORTE FINAL", Colors.BOLD)
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    print(f"\n{'Test':<40s} {'Resultado':<15s}")
    print("-" * 55)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}✓ PASÓ{Colors.END}" if result else f"{Colors.RED}❌ FALLÓ{Colors.END}"
        print(f"{test_name:<40s} {status}")
    
    print("-" * 55)
    print(f"{'TOTAL':<40s} {passed_tests}/{total_tests}")
    
    percentage = (passed_tests / total_tests) * 100
    
    print(f"\n📈 Porcentaje de éxito: {percentage:.1f}%")
    
    if percentage == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡PERFECTO! TODO FUNCIONA CORRECTAMENTE{Colors.END}")
    elif percentage >= 75:
        print(f"\n{Colors.GREEN}✓ Backend funcional con configuraciones opcionales pendientes{Colors.END}")
    elif percentage >= 50:
        print(f"\n{Colors.YELLOW}⚠️  Algunos componentes necesitan atención{Colors.END}")
    else:
        print(f"\n{Colors.RED}❌ Hay problemas que requieren corrección{Colors.END}")
    
    # Recommendations
    print(f"\n{Colors.BOLD}📝 RECOMENDACIONES:{Colors.END}")
    
    if not results.get("Dependencies"):
        print("   • Instala dependencias: pip install -r requirements.txt")
    
    if not results.get("ML Models"):
        print("   • Entrena modelos: python main.py")
    
    if not results.get("API Server"):
        print("   • Verifica errores en api/main.py")
    
    if not results.get("API Endpoints"):
        print("   • Inicia la API: python start_api.py")
        print("   • Luego ejecuta este test nuevamente")
    
    # Next steps
    print(f"\n{Colors.BOLD}🚀 SIGUIENTES PASOS:{Colors.END}")
    print("\n1. Si todo está OK:")
    print("   • Inicia la API: python start_api.py")
    print("   • Abre Swagger: http://localhost:8000/docs")
    print("   • Prueba endpoints manualmente")
    
    print("\n2. Pruebas específicas:")
    print("   • Speech-to-Text: python test_speech_to_text.py")
    print("   • Face Recognition: python test_face_recognition.py")
    print("   • Voice API: python test_voice_api.py")
    print("   • Face API: python test_face_api.py")
    
    print("\n3. Configurar credenciales (si aplica):")
    print("   • Google Cloud: python setup_speech.py")
    print("   • Azure Face: python setup_face_recognition.py")
    
    print("\n4. Implementar Frontend:")
    print("   • Ver guía: NEXT_STEPS.md")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run all tests."""
    print("\n")
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("  🧪 PRUEBA COMPLETA DEL BACKEND - JARVIS IA")
    print(f"{Colors.END}")
    print("=" * 70)
    
    results = {}
    
    # Run tests
    print_info("Iniciando pruebas exhaustivas del backend...")
    time.sleep(1)
    
    results["File Structure"] = test_file_structure()
    results["ML Models"] = test_ml_models()
    results["Dependencies"] = test_dependencies()
    results["Credentials"] = test_credentials()
    results["Services"] = test_services()
    results["API Server"] = test_api_server()
    results["API Endpoints"] = test_api_endpoints()
    test_devices()  # Informational only
    
    # Generate report
    generate_report(results)
    
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}✅ Prueba completa finalizada{Colors.END}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
