# 📁 Jarvis IA - Estructura del Proyecto

## 🗂️ Organización de Carpetas

```
Proyecto1IA-Jarvis/
├── backend/                    # Backend (API REST con FastAPI)
│   ├── api/                    # Código de la API
│   │   ├── routers/            # Endpoints
│   │   ├── services/           # Lógica de negocio
│   │   └── main.py             # Aplicación FastAPI
│   ├── src/                    # Código fuente del proyecto
│   │   ├── data_analysis.py
│   │   ├── data_loading.py
│   │   ├── dataset_registry.py
│   │   ├── modeling.py
│   │   └── pipeline.py
│   ├── data/                   # Datos del proyecto
│   │   └── raw/                # Datos crudos (CSVs)
│   ├── reports/                # Modelos entrenados y métricas
│   ├── temp_audio/             # Archivos de audio temporales
│   ├── start_api.py            # Script principal para iniciar API
│   ├── start_api_with_env.ps1 # Script PowerShell con Azure env vars
│   ├── run_api.py              # Script alternativo
│   └── requirements.txt        # Dependencias Python
│
├── frontend/                   # Frontend (vacío, para desarrollo futuro)
│   └── README.md               # Guía para desarrollo frontend
│
├── config/                     # Configuraciones y credenciales
│   ├── credentials/            # Credenciales de servicios cloud
│   │   └── google-credentials.json
│   └── requirements.txt        # Copia de dependencias
│
├── docs/                       # Documentación del proyecto
│   ├── guides/                 # Guías y tutoriales
│   │   ├── TESTING_GUIDE.md
│   │   ├── SWAGGER_TESTING_GUIDE.md
│   │   ├── QUICK_TEST_GUIDE.md
│   │   ├── FACE_RECOGNITION_SETUP.md
│   │   ├── SPEECH_TO_TEXT_SETUP.md
│   │   ├── FACE_RECOGNITION_IMPLEMENTATION.md
│   │   ├── IMPLEMENTACION_API.md
│   │   ├── IMPLEMENTACION_SPEECH_TO_TEXT.md
│   │   └── FIX_SPEECH_TO_TEXT.md
│   ├── reports/                # Reportes y resúmenes
│   │   ├── REPORTE_FINAL_ACTUALIZACION.md
│   │   ├── RESUMEN_ACTUALIZACION.md
│   │   ├── BACKEND_CHECKLIST.md
│   │   ├── BACKEND_TEST_REPORT.md
│   │   ├── EJEMPLOS_COMPLETOS_PREDICCION.md
│   │   ├── DEMO_RAPIDA_SWAGGER.md
│   │   ├── ejemplos_modelos_actualizados.json
│   │   └── ejemplos_prediccion_completos.json
│   ├── QUICK_START.md          # Guía de inicio rápido
│   └── NEXT_STEPS.md           # Próximos pasos
│
├── tests/                      # Scripts de testing y validación
│   ├── test_api.py
│   ├── test_api.html
│   ├── test_api_request.py
│   ├── test_complete_backend.py
│   ├── test_completo_9_modelos.py
│   ├── test_face_api.py
│   ├── test_face_recognition.py
│   ├── test_prediccion_directa.py
│   ├── test_speech_to_text.py
│   ├── test_voice_api.py
│   ├── test_wine_model.py
│   ├── test_report_9_modelos.json
│   └── quick_test.py
│
├── scripts/                    # Scripts de utilidades
│   ├── setup_face_recognition.py
│   ├── setup_speech.py
│   ├── verificar_modelos.py
│   ├── ver_columnas_modelo.py
│   ├── obtener_todas_columnas.py
│   ├── generar_ejemplos_completos.py
│   ├── comparar_modelos.py
│   └── debug_model_pipeline.py
│
├── .git/                       # Control de versiones
├── .gitignore
├── main.py                     # Script principal del proyecto original
├── README.md                   # Este archivo
└── run_jarvis.py               # Script para ejecutar el proyecto
```

---

## 🚀 Inicio Rápido

