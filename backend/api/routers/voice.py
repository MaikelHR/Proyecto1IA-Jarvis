"""Voice command endpoints (Speech-to-Text integration)."""

from fastapi import APIRouter, HTTPException, UploadFile, File
from google.api_core.exceptions import GoogleAPIError

from ..models import VoiceCommandRequest, VoiceCommandResponse, ErrorResponse
from ..services.speech_service import speech_to_text_service
from ..services.voice_command_service import voice_service

router = APIRouter(prefix="/voice", tags=["Voice Commands"])


@router.post(
    "/command",
    response_model=VoiceCommandResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid audio data"},
        503: {"model": ErrorResponse, "description": "Service not available"}
    },
    summary="Process Voice Command",
    description="Convierte audio a texto y reconoce comandos de Jarvis (requiere Google Speech-to-Text API)"
)
async def process_voice_command(request: VoiceCommandRequest) -> VoiceCommandResponse:
    """
    Process voice command using Google Speech-to-Text API.
    
    NOTE: This endpoint requires Google Cloud Speech-to-Text API credentials.
    Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    
    Args:
        request: Audio data in base64 format
        
    Returns:
        Transcribed text and recognized command
        
    Raises:
        HTTPException: If speech recognition fails or API not configured
    """
    # Check if service is available
    if not speech_to_text_service.is_available():
        # MODO DEMO: Simular transcripción cuando no hay API configurada
        demo_transcript = "Jarvis, predice el precio de Bitcoin"
        dataset_key = voice_service.parse_command(demo_transcript)
        
        return VoiceCommandResponse(
            transcript=f"[DEMO MODE] {demo_transcript}",
            command_recognized=dataset_key is not None,
            dataset_key=dataset_key,
            confidence=0.85
        )
    
    try:
        # Transcribe audio
        transcript, confidence = speech_to_text_service.transcribe_base64_audio(
            audio_base64=request.audio_base64,
            language_code=request.language_code
        )
        
        # Parse command
        dataset_key = voice_service.parse_command(transcript)
        
        return VoiceCommandResponse(
            transcript=transcript,
            command_recognized=dataset_key is not None,
            dataset_key=dataset_key,
            confidence=confidence
        )
    
    except GoogleAPIError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "GoogleAPIError",
                "message": f"Speech recognition failed: {str(e)}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ProcessingError",
                "message": f"Error processing audio: {str(e)}"
            }
        )


@router.post(
    "/upload",
    response_model=VoiceCommandResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid audio file"},
        503: {"model": ErrorResponse, "description": "Service not available"}
    },
    summary="Upload Audio File",
    description="Sube un archivo de audio para transcripción y reconocimiento de comandos"
)
async def upload_audio_file(
    file: UploadFile = File(...),
    language_code: str = "es-ES"
) -> VoiceCommandResponse:
    """
    Upload audio file for transcription and command recognition.
    
    Args:
        file: Audio file (WAV, MP3, etc.)
        language_code: Language code for recognition
        
    Returns:
        Transcribed text and recognized command
    """
    # Check if service is available
    if not speech_to_text_service.is_available():
        raise HTTPException(
            status_code=503,
            detail={
                "error": "ServiceUnavailable",
                "message": "Google Cloud Speech-to-Text API not configured"
            }
        )
    
    try:
        # Read audio file
        audio_content = await file.read()
        
        # Transcribe
        transcript, confidence = speech_to_text_service.transcribe_audio(
            audio_content=audio_content,
            language_code=language_code
        )
        
        # Parse command
        dataset_key = voice_service.parse_command(transcript)
        
        return VoiceCommandResponse(
            transcript=transcript,
            command_recognized=dataset_key is not None,
            dataset_key=dataset_key,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ProcessingError",
                "message": f"Error processing audio file: {str(e)}"
            }
        )


@router.post(
    "/parse",
    response_model=VoiceCommandResponse,
    summary="Parse Text Command",
    description="Analiza un texto transcrito para reconocer comandos (no requiere API externa)"
)
async def parse_text_command(text: str) -> VoiceCommandResponse:
    """
    Parse already transcribed text to recognize commands.
    
    This endpoint is useful for testing command recognition without audio.
    
    Args:
        text: Transcribed text to parse
        
    Returns:
        Command recognition result
    """
    dataset_key = voice_service.parse_command(text)
    
    return VoiceCommandResponse(
        transcript=text,
        command_recognized=dataset_key is not None,
        dataset_key=dataset_key,
        confidence=1.0 if dataset_key else 0.0
    )


@router.post(
    "/demo",
    response_model=VoiceCommandResponse,
    summary="Demo Voice Command",
    description="Endpoint de demostración que simula comandos de voz sin necesidad de audio"
)
async def demo_voice_command(command_text: str) -> VoiceCommandResponse:
    """
    Demo endpoint that simulates voice command recognition.
    Useful for testing without Google Cloud API.
    
    Args:
        command_text: Text command to simulate (e.g., "Jarvis, predice el precio de Bitcoin")
        
    Returns:
        Simulated voice command response
    """
    dataset_key = voice_service.parse_command(command_text)
    
    return VoiceCommandResponse(
        transcript=command_text,
        command_recognized=dataset_key is not None,
        dataset_key=dataset_key,
        confidence=0.95  # Simulated confidence
    )


@router.get(
    "/status",
    summary="Check Voice Service Status",
    description="Verifica si el servicio de Speech-to-Text está disponible"
)
async def voice_service_status():
    """Check if Speech-to-Text service is available."""
    return {
        "available": speech_to_text_service.is_available(),
        "service": "Google Cloud Speech-to-Text",
        "credentials_configured": speech_to_text_service.is_available()
    }
