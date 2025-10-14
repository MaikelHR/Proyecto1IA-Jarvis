"""
🤖 Jarvis IA - Script Principal de Ejecución
===========================================

Este script facilita la ejecución del proyecto desde la raíz.
"""
import sys
import subprocess
from pathlib import Path


def print_menu():
    """Muestra el menú principal."""
    print("\n" + "="*60)
    print("🤖 JARVIS IA - MENÚ PRINCIPAL".center(60))
    print("="*60)
    print("\n1. 🚀 Iniciar Backend (API)")
    print("2. 🧪 Ejecutar Pruebas Completas (9 modelos)")
    print("3. ⚡ Prueba Rápida")
    print("4. 🔍 Verificar Modelos")
    print("5. 📊 Ver Estructura del Proyecto")
    print("6. 📚 Abrir Documentación")
    print("7. ❌ Salir")
    print("="*60)


def start_backend():
    """Inicia el backend."""
    print("\n🚀 Iniciando Backend...")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("\nPresiona Ctrl+C para detener\n")
    
    backend_path = Path(__file__).parent / "backend"
    
    # Verificar si existe start_api_with_env.ps1
    ps1_script = backend_path / "start_api_with_env.ps1"
    
    if ps1_script.exists():
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps1_script)],
            cwd=backend_path
        )
    else:
        # Fallback a start_api.py
        subprocess.run(
            [sys.executable, "start_api.py"],
            cwd=backend_path
        )


def run_tests():
    """Ejecuta las pruebas completas."""
    print("\n🧪 Ejecutando Pruebas Completas...")
    
    tests_path = Path(__file__).parent / "tests"
    test_script = tests_path / "test_completo_9_modelos.py"
    
    if test_script.exists():
        subprocess.run([sys.executable, str(test_script)], cwd=tests_path)
    else:
        print("❌ Script de pruebas no encontrado")


def quick_test():
    """Ejecuta una prueba rápida."""
    print("\n⚡ Ejecutando Prueba Rápida...")
    
    tests_path = Path(__file__).parent / "tests"
    test_script = tests_path / "quick_test.py"
    
    if test_script.exists():
        subprocess.run([sys.executable, str(test_script)], cwd=tests_path)
    else:
        print("❌ Script de prueba rápida no encontrado")


def verify_models():
    """Verifica los modelos."""
    print("\n🔍 Verificando Modelos...")
    
    scripts_path = Path(__file__).parent / "scripts"
    verify_script = scripts_path / "verificar_modelos.py"
    
    if verify_script.exists():
        subprocess.run([sys.executable, str(verify_script)], cwd=scripts_path)
    else:
        print("❌ Script de verificación no encontrado")


def show_structure():
    """Muestra la estructura del proyecto."""
    print("\n📊 Estructura del Proyecto:")
    print("\n" + "="*60)
    
    structure = """
    Proyecto1IA-Jarvis/
    ├── backend/           # API REST con FastAPI
    ├── frontend/          # Frontend (vacío, para desarrollo)
    ├── config/            # Configuraciones y credenciales
    ├── docs/              # Documentación completa
    │   ├── guides/        # Guías y tutoriales
    │   └── reports/       # Reportes y resúmenes
    ├── tests/             # Scripts de testing
    ├── scripts/           # Scripts de utilidades
    ├── main.py            # Script original del proyecto
    └── run_jarvis.py      # Este script
    """
    
    print(structure)
    print("="*60)
    print("\n📁 Ver estructura completa: PROJECT_STRUCTURE.md")


def open_docs():
    """Abre la documentación."""
    print("\n📚 Documentación Disponible:\n")
    
    docs_path = Path(__file__).parent / "docs"
    
    docs = [
        ("QUICK_START.md", "Guía de inicio rápido"),
        ("reports/RESUMEN_ACTUALIZACION.md", "Resumen del proyecto"),
        ("reports/EJEMPLOS_COMPLETOS_PREDICCION.md", "Ejemplos de predicción"),
        ("guides/SWAGGER_TESTING_GUIDE.md", "Guía de testing con Swagger"),
    ]
    
    for i, (doc, desc) in enumerate(docs, 1):
        doc_path = docs_path / doc
        status = "✅" if doc_path.exists() else "❌"
        print(f"{i}. {status} {desc}")
        print(f"   📄 {doc}\n")
    
    print("\n💡 Abre los archivos .md con tu editor favorito")


def main():
    """Función principal."""
    while True:
        print_menu()
        
        try:
            choice = input("\n👉 Selecciona una opción (1-7): ").strip()
            
            if choice == "1":
                start_backend()
            elif choice == "2":
                run_tests()
            elif choice == "3":
                quick_test()
            elif choice == "4":
                verify_models()
            elif choice == "5":
                show_structure()
            elif choice == "6":
                open_docs()
            elif choice == "7":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("\n❌ Opción inválida. Elige entre 1 y 7.")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\n✅ Presiona Enter para continuar...")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 Bienvenido a Jarvis IA".center(60))
    print("Asistente Inteligente con Machine Learning".center(60))
    print("="*60)
    
    main()
