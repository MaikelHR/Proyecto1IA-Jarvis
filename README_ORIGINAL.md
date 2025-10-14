# 🤖 Proyecto Jarvis IA

Asistente inteligente con capacidades de **Machine Learning**, **reconocimiento de voz** 
y **análisis facial** desarrollado para el TEC.

## 🌟 Características

- 🎯 **9 Modelos de ML** entrenados para predicciones
- 🎤 **Speech-to-Text** con Google Cloud API
- 😊 **Face Recognition** con Azure Cognitive Services
- 📹 **Captura de video** con OpenCV
- 🚀 **API REST** completa con FastAPI
- 📚 **Documentación automática** con Swagger UI

## Estructura

```
├── data/
│   ├── README.md             # Documentación de los datos disponibles
│   └── raw/                  # Archivos CSV originales (no modificar)
├── reports/                  # Métricas y modelos generados automáticamente
├── requirements.txt          # Dependencias de Python
├── main.py                   # Punto de entrada CLI
└── src/
    ├── __init__.py
    ├── data_analysis.py      # Resúmenes exploratorios automatizados
    ├── data_loading.py       # Carga y limpieza específica por dataset
    ├── dataset_registry.py   # Metadatos y registro de datasets soportados
    ├── modeling.py           # Entrenamiento y evaluación de modelos
    └── pipeline.py           # Orquestador de la canalización
```

## Datasets soportados

La canalización incluye los siguientes casos de uso (clave entre paréntesis):

- Precio histórico de Bitcoin (`bitcoin_price`) – serie temporal con ingeniería
  de *lags*.
- Precios de aguacate por región (`avocado_prices`) – regresión multivariante.
- Porcentaje de grasa corporal (`body_fat`) – regresión.
- Valor de automóviles usados (`car_prices`) – regresión.
- Churn de clientes Telco (`telco_churn`) – clasificación binaria.
- Calidad de vinos (`wine_quality`) – clasificación multiclase.
- Predicción de derrame cerebral (`stroke_risk`) – clasificación binaria.
- Diagnóstico de hepatitis C (`hepatitis_c`) – clasificación multiclase.
- Estatus clínico de cirrosis (`cirrhosis_status`) – clasificación multiclase.

## Requisitos

```bash
pip install -r requirements.txt
```

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Entrenar modelos (si no existen)
```bash
python main.py
```

### 3. Configurar Speech-to-Text (opcional)
Ver guía completa en: [SPEECH_TO_TEXT_SETUP.md](SPEECH_TO_TEXT_SETUP.md)

```powershell
# Configurar credenciales de Google Cloud
$env:GOOGLE_APPLICATION_CREDENTIALS="credentials\google-credentials.json"
```

### 4. Configurar Face Recognition (opcional)
Ver guía completa en: [FACE_RECOGNITION_SETUP.md](FACE_RECOGNITION_SETUP.md)

```powershell
# Configurar credenciales de Azure Face API
$env:AZURE_FACE_KEY="tu-key-aquí"
$env:AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"

# Verificar configuración
python setup_face_recognition.py

# Probar con cámara
python test_face_recognition.py
```

### 5. Iniciar API REST
```bash
python run_api.py
```

### 6. Acceder a la documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 Uso

### Entrenar modelos específicos
```bash
# Procesar un dataset específico
python main.py --dataset telco_churn
```

### Usar la API REST

#### Predicciones de ML
```python
import requests

# Hacer predicción
response = requests.post(
    "http://localhost:8000/predictions/telco_churn",
    json={"features": {"tenure": 12, "monthly_charges": 70.5}}
)
print(response.json())
```

#### Comandos de voz
```bash
# Grabar y transcribir
python test_speech_to_text.py

# Probar API de voz
python test_voice_api.py
```

#### Reconocimiento facial
```python
import requests

# Verificar servicio
response = requests.get("http://localhost:8000/face/status")
print(response.json())

# Detectar emociones
with open("foto.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/face/emotion/upload",
        files=files
    )
    print(response.json())
    # Output: {"face_detected": true, "dominant_emotion_es": "felicidad", ...}

# Análisis completo de rostro
with open("foto.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/face/analyze",
        files=files
    )
    print(response.json())
    # Output: {"age": 25, "gender": "female", "emotions": {...}, ...}
```

## Notas

- No se generan datos sintéticos. Todos los experimentos utilizan únicamente los
  CSV almacenados en `data/raw/`.
- Evite versionar artefactos derivados distintos de los definidos en este
  repositorio. La canalización permite recrearlos cuando sea necesario.
