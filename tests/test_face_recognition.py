"""
Test Face Recognition Service with Azure Face API

This script tests the Face Recognition service by:
1. Checking camera availability
2. Capturing a photo
3. Detecting faces and emotions
4. Displaying results

Requirements:
- Azure Face API credentials configured
- Camera available
- OpenCV installed
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from api.services import (
    face_recognition_service,
    VideoCapture,
    get_available_cameras,
    print_available_cameras,
    frame_to_bytes,
)


def check_credentials():
    """Check if Azure credentials are configured."""
    print("\n" + "=" * 70)
    print("🔑 VERIFICACIÓN DE CREDENCIALES")
    print("=" * 70)
    
    api_key = os.getenv("AZURE_FACE_KEY")
    endpoint = os.getenv("AZURE_FACE_ENDPOINT")
    
    if not api_key:
        print("❌ AZURE_FACE_KEY no configurada")
        print("\n📝 Configura la variable de entorno:")
        print('   $env:AZURE_FACE_KEY="tu-api-key"')
        return False
    
    if not endpoint:
        print("❌ AZURE_FACE_ENDPOINT no configurada")
        print("\n📝 Configura la variable de entorno:")
        print('   $env:AZURE_FACE_ENDPOINT="tu-endpoint"')
        return False
    
    print(f"✓ AZURE_FACE_KEY: {'*' * 20}{api_key[-4:]}")
    print(f"✓ AZURE_FACE_ENDPOINT: {endpoint}")
    
    # Check service
    if face_recognition_service.is_available():
        print("✓ Face Recognition Service: DISPONIBLE")
        return True
    else:
        print("❌ Face Recognition Service: NO DISPONIBLE")
        return False


def test_camera():
    """Test camera availability."""
    print("\n" + "=" * 70)
    print("📹 VERIFICACIÓN DE CÁMARA")
    print("=" * 70)
    
    cameras = get_available_cameras()
    
    if not cameras:
        print("❌ No se encontraron cámaras disponibles")
        return False
    
    print(f"✓ {len(cameras)} cámara(s) disponible(s): {cameras}")
    return True


def capture_and_analyze():
    """Capture photo and analyze emotions."""
    print("\n" + "=" * 70)
    print("📸 CAPTURA Y ANÁLISIS DE ROSTRO")
    print("=" * 70)
    
    try:
        # Create output directory
        output_dir = Path("temp_images")
        output_dir.mkdir(exist_ok=True)
        
        # Initialize camera
        print("\n🎥 Inicializando cámara...")
        video = VideoCapture(camera_index=0)
        
        if not video.start():
            print("❌ No se pudo inicializar la cámara")
            return False
        
        print("✓ Cámara iniciada")
        print("\n📸 Capturando foto en 3 segundos...")
        print("   Mira a la cámara y prepara tu expresión!")
        
        # Wait a bit for camera to adjust
        import time
        time.sleep(3)
        
        # Capture frame
        frame = video.capture_photo()
        video.stop()
        
        if frame is None:
            print("❌ No se pudo capturar la foto")
            return False
        
        print("✓ Foto capturada")
        
        # Save frame
        photo_path = output_dir / "test_face.jpg"
        import cv2
        cv2.imwrite(str(photo_path), frame)
        print(f"✓ Foto guardada: {photo_path}")
        
        # Convert to bytes
        print("\n🔍 Analizando rostro...")
        image_bytes = frame_to_bytes(frame)
        
        # Analyze emotions
        result = face_recognition_service.analyze_emotions(image_bytes)
        
        print("\n" + "=" * 70)
        print("📊 RESULTADOS")
        print("=" * 70)
        
        if not result["face_detected"]:
            print(f"❌ {result['message']}")
            return False
        
        print(f"✓ {result['message']}")
        print(f"\n👤 Número de rostros: {result['num_faces']}")
        
        if result.get("emotions_es"):
            print("\n😊 Emociones detectadas:")
            for emotion, score in result["emotions_es"].items():
                bar_length = int(score * 50)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                print(f"   {emotion:15s} {bar} {score:.1%}")
        
        print(f"\n🎯 Emoción dominante: {result.get('dominant_emotion_es', 'N/A')}")
        print(f"   Confianza: {result['confidence']:.1%}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_analysis():
    """Test full face analysis."""
    print("\n" + "=" * 70)
    print("🔬 ANÁLISIS COMPLETO DE ROSTRO")
    print("=" * 70)
    
    try:
        # Read saved photo
        photo_path = Path("temp_images/test_face.jpg")
        
        if not photo_path.exists():
            print("❌ No se encontró la foto de prueba")
            print("   Ejecuta primero la captura y análisis")
            return False
        
        # Read image
        with open(photo_path, "rb") as f:
            image_data = f.read()
        
        print("\n🔍 Analizando atributos faciales...")
        result = face_recognition_service.analyze_face_attributes(image_data)
        
        if not result["face_detected"]:
            print("❌ No se detectó rostro")
            return False
        
        print("\n✓ Rostro detectado")
        
        # Display results
        if "age" in result:
            print(f"\n👤 Edad estimada: {result['age']} años")
        
        if "gender" in result:
            gender_es = "Masculino" if result["gender"] == "male" else "Femenino"
            print(f"👤 Género: {gender_es}")
        
        if "smile" in result:
            print(f"😊 Sonrisa: {result['smile']:.1%}")
        
        if "glasses" in result:
            print(f"👓 Gafas: {result['glasses']}")
        
        if "face_rectangle" in result:
            rect = result["face_rectangle"]
            print(f"\n📐 Posición del rostro:")
            print(f"   X: {rect['left']}, Y: {rect['top']}")
            print(f"   Ancho: {rect['width']}, Alto: {rect['height']}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("\n")
    print("=" * 70)
    print(" PRUEBA DE FACE RECOGNITION CON AZURE FACE API")
    print("=" * 70)
    
    # Check credentials
    if not check_credentials():
        print("\n❌ Configura las credenciales de Azure antes de continuar")
        print("\n📖 Instrucciones:")
        print("   1. Ve a Azure Portal")
        print("   2. Crea un recurso 'Face' en Cognitive Services")
        print("   3. Obtén la KEY y el ENDPOINT")
        print("   4. Configura las variables de entorno:")
        print('      $env:AZURE_FACE_KEY="tu-key"')
        print('      $env:AZURE_FACE_ENDPOINT="tu-endpoint"')
        return
    
    # Check camera
    if not test_camera():
        print("\n❌ No hay cámara disponible")
        return
    
    # Capture and analyze
    print("\n▶️  PRUEBA 1: Captura y Detección de Emociones")
    if not capture_and_analyze():
        print("\n❌ Falló la captura y análisis")
        return
    
    # Full analysis
    print("\n▶️  PRUEBA 2: Análisis Completo de Atributos")
    if not test_full_analysis():
        print("\n❌ Falló el análisis completo")
        return
    
    # Success
    print("\n" + "=" * 70)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 70)
    print("\n📌 Siguiente paso:")
    print("   - Prueba la API en http://localhost:8000/docs")
    print("   - Endpoints disponibles:")
    print("     • GET  /face/status")
    print("     • POST /face/emotion")
    print("     • POST /face/emotion/upload")
    print("     • POST /face/analyze")
    print("     • POST /face/detect/multiple")


if __name__ == "__main__":
    main()
