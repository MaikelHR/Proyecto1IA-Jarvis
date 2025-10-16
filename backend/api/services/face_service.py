"""Face recognition and emotion detection service using Azure Face API with local fallback."""

from __future__ import annotations

import os
import tempfile
from io import BytesIO
from typing import Dict, List, Optional, Tuple

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import (
    FaceAttributeType,
    DetectedFace,
)
from msrest.authentication import CognitiveServicesCredentials


class FaceRecognitionService:
    """
    Service for face detection and emotion analysis.
    
    Uses Azure Face API as primary service with DeepFace as local fallback.
    This hybrid approach ensures functionality during Azure approval process.
    """
    
    # Emotion labels in Spanish
    EMOTION_LABELS_ES = {
        "anger": "enojo",
        "contempt": "desprecio",
        "disgust": "disgusto",
        "fear": "miedo",
        "happiness": "felicidad",
        "happy": "felicidad",  # DeepFace usa "happy"
        "neutral": "neutral",
        "sadness": "tristeza",
        "sad": "tristeza",  # DeepFace usa "sad"
        "surprise": "sorpresa",
    }
    
    def __init__(self):
        """Initialize the Face Recognition client with hybrid support."""
        self._client: Optional[FaceClient] = None
        self._credentials_configured = False
        self._local_fallback_available = False
        self._check_credentials()
        self._init_local_fallback()
    
    def _check_credentials(self) -> None:
        """Check if Azure Face API credentials are configured."""
        self.api_key = os.getenv("AZURE_FACE_KEY")
        self.endpoint = os.getenv("AZURE_FACE_ENDPOINT")
        
        if self.api_key and self.endpoint:
            self._credentials_configured = True
            print(f"✓ Azure Face API configurada (Primary)")
            print(f"  Endpoint: {self.endpoint}")
        else:
            self._credentials_configured = False
            print("⚠ Azure Face API NO configurada")
            print("  Configure AZURE_FACE_KEY y AZURE_FACE_ENDPOINT")
    
    def _init_local_fallback(self) -> None:
        """Initialize local emotion detection as fallback."""
        try:
            # Try importing DeepFace with detailed error reporting
            import sys
            import deepface
            from deepface import DeepFace
            self._local_fallback_available = True
            print("+ DeepFace disponible (Local Fallback)")
            print("  Nota: Se usara si Azure Face API no esta disponible")
        except ImportError as e:
            self._local_fallback_available = False
            print(f"! DeepFace no disponible: {str(e)}")
            print("  Instalar con: pip install deepface")
        except Exception as e:
            self._local_fallback_available = False
            print(f"! Error al cargar DeepFace: {str(e)}")
    
    def _get_client(self) -> FaceClient:
        """Get or create Face API client."""
        if not self._credentials_configured:
            raise ValueError(
                "Azure Face API credentials not configured. "
                "Set AZURE_FACE_KEY and AZURE_FACE_ENDPOINT environment variables."
            )
        
        if self._client is None:
            credentials = CognitiveServicesCredentials(self.api_key)
            self._client = FaceClient(self.endpoint, credentials)
        
        return self._client
    
    def is_available(self) -> bool:
        """Check if the service is available (credentials configured)."""
        return self._credentials_configured
    
    def detect_faces(
        self,
        image_data: bytes,
        return_face_attributes: bool = True,
        return_face_landmarks: bool = False,
    ) -> List[DetectedFace]:
        """
        Detect faces in an image.
        
        Args:
            image_data: Image data in bytes
            return_face_attributes: Whether to return face attributes
            return_face_landmarks: Whether to return face landmarks
            
        Returns:
            List of detected faces
        """
        client = self._get_client()
        
        # Define attributes to detect
        face_attributes = None
        if return_face_attributes:
            face_attributes = [
                FaceAttributeType.emotion,
                FaceAttributeType.age,
                FaceAttributeType.gender,
                FaceAttributeType.smile,
                FaceAttributeType.glasses,
                FaceAttributeType.hair,
                FaceAttributeType.facial_hair,
                FaceAttributeType.head_pose,
                FaceAttributeType.accessories,
                FaceAttributeType.blur,
                FaceAttributeType.exposure,
                FaceAttributeType.noise,
            ]
        
        # Wrap bytes in BytesIO for stream processing
        image_stream = BytesIO(image_data)
        
        try:
            # Detect faces
            detected_faces = client.face.detect_with_stream(
                image=image_stream,
                return_face_attributes=face_attributes,
                return_face_landmarks=return_face_landmarks,
                recognition_model="recognition_04",  # Latest model
                detection_model="detection_03",      # Latest detection model
            )
            
            return detected_faces
        except Exception as e:
            print(f"❌ Error detallado de Azure Face API:")
            print(f"   - Tipo de error: {type(e).__name__}")
            print(f"   - Mensaje: {str(e)}")
            if hasattr(e, 'response'):
                print(f"   - Response: {e.response}")
            if hasattr(e, 'error'):
                print(f"   - Error details: {e.error}")
            raise
    
    def analyze_emotions(
        self,
        image_data: bytes
    ) -> Dict[str, any]:
        """
        Analyze emotions from an image using hybrid approach.
        
        Tries Azure Face API first, falls back to DeepFace if Azure fails.
        
        Args:
            image_data: Image data in bytes
            
        Returns:
            Dictionary with emotion analysis results
        """
        print(f"🔍 Analizando emociones (Hybrid Mode)...")
        print(f"   - Tamaño de imagen: {len(image_data)} bytes")
        
        # Try Azure Face API first
        if self._credentials_configured:
            try:
                print(f"   - Intentando con Azure Face API...")
                return self._analyze_emotions_azure(image_data)
            except Exception as e:
                print(f"⚠️ Azure Face API falló: {str(e)}")
                print(f"   - Probablemente requiere aprobación de Microsoft")
                print(f"   - Cambiando a fallback local (DeepFace)...")
        
        # Fallback to local DeepFace
        if self._local_fallback_available:
            try:
                print(f"   - Usando DeepFace (Local Fallback)...")
                return self._analyze_emotions_local(image_data)
            except Exception as e:
                print(f"❌ Error en DeepFace: {str(e)}")
                raise
        
        # No service available
        raise ValueError(
            "No emotion detection service available. "
            "Azure requires approval and DeepFace is not installed."
        )
    
    def _analyze_emotions_azure(self, image_data: bytes) -> Dict[str, any]:
        """
        Analyze emotions using Azure Face API.
        
        Args:
            image_data: Image data in bytes
            
        Returns:
            Dictionary with emotion analysis results
        """
        faces = self.detect_faces(image_data)
        
        if not faces:
            return {
                "face_detected": False,
                "num_faces": 0,
                "emotions": {},
                "dominant_emotion": None,
                "confidence": 0.0,
                "message": "No se detectó ningún rostro en la imagen"
            }
        
        # Get first face (main subject)
        face = faces[0]
        
        if not face.face_attributes or not face.face_attributes.emotion:
            return {
                "face_detected": True,
                "num_faces": len(faces),
                "emotions": {},
                "dominant_emotion": None,
                "confidence": 0.0,
                "message": "No se pudieron detectar emociones"
            }
        
        # Extract emotion scores
        emotion = face.face_attributes.emotion
        emotions = {
            "anger": emotion.anger,
            "contempt": emotion.contempt,
            "disgust": emotion.disgust,
            "fear": emotion.fear,
            "happiness": emotion.happiness,
            "neutral": emotion.neutral,
            "sadness": emotion.sadness,
            "surprise": emotion.surprise,
        }
        
        # Find dominant emotion
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        
        return {
            "face_detected": True,
            "num_faces": len(faces),
            "emotions": emotions,
            "emotions_es": {
                self.EMOTION_LABELS_ES[k]: v 
                for k, v in emotions.items()
            },
            "dominant_emotion": dominant_emotion[0],
            "dominant_emotion_es": self.EMOTION_LABELS_ES[dominant_emotion[0]],
            "confidence": dominant_emotion[1],
            "message": f"Emoción detectada: {self.EMOTION_LABELS_ES[dominant_emotion[0]]} ({dominant_emotion[1]:.2%})"
        }
    
    def analyze_face_attributes(
        self,
        image_data: bytes
    ) -> Dict[str, any]:
        """
        Analyze face attributes from an image.
        
        Args:
            image_data: Image data in bytes
            
        Returns:
            Dictionary with face analysis results
        """
        faces = self.detect_faces(image_data)
        
        if not faces:
            return {
                "face_detected": False,
                "message": "No se detectó ningún rostro"
            }
        
        face = faces[0]
        attrs = face.face_attributes
        
        result = {
            "face_detected": True,
            "face_id": face.face_id,
            "face_rectangle": {
                "left": face.face_rectangle.left,
                "top": face.face_rectangle.top,
                "width": face.face_rectangle.width,
                "height": face.face_rectangle.height,
            },
        }
        
        # Add attributes if available
        if attrs:
            result.update({
                "age": attrs.age,
                "gender": attrs.gender.value if attrs.gender else None,
                "smile": attrs.smile,
                "glasses": attrs.glasses.value if attrs.glasses else None,
            })
            
            # Emotions
            if attrs.emotion:
                result["emotions"] = self.analyze_emotions(image_data)
            
            # Hair
            if attrs.hair:
                result["hair"] = {
                    "bald": attrs.hair.bald,
                    "invisible": attrs.hair.invisible,
                    "hair_color": [
                        {"color": hc.color.value, "confidence": hc.confidence}
                        for hc in attrs.hair.hair_color
                    ] if attrs.hair.hair_color else []
                }
            
            # Facial hair
            if attrs.facial_hair:
                result["facial_hair"] = {
                    "moustache": attrs.facial_hair.moustache,
                    "beard": attrs.facial_hair.beard,
                    "sideburns": attrs.facial_hair.sideburns,
                }
            
            # Head pose
            if attrs.head_pose:
                result["head_pose"] = {
                    "pitch": attrs.head_pose.pitch,
                    "roll": attrs.head_pose.roll,
                    "yaw": attrs.head_pose.yaw,
                }
            
            # Image quality
            if attrs.blur:
                result["blur"] = {
                    "blur_level": attrs.blur.blur_level.value,
                    "value": attrs.blur.value,
                }
            
            if attrs.exposure:
                result["exposure"] = {
                    "exposure_level": attrs.exposure.exposure_level.value,
                    "value": attrs.exposure.value,
                }
            
            if attrs.noise:
                result["noise"] = {
                    "noise_level": attrs.noise.noise_level.value,
                    "value": attrs.noise.value,
                }
        
        return result
    
    def detect_multiple_faces(
        self,
        image_data: bytes
    ) -> List[Dict[str, any]]:
        """
        Detect and analyze multiple faces in an image.
        
        Args:
            image_data: Image data in bytes
            
        Returns:
            List of face analysis results
        """
        faces = self.detect_faces(image_data)
        
        results = []
        for face in faces:
            attrs = face.face_attributes
            
            face_data = {
                "face_id": face.face_id,
                "face_rectangle": {
                    "left": face.face_rectangle.left,
                    "top": face.face_rectangle.top,
                    "width": face.face_rectangle.width,
                    "height": face.face_rectangle.height,
                },
            }
            
            if attrs:
                # Basic attributes
                face_data["age"] = attrs.age
                face_data["gender"] = attrs.gender.value if attrs.gender else None
                
                # Emotions
                if attrs.emotion:
                    emotions = {
                        "anger": attrs.emotion.anger,
                        "happiness": attrs.emotion.happiness,
                        "neutral": attrs.emotion.neutral,
                        "sadness": attrs.emotion.sadness,
                        "surprise": attrs.emotion.surprise,
                    }
                    dominant = max(emotions.items(), key=lambda x: x[1])
                    face_data["emotion"] = {
                        "dominant": dominant[0],
                        "dominant_es": self.EMOTION_LABELS_ES[dominant[0]],
                        "confidence": dominant[1],
                    }
            
            results.append(face_data)
        
        return results
    
    def _analyze_emotions_local(self, image_data: bytes) -> Dict[str, any]:
        """
        Analyze emotions using DeepFace (local fallback).
        
        Args:
            image_data: Image data in bytes
            
        Returns:
            Dictionary with emotion analysis results in same format as Azure
        """
        from deepface import DeepFace
        import numpy as np
        import cv2
        
        # Convert bytes to numpy array for OpenCV
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("No se pudo decodificar la imagen")
        
        # Analyze with DeepFace
        try:
            result = DeepFace.analyze(
                img_path=img,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            # DeepFace returns a list if multiple faces, dict if single face
            if isinstance(result, list):
                if len(result) == 0:
                    return {
                        "face_detected": False,
                        "num_faces": 0,
                        "emotions": {},
                        "dominant_emotion": None,
                        "confidence": 0.0,
                        "message": "No se detectó ningún rostro en la imagen",
                        "source": "deepface"
                    }
                result = result[0]  # Use first face
            
            # Extract emotions
            emotions_raw = result.get('emotion', {})
            
            # Normalize emotion names to match Azure format
            # Convert numpy.float32 to native Python float
            emotions = {
                "anger": float(emotions_raw.get('angry', 0)) / 100,
                "disgust": float(emotions_raw.get('disgust', 0)) / 100,
                "fear": float(emotions_raw.get('fear', 0)) / 100,
                "happiness": float(emotions_raw.get('happy', 0)) / 100,
                "neutral": float(emotions_raw.get('neutral', 0)) / 100,
                "sadness": float(emotions_raw.get('sad', 0)) / 100,
                "surprise": float(emotions_raw.get('surprise', 0)) / 100,
                "contempt": 0.0  # DeepFace no tiene contempt
            }
            
            # Find dominant emotion
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            
            return {
                "face_detected": True,
                "num_faces": 1,
                "emotions": emotions,
                "emotions_es": {
                    self.EMOTION_LABELS_ES.get(k, k): float(v) 
                    for k, v in emotions.items()
                },
                "dominant_emotion": dominant_emotion[0],
                "dominant_emotion_es": self.EMOTION_LABELS_ES.get(
                    dominant_emotion[0], 
                    dominant_emotion[0]
                ),
                "confidence": float(dominant_emotion[1]),
                "message": f"Emoción detectada: {self.EMOTION_LABELS_ES.get(dominant_emotion[0], dominant_emotion[0])} ({dominant_emotion[1]:.2%})",
                "source": "deepface"  # Indicate this came from local fallback
            }
            
        except Exception as e:
            print(f"❌ Error en análisis DeepFace: {str(e)}")
            raise


# Global singleton instance
face_recognition_service = FaceRecognitionService()
