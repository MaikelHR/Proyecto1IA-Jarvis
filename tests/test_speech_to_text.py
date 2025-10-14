"""Script para grabar audio y probar Speech-to-Text."""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from api.services.audio_utils import AudioRecorder, print_available_devices
from api.services.speech_service import speech_to_text_service


def record_and_transcribe(duration: float = 5.0):
    """
    Graba audio y lo transcribe.
    
    Args:
        duration: Duración de grabación en segundos
    """
    print("\n" + "=" * 60)
    print("🎤 JARVIS - Grabación y Transcripción de Audio")
    print("=" * 60)
    
    # Check if Speech-to-Text is available
    if not speech_to_text_service.is_available():
        print("\n❌ ERROR: Google Cloud Speech-to-Text no está configurado")
        print("\nPara configurar:")
        print("1. Obtén credenciales de Google Cloud")
        print("2. Configura la variable de entorno:")
        print('   $env:GOOGLE_APPLICATION_CREDENTIALS="ruta\\a\\credenciales.json"')
        return
    
    print("\n✓ Speech-to-Text configurado correctamente")
    
    # Show available devices
    print_available_devices()
    
    # Record audio
    print(f"\n🎤 Grabando por {duration} segundos...")
    print("   Habla ahora: 'Jarvis, predice el precio de Bitcoin'")
    print()
    
    try:
        with AudioRecorder() as recorder:
            # Countdown
            for i in range(3, 0, -1):
                print(f"   {i}...")
                time.sleep(1)
            
            print("   🔴 GRABANDO...")
            audio_data = recorder.record_duration(duration)
            print("   ✓ Grabación completada")
        
        # Save to file (optional)
        output_dir = Path("temp_audio")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "recording.wav"
        
        with AudioRecorder() as recorder:
            recorder.save_to_wav(audio_data, str(output_file))
        
        # Transcribe
        print("\n🔄 Transcribiendo audio...")
        transcript, confidence = speech_to_text_service.transcribe_audio(
            audio_content=audio_data,
            language_code="es-ES"
        )
        
        # Display results
        print("\n" + "=" * 60)
        print("📝 RESULTADO DE TRANSCRIPCIÓN")
        print("=" * 60)
        print(f"Texto: {transcript}")
        print(f"Confianza: {confidence:.2%}")
        print("=" * 60)
        
        # Parse command
        from api.services import voice_service
        dataset_key = voice_service.parse_command(transcript)
        
        if dataset_key:
            print(f"\n✅ Comando reconocido: {dataset_key}")
        else:
            print("\n⚠ No se reconoció ningún comando válido")
        
        print(f"\n💾 Audio guardado en: {output_file}")
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Graba audio y transcribe con Google Speech-to-Text"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=5.0,
        help="Duración de grabación en segundos (default: 5)"
    )
    
    args = parser.parse_args()
    
    record_and_transcribe(duration=args.duration)


if __name__ == "__main__":
    main()
