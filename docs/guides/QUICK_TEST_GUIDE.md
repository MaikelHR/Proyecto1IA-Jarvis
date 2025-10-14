# 🎯 Guía Visual: Cómo Probar el Backend en 5 Minutos

Esta guía te muestra **exactamente** qué hacer para verificar que todo funciona.

---

## 🚀 Paso 1: Prueba Automática (1 minuto)

```powershell
python quick_test.py
```

### ✅ Resultado Esperado:

```
============================================================
  🚀 PRUEBA RÁPIDA DEL BACKEND - JARVIS IA
============================================================

[1/6] Verificando imports...                    ✓
[2/6] Verificando modelos ML...                 ✓ 9 modelos
[3/6] Probando predicción...                    ✓
[4/6] Verificando Speech-to-Text...             ✓
[5/6] Verificando Face Recognition...           ⚠️ (opcional)
[6/6] Verificando API Server...                 ✓

RESULTADO: 5.5/6 (92%)
✅ Backend funcional - Listo para usar
```

**Si ves esto → ¡Perfecto! Continúa al Paso 2**

---

## 🌐 Paso 2: Iniciar la API (1 minuto)

### Opción A: Script de inicio
```powershell
python start_api.py
```

### Opción B: Directo con uvicorn
```powershell
uvicorn api.main:app --reload
```

### ✅ Resultado Esperado:

```
🚀 JARVIS IA - API REST
======================================
✓ Modelos cargados: 9/9
✓ Speech-to-Text: Configurado
⚠️ Face Recognition: No configurado (opcional)

======================================
📚 Documentación disponible:
   • Swagger UI: http://localhost:8000/docs
   • ReDoc: http://localhost:8000/redoc
   • Health: http://localhost:8000/health

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Si ves esto → ¡API corriendo! Continúa al Paso 3**

---

## 📚 Paso 3: Probar Swagger UI (2 minutos)

### 3.1 Abre tu navegador

```
http://localhost:8000/docs
```

### ✅ Deberías Ver:

```
╔═══════════════════════════════════════════════╗
║         Jarvis IA - API REST                  ║
║                                               ║
║  FastAPI - Automatic API Documentation        ║
╚═══════════════════════════════════════════════╝

▼ health - Health Check
   GET /health - Check API Health

▼ predictions - ML Predictions  
   POST /predictions/{dataset_key} - Make Prediction

▼ voice - Speech Commands
   GET  /voice/status - Check Voice Service
   POST /voice/command - Process Voice Command
   POST /voice/upload - Upload Audio File
   POST /voice/parse - Parse Text Command

▼ face - Face Recognition
   GET  /face/status - Check Face Service
   POST /face/emotion - Detect Emotions
   POST /face/analyze - Analyze Face
```

### 3.2 Probar Health Check

1. Click en `GET /health`
2. Click en **"Try it out"**
3. Click en **"Execute"**

### ✅ Respuesta Esperada:

```json
{
  "status": "healthy",
  "models_loaded": 9,
  "speech_service_available": true,
  "face_service_available": false,
  "available_models": [
    "bitcoin_price",
    "avocado_prices",
    "body_fat",
    "car_prices",
    "telco_churn",
    "wine_quality",
    "stroke_risk",
    "hepatitis_c",
    "cirrhosis_status"
  ]
}
```

**Status Code:** `200` ✅

---

## 🤖 Paso 4: Probar Predicción ML (2 minutos)

### 4.1 En Swagger UI

1. Expande `POST /predictions/{dataset_key}`
2. Click en **"Try it out"**
3. En `dataset_key`, escribe: `bitcoin_price`
4. En el Request body, pega:

```json
{
  "features": {
    "lag_1": 45000,
    "lag_7": 44000,
    "lag_30": 43000
  }
}
```

5. Click en **"Execute"**

### ✅ Respuesta Esperada:

```json
{
  "prediction": 45234.56,
  "confidence": null,
  "dataset": "bitcoin_price",
  "dataset_name": "Precio histórico de Bitcoin",
  "task": "regression",
  "message": "Predicción exitosa",
  "features_used": {
    "lag_1": 45000,
    "lag_7": 44000,
    "lag_30": 43000
  }
}
```

**Status Code:** `200` ✅

### 4.2 Probar Otro Modelo (Clasificación)

Prueba con `telco_churn`:

```json
{
  "features": {}
}
```

### ⚠️ Error Esperado (y eso está bien):

```json
{
  "detail": {
    "error": "PredictionError",
    "message": "columns are missing: {...}",
    "details": {...}
  }
}
```

**Status Code:** `400` ✅

**¿Por qué es bueno?** Porque demuestra que:
- ✅ El modelo existe
- ✅ La validación funciona
- ✅ Los errores se manejan correctamente

---

## 🎤 Paso 5: Probar Speech-to-Text (2 minutos)

### 5.1 Verificar Estado

En Swagger UI:
1. Expande `GET /voice/status`
2. Click "Try it out" → "Execute"

### ✅ Respuesta Esperada:

```json
{
  "available": true,
  "message": "Speech-to-Text service disponible",
  "models_available": 9
}
```

### 5.2 Probar Comando de Texto

1. Expande `POST /voice/parse`
2. Click "Try it out"
3. Request body:

```json
{
  "text": "predice el precio del bitcoin"
}
```

4. Click "Execute"

### ✅ Respuesta Esperada:

```json
{
  "text": "predice el precio del bitcoin",
  "command_recognized": true,
  "dataset_key": "bitcoin_price",
  "dataset_name": "Precio histórico de Bitcoin",
  "message": "Comando reconocido: Precio histórico de Bitcoin"
}
```

---

## 😊 Paso 6: Verificar Face Recognition (Opcional)

### 6.1 Verificar Estado

En Swagger UI:
1. Expande `GET /face/status`
2. Click "Try it out" → "Execute"

### ⚠️ Respuesta Esperada (sin configurar):

```json
{
  "available": false,
  "message": "Face Recognition service NO disponible. Configure AZURE_FACE_KEY y AZURE_FACE_ENDPOINT"
}
```

**Esto es NORMAL y está bien.** Face Recognition es opcional.

### Para configurarlo (si quieres):

```powershell
# 1. Obtén credenciales de Azure (Free tier)
# 2. Configura:
$env:AZURE_FACE_KEY="tu-key"
$env:AZURE_FACE_ENDPOINT="tu-endpoint"

