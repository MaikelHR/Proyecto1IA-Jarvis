# 🎯 DEMO RÁPIDA - Predicción de Churn de Clientes

## Paso 1: Ver información del modelo

1. En Swagger, busca: `GET /predictions/{dataset_key}/info`
2. Clic en "Try it out"
3. En `dataset_key` escribe: `telco_churn`
4. Clic en "Execute"

**Verás:** Todas las features (características) que necesita el modelo para hacer una predicción.

---

## Paso 2: Hacer una predicción

1. En Swagger, busca: `POST /predictions/{dataset_key}`
2. Clic en "Try it out"
3. En `dataset_key` escribe: `telco_churn`
4. En el cuadro de "Request body", **BORRA TODO** y pega esto:

```json
{
  "features": {
    "tenure": 3,
    "MonthlyCharges": 85.0,
    "TotalCharges": 255.0,
    "Contract_Month-to-month": 1,
    "Contract_One year": 0,
    "Contract_Two year": 0,
    "InternetService_Fiber optic": 1,
    "InternetService_DSL": 0,
    "InternetService_No": 0,
    "PaymentMethod_Electronic check": 1,
    "PaymentMethod_Mailed check": 0,
    "PaymentMethod_Bank transfer (automatic)": 0,
    "PaymentMethod_Credit card (automatic)": 0
  }
}
```

5. Clic en "Execute"

**Interpretación del ejemplo:**
- Cliente nuevo (3 meses de antigüedad)
- Paga 85 dólares al mes (alto)
- Contrato mes a mes (sin compromiso)
- Fibra óptica (servicio caro)
- Paga con cheque electrónico

**Predicción esperada:** ⚠️ ALTO riesgo de abandono (probablemente ~75-85%)

---

## Paso 3: Comparar con un cliente fiel

Ahora prueba con este otro cliente:

```json
{
  "features": {
    "tenure": 48,
    "MonthlyCharges": 55.0,
    "TotalCharges": 2640.0,
    "Contract_Month-to-month": 0,
    "Contract_One year": 0,
    "Contract_Two year": 1,
    "InternetService_DSL": 1,
    "InternetService_Fiber optic": 0,
    "InternetService_No": 0,
    "PaymentMethod_Electronic check": 0,
    "PaymentMethod_Mailed check": 0,
    "PaymentMethod_Bank transfer (automatic)": 1,
    "PaymentMethod_Credit card (automatic)": 0
  }
}
```

**Interpretación:**
- Cliente antiguo (48 meses = 4 años)
- Paga 55 dólares al mes (moderado)
- Contrato de 2 años (comprometido)
- DSL (servicio económico)
- Pago automático por banco

**Predicción esperada:** ✅ BAJO riesgo de abandono (probablemente ~15-25%)

---

## 🎯 Otros Endpoints Interesantes

### 1. Ver todos los modelos disponibles
**Endpoint:** `GET /predictions/datasets`
- No necesita parámetros
- Te muestra los 9 modelos disponibles

### 2. Verificar que todo funciona
**Endpoint:** `GET /health`
- No necesita parámetros
- Te muestra el estado del sistema completo

### 3. Probar Face Recognition
**Endpoint:** `POST /face/emotion/upload`
- Necesitas una foto con un rostro
- Haz clic en "Choose File" y selecciona tu foto
- Te dirá qué emoción detecta

### 4. Probar Speech-to-Text
**Endpoint:** `POST /speech/transcribe`
- Necesitas un archivo de audio (WAV recomendado)
- Haz clic en "Choose File" y selecciona tu audio
- Te transcribe lo que dijiste

---

## 📊 Checklist de Pruebas Básicas (5 minutos)

✅ Completar esta secuencia:

1. [ ] `GET /health` - Ver estado del sistema
2. [ ] `GET /predictions/datasets` - Ver modelos disponibles
3. [ ] `GET /predictions/telco_churn/info` - Ver detalles del modelo
4. [ ] `POST /predictions/telco_churn` - Hacer predicción (cliente riesgo alto)
5. [ ] `POST /predictions/telco_churn` - Hacer predicción (cliente riesgo bajo)
6. [ ] `GET /face/status` - Verificar Face Recognition
7. [ ] `GET /speech/status` - Verificar Speech-to-Text

---

## 💡 Tips

- **Siempre haz clic en "Try it out"** primero
- **Lee las respuestas** - tienen información muy útil
- **Si hay error 400:** Falta algún campo o está mal escrito
- **Si hay error 404:** El dataset_key no existe
- **Los valores binarios (0 o 1)** representan categorías:
  - `Contract_Month-to-month: 1` = SÍ tiene contrato mes a mes
  - `Contract_One year: 0` = NO tiene contrato de 1 año

---

## 🎓 Entendiendo las Predicciones

### Para Clasificación (Churn, Stroke, Wine Quality):
- `prediction`: 0 o 1 (No/Yes, Bajo/Alto, Mala/Buena)
- `prediction_label`: Etiqueta en texto
- `probability`: % de confianza (0.0 a 1.0)
- `interpretation`: Explicación en español

### Para Regresión (Bitcoin, Avocado, Body Fat):
- `prediction`: Valor numérico (precio, porcentaje, etc.)
- `confidence_interval`: Rango de confianza
- `interpretation`: Explicación en español

---

¡Ahora pruébalo! 🚀
