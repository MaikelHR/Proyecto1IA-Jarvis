# ✅ Checklist de Pruebas del Backend

Usa este checklist para verificar que todo funciona antes de pasar al frontend.

## 🎯 Objetivo
Verificar que el backend está **100% funcional** y listo para integrarse con el frontend.

---

## 📦 Pre-requisitos

### Instalación
- [ ] Python 3.8+ instalado
- [ ] Git instalado
- [ ] Editor de código (VS Code recomendado)

### Dependencias
```powershell
pip install -r requirements.txt
```
- [ ] FastAPI instalado
- [ ] Uvicorn instalado
- [ ] Pandas, NumPy, Scikit-learn instalados
- [ ] PyAudio instalado
- [ ] Google Cloud Speech instalado
- [ ] Azure Face API instalado
- [ ] OpenCV instalado

---

## 🧪 Pruebas Básicas (OBLIGATORIO)

### 1. Estructura del Proyecto
```powershell
python test_complete_backend.py
```

Verifica que existan:
- [ ] `api/main.py`
- [ ] `api/routers/` (health, predictions, voice, face)
- [ ] `api/services/` (model, speech, face, voice, audio, video)
- [ ] `src/` (pipeline, modeling, data_loading)
- [ ] `data/raw/` (9 archivos CSV)
- [ ] `reports/` (modelos y métricas)

### 2. Modelos de Machine Learning
```powershell
# Si no existen, entrenar
python main.py
```

Verifica que existan 9 modelos:
- [ ] `bitcoin_price_*.pkl`
- [ ] `avocado_prices_*.pkl`
- [ ] `body_fat_*.pkl`
- [ ] `car_prices_*.pkl`
- [ ] `telco_churn_*.pkl`
- [ ] `wine_quality_*.pkl`
- [ ] `stroke_risk_*.pkl`
- [ ] `hepatitis_c_*.pkl`
- [ ] `cirrhosis_status_*.pkl`

### 3. Servidor API
```powershell
python start_api.py
```

Verifica:
- [ ] API inicia sin errores
- [ ] Puerto 8000 abierto
- [ ] Mensaje de éxito visible
- [ ] No hay errores de import

### 4. Documentación API
Abre en el navegador:
- [ ] http://localhost:8000/docs (Swagger UI)
- [ ] http://localhost:8000/redoc (ReDoc)
- [ ] http://localhost:8000/health (Health check)

### 5. Endpoints Básicos

#### Health Check
```powershell
curl http://localhost:8000/health
```
- [ ] Status: "healthy"
- [ ] Models loaded: 9
- [ ] Speech service: mostrado

