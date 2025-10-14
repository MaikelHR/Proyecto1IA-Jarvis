"""Health check endpoints."""

from fastapi import APIRouter

from ..models import HealthResponse
from ..services.model_service import model_service

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica el estado de la API y modelos cargados"
)
async def health_check() -> HealthResponse:
    """Check API health and models status."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        models_loaded=model_service.get_models_count()
    )
