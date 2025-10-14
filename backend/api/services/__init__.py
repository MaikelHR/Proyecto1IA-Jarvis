"""Services initialization."""

from .speech_service import speech_to_text_service, SpeechToTextService
from .audio_utils import AudioRecorder, get_available_devices, print_available_devices
from .voice_command_service import voice_service, VoiceCommandService
from .model_service import model_service, ModelService
from .face_service import face_recognition_service, FaceRecognitionService
from .video_utils import VideoCapture, get_available_cameras, print_available_cameras

__all__ = [
    "speech_to_text_service",
    "SpeechToTextService",
    "AudioRecorder",
    "get_available_devices",
    "print_available_devices",
    "voice_service",
    "VoiceCommandService",
    "model_service",
    "ModelService",
    "face_recognition_service",
    "FaceRecognitionService",
    "VideoCapture",
    "get_available_cameras",
    "print_available_cameras",
]
