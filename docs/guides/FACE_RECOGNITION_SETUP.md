# Configuración de Face Recognition con Azure Face API

Este documento explica cómo configurar el servicio de reconocimiento facial usando Azure Cognitive Services Face API.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Crear Recurso en Azure](#crear-recurso-en-azure)
- [Configurar Credenciales](#configurar-credenciales)
- [Verificar Configuración](#verificar-configuración)
- [Usar el Servicio](#usar-el-servicio)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Solución de Problemas](#solución-de-problemas)

## Requisitos

### Paquetes Python

```bash
pip install azure-cognitiveservices-vision-face
pip install opencv-python
pip install pillow
pip install msrest
```

Estos paquetes ya están incluidos en `requirements.txt`.

### Cuenta de Azure

- Suscripción activa de Azure
- Acceso al Azure Portal (https://portal.azure.com)

## Crear Recurso en Azure

### Paso 1: Acceder al Portal

1. Ve a [Azure Portal](https://portal.azure.com)
2. Inicia sesión con tu cuenta

### Paso 2: Crear Recurso Face

1. Haz clic en **"Crear un recurso"**
2. Busca **"Face"** en el buscador
3. Selecciona **"Face"** de Microsoft
4. Haz clic en **"Crear"**

### Paso 3: Configurar el Recurso

Completa el formulario:

- **Suscripción**: Selecciona tu suscripción
- **Grupo de recursos**: Crea uno nuevo o usa existente
- **Región**: Selecciona la más cercana (ej: East US, West Europe)
- **Nombre**: Nombre único para tu recurso (ej: `jarvis-face-api`)
- **Plan de tarifa**: 
  - **F0 (Free)**: 20 llamadas/min, 30,000 llamadas/mes - **RECOMENDADO PARA PRUEBAS**
  - **S0 (Standard)**: 10 llamadas/segundo - Para producción

### Paso 4: Obtener Credenciales

Una vez creado el recurso:

1. Ve al recurso creado
2. En el menú lateral, selecciona **"Keys and Endpoint"**
3. Copia:
   - **KEY 1** o **KEY 2** (cualquiera funciona)
   - **ENDPOINT** (URL completa)

Ejemplo de endpoint:
```
https://eastus.api.cognitive.microsoft.com/
```

## Configurar Credenciales

### Windows (PowerShell)

#### Configuración Temporal (Solo para la sesión actual)

```powershell
$env:AZURE_FACE_KEY="tu-key-aquí"
$env:AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"
```

#### Configuración Permanente (Sistema)

```powershell
# Configurar para el usuario actual
[System.Environment]::SetEnvironmentVariable('AZURE_FACE_KEY', 'tu-key-aquí', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_FACE_ENDPOINT', 'https://tu-endpoint.cognitiveservices.azure.com/', 'User')

# Luego REINICIA la terminal para que tome efecto
```

### Linux/Mac (Bash)

```bash
# Temporal
export AZURE_FACE_KEY="tu-key-aquí"
export AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"

# Permanente - Agregar a ~/.bashrc o ~/.zshrc
echo 'export AZURE_FACE_KEY="tu-key-aquí"' >> ~/.bashrc
echo 'export AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"' >> ~/.bashrc
source ~/.bashrc
```

## Verificar Configuración

### Script de Verificación

```bash
python setup_face_recognition.py
```

Este script verificará:
- ✓ Variables de entorno configuradas
- ✓ Servicio de Face Recognition disponible
- ✓ Conexión con Azure Face API

### Salida Esperada

```
======================================================================
 CONFIGURACIÓN DE AZURE FACE API
======================================================================

======================================================================
 VERIFICACIÓN DE VARIABLES DE ENTORNO
======================================================================

1. AZURE_FACE_KEY
   ✓ Configurada: ********************abc1

2. AZURE_FACE_ENDPOINT
   ✓ Configurada: https://eastus.api.cognitive.microsoft.com/

======================================================================
 VERIFICACIÓN DE SERVICIOS
======================================================================

✓ Face Recognition Service importado correctamente
✓ Service disponible y configurado

======================================================================
 PRUEBA DE CONEXIÓN CON AZURE
======================================================================

🔄 Intentando conectar con Azure Face API...
✓ Cliente creado correctamente
✓ Endpoint: https://eastus.api.cognitive.microsoft.com/

✓ Conexión establecida correctamente

======================================================================
 ESTADO DE CONFIGURACIÓN
======================================================================

✅ TODO CONFIGURADO CORRECTAMENTE
```

## Usar el Servicio

### Prueba con Cámara

```bash
python test_face_recognition.py
```

Este script:
1. Verifica credenciales
2. Detecta cámaras disponibles
3. Captura una foto
4. Detecta emociones
5. Analiza atributos faciales

### Iniciar API

```bash
python start_api.py
```

O directamente:

```bash
uvicorn api.main:app --reload
```

## Endpoints Disponibles

### 1. Estado del Servicio

```http
GET /face/status
```

**Respuesta:**
```json
{
  "available": true,
  "message": "Face Recognition service disponible"
}
```

### 2. Detectar Emociones (Base64)

```http
POST /face/emotion
Content-Type: application/json

{
  "image": "base64_encoded_image_data"
}
```

**Respuesta:**
```json
{
  "face_detected": true,
  "num_faces": 1,
  "emotions": {
    "anger": 0.001,
    "contempt": 0.002,
    "disgust": 0.001,
    "fear": 0.001,
    "happiness": 0.987,
    "neutral": 0.005,
    "sadness": 0.002,
    "surprise": 0.001
  },
  "emotions_es": {
    "enojo": 0.001,
    "desprecio": 0.002,
    "disgusto": 0.001,
    "miedo": 0.001,
    "felicidad": 0.987,
    "neutral": 0.005,
    "tristeza": 0.002,
    "sorpresa": 0.001
  },
  "dominant_emotion": "happiness",
  "dominant_emotion_es": "felicidad",
  "confidence": 0.987,
  "message": "Emoción detectada: felicidad (98.70%)"
}
```

### 3. Detectar Emociones (Archivo)

```http
POST /face/emotion/upload
Content-Type: multipart/form-data

file: [imagen.jpg]
```

### 4. Análisis Completo de Rostro

```http
POST /face/analyze
Content-Type: multipart/form-data

file: [imagen.jpg]
```

**Respuesta:**
```json
{
  "face_detected": true,
  "face_id": "face-uuid",
  "face_rectangle": {
    "left": 123,
    "top": 45,
    "width": 200,
    "height": 250
  },
  "age": 25,
  "gender": "female",
  "smile": 0.95,
  "glasses": "NoGlasses",
  "emotions": {
    "happiness": 0.95
  },
  "hair": {
    "bald": 0.01,
    "invisible": false,
    "hair_color": [
      {"color": "brown", "confidence": 0.95}
    ]
  },
  "facial_hair": {
    "moustache": 0.0,
    "beard": 0.0,
    "sideburns": 0.0
  }
}
```

### 5. Detectar Múltiples Rostros

```http
POST /face/detect/multiple
Content-Type: multipart/form-data

file: [imagen.jpg]
```

**Respuesta:**
```json
{
  "num_faces": 3,
  "faces": [
    {
      "face_id": "face-uuid-1",
      "face_rectangle": {...},
      "age": 25,
      "gender": "female",
      "emotion": {
        "dominant": "happiness",
        "dominant_es": "felicidad",
        "confidence": 0.95
      }
    },
    ...
  ]
}
```

## Ejemplos de Uso

### Python con requests

```python
import requests
import base64

# 1. Verificar estado
response = requests.get("http://localhost:8000/face/status")
print(response.json())

# 2. Detectar emociones con archivo
with open("foto.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/face/emotion/upload",
        files=files
    )
    print(response.json())

# 3. Detectar emociones con base64
with open("foto.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()
    
response = requests.post(
    "http://localhost:8000/face/emotion",
    json={"image": image_data}
)
print(response.json())

# 4. Análisis completo
with open("foto.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/face/analyze",
        files=files
    )
    print(response.json())
```

### JavaScript (Fetch API)

```javascript
// 1. Verificar estado
fetch('http://localhost:8000/face/status')
  .then(response => response.json())
  .then(data => console.log(data));

// 2. Detectar emociones con archivo
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/face/emotion/upload', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data));

// 3. Detectar emociones con base64
const reader = new FileReader();
reader.onload = function(e) {
  const base64 = e.target.result.split(',')[1];
  
  fetch('http://localhost:8000/face/emotion', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({image: base64})
  })
    .then(response => response.json())
    .then(data => console.log(data));
};
reader.readAsDataURL(fileInput.files[0]);
```

### cURL

```bash
# 1. Verificar estado
curl http://localhost:8000/face/status

# 2. Detectar emociones con archivo
curl -X POST "http://localhost:8000/face/emotion/upload" \
  -F "file=@foto.jpg"

# 3. Análisis completo
curl -X POST "http://localhost:8000/face/analyze" \
  -F "file=@foto.jpg"
```

## Solución de Problemas

### Error: "Face Recognition service not configured"

**Causa:** Variables de entorno no configuradas.

**Solución:**
```powershell
$env:AZURE_FACE_KEY="tu-key"
$env:AZURE_FACE_ENDPOINT="tu-endpoint"
```

### Error: "Access denied" o "401 Unauthorized"

**Causa:** Key incorrecta o expirada.

**Solución:**
1. Verifica que la KEY sea correcta en Azure Portal
2. Regenera la KEY si es necesario
3. Actualiza la variable de entorno

### Error: "Rate limit exceeded"

**Causa:** Has superado el límite del plan Free (20 llamadas/min).

**Solución:**
- Espera un minuto antes de hacer más llamadas
- Considera actualizar al plan S0 si necesitas más llamadas

### Error: "No se detectó ningún rostro"

**Causas posibles:**
- Imagen muy oscura o borrosa
- Rostro muy pequeño en la imagen
- Ángulo muy pronunciado

**Solución:**
- Usa imágenes con buena iluminación
- Asegúrate que el rostro ocupe al menos 36x36 píxeles
- El rostro debe estar relativamente frontal

### Error: "Camera not found"

**Causa:** No hay cámara disponible o no tiene permisos.

**Solución:**
1. Verifica que tu dispositivo tiene cámara
2. Asegúrate que no está en uso por otra aplicación
3. En Windows, permite el acceso a la cámara en Configuración > Privacidad

### Error de importación de OpenCV

**Solución:**
```bash
pip install --upgrade opencv-python
```

## Límites y Cuotas

### Plan Free (F0)
- **Transacciones por minuto:** 20
- **Transacciones por mes:** 30,000
- **Costo:** Gratis

### Plan Standard (S0)
- **Transacciones por segundo:** 10
- **Costo:** Ver pricing de Azure

### Límites de Imagen
- **Formatos soportados:** JPEG, PNG, GIF, BMP
- **Tamaño máximo:** 6 MB
- **Tamaño mínimo de rostro:** 36x36 píxeles
- **Máximo de rostros detectables:** 100 por imagen

## Recursos Adicionales

- [Documentación oficial de Azure Face API](https://docs.microsoft.com/azure/cognitive-services/face/)
- [API Reference](https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/)
- [SDK Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cognitiveservices/azure-cognitiveservices-vision-face)
- [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/face-api/)

## Notas de Privacidad

⚠️ **IMPORTANTE:** 

- Azure Face API procesa las imágenes en la nube de Microsoft
- Los datos se procesan según la política de privacidad de Azure
- Para producción, asegúrate de cumplir con las leyes de privacidad (GDPR, etc.)
- No almacenes datos biométricos sin consentimiento explícito

## Contacto y Soporte

Si tienes problemas:
1. Revisa esta documentación
2. Ejecuta `python setup_face_recognition.py`
3. Consulta los logs de error
4. Verifica el estado del servicio en Azure Portal
