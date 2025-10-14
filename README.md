# 🤖 Jarvis IA - Asistente Inteligente# 🤖 Proyecto Jarvis IA



![Status](https://img.shields.io/badge/Backend-100%25%20Operativo-success)Asistente inteligente con capacidades de **Machine Learning**, **reconocimiento de voz** 

![Tests](https://img.shields.io/badge/Tests-9%2F9%20Passed-success)y **análisis facial** desarrollado para el TEC.

![API](https://img.shields.io/badge/API-FastAPI-blue)

![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange)## 🌟 Características



Asistente inteligente avanzado con **9 Modelos de Machine Learning**, **Speech-to-Text** y **Face Recognition** desarrollado como proyecto del TEC.- 🎯 **9 Modelos de ML** entrenados para predicciones

- 🎤 **Speech-to-Text** con Google Cloud API

---- 😊 **Face Recognition** con Azure Cognitive Services

- 📹 **Captura de video** con OpenCV

## 🌟 Características Principales- 🚀 **API REST** completa con FastAPI

- 📚 **Documentación automática** con Swagger UI

### 🧠 Machine Learning

- ✅ **9 Modelos Entrenados** y operativos (100% funcionales)## Estructura

- 🎯 Predicciones en tiempo real vía API REST

- 📊 Clasificación, Regresión y Series Temporales```

- 🔄 Pipeline automatizado de entrenamiento├── data/

│   ├── README.md             # Documentación de los datos disponibles

### 🎤 Speech-to-Text│   └── raw/                  # Archivos CSV originales (no modificar)

- 🗣️ Reconocimiento de voz con Google Cloud API├── reports/                  # Métricas y modelos generados automáticamente

- 🎙️ Comandos por voz en tiempo real├── requirements.txt          # Dependencias de Python

- 🌐 Soporte multiidioma├── main.py                   # Punto de entrada CLI

└── src/

### 😊 Face Recognition    ├── __init__.py

- 📷 Reconocimiento facial con Azure Cognitive Services    ├── data_analysis.py      # Resúmenes exploratorios automatizados

- 🔐 Verificación de identidad    ├── data_loading.py       # Carga y limpieza específica por dataset

- 👥 Registro de usuarios    ├── dataset_registry.py   # Metadatos y registro de datasets soportados

    ├── modeling.py           # Entrenamiento y evaluación de modelos

### 🚀 API REST    └── pipeline.py           # Orquestador de la canalización

- ⚡ FastAPI de alto rendimiento```

- 📚 Documentación automática con Swagger UI

- 🔄 CORS configurado## Datasets soportados

- 🛡️ Manejo robusto de errores

La canalización incluye los siguientes casos de uso (clave entre paréntesis):

---

- Precio histórico de Bitcoin (`bitcoin_price`) – serie temporal con ingeniería

## 📦 Los 9 Modelos ML  de *lags*.

- Precios de aguacate por región (`avocado_prices`) – regresión multivariante.

| # | Modelo | Tipo | Accuracy/R² | Estado |- Porcentaje de grasa corporal (`body_fat`) – regresión.

|---|--------|------|-------------|--------|- Valor de automóviles usados (`car_prices`) – regresión.

| 1 | Bitcoin Price | Time Series | MAE: 404.33 | ✅ |- Churn de clientes Telco (`telco_churn`) – clasificación binaria.

| 2 | Avocado Prices | Regresión | R²: 68.13% | ✅ |- Calidad de vinos (`wine_quality`) – clasificación multiclase.

| 3 | Body Fat | Regresión | R²: 99.82% | ✅ |- Predicción de derrame cerebral (`stroke_risk`) – clasificación binaria.

| 4 | Car Prices | Regresión | R²: 96.28% | ✅ |- Diagnóstico de hepatitis C (`hepatitis_c`) – clasificación multiclase.

| 5 | Telco Churn | Clasificación | Acc: 80.34% | ✅ |- Estatus clínico de cirrosis (`cirrhosis_status`) – clasificación multiclase.

| 6 | Wine Quality | Clasificación | Acc: 53.85% | ✅ |

| 7 | Stroke Risk | Clasificación | Acc: 95.21% | ✅ |## Requisitos

| 8 | Hepatitis C | Clasificación | Acc: 94.31% | ✅ |

| 9 | Cirrhosis Status | Clasificación | Acc: 76.19% | ✅ |```bash

pip install -r requirements.txt

---```



## 🚀 Inicio Rápido## 🚀 Inicio Rápido



### Opción 1: Script Interactivo (Recomendado)### 1. Instalar dependencias

```bash

```powershellpip install -r requirements.txt

python run_jarvis.py```

```

### 2. Entrenar modelos (si no existen)

Menú interactivo con opciones para:```bash

- Iniciar Backendpython main.py

- Ejecutar Pruebas```

- Verificar Modelos

- Ver Documentación### 3. Configurar Speech-to-Text (opcional)

Ver guía completa en: [SPEECH_TO_TEXT_SETUP.md](SPEECH_TO_TEXT_SETUP.md)

### Opción 2: Inicio Manual

```powershell

```powershell# Configurar credenciales de Google Cloud

# Iniciar Backend$env:GOOGLE_APPLICATION_CREDENTIALS="credentials\google-credentials.json"

cd backend```

.\start_api_with_env.ps1

### 4. Configurar Face Recognition (opcional)

# En otra terminal: Ejecutar pruebasVer guía completa en: [FACE_RECOGNITION_SETUP.md](FACE_RECOGNITION_SETUP.md)

cd tests

python test_completo_9_modelos.py```powershell

```# Configurar credenciales de Azure Face API

$env:AZURE_FACE_KEY="tu-key-aquí"

### Verificar Funcionamiento$env:AZURE_FACE_ENDPOINT="https://tu-endpoint.cognitiveservices.azure.com/"



```powershell# Verificar configuración

curl http://localhost:8000/healthpython setup_face_recognition.py

```

# Probar con cámara

**Respuesta esperada:**python test_face_recognition.py

```json```

{

  "status": "healthy",### 5. Iniciar API REST

  "models_loaded": 9,```bash

  "azure_face_configured": truepython run_api.py

}```

```

### 6. Acceder a la documentación

---- **Swagger UI**: http://localhost:8000/docs

- **ReDoc**: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

## 📖 Uso

```

Proyecto1IA-Jarvis/### Entrenar modelos específicos

│```bash

├── backend/                    # 🔧 Backend (API REST)# Procesar un dataset específico

│   ├── api/                    # Endpoints y serviciospython main.py --dataset telco_churn

│   ├── src/                    # Código ML```

│   ├── data/                   # Datasets

│   ├── reports/                # Modelos entrenados### Usar la API REST

│   └── start_api.py            # Iniciar API

│#### Predicciones de ML

├── frontend/                   # 🎨 Frontend (en desarrollo)```python

│   └── README.md               # Guía de desarrolloimport requests

│

├── config/                     # ⚙️ Configuraciones# Hacer predicción

│   └── credentials/            # Credenciales cloudresponse = requests.post(

│    "http://localhost:8000/predictions/telco_churn",

├── docs/                       # 📚 Documentación    json={"features": {"tenure": 12, "monthly_charges": 70.5}}

│   ├── guides/                 # Guías y tutoriales)

│   └── reports/                # Reportes técnicosprint(response.json())

│```

├── tests/                      # 🧪 Suite de pruebas

│   ├── test_completo_9_modelos.py#### Comandos de voz

│   └── quick_test.py```bash

│# Grabar y transcribir

├── scripts/                    # 🔧 Utilidadespython test_speech_to_text.py

│   ├── verificar_modelos.py

│   └── setup_*.py# Probar API de voz

│python test_voice_api.py

├── run_jarvis.py              # 🚀 Script principal```

├── PROJECT_STRUCTURE.md       # 📋 Estructura detallada

└── README.md                  # 📖 Este archivo#### Reconocimiento facial

``````python

import requests

**Ver estructura completa:** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

# Verificar servicio

---response = requests.get("http://localhost:8000/face/status")

print(response.json())

## 🛠️ Instalación

# Detectar emociones

### Prerrequisitoswith open("foto.jpg", "rb") as f:

    files = {"file": f}

- Python 3.8+    response = requests.post(

- pip        "http://localhost:8000/face/emotion/upload",

- PowerShell (Windows)        files=files

    )

### Paso 1: Clonar Repositorio    print(response.json())

    # Output: {"face_detected": true, "dominant_emotion_es": "felicidad", ...}

```bash

git clone https://github.com/MaikelHR/Proyecto1IA-Jarvis.git# Análisis completo de rostro

cd Proyecto1IA-Jarviswith open("foto.jpg", "rb") as f:

```    files = {"file": f}

    response = requests.post(

### Paso 2: Instalar Dependencias        "http://localhost:8000/face/analyze",

        files=files

```powershell    )

cd backend    print(response.json())

pip install -r requirements.txt    # Output: {"age": 25, "gender": "female", "emotions": {...}, ...}

``````



### Paso 3: Configurar Credenciales (Opcional)## Notas



#### Google Cloud (Speech-to-Text)- No se generan datos sintéticos. Todos los experimentos utilizan únicamente los

1. Obtén credenciales en [Google Cloud Console](https://console.cloud.google.com)  CSV almacenados en `data/raw/`.

2. Guarda el archivo en `config/credentials/google-credentials.json`- Evite versionar artefactos derivados distintos de los definidos en este

  repositorio. La canalización permite recrearlos cuando sea necesario.

#### Azure Face API
```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_FACE_KEY', 'tu_key', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_FACE_ENDPOINT', 'tu_endpoint', 'User')
```

### Paso 4: Iniciar API

```powershell
cd backend
python start_api.py
```

---

## 📚 Documentación

### Guías Principales

| Documento | Descripción |
|-----------|-------------|
| [QUICK_START.md](docs/QUICK_START.md) | Inicio rápido |
| [EJEMPLOS_COMPLETOS_PREDICCION.md](docs/reports/EJEMPLOS_COMPLETOS_PREDICCION.md) | Ejemplos de uso de los 9 modelos |
| [SWAGGER_TESTING_GUIDE.md](docs/guides/SWAGGER_TESTING_GUIDE.md) | Testing con Swagger UI |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Estructura del proyecto |

### Reportes

- **[RESUMEN_ACTUALIZACION.md](docs/reports/RESUMEN_ACTUALIZACION.md)** - Estado actual
- **[REPORTE_FINAL_ACTUALIZACION.md](docs/reports/REPORTE_FINAL_ACTUALIZACION.md)** - Reporte técnico

---

## 🧪 Testing

### Prueba Completa (9 Modelos)

```powershell
cd tests
python test_completo_9_modelos.py
```

**Resultado esperado:**
```
✅ Exitosas: 9/9
❌ Fallidas: 0/9
📊 Tasa de éxito: 100.0%
```

### Prueba Rápida

```powershell
cd tests
python quick_test.py
```

### Testing en Swagger UI

1. Inicia la API
2. Abre http://localhost:8000/docs
3. Prueba cualquier endpoint
4. Usa ejemplos de [EJEMPLOS_COMPLETOS_PREDICCION.md](docs/reports/EJEMPLOS_COMPLETOS_PREDICCION.md)

---

## 🎯 Uso de la API

### Health Check

```bash
curl http://localhost:8000/health
```

### Predicción - Wine Quality

```bash
curl -X POST "http://localhost:8000/predictions/wine_quality" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "fixed_acidity": 7.0,
      "volatile_acidity": 0.27,
      "citric_acid": 0.36,
      "residual_sugar": 20.7,
      "chlorides": 0.045,
      "free_sulfur_dioxide": 45.0,
      "total_sulfur_dioxide": 170.0,
      "density": 1.001,
      "p_h": 3.0,
      "sulphates": 0.45,
      "alcohol": 8.8,
      "type": "white"
    }
  }'
