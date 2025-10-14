# 🔧 Scripts de Utilidades - Jarvis IA

## 📋 Scripts Disponibles

Esta carpeta contiene scripts de utilidades para configuración, verificación y generación de datos del proyecto.

---

## 🛠️ Scripts de Setup

### 1. Setup Face Recognition
**Archivo:** `setup_face_recognition.py`

Configura Azure Face API y registra usuarios.

```powershell
python setup_face_recognition.py
```

**Requiere:**
- Variables de entorno `AZURE_FACE_KEY` y `AZURE_FACE_ENDPOINT`
- Imágenes de usuarios para registro

---

### 2. Setup Speech-to-Text
**Archivo:** `setup_speech.py`

Configura Google Cloud Speech-to-Text API.

```powershell
python setup_speech.py
```

**Requiere:**
- Archivo `google-credentials.json` en `../config/credentials/`

---

## 🔍 Scripts de Verificación

### 1. Verificar Modelos
**Archivo:** `verificar_modelos.py`

Verifica que los 9 modelos estén entrenados y funcionando correctamente.

```powershell
python verificar_modelos.py
```

**Output:**
```
================================================================================
                          VERIFICACIÓN DE MODELOS
================================================================================

✅ Bitcoin Price - MAE: 404.33
✅ Body Fat - R²: 99.82%
✅ Telco Churn - Accuracy: 80.34%
...
```

---

### 2. Ver Columnas del Modelo
**Archivo:** `ver_columnas_modelo.py`

Muestra las columnas que espera un modelo específico.

```powershell
python ver_columnas_modelo.py
```

**Uso:**
```python
# En el script, modificar:
dataset_key = "wine_quality"  # Cambiar al modelo deseado
```

---

### 3. Obtener Todas las Columnas
**Archivo:** `obtener_todas_columnas.py`

Extrae las columnas de todos los 9 modelos y genera ejemplos.

```powershell
python obtener_todas_columnas.py
```

**Output:**
- Muestra columnas en terminal
- Genera `ejemplos_modelos_actualizados.json`

---

## 📊 Scripts de Generación

### 1. Generar Ejemplos Completos
**Archivo:** `generar_ejemplos_completos.py`

Genera ejemplos JSON completos para todos los modelos.

```powershell
python generar_ejemplos_completos.py
```

**Output:**
- Genera `ejemplos_prediccion_completos.json`
- Incluye descripción, endpoint y ejemplo para cada modelo

---

## 🐛 Scripts de Debug

### 1. Comparar Modelos
**Archivo:** `comparar_modelos.py`

Compara diferentes modelos y sus características.

```powershell
python comparar_modelos.py
```

**Uso:** Analiza diferencias entre modelos que funcionan y los que no.

---

### 2. Debug Model Pipeline
**Archivo:** `debug_model_pipeline.py`

Analiza la estructura interna de un pipeline de modelo.

```powershell
python debug_model_pipeline.py
```

**Uso:**
```python
# En el script, especificar el modelo:
model_path = "../backend/reports/winequality_model.pkl"
```

---

## 📝 Uso Común

### Workflow de Verificación

1. **Verificar modelos:**
   ```powershell
   python verificar_modelos.py
   ```

2. **Ver columnas específicas:**
   ```powershell
   python ver_columnas_modelo.py
   ```

3. **Generar ejemplos:**
   ```powershell
   python generar_ejemplos_completos.py
   ```

---

### Workflow de Setup

1. **Configurar Face Recognition:**
   ```powershell
   # Primero, set environment variables
   [System.Environment]::SetEnvironmentVariable('AZURE_FACE_KEY', 'your_key', 'User')
   [System.Environment]::SetEnvironmentVariable('AZURE_FACE_ENDPOINT', 'your_endpoint', 'User')
   
   # Luego ejecutar setup
   python setup_face_recognition.py
   ```

2. **Configurar Speech-to-Text:**
   ```powershell
   # Colocar google-credentials.json en config/credentials/
   python setup_speech.py
   ```

---

## 🔧 Modificar Scripts

### Template Básico para Nuevo Script

```python
"""
Script para [descripción].
"""
import sys
from pathlib import Path

# Agregar backend al path
project_root = Path(__file__).parent.parent
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

# Importar módulos del proyecto
from src.dataset_registry import get_dataset
from api.services.model_service import ModelService

def main():
    """Función principal."""
    print("=" * 80)
    print("NOMBRE DEL SCRIPT".center(80))
    print("=" * 80)
    
    # Tu código aquí
    pass

if __name__ == "__main__":
    main()
```

---

## 📊 Outputs Generados

### Archivos JSON

Los scripts generan archivos JSON que se guardan en `../docs/reports/`:

1. **ejemplos_modelos_actualizados.json**
   - Columnas de cada modelo
   - Ejemplos básicos extraídos de CSVs

2. **ejemplos_prediccion_completos.json**
   - Ejemplos completos y validados
   - Descripción de cada modelo
   - Expected outputs

---

## ⚠️ Consideraciones

### Paths Relativos

Los scripts asumen que se ejecutan desde `scripts/`:
```python
project_root = Path(__file__).parent.parent  # Proyecto1IA-Jarvis/
backend_path = project_root / "backend"
config_path = project_root / "config"
```

### Dependencias

Todos los scripts requieren:
- Backend instalado (`backend/requirements.txt`)
- Modelos entrenados en `backend/reports/`
- Datos en `backend/data/raw/`

---

## 🎯 Scripts por Categoría

### Configuración
- `setup_face_recognition.py` - Azure Face API
- `setup_speech.py` - Google Speech-to-Text

### Verificación
- `verificar_modelos.py` - Verificar 9 modelos
- `ver_columnas_modelo.py` - Ver columnas de 1 modelo
- `obtener_todas_columnas.py` - Ver columnas de todos

### Generación
- `generar_ejemplos_completos.py` - Generar ejemplos JSON

### Debugging
- `comparar_modelos.py` - Comparar modelos
- `debug_model_pipeline.py` - Analizar pipeline

---

## 📚 Documentación Relacionada

- **Guía de Setup:** `../docs/guides/*_SETUP.md`
- **Reportes:** `../docs/reports/`
- **Testing:** `../tests/README.md`

---

**Última actualización:** 13 de octubre de 2025  
**Scripts totales:** 8  
**Status:** ✅ Todos los scripts operativos
