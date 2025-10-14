"""Script para iniciar el servidor API de Jarvis IA."""

import uvicorn

if __name__ == "__main__":
    print("🤖 Iniciando Jarvis IA API...")
    print("📚 Documentación disponible en: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