# 3. Reinicia la API
python start_api.py

# 4. Prueba nuevamente
```

---

## 🧪 Paso 7: Pruebas con Scripts (Opcional)

### Test Speech-to-Text en vivo

```powershell
# Graba 3 segundos de audio y transcribe
python test_speech_to_text.py --duration 3
```

**Qué hacer:**
- Di claramente: "predice el precio del bitcoin"
- Espera el resultado

**Resultado esperado:**
```
📊 RESULTADOS
======================================
✓ Transcripción exitosa
   Texto: "predice el precio del bitcoin"
   Confianza: 98.02%

✓ Comando reconocido: bitcoin_price
```

### Test Face Recognition con cámara

```powershell
# Solo si configuraste Azure Face API
python test_face_recognition.py
```

---

## 📊 Checklist de Verificación

Marca lo que hayas probado:

### Básico (Obligatorio)
- [ ] `python quick_test.py` → 5.5/6 o mejor
- [ ] API inicia sin errores
- [ ] Swagger UI accesible
- [ ] Health check responde
- [ ] Al menos 1 predicción probada

### Intermedio (Recomendado)
- [ ] Todos los básicos ✓
- [ ] Voice status disponible
- [ ] Comando de texto reconocido
- [ ] Error handling funciona

### Avanzado (Opcional)
- [ ] Todos los intermedios ✓
- [ ] Speech-to-Text en vivo
- [ ] Face Recognition configurado
- [ ] Múltiples modelos probados

---

## 🎯 Interpretación de Resultados

### ✅ TODO OK si ves:

| Test | Resultado Esperado |
|------|-------------------|
| Quick test | 5.5/6 o 6/6 |
| API startup | Sin errores, puerto 8000 |
| Health check | Status: "healthy", 9 models |
| Predicción | 200 OK o 400 con mensaje claro |
| Voice status | available: true |
| Face status | available: false (OK si no configuraste) |

### ⚠️ Problemas Comunes

**Si quick_test da menos de 4/6:**
```powershell
# Reinstala dependencias
pip install -r requirements.txt

# Re-entrena modelos
python main.py
```

**Si API no inicia:**
```powershell
# Verifica errores
python -c "from api.main import app; print('OK')"
```

**Si Speech no funciona:**
```powershell
# Verifica credenciales
python setup_speech.py
```

---

## 🎉 Conclusión

### Si completaste Pasos 1-4:
**✅ Tu backend está 100% funcional para lo core**

Puedes:
- Proceder con el frontend
- Hacer demos
- Presentar el proyecto

### Si completaste Pasos 1-5:
**⭐ Excelente - Backend completo con Speech**

### Si completaste Pasos 1-6:
**🏆 Perfecto - Backend 100% completo**

---

## 📞 ¿Necesitas Ayuda?

### Documentación Completa
- `TESTING_GUIDE.md` - Guía exhaustiva
- `BACKEND_TEST_REPORT.md` - Reporte detallado
- `NEXT_STEPS.md` - Qué hacer después

### Scripts de Diagnóstico
```powershell
python test_complete_backend.py  # Diagnóstico completo
python setup_speech.py           # Verificar Speech
python setup_face_recognition.py # Verificar Face
```

### Swagger UI
```
http://localhost:8000/docs
```

---

**¡Listo! Tu backend está funcionando correctamente.** 🚀

**Siguiente paso:** Implementar el frontend (ver `NEXT_STEPS.md`)
