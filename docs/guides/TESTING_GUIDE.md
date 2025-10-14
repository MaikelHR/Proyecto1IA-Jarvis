# 🧪 Guía de Pruebas del Backend - Jarvis IA

Esta guía te ayudará a verificar que TODAS las funcionalidades del backend estén funcionando correctamente antes de pasar al frontend.

## 📋 Índice

1. [Prueba Rápida (5 minutos)](#prueba-rápida)
2. [Prueba Completa (15 minutos)](#prueba-completa)
3. [Pruebas por Módulo](#pruebas-por-módulo)
4. [Solución de Problemas](#solución-de-problemas)

---

## ⚡ Prueba Rápida (5 minutos)

### Paso 1: Verificación Automática

```powershell
# Ejecuta el script de prueba completa
python test_complete_backend.py
```

Este script verifica:
- ✅ Estructura de archivos
- ✅ Modelos ML entrenados
- ✅ Dependencias instaladas
- ✅ Credenciales configuradas
- ✅ Servicios funcionales
- ✅ API importable

**Resultado esperado:**
```
📊 REPORTE FINAL
================================================
Test                                     Resultado
-------------------------------------------------------
File Structure                           ✓ PASÓ
ML Models                               ✓ PASÓ
Dependencies                            ✓ PASÓ
Credentials                             ⚠️  OPCIONAL
Services                                ✓ PASÓ
API Server                              ✓ PASÓ

🎉 ¡PERFECTO! TODO FUNCIONA CORRECTAMENTE
```

### Paso 2: Iniciar la API

```powershell
# Terminal 1: Inicia el servidor
python start_api.py
```

**Salida esperada:**
```
🚀 JARVIS IA - API REST
======================================================================
✓ Modelos cargados: 9/9
✓ Speech-to-Text: Configurado
⚠️  Face Recognition: No configurado (opcional)

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Paso 3: Verificar Documentación

Abre tu navegador:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

✅ **Si ves la documentación interactiva → Backend funcionando correctamente**

---

## 🔬 Prueba Completa (15 minutos)

### Test 1: Estructura y Modelos ML

```powershell
# Verifica que los 9 modelos estén entrenados
python test_complete_backend.py
```

**Checklist:**
- [ ] 9 archivos `.pkl` en carpeta `reports/`
- [ ] Todos los servicios se importan sin errores
- [ ] No hay errores de módulos faltantes

**Si faltan modelos:**
```powershell
# Entrenar todos los modelos (toma ~5 minutos)
python main.py
```

---

### Test 2: API REST y Predicciones ML

```powershell
# Terminal 1: Inicia API (si no está corriendo)
python start_api.py

# Terminal 2: Prueba los endpoints
python -c "
import requests

# Health check
r = requests.get('http://localhost:8000/health')
print('Health:', r.json())

# Predicción de ejemplo (Telco Churn)
r = requests.post(
    'http://localhost:8000/predictions/telco_churn',
    json={
        'features': {
            'tenure': 12,
            'MonthlyCharges': 70.5,
            'TotalCharges': 846.0,
            'Contract': 'Month-to-month',
            'InternetService': 'Fiber optic'
        }
    }
)
print('Predicción:', r.json())
"
```

**Resultado esperado:**
```json
{
  "prediction": 1,
  "prediction_label": "Churn",
  "confidence": 0.85,
  "dataset": "telco_churn"
}
```

**Prueba manual en Swagger:**
1. Ve a http://localhost:8000/docs
2. Expande `POST /predictions/{dataset_key}`
3. Click en "Try it out"
4. Dataset: `telco_churn`
5. Request body:
```json
{
  "features": {
    "tenure": 12,
    "MonthlyCharges": 70.5
  }
}
```
6. Click "Execute"
7. ✅ Debes ver una respuesta con predicción

---

### Test 3: Speech-to-Text

#### 3.1 Verificar Configuración

```powershell
python setup_speech.py
```

**Salida esperada:**
```
✓ GOOGLE_APPLICATION_CREDENTIALS: credentials\google-credentials.json
✓ Archivo existe
✓ Speech-to-Text Service: DISPONIBLE
✅ TODO CONFIGURADO CORRECTAMENTE
```

**Si no está configurado:**
```powershell
# Configura la ruta a tus credenciales
$env:GOOGLE_APPLICATION_CREDENTIALS="credentials\google-credentials.json"

# Verifica nuevamente
python setup_speech.py
```

#### 3.2 Prueba con Audio

```powershell
# Prueba grabando 3 segundos de audio
python test_speech_to_text.py --duration 3
```

**Qué hacer:**
1. El script inicia grabación
2. Habla claramente: "predice el precio del bitcoin"
3. Espera el resultado

**Resultado esperado:**
```
📊 RESULTADOS
==================================================
✓ Transcripción exitosa
   Texto: "predice el precio del bitcoin"
   Confianza: 98.02%

✓ Comando reconocido: bitcoin_price
```

#### 3.3 Prueba API de Voz

```powershell
# API debe estar corriendo
python test_voice_api.py
```

Prueba:
- Upload de audio
- Transcripción
- Reconocimiento de comandos

---

### Test 4: Face Recognition

#### 4.1 Verificar Configuración

```powershell
python setup_face_recognition.py
```

**Si no está configurado (OPCIONAL):**
```powershell
# Configura credenciales de Azure
$env:AZURE_FACE_KEY="tu-key-aquí"
$env:AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"

# Verifica
python setup_face_recognition.py
```

#### 4.2 Prueba con Cámara

```powershell
# Requiere cámara disponible
python test_face_recognition.py
```

**Qué hace:**
1. Detecta tu cámara
2. Captura tu foto automáticamente
3. Detecta tu rostro
4. Analiza tus emociones
5. Muestra resultados

**Resultado esperado:**
```
📊 RESULTADOS
==================================================
✓ Emoción detectada: felicidad (87.5%)

😊 Emociones detectadas:
   felicidad       ████████████████████████████ 87.5%
   neutral         ██████░░░░░░░░░░░░░░░░░░░░░░ 10.2%
   sorpresa        ██░░░░░░░░░░░░░░░░░░░░░░░░░░  2.3%

🎯 Emoción dominante: felicidad
   Confianza: 87.5%

👤 Edad estimada: 25 años
👤 Género: Masculino
```

#### 4.3 Prueba API de Face

```powershell
# API debe estar corriendo
python test_face_api.py
```

---

### Test 5: Prueba de Integración Completa

```powershell
# Prueba todos los endpoints de la API
python -c "
import requests

api = 'http://localhost:8000'

# 1. Health
print('1. Health Check...')
r = requests.get(f'{api}/health')
print(f'   Status: {r.status_code} - {r.json()[\"status\"]}\n')

# 2. Predicción ML
print('2. ML Prediction...')
r = requests.post(
    f'{api}/predictions/bitcoin_price',
    json={'features': {'lag_1': 45000, 'lag_7': 44000}}
)
print(f'   Prediction: {r.json().get(\"prediction\")}\n')

# 3. Speech Status
print('3. Speech Service...')
r = requests.get(f'{api}/voice/status')
print(f'   Available: {r.json().get(\"available\")}\n')

# 4. Face Status
print('4. Face Service...')
r = requests.get(f'{api}/face/status')
print(f'   Available: {r.json().get(\"available\")}\n')

print('✅ Todos los servicios respondieron correctamente')
"
```

---

## 📦 Pruebas por Módulo

### Módulo 1: Machine Learning

**Datasets disponibles:**
```python
datasets = [
    "bitcoin_price",          # Regresión - Precio de Bitcoin
    "avocado_prices",         # Regresión - Precio de aguacates
    "body_fat",               # Regresión - Grasa corporal
    "car_prices",             # Regresión - Valor de autos
    "telco_churn",            # Clasificación - Churn de clientes
    "wine_quality",           # Clasificación - Calidad de vinos
    "stroke_risk",            # Clasificación - Riesgo de derrame
    "hepatitis_c",            # Clasificación - Hepatitis C
    "cirrhosis_status",       # Clasificación - Cirrosis
]
```

**Prueba cada modelo:**
```powershell
# En PowerShell
$datasets = @(
    "bitcoin_price",
    "avocado_prices",
    "body_fat",
    "car_prices",
    "telco_churn",
    "wine_quality",
    "stroke_risk",
    "hepatitis_c",
    "cirrhosis_status"
)

foreach ($dataset in $datasets) {
    Write-Host "`nProbando $dataset..." -ForegroundColor Cyan
    
    $response = Invoke-RestMethod `
        -Uri "http://localhost:8000/predictions/$dataset" `
        -Method Post `
        -ContentType "application/json" `
        -Body '{"features": {}}'
    
    Write-Host "  ✓ Predicción: $($response.prediction)" -ForegroundColor Green
}
```

---

### Módulo 2: Speech-to-Text

**Test de audio pregrabado:**

```python
# test_speech_custom.py
import requests
import base64

# Lee un archivo de audio
with open("test_audio.wav", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

# Envía a la API
response = requests.post(
    "http://localhost:8000/voice/command",
    json={"audio": audio_b64}
)

print(response.json())
```

---

### Módulo 3: Face Recognition

**Test con imagen:**

```python
# test_face_custom.py
import requests

# Sube una imagen
with open("test_face.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/face/emotion/upload",
        files={"file": f}
    )

print(response.json())
```

---

## 🔧 Solución de Problemas

### Problema 1: "Module not found"

```powershell
# Reinstala dependencias
pip install -r requirements.txt
```

### Problema 2: "No module named 'api'"

```powershell
# Asegúrate de estar en la carpeta del proyecto
cd D:\TEC\IA\Proyecto1IA-Jarvis

# Ejecuta desde ahí
python test_complete_backend.py
```

### Problema 3: "Connection refused" en API

```powershell
# Verifica que la API esté corriendo
python start_api.py

# En otra terminal, prueba
curl http://localhost:8000/health
```

### Problema 4: Modelos no encontrados

```powershell
# Entrena todos los modelos
python main.py

# O uno específico
python main.py --dataset telco_churn
```

### Problema 5: Speech-to-Text no funciona

```powershell
# Verifica credenciales
python setup_speech.py

# Prueba la conexión
python test_speech_to_text.py --duration 2
```

### Problema 6: Face Recognition no disponible

**Es OPCIONAL - puedes continuar sin Azure:**

```powershell
# Si quieres configurarlo:
$env:AZURE_FACE_KEY="tu-key"
$env:AZURE_FACE_ENDPOINT="tu-endpoint"

python setup_face_recognition.py
```

---

## ✅ Checklist de Pruebas Completas

### Pre-requisitos
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Modelos ML entrenados (9 archivos .pkl)

### Funcionalidades Core
- [ ] API inicia sin errores
- [ ] Health endpoint responde
- [ ] Documentación Swagger accesible
- [ ] 9 modelos ML hacen predicciones

### Funcionalidades Opcionales
- [ ] Speech-to-Text configurado y funcional
- [ ] Comandos de voz reconocidos
- [ ] Face Recognition configurado (opcional)
- [ ] Detección de emociones funcional (opcional)

### Pruebas de Integración
- [ ] Todos los endpoints responden correctamente
- [ ] Errores manejados apropiadamente
- [ ] CORS configurado
- [ ] Logs sin errores críticos

---

## 🎯 Criterios de Éxito

### ✅ Mínimo Aceptable (Core)
- API REST funcional
- 9 modelos ML respondiendo
- Documentación accesible
- Health check operativo

### ⭐ Recomendado
- Core + Speech-to-Text funcional
- Comandos de voz reconocidos
- Audio grabable y transcribible

### 🏆 Completo
- Recomendado + Face Recognition
- Detección de emociones
- Análisis facial completo
- Captura desde cámara

---

## 📊 Matriz de Pruebas

| Componente | Comando | Tiempo | Resultado Esperado |
|------------|---------|--------|-------------------|
| Estructura | `python test_complete_backend.py` | 1 min | ✓ Todos los archivos |
| Modelos ML | `python main.py` | 5 min | 9 modelos .pkl |
| API REST | `python start_api.py` | - | Server en :8000 |
| Swagger | Abrir browser | - | UI interactiva |
| Predicciones | Swagger → Try it out | 1 min | JSON con predicción |
| Speech Setup | `python setup_speech.py` | 1 min | ✓ Configurado |
| Speech Test | `python test_speech_to_text.py` | 30 seg | Transcripción exitosa |
| Voice API | `python test_voice_api.py` | 1 min | Comandos reconocidos |
| Face Setup | `python setup_face_recognition.py` | 1 min | ✓ Configurado (opcional) |
| Face Test | `python test_face_recognition.py` | 30 seg | Emociones detectadas |
| Face API | `python test_face_api.py` | 1 min | Análisis exitoso |

---

## 🚀 Después de las Pruebas

### Si todo funciona ✅

**¡Excelente! Tu backend está listo.**

Próximos pasos:
1. **Documenta** lo que funciona
2. **Captura screenshots** de Swagger UI
3. **Graba un video** demostrando las funcionalidades
4. **Implementa el frontend** (ver NEXT_STEPS.md)

### Si hay problemas ⚠️

1. **Revisa los logs** de errores
2. **Consulta** esta guía de solución de problemas
3. **Verifica** dependencias y credenciales
4. **Ejecuta** `python test_complete_backend.py` para diagnóstico

---

## 📝 Generar Reporte de Pruebas

```powershell
# Ejecuta todas las pruebas y guarda el output
python test_complete_backend.py > test_report.txt 2>&1

# Revisa el reporte
cat test_report.txt
```

---

## 📞 Recursos Adicionales

- **Documentación de la API**: http://localhost:8000/docs
- **Guía Speech-to-Text**: [SPEECH_TO_TEXT_SETUP.md](SPEECH_TO_TEXT_SETUP.md)
- **Guía Face Recognition**: [FACE_RECOGNITION_SETUP.md](FACE_RECOGNITION_SETUP.md)
- **Próximos pasos**: [NEXT_STEPS.md](NEXT_STEPS.md)

---

**¡Listo para probar! 🧪**

Empieza con:
```powershell
python test_complete_backend.py
```
