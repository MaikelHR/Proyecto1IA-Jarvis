"""Face emotion recognition endpoints (Azure Face API integration)."""

import base64
from typing import Dict, List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from ..services import face_recognition_service

router = APIRouter(prefix="/face", tags=["Face Recognition"])


# Request/Response Models
class ImageBase64Request(BaseModel):
    """Request model for base64 encoded image."""
    image: str  # Base64 encoded image


class EmotionResponse(BaseModel):
    """Response model for emotion detection."""
    face_detected: bool
    num_faces: int
    emotions: Dict[str, float]
    emotions_es: Optional[Dict[str, float]] = None
    dominant_emotion: Optional[str] = None
    dominant_emotion_es: Optional[str] = None
    confidence: float
    message: str


class FaceAttributesResponse(BaseModel):
    """Response model for face attributes analysis."""
    face_detected: bool
    message: Optional[str] = None


class FaceStatusResponse(BaseModel):
    """Response model for face service status."""
    available: bool
    message: str


# Endpoints
@router.get("/status", response_model=FaceStatusResponse)
async def get_face_service_status():
    """
    Get Face Recognition service status.
    
    Returns service availability and configuration status.
    """
    available = face_recognition_service.is_available()
    
    if available:
        message = "Face Recognition service disponible"
    else:
        message = (
            "Face Recognition service NO disponible. "
            "Configure AZURE_FACE_KEY y AZURE_FACE_ENDPOINT"
        )
    
    return {
        "available": available,
        "message": message
    }


@router.post("/emotion", response_model=EmotionResponse)
async def detect_emotion_base64(request: ImageBase64Request):
    """
    Detect emotions from base64 encoded image.
    
    Args:
        request: ImageBase64Request with base64 encoded image
        
    Returns:
        EmotionResponse with detected emotions
    """
    if not face_recognition_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Face Recognition service not configured"
        )
    
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image)
        
        # Analyze emotions
        result = face_recognition_service.analyze_emotions(image_data)
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing emotions: {str(e)}"
        )


@router.post("/emotion/upload")
async def detect_emotion_upload(file: UploadFile = File(...)):
    """
    Detect emotions from uploaded image file.
    
    Args:
        file: Uploaded image file
        
    Returns:
        EmotionResponse with detected emotions
    """
    if not face_recognition_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Face Recognition service not configured"
        )
    
    try:
        # Read file content
        image_data = await file.read()
        
        # Log image info
        print(f"📷 Imagen recibida:")
        print(f"   - Tamaño: {len(image_data)} bytes")
        print(f"   - Tipo: {file.content_type}")
        print(f"   - Nombre: {file.filename}")
        
        # Validate image data
        if len(image_data) == 0:
            raise ValueError("La imagen está vacía")
        
        # Analyze emotions
        result = face_recognition_service.analyze_emotions(image_data)
        
        return result
    
    except Exception as e:
        print(f"❌ Error en emotion/upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing emotions: {str(e)}"
        )


@router.post("/analyze")
async def analyze_face_attributes(file: UploadFile = File(...)):
    """
    Analyze face attributes from uploaded image.
    
    Returns comprehensive face analysis including:
    - Age estimation
    - Gender detection
    - Emotion analysis
    - Facial features (hair, glasses, etc.)
    - Image quality metrics
    
    Args:
        file: Uploaded image file
        
    Returns:
        Detailed face analysis results
    """
    if not face_recognition_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Face Recognition service not configured"
        )
    
    try:
        # Read file content
        image_data = await file.read()
        
        # Analyze face attributes
        result = face_recognition_service.analyze_face_attributes(image_data)
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing face: {str(e)}"
        )


@router.post("/analyze/base64")
async def analyze_face_attributes_base64(request: ImageBase64Request):
    """
    Analyze face attributes from base64 encoded image.
    
    Args:
        request: ImageBase64Request with base64 encoded image
        
    Returns:
        Detailed face analysis results
    """
    if not face_recognition_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Face Recognition service not configured"
        )
    
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image)
        
        # Analyze face attributes
        result = face_recognition_service.analyze_face_attributes(image_data)
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing face: {str(e)}"
        )


@router.post("/detect/multiple")
async def detect_multiple_faces(file: UploadFile = File(...)):
    """
    Detect and analyze multiple faces in an image.
    
    Args:
        file: Uploaded image file
        
    Returns:
        List of detected faces with basic analysis
    """
    if not face_recognition_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Face Recognition service not configured"
        )
    
    try:
        # Read file content
        image_data = await file.read()
        
        # Detect multiple faces
        result = face_recognition_service.detect_multiple_faces(image_data)
        
        return {
            "num_faces": len(result),
            "faces": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting faces: {str(e)}"
        )
