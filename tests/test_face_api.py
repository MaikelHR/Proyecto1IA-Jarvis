"""
Test Face Recognition API endpoints

This script tests all Face Recognition API endpoints:
- GET /face/status
- POST /face/emotion (base64)
- POST /face/emotion/upload (file)
- POST /face/analyze (file)
- POST /face/detect/multiple (file)

Requirements:
- API server running (python start_api.py)
- Azure Face API credentials configured
- Test image available (or will capture from camera)
"""

import base64
import os
import sys
from pathlib import Path
import time

import requests

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# API base URL
API_URL = "http://localhost:8000"


def print_header(title: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def check_api_running():
    """Check if API server is running."""
    print_header("VERIFICACIÓN DEL SERVIDOR API")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API Server: Running")
            print(f"✓ Models loaded: {data.get('models_loaded', 'N/A')}")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar con la API")
        print("\n💡 Inicia el servidor con:")
        print("   python start_api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_status_endpoint():
    """Test GET /face/status endpoint."""
    print_header("TEST 1: GET /face/status")
    
    try:
        response = requests.get(f"{API_URL}/face/status")
        
        print(f"\n📡 Status Code: {response.status_code}")
        
        data = response.json()
        print(f"\n📊 Response:")
        print(f"   Available: {data.get('available')}")
        print(f"   Message: {data.get('message')}")
        
        if data.get('available'):
            print("\n✓ Face Recognition service disponible")
            return True
        else:
            print("\n⚠️  Face Recognition service NO disponible")
            print("   Configura AZURE_FACE_KEY y AZURE_FACE_ENDPOINT")
            return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def get_test_image():
    """Get test image (capture or use existing)."""
    print_header("OBTENER IMAGEN DE PRUEBA")
    
    # Check if test image exists
    test_image = Path("temp_images/test_face.jpg")
    
    if test_image.exists():
        print(f"✓ Usando imagen existente: {test_image}")
        return test_image
    
    # Try to capture from camera
    print("\n📸 No se encontró imagen de prueba")
    print("   Intentando capturar desde cámara...")
    
    try:
        from api.services import VideoCapture, frame_to_bytes
        import cv2
        
        # Create output directory
        output_dir = Path("temp_images")
        output_dir.mkdir(exist_ok=True)
        
        # Initialize camera
        video = VideoCapture(camera_index=0)
        
        if not video.start():
            print("❌ No se pudo inicializar la cámara")
            return None
        
        print("✓ Cámara iniciada")
        print("📸 Capturando foto en 2 segundos...")
        time.sleep(2)
        
        # Capture frame
        frame = video.capture_photo()
        video.stop()
        
        if frame is None:
            print("❌ No se pudo capturar la foto")
            return None
        
        # Save frame
        cv2.imwrite(str(test_image), frame)
        print(f"✓ Foto guardada: {test_image}")
        
        return test_image
    
    except Exception as e:
        print(f"❌ Error al capturar: {e}")
        return None


def test_emotion_base64(image_path: Path):
    """Test POST /face/emotion with base64 image."""
    print_header("TEST 2: POST /face/emotion (base64)")
    
    try:
        # Read and encode image
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        
        print("\n🔄 Enviando imagen en base64...")
        
        response = requests.post(
            f"{API_URL}/face/emotion",
            json={"image": image_data}
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 503:
            print("⚠️  Servicio no configurado")
            return False
        
        data = response.json()
        
        print(f"\n📊 Response:")
        print(f"   Face detected: {data.get('face_detected')}")
        print(f"   Num faces: {data.get('num_faces')}")
        
        if data.get('face_detected'):
            print(f"   Dominant emotion: {data.get('dominant_emotion_es')}")
            print(f"   Confidence: {data.get('confidence'):.2%}")
            
            print(f"\n😊 Emociones:")
            emotions = data.get('emotions_es', {})
            for emotion, score in emotions.items():
                bar_length = int(score * 30)
                bar = "█" * bar_length + "░" * (30 - bar_length)
                print(f"   {emotion:12s} {bar} {score:.1%}")
            
            print(f"\n✓ {data.get('message')}")
            return True
        else:
            print(f"   Message: {data.get('message')}")
            return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_emotion_upload(image_path: Path):
    """Test POST /face/emotion/upload with file."""
    print_header("TEST 3: POST /face/emotion/upload (file)")
    
    try:
        print("\n🔄 Subiendo archivo de imagen...")
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{API_URL}/face/emotion/upload",
                files=files
            )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 503:
            print("⚠️  Servicio no configurado")
            return False
        
        data = response.json()
        
        print(f"\n📊 Response:")
        print(f"   Face detected: {data.get('face_detected')}")
        
        if data.get('face_detected'):
            print(f"   Dominant emotion: {data.get('dominant_emotion_es')}")
            print(f"   Confidence: {data.get('confidence'):.2%}")
            print(f"\n✓ {data.get('message')}")
            return True
        else:
            print(f"   Message: {data.get('message')}")
            return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_analyze_face(image_path: Path):
    """Test POST /face/analyze."""
    print_header("TEST 4: POST /face/analyze")
    
    try:
        print("\n🔄 Analizando atributos faciales...")
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{API_URL}/face/analyze",
                files=files
            )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 503:
            print("⚠️  Servicio no configurado")
            return False
        
        data = response.json()
        
        print(f"\n📊 Response:")
        print(f"   Face detected: {data.get('face_detected')}")
        
        if data.get('face_detected'):
            print(f"\n👤 Atributos:")
            if 'age' in data:
                print(f"   Edad: {data['age']} años")
            if 'gender' in data:
                gender_es = "Masculino" if data['gender'] == 'male' else "Femenino"
                print(f"   Género: {gender_es}")
            if 'smile' in data:
                print(f"   Sonrisa: {data['smile']:.1%}")
            if 'glasses' in data:
                print(f"   Gafas: {data['glasses']}")
            
            if 'face_rectangle' in data:
                rect = data['face_rectangle']
                print(f"\n📐 Rectángulo:")
                print(f"   Position: ({rect['left']}, {rect['top']})")
                print(f"   Size: {rect['width']}x{rect['height']}")
            
            print("\n✓ Análisis completo exitoso")
            return True
        else:
            print(f"   Message: {data.get('message')}")
            return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_detect_multiple(image_path: Path):
    """Test POST /face/detect/multiple."""
    print_header("TEST 5: POST /face/detect/multiple")
    
    try:
        print("\n🔄 Detectando múltiples rostros...")
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{API_URL}/face/detect/multiple",
                files=files
            )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 503:
            print("⚠️  Servicio no configurado")
            return False
        
        data = response.json()
        
        print(f"\n📊 Response:")
        print(f"   Num faces: {data.get('num_faces')}")
        
        faces = data.get('faces', [])
        if faces:
            for i, face in enumerate(faces, 1):
                print(f"\n   Rostro {i}:")
                if 'age' in face:
                    print(f"      Edad: {face['age']} años")
                if 'gender' in face:
                    gender_es = "Masculino" if face['gender'] == 'male' else "Femenino"
                    print(f"      Género: {gender_es}")
                if 'emotion' in face:
                    emotion = face['emotion']
                    print(f"      Emoción: {emotion.get('dominant_es')} ({emotion.get('confidence'):.1%})")
            
            print(f"\n✓ Detectados {len(faces)} rostro(s)")
            return True
        else:
            print("   No se detectaron rostros")
            return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    """Main test function."""
    print("\n")
    print("=" * 70)
    print(" PRUEBAS DE API - FACE RECOGNITION")
    print("=" * 70)
    
    results = {}
    
    # Check API
    if not check_api_running():
        return
    
    # Test status
    results['status'] = test_status_endpoint()
    
    if not results['status']:
        print("\n⚠️  Face Recognition no disponible")
        print("   Configura las credenciales de Azure y reinicia")
        return
    
    # Get test image
    image_path = get_test_image()
    
    if not image_path:
        print("\n❌ No se pudo obtener imagen de prueba")
        print("   Coloca una imagen en: temp_images/test_face.jpg")
        return
    
    # Run tests
    results['emotion_base64'] = test_emotion_base64(image_path)
    results['emotion_upload'] = test_emotion_upload(image_path)
    results['analyze'] = test_analyze_face(image_path)
    results['multiple'] = test_detect_multiple(image_path)
    
    # Summary
    print_header("RESUMEN DE PRUEBAS")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\n📊 Resultados:")
    for test_name, result in results.items():
        icon = "✓" if result else "❌"
        print(f"   {icon} {test_name}")
    
    print(f"\n📈 Total: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n✅ TODAS LAS PRUEBAS PASARON")
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")


if __name__ == "__main__":
    main()
