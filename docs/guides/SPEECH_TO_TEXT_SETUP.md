# 🎤 Speech-to-Text - Guía de Configuración

## ✅ **Implementación Completada**

Se ha implementado el sistema completo de Speech-to-Text usando Google Cloud:

### **Archivos Creados:**
```
api/services/
├── speech_service.py    # Servicio de Google Speech-to-Text
├── audio_utils.py       # Captura y procesamiento de audio
└── __init__.py

api/routers/
└── voice.py             # Endpoints actualizados

Scripts:
├── test_speech_to_text.py  # Grabar audio y transcribir
└── test_voice_api.py        # Tests de la API
```

### **Endpoints Disponibles:**
- ✅ `POST /voice/command` - Transcribir audio base64
- ✅ `POST /voice/upload` - Subir archivo de audio
- ✅ `POST /voice/parse` - Parsear texto (sin audio)
- ✅ `GET /voice/status` - Estado del servicio

---

## 🔑 **PASO 1: Obtener Credenciales de Google Cloud**

### **Opción A: Con cuenta de estudiante/educación (GRATIS)**
1. Ve a: https://cloud.google.com/edu
2. Usa tu correo institucional (@tec.ac.cr)
3. Obtendrás créditos gratis para usar las APIs

### **Opción B: Con cuenta personal (GRATIS por 12 meses)**
1. Ve a: https://cloud.google.com/free
2. Crea una cuenta (requiere tarjeta pero no cobran)
3. Obtienes $300 en créditos gratis

### **Pasos para configurar:**

#### 1. Crear Proyecto
```
1. Ve a: https://console.cloud.google.com/
2. Click en "Crear Proyecto"
3. Nombre: "jarvis-ia-tec"
4. Click "Crear"
```

#### 2. Habilitar Speech-to-Text API
```
1. En el menú, ve a: "APIs y servicios" → "Biblioteca"
2. Busca: "Cloud Speech-to-Text API"
3. Click "Habilitar"
```

#### 3. Crear Credenciales
```
1. Ve a: "APIs y servicios" → "Credenciales"
2. Click "Crear credenciales" → "Cuenta de servicio"
3. Nombre: "jarvis-speech-service"
4. Rol: "Propietario del proyecto" o "Usuario de Speech-to-Text"
5. Click "Crear y continuar"
6. Click "Listo"
```

#### 4. Descargar Credenciales JSON
```
1. En "Credenciales", click en la cuenta de servicio creada
2. Tab "Claves"
3. Click "Agregar clave" → "Crear clave nueva"
4. Tipo: JSON
5. Click "Crear"
6. Se descargará un archivo JSON
```

#### 5. Guardar el archivo
```
1. Guarda el archivo en tu proyecto:
   D:\TEC\IA\Proyecto1IA-Jarvis\credentials\
   
2. Renómbralo a: google-credentials.json
```

---

## 🚀 **PASO 2: Configurar el Proyecto**

### **Windows PowerShell:**
```powershell
# Crear carpeta de credenciales
mkdir credentials

# Mover el archivo descargado
Move-Item "C:\Users\TU_USUARIO\Downloads\jarvis-*.json" "credentials\google-credentials.json"

# Configurar variable de entorno (temporal)
$env:GOOGLE_APPLICATION_CREDENTIALS="D:\TEC\IA\Proyecto1IA-Jarvis\credentials\google-credentials.json"

# Configurar variable permanente (opcional)
[System.Environment]::SetEnvironmentVariable(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "D:\TEC\IA\Proyecto1IA-Jarvis\credentials\google-credentials.json",
    "User"
)
```

### **Verificar configuración:**
```powershell
# Verificar que la variable está configurada
echo $env:GOOGLE_APPLICATION_CREDENTIALS

# Debería mostrar: D:\TEC\IA\Proyecto1IA-Jarvis\credentials\google-credentials.json
```

---

## 🧪 **PASO 3: Probar el Sistema**

### **Test 1: Estado del servicio**
```powershell
# Iniciar API (en una terminal)
python run_api.py

# En otra terminal, verificar estado
curl http://localhost:8000/voice/status
```

