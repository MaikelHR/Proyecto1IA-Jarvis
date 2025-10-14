# 🤖 Jarvis IA - API REST

API REST completa para el asistente inteligente Jarvis con integración de Machine Learning, reconocimiento de voz y análisis facial.

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Entrenar modelos (si no existen)

```bash
python main.py
```

### 3. Iniciar servidor API

```bash
uvicorn api.main:app --reload
```

O simplemente:

```bash
python run_api.py
```

### 4. Acceder a la documentación

Abre en tu navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Endpoints Principales

### Health Check
```bash
GET /health
```

### Listar Modelos Disponibles
```bash
GET /predictions/datasets
```

### Hacer Predicción
```bash
POST /predictions/{dataset_key}
Content-Type: application/json

{
  "features": {
    "age": 45,
    "gender": "Male",
    "tenure": 24,
    "monthly_charges": 89.5
  }
}
```

### Analizar Comando de Voz (texto)
```bash
POST /voice/parse?text=Jarvis%20predice%20el%20precio%20de%20Bitcoin
```

## 🎯 Modelos Disponibles

| Dataset Key | Nombre | Tipo | Descripción |
|------------|--------|------|-------------|
| `bitcoin_price` | Precio histórico de Bitcoin | Time Series | Predicción de precios |
| `avocado_prices` | Precios de aguacate | Regresión | Precios por región |
| `body_fat` | Grasa corporal | Regresión | Porcentaje de grasa |
| `car_prices` | Valor de autos | Regresión | Precio de vehículos usados |
| `telco_churn` | Churn Telco | Clasificación | Abandono de clientes |
| `wine_quality` | Calidad de vinos | Clasificación | Evaluación de vinos |
| `stroke_risk` | Riesgo de derrame | Clasificación | Predicción de stroke |
| `hepatitis_c` | Hepatitis C | Clasificación | Diagnóstico médico |
| `cirrhosis_status` | Estado de cirrosis | Clasificación | Evaluación clínica |

## 🎤 Comandos de Voz

Ejemplos de comandos reconocidos:

- "Jarvis, predice el precio de Bitcoin"
- "Jarvis, analiza riesgo de churn"
- "Jarvis, evalúa la calidad del vino"
- "Jarvis, calcula mi grasa corporal"
- "Jarvis, valora este auto usado"

## 📝 Ejemplos de Uso

### Python (requests)

```python
import requests

# Predicción de Churn
response = requests.post(
    "http://localhost:8000/predictions/telco_churn",
    json={
        "features": {
            "gender": "Female",
            "senior_citizen": 0,
            "partner": "Yes",
            "dependents": "No",
            "tenure": 12,
            "phone_service": "Yes",
            "monthly_charges": 70.5,
            "total_charges": 846.0
        }
    }
)

result = response.json()
print(f"Predicción: {result['prediction']}")
print(f"Confianza: {result['confidence']}")
```

### JavaScript (fetch)

```javascript
const response = await fetch('http://localhost:8000/predictions/bitcoin_price', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    features: {
      open: 45000,
      high: 46000,
      low: 44500,
      volume: 1000000
    }
  })
});

const result = await response.json();
console.log(result);
```

### cURL

```bash
curl -X POST http://localhost:8000/predictions/wine_quality \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "fixed_acidity": 7.4,
      "volatile_acidity": 0.7,
      "citric_acid": 0,
      "residual_sugar": 1.9,
      "chlorides": 0.076,
      "free_sulfur_dioxide": 11,
      "total_sulfur_dioxide": 34,
      "density": 0.9978,
      "ph": 3.51,
      "sulphates": 0.56,
      "alcohol": 9.4
    }
  }'
```

## 🔧 Configuración Avanzada

### Variables de Entorno

Para funcionalidades completas, configurar:

```bash
# Google Speech-to-Text (opcional)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"

# Azure Face API (opcional)
export AZURE_FACE_KEY="tu-api-key"
export AZURE_FACE_ENDPOINT="https://tu-recurso.cognitiveservices.azure.com/"
```

### Puerto Personalizado

```bash
uvicorn api.main:app --host 0.0.0.0 --port 5000
```

## 🏗️ Estructura de la API

```
api/
├── main.py              # Aplicación FastAPI principal
├── models.py            # Modelos Pydantic (request/response)
├── services.py          # Lógica de negocio
└── routers/
    ├── health.py        # Health checks
    ├── predictions.py   # Predicciones ML
    ├── voice.py         # Comandos de voz
    └── face.py          # Reconocimiento facial
```

## 🎯 Próximos Pasos

1. ✅ **API REST implementada**
2. ⏳ Integrar Google Speech-to-Text API
3. ⏳ Integrar Azure Face API
4. ⏳ Crear interfaz web
5. ⏳ Implementar WebSockets para streaming

## 📄 Documentación Completa

La documentación interactiva está disponible en:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## ⚠️ Notas

- Los modelos deben estar entrenados antes de iniciar la API
- Las funcionalidades de voz y rostro requieren configuración adicional
- Para producción, configurar CORS apropiadamente
