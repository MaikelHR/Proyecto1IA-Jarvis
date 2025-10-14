"""Script de prueba completo para Speech-to-Text API."""

import base64
import requests
from pathlib import Path


BASE_URL = "http://localhost:8000"


def test_voice_status():
    """Probar estado del servicio de voz."""
    print("=" * 60)
    print("TEST 1: Estado del Servicio Speech-to-Text")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/voice/status")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Disponible: {result['available']}")
        print(f"Servicio: {result['service']}")
        print(f"Credenciales: {'✓ Configuradas' if result['credentials_configured'] else '✗ NO configuradas'}")
    else:
        print(f"Error: {response.text}")
    print()


def test_parse_text():
    """Probar parsing de comandos de texto."""
    print("=" * 60)
    print("TEST 2: Parsing de Comandos (sin audio)")
    print("=" * 60)
    
    commands = [
        "Jarvis predice el precio de Bitcoin",
        "Analiza riesgo de churn del cliente",
        "Evalúa la calidad de este vino",
        "Calcula mi porcentaje de grasa corporal",
        "Valora este automóvil usado"
    ]
    
    for command in commands:
        response = requests.post(
            f"{BASE_URL}/voice/parse",
            params={"text": command}
        )
        
        if response.status_code == 200:
            result = response.json()
            status = "✓" if result['command_recognized'] else "✗"
            dataset = result.get('dataset_key', 'N/A')
            print(f"{status} '{command}' → {dataset}")
        else:
            print(f"✗ Error: {response.text}")
    print()


def test_upload_audio():
    """Probar subida de archivo de audio."""
    print("=" * 60)
    print("TEST 3: Subida de Archivo de Audio")
    print("=" * 60)
    
    # Check if test audio exists
    audio_file = Path("temp_audio/recording.wav")
    
    if not audio_file.exists():
        print("⚠ No hay archivo de audio de prueba")
        print("  Ejecuta primero: python test_speech_to_text.py")
        print()
        return
    
    print(f"Subiendo: {audio_file}")
    
    with open(audio_file, "rb") as f:
        files = {"file": ("recording.wav", f, "audio/wav")}
        response = requests.post(
            f"{BASE_URL}/voice/upload",
            files=files,
            params={"language_code": "es-ES"}
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Transcripción: {result['transcript']}")
        print(f"Confianza: {result['confidence']:.2%}")
        print(f"Comando reconocido: {result['command_recognized']}")
        if result['dataset_key']:
            print(f"Dataset: {result['dataset_key']}")
    else:
        print(f"Error: {response.json()}")
    print()


def test_base64_audio():
    """Probar envío de audio en base64."""
    print("=" * 60)
    print("TEST 4: Audio en Base64")
    print("=" * 60)
    
    audio_file = Path("temp_audio/recording.wav")
    
    if not audio_file.exists():
        print("⚠ No hay archivo de audio de prueba")
        print()
        return
    
    # Read and encode audio
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    print(f"Audio codificado: {len(audio_base64)} caracteres")
    
    data = {
        "audio_base64": audio_base64,
        "language_code": "es-ES"
    }
    
    response = requests.post(
        f"{BASE_URL}/voice/command",
        json=data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Transcripción: {result['transcript']}")
        print(f"Confianza: {result['confidence']:.2%}")
        print(f"Comando reconocido: {result['command_recognized']}")
        if result['dataset_key']:
            print(f"Dataset: {result['dataset_key']}")
    else:
        print(f"Error: {response.json()}")
    print()


def main():
    """Run all tests."""
    print("\n🎤 JARVIS - Test Suite Speech-to-Text\n")
    
    try:
        test_voice_status()
        test_parse_text()
        test_upload_audio()
        test_base64_audio()
        
        print("=" * 60)
        print("✅ TESTS COMPLETADOS")
        print("=" * 60)
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar a la API")
        print("Asegúrate de que el servidor esté corriendo:")
        print("  python run_api.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    main()