### **Test 2: Grabar y transcribir**
```powershell
# Graba 5 segundos de audio y transcribe
python test_speech_to_text.py

# Graba 10 segundos
python test_speech_to_text.py --duration 10
```

### **Test 3: Tests de la API**
```powershell
# Ejecutar suite completa de tests
python test_voice_api.py
```

---

## 📝 **PASO 4: Uso desde la API**

### **Ejemplo: Python**
```python
import requests
import base64

# Leer archivo de audio
with open("audio.wav", "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()

# Enviar a la API
response = requests.post(
    "http://localhost:8000/voice/command",
    json={
        "audio_base64": audio_base64,
        "language_code": "es-ES"
    }
)

result = response.json()
print(f"Transcripción: {result['transcript']}")
print(f"Comando: {result['dataset_key']}")
```

### **Ejemplo: cURL**
```bash
# Upload audio file
curl -X POST http://localhost:8000/voice/upload \
  -F "file=@audio.wav" \
  -F "language_code=es-ES"
```

### **Ejemplo: JavaScript**
```javascript
const audioBlob = await recorder.getBlob();
const base64 = await blobToBase64(audioBlob);

const response = await fetch('http://localhost:8000/voice/command', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    audio_base64: base64.split(',')[1],
    language_code: 'es-ES'
  })
});

const result = await response.json();
console.log(result.transcript);
```

---

## 🎯 **Comandos Reconocidos**

El sistema reconoce los siguientes patrones:

| Comando de Voz | Dataset |
|----------------|---------|
| "Jarvis, predice el precio de Bitcoin" | `bitcoin_price` |
| "Analiza riesgo de churn" | `telco_churn` |
| "Evalúa la calidad del vino" | `wine_quality` |
| "Calcula mi grasa corporal" | `body_fat` |
| "Valora este auto usado" | `car_prices` |
| "Predice precio de aguacate" | `avocado_prices` |
| "Evalúa riesgo de derrame" | `stroke_risk` |
| "Diagnostica hepatitis C" | `hepatitis_c` |
| "Analiza estado de cirrosis" | `cirrhosis_status` |

---

## 🔧 **Troubleshooting**

### **Error: "credentials not configured"**
```powershell
# Verifica la variable de entorno
echo $env:GOOGLE_APPLICATION_CREDENTIALS

# Verifica que el archivo existe
Test-Path $env:GOOGLE_APPLICATION_CREDENTIALS
```

### **Error: "PyAudio not found"**
```powershell
# En Windows puede requerir instalación manual
pip install pipwin
pipwin install pyaudio
```

### **Error: "Permission denied"**
```powershell
# Verifica permisos del archivo JSON
icacls credentials\google-credentials.json
```

### **Error: "Quota exceeded"**
- Google Cloud da 60 minutos gratis/mes
- Verifica uso en: https://console.cloud.google.com/apis/api/speech.googleapis.com/quotas

---

## 📊 **Costos (Tranquilo, es GRATIS)**

- **Capa gratuita:** 60 minutos/mes GRATIS
- **Después:** $0.006 por 15 segundos
- **Tu uso estimado:** ~30 minutos para pruebas = $0 💰

---

## ✅ **Checklist de Implementación**

- [x] ✅ Librerías instaladas
- [x] ✅ Servicio de Speech-to-Text creado
- [x] ✅ Endpoints de API actualizados
- [x] ✅ Scripts de prueba creados
- [ ] ⏳ Obtener credenciales de Google Cloud
- [ ] ⏳ Configurar variable de entorno
- [ ] ⏳ Probar grabación y transcripción
- [ ] ⏳ Integrar con interfaz de usuario

---

## 🎓 **Para la Documentación del Proyecto**

Incluye en tu documento:

**Papers relevantes:**
- "Attention Is All You Need" (Transformers - base de los modelos modernos)
- "Deep Speech 2: End-to-End Speech Recognition" (Baidu)
- "Listen, Attend and Spell" (Google Brain)

**Justificación técnica:**
- Uso de Transformer-based ASR (Automatic Speech Recognition)
- Pre-entrenamiento en millones de horas de audio
- Fine-tuning para español con diacríticos

---

**¿Necesitas ayuda con algún paso específico?** 🚀
