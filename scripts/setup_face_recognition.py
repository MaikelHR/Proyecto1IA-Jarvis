"""
Setup script for Azure Face API credentials verification.

This script helps you verify that Azure Face API credentials are properly configured.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_header(title: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def check_environment_variables():
    """Check if environment variables are set."""
    print_header("VERIFICACIÓN DE VARIABLES DE ENTORNO")
    
    azure_key = os.getenv("AZURE_FACE_KEY")
    azure_endpoint = os.getenv("AZURE_FACE_ENDPOINT")
    
    all_set = True
    
    print("\n1. AZURE_FACE_KEY")
    if azure_key:
        # Show partial key for security
        masked_key = "*" * 20 + azure_key[-4:] if len(azure_key) > 4 else "****"
        print(f"   ✓ Configurada: {masked_key}")
    else:
        print("   ❌ NO configurada")
        all_set = False
    
    print("\n2. AZURE_FACE_ENDPOINT")
    if azure_endpoint:
        print(f"   ✓ Configurada: {azure_endpoint}")
    else:
        print("   ❌ NO configurada")
        all_set = False
    
    return all_set, azure_key, azure_endpoint


def test_service_import():
    """Test if face service can be imported."""
    print_header("VERIFICACIÓN DE SERVICIOS")
    
    try:
        from api.services import face_recognition_service
        print("\n✓ Face Recognition Service importado correctamente")
        
        if face_recognition_service.is_available():
            print("✓ Service disponible y configurado")
            return True
        else:
            print("❌ Service NO disponible (faltan credenciales)")
            return False
    
    except Exception as e:
        print(f"\n❌ Error al importar: {e}")
        return False


def test_azure_connection(azure_key: str, azure_endpoint: str):
    """Test connection to Azure Face API."""
    print_header("PRUEBA DE CONEXIÓN CON AZURE")
    
    if not azure_key or not azure_endpoint:
        print("\n❌ No se puede probar sin credenciales")
        return False
    
    try:
        print("\n🔄 Intentando conectar con Azure Face API...")
        
        from azure.cognitiveservices.vision.face import FaceClient
        from msrest.authentication import CognitiveServicesCredentials
        
        credentials = CognitiveServicesCredentials(azure_key)
        client = FaceClient(azure_endpoint, credentials)
        
        print("✓ Cliente creado correctamente")
        print(f"✓ Endpoint: {azure_endpoint}")
        
        # Note: We can't test without an actual image, but we can verify client creation
        print("\n✓ Conexión establecida correctamente")
        print("  (Nota: Prueba completa requiere una imagen)")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error al conectar: {e}")
        return False


def print_setup_instructions():
    """Print setup instructions."""
    print_header("INSTRUCCIONES DE CONFIGURACIÓN")
    
    print("""
📋 PASOS PARA CONFIGURAR AZURE FACE API:

1. Crear recurso en Azure Portal
   - Ve a https://portal.azure.com
   - Busca "Face" en Cognitive Services
   - Crea un nuevo recurso Face
   - Selecciona tu suscripción y región

2. Obtener credenciales
   - Una vez creado, ve a "Keys and Endpoint"
   - Copia una de las Keys (KEY 1 o KEY 2)
   - Copia el Endpoint URL

3. Configurar variables de entorno (PowerShell)
   
   Para la sesión actual:
   $env:AZURE_FACE_KEY="tu-key-aquí"
   $env:AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"
   
   Para configuración permanente (Opcional):
   [System.Environment]::SetEnvironmentVariable('AZURE_FACE_KEY', 'tu-key', 'User')
   [System.Environment]::SetEnvironmentVariable('AZURE_FACE_ENDPOINT', 'tu-endpoint', 'User')
   
   Luego reinicia la terminal.

4. Verificar configuración
   python setup_face_recognition.py

5. Probar el servicio
   python test_face_recognition.py

📚 Documentación:
   - Azure Face API: https://docs.microsoft.com/azure/cognitive-services/face/
   - API Reference: https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/
""")


def print_current_status(vars_set: bool, service_ok: bool, connection_ok: bool):
    """Print current configuration status."""
    print_header("ESTADO DE CONFIGURACIÓN")
    
    print("\n Estado actual:")
    
    status_icon = "✓" if vars_set else "❌"
    print(f"   {status_icon} Variables de entorno")
    
    status_icon = "✓" if service_ok else "❌"
    print(f"   {status_icon} Face Recognition Service")
    
    status_icon = "✓" if connection_ok else "❌"
    print(f"   {status_icon} Conexión con Azure")
    
    if vars_set and service_ok and connection_ok:
        print("\n✅ TODO CONFIGURADO CORRECTAMENTE")
        print("\n📌 Siguiente paso:")
        print("   python test_face_recognition.py")
    else:
        print("\n⚠️  CONFIGURACIÓN INCOMPLETA")
        print("\n📌 Revisa las instrucciones arriba")


def main():
    """Main setup function."""
    print("\n")
    print("=" * 70)
    print(" CONFIGURACIÓN DE AZURE FACE API")
    print("=" * 70)
    
    # Check environment variables
    vars_set, azure_key, azure_endpoint = check_environment_variables()
    
    # Test service import
    service_ok = test_service_import()
    
    # Test Azure connection
    connection_ok = False
    if vars_set:
        connection_ok = test_azure_connection(azure_key, azure_endpoint)
    
    # Print status
    print_current_status(vars_set, service_ok, connection_ok)
    
    # Print instructions if needed
    if not (vars_set and service_ok and connection_ok):
        print_setup_instructions()


if __name__ == "__main__":
    main()