### 1. Iniciar Backend (API)

```powershell
# Desde la raíz del proyecto
cd backend
.\start_api_with_env.ps1
```

O si no tienes Azure configurado:

```powershell
cd backend
python start_api.py
```

### 2. Verificar que funciona

```powershell
curl http://localhost:8000/health
```

### 3. Acceder a la documentación

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📚 Documentación

### Guías Principales

1. **[QUICK_START.md](docs/QUICK_START.md)** - Comienza aquí
2. **[EJEMPLOS_COMPLETOS_PREDICCION.md](docs/reports/EJEMPLOS_COMPLETOS_PREDICCION.md)** - Ejemplos de uso de los 9 modelos
3. **[SWAGGER_TESTING_GUIDE.md](docs/guides/SWAGGER_TESTING_GUIDE.md)** - Testing con Swagger UI

### Reportes

- **[RESUMEN_ACTUALIZACION.md](docs/reports/RESUMEN_ACTUALIZACION.md)** - Último estado del proyecto
- **[REPORTE_FINAL_ACTUALIZACION.md](docs/reports/REPORTE_FINAL_ACTUALIZACION.md)** - Reporte técnico completo

---

## 🧪 Testing

### Ejecutar pruebas completas:

```powershell
cd tests
python test_completo_9_modelos.py
```

### Ejecutar prueba rápida:

```powershell
cd tests
python quick_test.py
```

---

## 🔧 Scripts de Utilidades

### Verificar modelos:

```powershell
cd scripts
python verificar_modelos.py
```

### Obtener columnas de modelos:

```powershell
cd scripts
python obtener_todas_columnas.py
```

---

## 📊 Estado del Proyecto

- ✅ **Backend:** 100% operativo (9/9 modelos funcionando)
- ⏳ **Frontend:** Pendiente de desarrollo
- ✅ **Documentación:** Completa y actualizada
- ✅ **Testing:** Suite completa de pruebas

---

## 🛠️ Tecnologías

### Backend
- **Framework:** FastAPI
- **ML:** scikit-learn, pandas, numpy
- **Speech-to-Text:** Google Cloud Speech-to-Text API
- **Face Recognition:** Azure Face API
- **Server:** Uvicorn

### Modelos ML (9 modelos)
1. Bitcoin Price (Time Series)
2. Avocado Prices (Regresión)
3. Body Fat (Regresión)
4. Car Prices (Regresión)
5. Telco Churn (Clasificación)
6. Wine Quality (Clasificación)
7. Stroke Risk (Clasificación)
8. Hepatitis C (Clasificación)
9. Cirrhosis Status (Clasificación)

---

## 📝 Notas Importantes

### Rutas Actualizadas

Después de la reorganización, las rutas han cambiado:

- **Credenciales:** `config/credentials/google-credentials.json`
- **Modelos:** `backend/reports/*.pkl`
- **Datos:** `backend/data/raw/*.csv`
- **Tests:** `tests/test_*.py`
- **Scripts:** `scripts/*.py`

### Variables de Entorno

```powershell
# Azure Face API (opcional)
AZURE_FACE_KEY=your_key_here
AZURE_FACE_ENDPOINT=your_endpoint_here

# Google Cloud (opcional, para Speech-to-Text)
GOOGLE_APPLICATION_CREDENTIALS=path/to/google-credentials.json
```

---

## 🤝 Contribución

Este proyecto fue desarrollado como parte del curso de Inteligencia Artificial en el TEC.

**Desarrollador:** MaikelHR  
**Fecha:** Octubre 2025  
**Versión:** 1.0.0

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa [TESTING_GUIDE.md](docs/guides/TESTING_GUIDE.md)
2. Consulta [SWAGGER_TESTING_GUIDE.md](docs/guides/SWAGGER_TESTING_GUIDE.md)
3. Ejecuta `python tests/test_completo_9_modelos.py` para diagnóstico

---

**Estado:** ✅ Backend completado al 100% - Listo para desarrollo de Frontend
