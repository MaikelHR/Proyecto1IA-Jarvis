# 🔬 Tests - Jarvis IA

## 📋 Suite de Pruebas

Esta carpeta contiene todos los scripts de testing y validación del proyecto Jarvis IA.

---

## 🧪 Scripts de Testing Disponibles

### 1. Prueba Completa de 9 Modelos ⭐
**Archivo:** `test_completo_9_modelos.py`

Prueba automática de todos los modelos ML con generación de reporte.

```powershell
python test_completo_9_modelos.py
```

**Resultado:** Genera `test_report_9_modelos.json`

---

### 2. Prueba Rápida
**Archivo:** `quick_test.py`

Verificación rápida del estado del backend.

```powershell
python quick_test.py
```

---

### 3. Testing de API

#### Test API General
**Archivo:** `test_api.py`
```powershell
python test_api.py
```

#### Test API Request
**Archivo:** `test_api_request.py`
```powershell
python test_api_request.py
```

#### Test Completo Backend
**Archivo:** `test_complete_backend.py`
```powershell
python test_complete_backend.py
```

---

### 4. Testing de Modelos Específicos

#### Test Wine Quality
**Archivo:** `test_wine_model.py`
```powershell
python test_wine_model.py
```

#### Test Predicción Directa
**Archivo:** `test_prediccion_directa.py`
```powershell
python test_prediccion_directa.py
```

---

### 5. Testing de Servicios

#### Test Face Recognition
**Archivo:** `test_face_recognition.py`
```powershell
python test_face_recognition.py
```

**Archivo:** `test_face_api.py`
```powershell
python test_face_api.py
```

#### Test Speech-to-Text
**Archivo:** `test_speech_to_text.py`
```powershell
python test_speech_to_text.py --duration 3
```

#### Test Voice API
**Archivo:** `test_voice_api.py`
```powershell
python test_voice_api.py
```

---

### 6. Testing HTML
**Archivo:** `test_api.html`

Interfaz HTML para probar la API desde el navegador.

**Uso:** Abre el archivo en tu navegador mientras la API está corriendo.

---

## 📊 Reportes Generados

### test_report_9_modelos.json
Reporte completo de la última ejecución de pruebas:

```json
{
  "timestamp": "2025-10-13T15:59:49.834625",
  "total_tests": 9,
  "successful": 9,
  "failed": 0,
  "success_rate": 100.0,
  "results": [...]
}
```

---

## 🚀 Ejecución de Pruebas

### Prerrequisitos

1. **Backend corriendo:**
   ```powershell
   cd ../backend
   .\start_api_with_env.ps1
   ```

2. **Verificar API:**
   ```powershell
   curl http://localhost:8000/health
   ```

### Ejecutar Suite Completa

```powershell
# Prueba completa de 9 modelos
python test_completo_9_modelos.py

# Prueba rápida
python quick_test.py

# Testing de backend completo
python test_complete_backend.py
```

---

## 📈 Interpretación de Resultados

### Estados Posibles

#### ✅ Success (200)
```
✅ ÉXITO
   Predicción: 5
   Confianza: 47.66%
   Tipo: classification
```

#### ❌ Error (4xx/5xx)
```
❌ ERROR 422
   {"detail": "Invalid input features"}
```

### Códigos de Estado HTTP

- **200 OK:** Predicción exitosa
- **400 Bad Request:** Datos inválidos
- **422 Unprocessable Entity:** Columnas faltantes o incorrectas
- **500 Internal Server Error:** Error en el servidor

---

## 🔍 Debugging

### Ver Logs Detallados

Los logs de la API muestran:
```
🔍 Predicción para: wine_quality
📥 Features recibidas: {...}
📊 Tipo de features: <class 'dict'>
📊 Keys: [...]
✅ Predicción exitosa: 5 (confianza: 0.47661808811197665)
```

### Problemas Comunes

#### 1. API no disponible
```
❌ No se puede conectar a la API
```
**Solución:** Inicia el backend primero

#### 2. Columnas incorrectas
```
❌ ERROR 422: Invalid input features
```
**Solución:** Verifica que uses formato `snake_case`

#### 3. Azure/Google no configurado
```
⚠️ Azure Face API no configurada
⚠️ Google Cloud credentials no encontradas
```
**Solución:** Opcional, solo afecta servicios específicos

---

## 📝 Crear Nuevos Tests

### Template Básico

```python
"""
Test para [nombre del componente].
"""
import requests

API_URL = "http://localhost:8000"

def test_endpoint():
    """Prueba un endpoint específico."""
    url = f"{API_URL}/endpoint"
    data = {"key": "value"}
    
    response = requests.post(url, json=data)
    
    assert response.status_code == 200
    result = response.json()
    print(f"✅ Resultado: {result}")

if __name__ == "__main__":
    test_endpoint()
```

---

## 🎯 Coverage

### Cobertura Actual

| Componente | Coverage | Tests |
|------------|----------|-------|
| Modelos ML | 100% | test_completo_9_modelos.py |
| API Health | 100% | quick_test.py |
| Predicciones | 100% | test_complete_backend.py |
| Face API | Partial | test_face_api.py |
| Voice API | Partial | test_voice_api.py |

---

## 📚 Documentación Relacionada

- **Guía de Testing:** `../docs/guides/TESTING_GUIDE.md`
- **Swagger Testing:** `../docs/guides/SWAGGER_TESTING_GUIDE.md`
- **Ejemplos Completos:** `../docs/reports/EJEMPLOS_COMPLETOS_PREDICCION.md`

---

## ✅ Checklist de Testing

Antes de un deployment o release:

- [ ] Ejecutar `test_completo_9_modelos.py` (debe ser 100%)
- [ ] Ejecutar `quick_test.py` (debe pasar)
- [ ] Probar endpoints manualmente en Swagger
- [ ] Verificar health check
- [ ] Probar test_api.html en navegador
- [ ] Revisar logs de la API
- [ ] Validar ejemplos en documentación

---

**Última actualización:** 13 de octubre de 2025  
**Status:** ✅ Suite de pruebas completa y funcional
