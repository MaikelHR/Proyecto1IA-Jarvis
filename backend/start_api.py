"""Script mejorado para iniciar la API con credenciales configuradas."""

import os
import sys
from pathlib import Path


def configure_credentials():
    """Configure Google Cloud and Azure credentials if not already set."""
    project_root = Path(__file__).parent.parent  # backend/ -> project root
    
    # Configure Google Cloud credentials
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not creds_path:
        # Try to find credentials in default location
        default_creds = project_root / "config" / "credentials" / "google-credentials.json"
        
        if default_creds.exists():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(default_creds)
            print(f"✓ Google Cloud credentials: {default_creds}")
        else:
            print("⚠ Google Cloud credentials no encontradas")
            print(f"  Buscando en: {default_creds}")
    else:
        print(f"✓ Google Cloud credentials: {creds_path}")
    
    # Configure Azure Face API credentials
    azure_key = os.getenv("AZURE_FACE_KEY")
    azure_endpoint = os.getenv("AZURE_FACE_ENDPOINT")
    
    if not azure_key or not azure_endpoint:
        # Try to load from .env file
        env_file = project_root / "config" / ".env.azure"
        if env_file.exists():
            print(f"📄 Cargando configuración de Azure desde: {env_file}")
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key == "AZURE_FACE_KEY" and not azure_key:
                            os.environ["AZURE_FACE_KEY"] = value
                            print(f"✓ Azure Face Key configurada desde .env.azure")
                        elif key == "AZURE_FACE_ENDPOINT" and not azure_endpoint:
                            os.environ["AZURE_FACE_ENDPOINT"] = value
                            print(f"✓ Azure Face Endpoint configurado desde .env.azure")
        else:
            print("⚠ Azure Face API no configurada")
            print(f"  Crea el archivo: {env_file}")
            print(f"  Usa como plantilla: {project_root / 'config' / '.env.azure.example'}")
    else:
        print("✓ Azure Face API configurada desde variables de entorno")


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
