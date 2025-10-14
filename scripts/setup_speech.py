"""Script helper para configuración rápida de Speech-to-Text."""

import os
import sys
from pathlib import Path


def check_credentials():
    """Verifica si las credenciales están configuradas."""
    print("\n" + "=" * 60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN")
    print("=" * 60)
    
    # Check environment variable
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if creds_path:
        print(f"✓ Variable de entorno configurada:")
        print(f"  {creds_path}")
        
        # Check if file exists
        if os.path.exists(creds_path):
            print(f"✓ Archivo de credenciales existe")
            
            # Check if valid JSON
            try:
                import json
                with open(creds_path, 'r') as f:
                    data = json.load(f)
                
                if 'type' in data and data['type'] == 'service_account':
                    print(f"✓ Archivo JSON válido (Service Account)")
                    print(f"  Project ID: {data.get('project_id', 'N/A')}")
                    print(f"  Client Email: {data.get('client_email', 'N/A')}")
                    
                    print("\n✅ CONFIGURACIÓN CORRECTA")
                    print("   Puedes usar Speech-to-Text")
                    return True
                else:
                    print("✗ Archivo JSON no es de Service Account")
            except Exception as e:
                print(f"✗ Error leyendo JSON: {e}")
        else:
            print(f"✗ Archivo no existe en la ruta especificada")
    else:
        print("✗ Variable GOOGLE_APPLICATION_CREDENTIALS no configurada")
    
    print("\n❌ CONFIGURACIÓN INCOMPLETA")
    print_setup_instructions()
    return False


def print_setup_instructions():
    """Imprime instrucciones de configuración."""
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES DE CONFIGURACIÓN")
    print("=" * 60)
    
    print("\n1️⃣  OBTENER CREDENCIALES:")
    print("   • Ve a: https://console.cloud.google.com/")
    print("   • Crea un proyecto o selecciona uno existente")
    print("   • Habilita 'Cloud Speech-to-Text API'")
    print("   • Ve a: APIs y servicios → Credenciales")
    print("   • Crear credenciales → Cuenta de servicio")
    print("   • Descarga el archivo JSON")
    
    print("\n2️⃣  GUARDAR ARCHIVO:")
    project_root = Path(__file__).parent
    creds_dir = project_root / "credentials"
    
    print(f"   • Crea la carpeta: {creds_dir}")
    print(f"   • Guarda el archivo como: google-credentials.json")
    
    print("\n3️⃣  CONFIGURAR VARIABLE:")
    creds_file = creds_dir / "google-credentials.json"
    
    print(f"\n   PowerShell:")
    print(f'   $env:GOOGLE_APPLICATION_CREDENTIALS="{creds_file}"')
    
    print(f"\n   CMD:")
    print(f'   set GOOGLE_APPLICATION_CREDENTIALS={creds_file}')
    
    print(f"\n   Bash/Linux:")
    print(f'   export GOOGLE_APPLICATION_CREDENTIALS="{creds_file}"')
    
    print("\n4️⃣  VERIFICAR:")
    print("   python setup_speech.py")
    
    print("\n" + "=" * 60)


def create_credentials_folder():
    """Crea la carpeta de credenciales si no existe."""
    creds_dir = Path(__file__).parent / "credentials"
    
    if not creds_dir.exists():
        creds_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Carpeta creada: {creds_dir}")
        
        # Create README
        readme = creds_dir / "README.md"
        readme.write_text("""# Credenciales

Esta carpeta contiene las credenciales de Google Cloud.

**NO subir a Git** - Esta en .gitignore

## Archivo requerido:
- `google-credentials.json` - Credenciales de Service Account

## Como obtenerlo:
1. https://console.cloud.google.com/
2. APIs y servicios > Credenciales
3. Crear credenciales > Cuenta de servicio
4. Descargar JSON
""", encoding='utf-8')
        print(f"✓ README creado en: {readme}")
    else:
        print(f"✓ Carpeta ya existe: {creds_dir}")


def test_speech_service():
    """Prueba el servicio de Speech-to-Text."""
    try:
        from api.services import speech_to_text_service
        
        if speech_to_text_service.is_available():
            print("\n✅ Servicio de Speech-to-Text DISPONIBLE")
            print("\nPuedes probar con:")
            print("  python test_speech_to_text.py")
            return True
        else:
            print("\n⚠ Servicio NO disponible")
            print("  Configura las credenciales primero")
            return False
    
    except Exception as e:
        print(f"\n❌ Error al verificar servicio: {e}")
        return False


def main():
    """Main entry point."""
    print("\n🤖 JARVIS IA - Setup Speech-to-Text")
    
    # Create credentials folder
    create_credentials_folder()
    
    # Check configuration
    is_configured = check_credentials()
    
    if is_configured:
        # Test service
        test_speech_service()
        
        print("\n🎉 ¡TODO LISTO!")
        print("\nPróximos pasos:")
        print("  1. python test_speech_to_text.py    # Grabar y transcribir")
        print("  2. python run_api.py                # Iniciar API")
        print("  3. python test_voice_api.py         # Probar endpoints")
    else:
        print("\n⏳ Sigue las instrucciones arriba para configurar")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