#### Predicción ML
En Swagger UI (http://localhost:8000/docs):
1. Expande `POST /predictions/{dataset_key}`
2. Click "Try it out"
3. Dataset: `telco_churn`
4. Body: `{"features": {}}`
5. Click "Execute"

- [ ] Response 200
- [ ] Contiene "prediction"
- [ ] Contiene "confidence"

---

## 🎤 Pruebas de Speech-to-Text (RECOMENDADO)

### 1. Verificar Configuración
```powershell
python setup_speech.py
```

- [ ] Variable `GOOGLE_APPLICATION_CREDENTIALS` configurada
- [ ] Archivo de credenciales existe
- [ ] Service disponible

### 2. Configurar Credenciales (si falta)
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="credentials\google-credentials.json"
```

- [ ] Variable configurada en sesión actual
- [ ] Archivo JSON válido
- [ ] Sin errores al verificar

### 3. Probar Grabación y Transcripción
```powershell
python test_speech_to_text.py --duration 3
```

Al ejecutar:
- [ ] Micrófono detectado
- [ ] Grabación inicia
- [ ] Audio capturado (3 segundos)
- [ ] Transcripción exitosa
- [ ] Texto mostrado correctamente

### 4. Probar Comandos de Voz
```powershell
python test_voice_api.py
```

- [ ] Endpoint `/voice/command` responde
- [ ] Audio se transcribe
- [ ] Comandos se reconocen
- [ ] Mapeo a datasets funciona

### 5. Verificar Endpoints de Voice

En Swagger UI:
- [ ] `GET /voice/status` → available: true
- [ ] `POST /voice/command` → acepta base64
- [ ] `POST /voice/upload` → acepta archivo
- [ ] `POST /voice/parse` → reconoce comando

---

## 😊 Pruebas de Face Recognition (OPCIONAL)

### 1. Verificar Configuración
```powershell
python setup_face_recognition.py
```

- [ ] Variables `AZURE_FACE_KEY` y `AZURE_FACE_ENDPOINT` configuradas
- [ ] Service disponible
- [ ] Conexión con Azure exitosa

### 2. Configurar Credenciales (si falta)
```powershell
$env:AZURE_FACE_KEY="tu-key"
$env:AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"
```

- [ ] Variables configuradas
- [ ] Key válida
- [ ] Endpoint accesible

### 3. Probar Cámara
```powershell
python test_face_recognition.py
```

Al ejecutar:
- [ ] Cámara detectada
- [ ] Foto capturada automáticamente
- [ ] Rostro detectado
- [ ] Emociones analizadas
- [ ] Atributos mostrados (edad, género)

### 4. Probar API de Face
```powershell
python test_face_api.py
```

- [ ] Todos los endpoints responden
- [ ] Emociones detectadas correctamente
- [ ] Análisis completo funciona
- [ ] Múltiples rostros detectables

### 5. Verificar Endpoints de Face

En Swagger UI:
- [ ] `GET /face/status` → available: true
- [ ] `POST /face/emotion` → acepta base64
- [ ] `POST /face/emotion/upload` → acepta archivo
- [ ] `POST /face/analyze` → análisis completo
- [ ] `POST /face/detect/multiple` → múltiples rostros

---

## 🔧 Pruebas de Integración

### 1. Prueba Rápida (5 min)
```powershell
python quick_test.py
```

Resultado esperado:
- [ ] 6/6 tests pasados
- [ ] Backend funcional
- [ ] Listo para usar

### 2. Prueba Completa (15 min)
```powershell
python test_complete_backend.py
```

Resultado esperado:
- [ ] File Structure ✓
- [ ] ML Models ✓
- [ ] Dependencies ✓
- [ ] Services ✓
- [ ] API Server ✓

### 3. Prueba Manual de Todos los Endpoints

#### ML Predictions (9 modelos)
- [ ] bitcoin_price
- [ ] avocado_prices
- [ ] body_fat
- [ ] car_prices
- [ ] telco_churn
- [ ] wine_quality
- [ ] stroke_risk
- [ ] hepatitis_c
- [ ] cirrhosis_status

#### Voice Endpoints (4)
- [ ] GET /voice/status
- [ ] POST /voice/command
- [ ] POST /voice/upload
- [ ] POST /voice/parse

#### Face Endpoints (5)
- [ ] GET /face/status
- [ ] POST /face/emotion
- [ ] POST /face/emotion/upload
- [ ] POST /face/analyze
- [ ] POST /face/detect/multiple

---

## 📊 Prueba de Carga (OPCIONAL)

```powershell
# Instalar herramienta de carga
pip install locust

# Crear locustfile.py (si no existe)
# Ejecutar prueba de carga
locust -f locustfile.py --host=http://localhost:8000
```

- [ ] API soporta 10 usuarios concurrentes
- [ ] Tiempo de respuesta < 1 segundo
- [ ] Sin errores bajo carga

---

## 🐛 Manejo de Errores

### Prueba de Errores Controlados

#### Predicción con datos inválidos
```powershell
curl -X POST "http://localhost:8000/predictions/telco_churn" \
  -H "Content-Type: application/json" \
  -d '{"features": "invalid"}'
```
- [ ] Response 422 (Validation Error)
- [ ] Mensaje de error claro

#### Dataset inexistente
```powershell
curl http://localhost:8000/predictions/invalid_dataset
```
- [ ] Response 404
- [ ] Mensaje descriptivo

#### Audio sin credenciales
- [ ] Response 503
- [ ] Mensaje indica falta de configuración

---

## 📝 Documentación

### Verificar que existan:
- [ ] `README.md` - Documentación general
- [ ] `SPEECH_TO_TEXT_SETUP.md` - Guía Speech
- [ ] `FACE_RECOGNITION_SETUP.md` - Guía Face
- [ ] `TESTING_GUIDE.md` - Esta guía de pruebas
- [ ] `NEXT_STEPS.md` - Próximos pasos

### Contenido de la documentación:
- [ ] Instrucciones claras de instalación
- [ ] Ejemplos de uso
- [ ] Solución de problemas
- [ ] Screenshots (si aplica)

---

## 🎬 Demo Script

Prepara una demostración:

### 1. Inicio
```powershell
python start_api.py
```
- [ ] API inicia limpiamente
- [ ] Mensaje de bienvenida claro

### 2. Swagger UI
http://localhost:8000/docs
- [ ] Interfaz carga correctamente
- [ ] Todos los endpoints visibles
- [ ] Documentación clara

### 3. Predicción ML
- [ ] Seleccionar modelo
- [ ] Ingresar datos
- [ ] Obtener predicción
- [ ] Mostrar confianza

### 4. Speech-to-Text (si configurado)
```powershell
python test_speech_to_text.py --duration 3
```
- [ ] Grabar comando
- [ ] Mostrar transcripción
- [ ] Reconocer comando
- [ ] Ejecutar predicción

### 5. Face Recognition (si configurado)
```powershell
python test_face_recognition.py
```
- [ ] Capturar rostro
- [ ] Detectar emociones
- [ ] Mostrar resultados
- [ ] Análisis completo

---

## 🎯 Criterios de Aprobación

### ⭐ Nivel Básico (MÍNIMO REQUERIDO)
- ✅ API REST funcional
- ✅ 9 modelos ML prediciendo
- ✅ Documentación Swagger
- ✅ Health check operativo
- ✅ Sin errores críticos

**Puntuación: 35/60 puntos**

### ⭐⭐ Nivel Intermedio (RECOMENDADO)
- ✅ Todo del nivel básico
- ✅ Speech-to-Text configurado
- ✅ Comandos de voz funcionando
- ✅ Transcripción exitosa
- ✅ Documentación completa

**Puntuación: 47/60 puntos**

### ⭐⭐⭐ Nivel Avanzado (IDEAL)
- ✅ Todo del nivel intermedio
- ✅ Face Recognition configurado
- ✅ Detección de emociones
- ✅ Análisis facial completo
- ✅ Captura desde cámara
- ✅ Todos los tests pasando

**Puntuación: 58/60 puntos**

---

## 📋 Reporte Final

Completa este resumen:

```
REPORTE DE PRUEBAS DEL BACKEND
================================

Fecha: _____________
Probado por: _____________

RESULTADOS:

[  ] Estructura de archivos: OK / FALLA
[  ] Modelos ML: ___/9 funcionando
[  ] API REST: OK / FALLA
[  ] Documentación: OK / FALLA
[  ] Speech-to-Text: OK / NO CONFIGURADO / FALLA
[  ] Face Recognition: OK / NO CONFIGURADO / FALLA

PUNTUACIÓN TOTAL: ___/60 puntos

NIVEL ALCANZADO:
[  ] Básico (35-46 pts)
[  ] Intermedio (47-54 pts)
[  ] Avanzado (55-60 pts)

OBSERVACIONES:
_________________________________________________
_________________________________________________
_________________________________________________

PRÓXIMOS PASOS:
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## ✅ Firma de Aprobación

Una vez completado este checklist:

- [ ] Todos los tests críticos pasaron
- [ ] Documentación actualizada
- [ ] Screenshots capturados
- [ ] Video demo grabado (opcional)
- [ ] Código commiteado a Git

**Backend aprobado para integración con Frontend** ✓

---

## 🚀 ¿Todo Listo?

Si completaste este checklist exitosamente:

### Siguiente paso:
```powershell
# Lee la guía de próximos pasos
code NEXT_STEPS.md

# O empieza el frontend directamente
npm create vite@latest frontend -- --template react
```

**¡Excelente trabajo! El backend está listo.** 🎉