```

**Respuesta:**
```json
{
  "dataset": "Calidad de vinos",
  "prediction": 5,
  "confidence": 0.48,
  "task_type": "classification"
}
```

**Ver todos los ejemplos:** [EJEMPLOS_COMPLETOS_PREDICCION.md](docs/reports/EJEMPLOS_COMPLETOS_PREDICCION.md)

---

## 📞 Contacto y Soporte

- **Documentación:** [docs/](docs/)
- **Testing:** [tests/README.md](tests/README.md)
- **Reportes:** [docs/reports/](docs/reports/)

---

## 📊 Estadísticas del Proyecto

```
📦 Backend: 100% operativo
🧪 Tests: 9/9 pasando (100%)
📚 Documentación: Completa
🔧 Scripts de utilidad: 8
📄 Guías: 10+
🎯 Modelos ML: 9/9 funcionando
⚡ Endpoints API: 15+
```

---

**Estado del Proyecto:** ✅ Backend Completado - Listo para Frontend

**Última actualización:** 13 de octubre de 2025

---

<div align="center">

### 🚀 ¡El futuro de la IA está aquí! 🤖

**[Iniciar Jarvis](run_jarvis.py)** | **[Ver Docs](docs/)** | **[Ejecutar Tests](tests/)**

</div>
