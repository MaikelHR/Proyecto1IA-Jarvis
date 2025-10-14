"""Pydantic models for API request/response validation."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Request model for predictions."""
    
    features: Dict[str, Any] = Field(
        ...,
        description="Dictionary of feature names and their values",
        example={
            "age": 45,
            "gender": "Male",
            "tenure": 24,
            "monthly_charges": 89.5
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": {
                    "age": 45,
                    "gender": "Male",
                    "tenure": 24
                }
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    
    dataset: str = Field(..., description="Name of the dataset/model used")
    prediction: Any = Field(..., description="Predicted value or class")
    task_type: str = Field(..., description="Type of ML task (regression/classification)")
    confidence: Optional[float] = Field(None, description="Confidence score (for classification)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "dataset": "Churn de clientes Telco",
                "prediction": 1,
                "task_type": "classification",
                "confidence": 0.87
            }
        }


class VoiceCommandRequest(BaseModel):
    """Request model for voice commands."""
    
    audio_base64: str = Field(
        ...,
        description="Base64 encoded audio data",
        min_length=10
    )
    language_code: str = Field(
        default="es-ES",
        description="Language code for speech recognition"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "audio_base64": "UklGRiQAAABXQVZFZm10...",
                "language_code": "es-ES"
            }
        }


class VoiceCommandResponse(BaseModel):
    """Response model for voice commands."""
    
    transcript: str = Field(..., description="Transcribed text from audio")
    command_recognized: bool = Field(..., description="Whether a valid command was recognized")
    dataset_key: Optional[str] = Field(None, description="Dataset key if command matched")
    confidence: float = Field(..., description="Speech recognition confidence")
    
    class Config:
        json_schema_extra = {
            "example": {
                "transcript": "Jarvis predice el precio de Bitcoin",
                "command_recognized": True,
                "dataset_key": "bitcoin_price",
                "confidence": 0.95
            }
        }


class FaceEmotionRequest(BaseModel):
    """Request model for face emotion analysis."""
    
    image_base64: str = Field(
        ...,
        description="Base64 encoded image data",
        min_length=10
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_base64": "/9j/4AAQSkZJRgABAQEA..."
            }
        }


class FaceEmotionResponse(BaseModel):
    """Response model for face emotion analysis."""
    
    emotions: Dict[str, float] = Field(
        ...,
        description="Detected emotions with confidence scores"
    )
    dominant_emotion: str = Field(..., description="Most prominent emotion detected")
    face_detected: bool = Field(..., description="Whether a face was detected")
    
    class Config:
        json_schema_extra = {
            "example": {
                "emotions": {
                    "happiness": 0.85,
                    "neutral": 0.10,
                    "sadness": 0.05
                },
                "dominant_emotion": "happiness",
                "face_detected": True
            }
        }


class DatasetInfo(BaseModel):
    """Information about available datasets."""
    
    key: str = Field(..., description="Dataset key identifier")
    name: str = Field(..., description="Human-readable name")
    task: str = Field(..., description="Task type (regression/classification/time_series)")
    target: str = Field(..., description="Target variable name")
    description: str = Field(..., description="Dataset description")
    voice_commands: List[str] = Field(..., description="Example voice commands")
    
    class Config:
        json_schema_extra = {
            "example": {
                "key": "telco_churn",
                "name": "Churn de clientes Telco",
                "task": "classification",
                "target": "churn",
                "description": "Predicción de abandono de clientes",
                "voice_commands": [
                    "predice el churn",
                    "analiza riesgo de abandono"
                ]
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    models_loaded: int = Field(..., description="Number of models loaded")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "models_loaded": 9
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Detailed error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ModelNotFound",
                "message": "The requested model does not exist",
                "details": {"dataset_key": "invalid_key"}
            }
        }
