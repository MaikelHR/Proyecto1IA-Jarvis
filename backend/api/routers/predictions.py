"""Prediction endpoints for ML models."""

from typing import List

from fastapi import APIRouter, HTTPException

from ..models import (
    PredictionRequest,
    PredictionResponse,
    DatasetInfo as DatasetInfoModel,
    ErrorResponse
)
from ..services.model_service import model_service
from ..services.voice_command_service import voice_service

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get(
    "/datasets",
    response_model=List[DatasetInfoModel],
    summary="List Available Datasets",
    description="Obtiene la lista de todos los datasets y modelos disponibles"
)
async def list_datasets() -> List[DatasetInfoModel]:
    """List all available datasets with their information."""
    datasets = []
    
    for dataset_key in model_service.get_available_models():
        info = model_service.get_model_info(dataset_key)
        if info:
            datasets.append(
                DatasetInfoModel(
                    key=dataset_key,
                    name=info.name,
                    task=info.task.value,
                    target=info.target,
                    description=info.description,
                    voice_commands=voice_service.get_command_examples(dataset_key)
                )
            )
    
    return datasets


@router.post(
    "/{dataset_key}",
    response_model=PredictionResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Model not found"},
        400: {"model": ErrorResponse, "description": "Invalid input features"}
    },
    summary="Make Prediction",
    description="Realiza una predicción usando el modelo especificado"
)
async def make_prediction(
    dataset_key: str,
    request: PredictionRequest
) -> PredictionResponse:
    """
    Make a prediction using the specified model.
    
    Args:
        dataset_key: Identifier of the dataset/model (e.g., 'telco_churn', 'bitcoin_price')
        request: Features for prediction
        
    Returns:
        Prediction result with confidence score
        
    Raises:
        HTTPException: If model not found or prediction fails
    """
    try:
        # Log incoming request for debugging
        print(f"\n🔍 Predicción para: {dataset_key}")
        print(f"📥 Features recibidas: {request.features}")
        print(f"📊 Tipo de features: {type(request.features)}")
        print(f"📊 Keys: {list(request.features.keys())}")
        
        # Get dataset info
        dataset_info = model_service.get_model_info(dataset_key)
        if not dataset_info:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ModelNotFound",
                    "message": f"Model '{dataset_key}' not found",
                    "details": {
                        "available_models": model_service.get_available_models()
                    }
                }
            )
        
        # Make prediction
        prediction, confidence = model_service.predict(dataset_key, request.features)
        print(f"✅ Predicción exitosa: {prediction} (confianza: {confidence})")
        
        return PredictionResponse(
            dataset=dataset_info.name,
            prediction=prediction,
            task_type=dataset_info.task.value,
            confidence=confidence
        )
    
    except ValueError as e:
        print(f"❌ ValueError: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail={
                "error": "PredictionError",
                "message": str(e),
                "details": {"features": request.features}
            }
        )
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": f"Unexpected error: {str(e)}"
            }
        )


@router.get(
    "/{dataset_key}/info",
    response_model=DatasetInfoModel,
    responses={
        404: {"model": ErrorResponse, "description": "Dataset not found"}
    },
    summary="Get Dataset Info",
    description="Obtiene información detallada sobre un dataset específico"
)
async def get_dataset_info(dataset_key: str) -> DatasetInfoModel:
    """Get detailed information about a specific dataset."""
    info = model_service.get_model_info(dataset_key)
    
    if not info:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "DatasetNotFound",
                "message": f"Dataset '{dataset_key}' not found",
                "details": {
                    "available_datasets": model_service.get_available_models()
                }
            }
        )
    
    return DatasetInfoModel(
        key=dataset_key,
        name=info.name,
        task=info.task.value,
        target=info.target,
        description=info.description,
        voice_commands=voice_service.get_command_examples(dataset_key)
    )
