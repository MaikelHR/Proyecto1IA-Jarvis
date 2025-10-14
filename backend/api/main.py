"""FastAPI main application for Jarvis IA."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .routers import health, predictions, voice, face

# Create FastAPI application
app = FastAPI(
    title="Jarvis IA - API REST",
    description="""
    🤖 **Jarvis IA** es un asistente inteligente que integra:
    
    - 🎯 **Machine Learning**: 9 modelos predictivos entrenados
    - 🎤 **Reconocimiento de Voz**: Comandos por voz (Speech-to-Text)
    - 😊 **Análisis Facial**: Detección de emociones (Azure Face API)
    
    ## Características
    
    - ✅ Predicciones de ML para diversos casos de uso
    - ✅ API REST completa con documentación automática
    - ✅ Sistema de comandos de voz inteligente
    - ✅ Análisis de sentimientos faciales en tiempo real
    
    ## Modelos Disponibles
    
    1. **Bitcoin Price** - Predicción de precios de criptomonedas
    2. **Avocado Prices** - Precios de aguacate por región
    3. **Body Fat** - Porcentaje de grasa corporal
    4. **Car Prices** - Valor de automóviles usados
    5. **Telco Churn** - Predicción de abandono de clientes
    6. **Wine Quality** - Clasificación de calidad de vinos
    7. **Stroke Risk** - Predicción de riesgo de derrame cerebral
    8. **Hepatitis C** - Diagnóstico de hepatitis C
    9. **Cirrhosis Status** - Estado clínico de cirrosis
    
    ## Uso Rápido
    
    ```bash
    # Iniciar servidor
    uvicorn api.main:app --reload
    
    # Verificar salud
    curl http://localhost:8000/health
    
    # Listar modelos
    curl http://localhost:8000/predictions/datasets
    
    # Hacer predicción
    curl -X POST http://localhost:8000/predictions/telco_churn \\
         -H "Content-Type: application/json" \\
         -d '{"features": {"age": 45, "tenure": 24}}'
    ```
    
    ## Autor
    
    Proyecto IA - TEC
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(predictions.router)
app.include_router(voice.router)
app.include_router(face.router)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/api", include_in_schema=False)
async def api_root():
    """Redirect /api to documentation."""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
