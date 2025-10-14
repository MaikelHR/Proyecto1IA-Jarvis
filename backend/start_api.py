"""Script mejorado para iniciar la API con credenciales configuradas."""

import os
import sys
from pathlib import Path


def configure_credentials():
    """Configure Google Cloud credentials if not already set."""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not creds_path:
        # Try to find credentials in default location
        project_root = Path(__file__).parent.parent  # backend/ -> project root
        default_creds = project_root / "config" / "credentials" / "google-credentials.json"
        
        if default_creds.exists():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(default_creds)
            print(f"✓ Credenciales configuradas automáticamente: {default_creds}")
        else:
            print("⚠ Advertencia: Google Cloud credentials no encontradas")
            print(f"  Buscando en: {default_creds}")
            print("  Speech-to-Text no estará disponible")
    else:
        print(f"✓ Usando credenciales: {creds_path}")


def main():
    """Start the API server."""
    configure_credentials()
    
    print("\n🤖 Iniciando Jarvis IA API...")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print()
    
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
