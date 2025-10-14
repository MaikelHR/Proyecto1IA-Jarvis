# 🎨 Frontend - Jarvis IA

Interfaz web moderna y funcional para interactuar con el sistema de IA.

![Frontend Status](https://img.shields.io/badge/Status-Completado-success)
![Tech](https://img.shields.io/badge/Tech-HTML%2FCSS%2FJS-blue)

---

## ✅ Estado Actual

**✅ COMPLETADO** - Frontend totalmente funcional con HTML/CSS/JavaScript vanilla

---

## 🎯 Características Implementadas

### 1. 📊 Dashboard Interactivo
- ✅ Vista general del sistema
- ✅ Estadísticas en tiempo real (modelos, servicios, API)
- ✅ Estado de servicios (ML, Voice, Face)
- ✅ Guía rápida de uso
- ✅ Cards informativos con iconos

### 2. 🧠 Modelos de Machine Learning
- ✅ Lista de 9 modelos disponibles
- ✅ Información detallada de cada modelo
- ✅ Formularios dinámicos con datos de ejemplo
- ✅ Ejecución de predicciones en tiempo real
- ✅ Visualización de resultados con confianza
- ✅ Comandos de voz sugeridos

### 3. 🎤 Speech-to-Text
- ✅ Grabación de audio desde el navegador
- ✅ Transcripción de voz a texto (Google Speech-to-Text)
- ✅ Reconocimiento de comandos de voz
- ✅ Visualizador de audio animado
- ✅ Lista de comandos de ejemplo
- ✅ Estado del servicio en tiempo real

### 4. 😊 Reconocimiento Facial
- ✅ Captura desde webcam en tiempo real
- ✅ Subida de imágenes
- ✅ Análisis de emociones (Azure Face API)
- ✅ Gráficos de barras con todas las emociones
- ✅ Emoción dominante destacada
- ✅ Contador de rostros detectados

---

## 🚀 Cómo Iniciar el Frontend

### Prerrequisitos

1. **Backend corriendo** en `http://localhost:8000`
   ```powershell
   cd backend
   python start_api.py
   ```

2. **Navegador moderno** (Chrome, Firefox, Edge)

### Opción 1: Servidor Python (Recomendado)

```powershell
# Desde la carpeta frontend/
cd frontend
python -m http.server 8080
```

Luego abre: **http://localhost:8080**

### Opción 2: Live Server (VS Code)

1. Instala la extensión **"Live Server"** en VS Code
2. Click derecho en `index.html`
3. Selecciona **"Open with Live Server"**

### Opción 3: Abrir directamente

Simplemente abre `index.html` en tu navegador (algunas funciones pueden requerir servidor).

---

## 📁 Estructura de Archivos

```
frontend/
├── index.html          # Estructura HTML principal
├── styles.css          # Estilos CSS completos
├── app.js              # Lógica JavaScript
└── README.md           # Este archivo
```

---

## 🎨 Diseño y UI

### Paleta de Colores

- **Primario:** `#2563eb` (Azul)
- **Secundario:** `#8b5cf6` (Púrpura)
- **Éxito:** `#10b981` (Verde)
- **Peligro:** `#ef4444` (Rojo)
- **Fondo:** `#0f172a` (Azul oscuro)

### Características de Diseño

- 🌙 **Tema oscuro** profesional
- 🎯 **Diseño responsive** (desktop, tablet, mobile)
- ✨ **Animaciones suaves** en transiciones
- 🎨 **Gradientes modernos** en iconos
- 📱 **Mobile-first** approach

---

## 🧪 Probar las Funcionalidades

### 1. Dashboard
1. Abre la aplicación
2. Verifica que el indicador de estado muestre "API Conectada" (verde)
3. Revisa las estadísticas de los 4 cards

### 2. Modelos ML

#### Ejemplo: Wine Quality
1. Ve a la pestaña "Modelos ML"
2. Selecciona "Calidad de vinos"
3. Los campos ya tienen valores de ejemplo
4. Presiona "Predecir"
5. Verás el resultado con la calidad predicha (1-10)

#### Ejemplo: Bitcoin Price
1. Selecciona "Precio histórico de Bitcoin"
2. Ajusta los valores: Open, High, Low, Volume
3. Presiona "Predecir"
4. Obtendrás el precio de cierre estimado

### 3. Speech-to-Text

**Nota:** Requiere Google Cloud Speech-to-Text configurado

1. Ve a la pestaña "Speech-to-Text"
2. Presiona "Iniciar Grabación"
3. Permite el acceso al micrófono
4. Di un comando: *"Jarvis, predice el precio de Bitcoin"*
5. Presiona "Detener Grabación"
6. Verás la transcripción y el comando reconocido

### 4. Reconocimiento Facial

**Nota:** Requiere Azure Face API configurado

#### Opción A: Webcam
1. Ve a la pestaña "Reconocimiento Facial"
2. Presiona "Iniciar Cámara"
3. Permite el acceso a la cámara
4. Presiona "Capturar Foto"
5. Verás el análisis de emociones

#### Opción B: Subir Imagen
1. Presiona "Subir Imagen"
2. Selecciona una foto con un rostro
3. Verás el análisis automáticamente

---

## 🔌 Integración con Backend

El frontend se comunica con estos endpoints:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Verificar estado de la API |
| `/predictions/datasets` | GET | Obtener lista de modelos |
| `/predictions/{model}` | POST | Realizar predicción |
| `/voice/command` | POST | Procesar comando de voz |
| `/voice/status` | GET | Estado del servicio de voz |
| `/face/emotion/upload` | POST | Analizar emociones |
| `/face/status` | GET | Estado del servicio facial |

### Configuración de API

El frontend está configurado para conectarse a:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

Si tu backend está en otro puerto, edita esta línea en `app.js`.

---

## 📊 Modelos Disponibles en la UI

| # | Modelo | Tipo | UI Form |
|---|--------|------|---------|
| 1 | Bitcoin Price | Regresión | ✅ Completo |
| 2 | Avocado Prices | Regresión | ✅ Completo |
| 3 | Body Fat | Regresión | ✅ Completo |
| 4 | Car Prices | Regresión | ✅ Completo |
| 5 | Telco Churn | Clasificación | ✅ Completo |
| 6 | Wine Quality | Clasificación | ✅ Completo |
| 7 | Stroke Risk | Clasificación | ✅ Completo |
| 8 | Hepatitis C | Clasificación | ✅ Completo |
| 9 | Cirrhosis Status | Clasificación | ✅ Completo |

Cada modelo tiene un formulario con valores de ejemplo pre-cargados.

---

## 🐛 Solución de Problemas

### El indicador muestra "API Desconectada"

```powershell
# Verifica que el backend esté corriendo
cd backend
python start_api.py

# Verifica el estado
curl http://localhost:8000/health
```

### Las predicciones no funcionan

1. Verifica la consola del navegador (F12)
2. Asegúrate de que el backend está en el puerto 8000
3. Revisa que los modelos estén cargados en el backend

### Speech-to-Text no funciona

1. Verifica que Google Cloud está configurado:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS
   ```
2. El servicio mostrará "No configurado" si falta la API key

### Face Recognition no funciona

1. Verifica las variables de Azure:
   ```powershell
   [System.Environment]::GetEnvironmentVariable('AZURE_FACE_KEY', 'User')
   [System.Environment]::GetEnvironmentVariable('AZURE_FACE_ENDPOINT', 'User')
   ```

### CORS Errors

El backend ya tiene CORS configurado. Si persiste:
```python
# backend/api/main.py ya tiene:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

---

## 🎯 Funcionalidades Adicionales (Opcional)

Si quieres mejorar el frontend, puedes agregar:

- [ ] Sistema de notificaciones toast
- [ ] Historial de predicciones
- [ ] Gráficos interactivos (Chart.js)
- [ ] Modo claro/oscuro toggle
- [ ] Exportar resultados a PDF/CSV
- [ ] Animación de Jarvis respondiendo
- [ ] Múltiples idiomas (i18n)

---

## 📱 Responsive Design

El frontend es completamente responsive:

- ✅ **Desktop** (1920x1080+): Grid de 2-4 columnas
- ✅ **Laptop** (1366x768): Grid de 2-3 columnas
- ✅ **Tablet** (768x1024): Grid de 1-2 columnas
- ✅ **Mobile** (375x667): Stack vertical, menú colapsable

---

## 🎬 Demo en Vivo

1. Inicia el backend:
   ```powershell
   cd backend
   python start_api.py
   ```

2. Inicia el frontend:
   ```powershell
   cd frontend
   python -m http.server 8080
   ```

3. Abre: http://localhost:8080

---

## 📖 Documentación Relacionada

- [Quick Start](../docs/QUICK_START.md) - Guía de inicio rápido
- [Ejemplos de Predicción](../docs/reports/EJEMPLOS_COMPLETOS_PREDICCION.md) - Ejemplos de uso
- [API Documentation](http://localhost:8000/docs) - Swagger UI del backend

---

## 🎓 Para el Proyecto del TEC

### Requerimientos Cumplidos

✅ **1. Reconocimiento de sentimiento con foto**
   - Implementado en pestaña "Reconocimiento Facial"
   - Captura desde webcam o subida de imagen
   - Análisis de 8 emociones con Azure Face API

✅ **2. Audio → Texto → Ejecutar instrucción**
   - Implementado en pestaña "Speech-to-Text"
   - Grabación desde navegador
   - Transcripción con Google Speech-to-Text
   - Reconocimiento de comandos asociados a modelos

✅ **3. 10 algoritmos de ML** (9 implementados)
   - Interfaz completa para los 9 modelos
   - Formularios dinámicos con validación
   - Visualización de resultados

✅ **4. Comandos de voz asociados**
   - Cada modelo tiene comandos de voz definidos
   - Parser de comandos implementado
   - Ejemplos visibles en la UI

### Presentación/Demo

Para tu presentación del proyecto:

1. **Muestra el Dashboard** - Estado general del sistema
2. **Ejecuta una predicción ML** - Ejemplo: Wine Quality
3. **Graba un comando de voz** - Demuestra Speech-to-Text
4. **Analiza una emoción** - Captura con webcam
5. **Explica la arquitectura** - Frontend → API → ML Models

---

## 🤝 Contribuir

Si quieres mejorar el frontend:

1. Los formularios están en `app.js` → `formFields`
2. Los estilos están organizados por sección en `styles.css`
3. Los colores están en variables CSS en `:root`
4. Las funciones están bien documentadas

---

## 📞 Soporte

Si tienes problemas:
1. Revisa la consola del navegador (F12)
2. Verifica que el backend esté corriendo
3. Consulta la documentación del backend

---

<div align="center">

**🤖 Jarvis IA Frontend**

Interfaz moderna para tu asistente inteligente

[Ver Backend](../backend/) • [Documentación](../docs/) • [API Docs](http://localhost:8000/docs)

</div>
