"""Speech-to-Text service using Google Cloud API."""

from __future__ import annotations

import base64
import io
import os
from typing import Optional, Tuple

from google.cloud import speech_v1 as speech
from google.api_core.exceptions import GoogleAPIError


class SpeechToTextService:
    """Service for converting audio to text using Google Cloud Speech-to-Text."""
    
    def __init__(self):
        """Initialize the Speech-to-Text client."""
        self._client: Optional[speech.SpeechClient] = None
        self._credentials_configured = False
        self._check_credentials()
    
    def _check_credentials(self) -> None:
        """Check if Google Cloud credentials are configured."""
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if credentials_path and os.path.exists(credentials_path):
            self._credentials_configured = True
            print(f"✓ Google Cloud credentials encontradas: {credentials_path}")
        else:
            self._credentials_configured = False
            print("⚠ Google Cloud credentials NO configuradas")
            print("  Configure la variable GOOGLE_APPLICATION_CREDENTIALS")
    
    def _get_client(self) -> speech.SpeechClient:
        """Get or create Speech-to-Text client."""
        if not self._credentials_configured:
            raise ValueError(
                "Google Cloud credentials not configured. "
                "Set GOOGLE_APPLICATION_CREDENTIALS environment variable."
            )
        
        if self._client is None:
            self._client = speech.SpeechClient()
        
        return self._client
    
    def is_available(self) -> bool:
        """Check if the service is available (credentials configured)."""
        return self._credentials_configured
    
    def transcribe_audio(
        self,
        audio_content: bytes,
        language_code: str = "es-ES",
        sample_rate_hertz: int = 16000,
        encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        use_enhanced: bool = True
    ) -> Tuple[str, float]:
        """
        Transcribe audio content to text.
        
        Args:
            audio_content: Raw audio bytes
            language_code: Language code (default: es-ES for Spanish)
            sample_rate_hertz: Audio sample rate
            encoding: Audio encoding format
            use_enhanced: Use enhanced model optimized for commands
            
        Returns:
            Tuple of (transcribed_text, confidence_score)
            
        Raises:
            ValueError: If credentials not configured
            GoogleAPIError: If API call fails
        """
        client = self._get_client()
        
        # Configure recognition settings
        # Use "command_and_search" model for better command recognition
        config = speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="command_and_search" if use_enhanced else "default",
            use_enhanced=use_enhanced,
            # Add alternative languages for better recognition
            alternative_language_codes=["es-MX", "es-419"] if language_code.startswith("es") else [],
        )
        
        audio = speech.RecognitionAudio(content=audio_content)
        
        try:
            print(f"🎤 Enviando a Google Speech API...")
            print(f"   - Audio size: {len(audio_content)} bytes")
            print(f"   - Language: {language_code}")
            print(f"   - Sample rate: {sample_rate_hertz}")
            print(f"   - Encoding: {encoding}")
            
            # Perform recognition
            response = client.recognize(config=config, audio=audio)
            
            print(f"📤 Respuesta recibida de Google")
            print(f"   - Número de resultados: {len(response.results) if response.results else 0}")
            
            # Extract best result
            if response.results:
                result = response.results[0]
                print(f"   - Resultado tiene {len(result.alternatives)} alternativas")
                if result.alternatives:
                    alternative = result.alternatives[0]
                    transcript = alternative.transcript
                    confidence = alternative.confidence
                    print(f"✅ Transcripción exitosa: '{transcript}' (confianza: {confidence})")
                    return transcript, confidence
            
            # No speech detected
            print("⚠️ No se detectó voz en el audio")
            return "", 0.0
            
        except GoogleAPIError as e:
            print(f"❌ GoogleAPIError: {str(e)}")
            import traceback
            traceback.print_exc()
            raise GoogleAPIError(f"Google Speech API error: {str(e)}") from e
    
    def transcribe_base64_audio(
        self,
        audio_base64: str,
        language_code: str = "es-ES"
    ) -> Tuple[str, float]:
        """
        Transcribe base64-encoded audio to text.
        
        Args:
            audio_base64: Base64 encoded audio data
            language_code: Language code
            
        Returns:
            Tuple of (transcribed_text, confidence_score)
        """
        # Decode base64 audio
        print(f"📥 Decodificando base64 audio: {len(audio_base64)} caracteres")
        audio_content = base64.b64decode(audio_base64)
        print(f"📥 Audio decodificado: {len(audio_content)} bytes")
        
        # Try WEBM_OPUS first (browser default)
        print("🎯 Intentando con WEBM_OPUS encoding...")
        try:
            transcript, confidence = self.transcribe_audio(
                audio_content=audio_content,
                language_code=language_code,
                sample_rate_hertz=48000,
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                use_enhanced=True
            )
            
            if transcript:  # Si obtenemos transcripción, retornar
                return transcript, confidence
            
            print("⚠️ WEBM_OPUS no detectó voz. Intentando con ENCODING_UNSPECIFIED...")
        except Exception as e:
            print(f"⚠️ Error con WEBM_OPUS: {str(e)}")
            print("🔄 Intentando con ENCODING_UNSPECIFIED...")
        
        # Fallback: Let Google auto-detect the encoding
        try:
            return self.transcribe_audio(
                audio_content=audio_content,
                language_code=language_code,
                sample_rate_hertz=48000,
                encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                use_enhanced=True
            )
        except Exception as e:
            print(f"❌ Error con ENCODING_UNSPECIFIED: {str(e)}")
            # Return empty if all attempts fail
            return "", 0.0
    
    def transcribe_file(
        self,
        file_path: str,
        language_code: str = "es-ES"
    ) -> Tuple[str, float]:
        """
        Transcribe audio file to text.
        
        Args:
            file_path: Path to audio file
            language_code: Language code
            
        Returns:
            Tuple of (transcribed_text, confidence_score)
        """
        with open(file_path, "rb") as audio_file:
            audio_content = audio_file.read()
        
        return self.transcribe_audio(
            audio_content=audio_content,
            language_code=language_code
        )
    
    def transcribe_streaming(
        self,
        audio_generator,
        language_code: str = "es-ES",
        sample_rate_hertz: int = 16000
    ):
        """
        Transcribe audio stream in real-time.
        
        Args:
            audio_generator: Generator yielding audio chunks
            language_code: Language code
            sample_rate_hertz: Audio sample rate
            
        Yields:
            Interim and final transcription results
        """
        client = self._get_client()
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )
        
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True
        )
        
        # Create requests generator
        def request_generator():
            yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
            for content in audio_generator:
                yield speech.StreamingRecognizeRequest(audio_content=content)
        
        try:
            responses = client.streaming_recognize(request_generator())
            
            for response in responses:
                for result in response.results:
                    if result.alternatives:
                        transcript = result.alternatives[0].transcript
                        confidence = result.alternatives[0].confidence
                        is_final = result.is_final
                        
                        yield {
                            "transcript": transcript,
                            "confidence": confidence,
                            "is_final": is_final
                        }
        
        except GoogleAPIError as e:
            raise GoogleAPIError(f"Streaming recognition error: {str(e)}") from e


# Global singleton instance
speech_to_text_service = SpeechToTextService()
