# 🚀 Guía Completa de Testing con Swagger UI

> **Última actualización:** 13 de octubre de 2025  
> **Estado:** ✅ Validado con los 9 modelos funcionando

Esta guía te enseñará cómo probar cada uno de los 9 modelos de Machine Learning usando la interfaz interactiva de Swagger UI.

---

## 📋 Índice

1. [Iniciar la API](#1-iniciar-la-api)
2. [Acceder a Swagger UI](#2-acceder-a-swagger-ui)
3. [Testing por Modelo](#3-testing-por-modelo)
4. [Interpretación de Resultados](#4-interpretación-de-resultados)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Iniciar la API

### Opción A: Con variables de entorno de Azure (Recomendado)
```powershell
.\start_api_with_env.ps1
```

### Opción B: Sin Azure Face Recognition
```powershell
python start_api.py
```

### Verificar que la API está funcionando:
```powershell
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "models_loaded": 9,
  "azure_face_configured": true
}
```

---

## 2. Acceder a Swagger UI

1. Abre tu navegador
2. Navega a: **http://localhost:8000/docs**
3. Verás la documentación interactiva de la API

### Estructura de Swagger UI:

- **GET /health** - Verificar estado de la API
- **POST /predictions/{dataset_key}** - Endpoint principal de predicción
- **POST /voice/command** - Comandos de voz
- **POST /face/verify** - Reconocimiento facial (requiere Azure)

---

## 3. Testing por Modelo

### ⚠️ IMPORTANTE: Convención de Nombres

**Todos los modelos esperan nombres de columnas en formato `snake_case`:**
- ✅ Correcto: `fixed_acidity`, `senior_citizen`, `p_h`
- ❌ Incorrecto: `fixedAcidity`, `SeniorCitizen`, `pH`

---

### 3.1 Bitcoin Price (Regresión)

**Endpoint:** `POST /predictions/bitcoin_price`

1. Click en el endpoint
2. Click en "Try it out"
3. En el campo `dataset_key` escribe: `bitcoin_price`
4. En el campo `request body` pega:

```json
{
  "features": {
    "open": 2763.24,
    "high": 2889.62,
    "low": 2720.61,
    "volume": 860575000.0,
    "market_cap": 45535800000.0,
    "lag_1": 2726.45,
    "lag_7": 2408.37,
    "rolling_mean_7": 2700.15
  }
}
```

5. Click "Execute"

**Respuesta esperada:**
```json
{
  "dataset": "bitcoin_price",
  "prediction": 2875.34,
  "confidence": 0.89,
  "model_type": "regression"
}
```

---

### 3.2 Avocado Prices (Regresión)

**Endpoint:** `POST /predictions/avocado_prices`

```json
{
  "features": {
    "total_volume": 64236.62,
    "col_4046": 1036.74,
    "col_4225": 54454.85,
    "col_4770": 48.16,
    "total_bags": 8696.87,
    "small_bags": 8603.62,
    "large_bags": 93.25,
    "xlarge_bags": 0.0,
    "year": 2015,
    "date": "2015-12-27",
    "type": "conventional",
    "region": "Albany"
  }
}
```

**Interpretación:** Precio promedio del aguacate en USD.

---

### 3.3 Body Fat (Regresión)

**Endpoint:** `POST /predictions/body_fat`

```json
{
  "features": {
    "density": 1.0708,
    "age": 23.0,
    "weight": 154.25,
    "height": 67.75,
    "neck": 36.2,
    "chest": 93.1,
    "abdomen": 85.2,
    "hip": 94.5,
    "thigh": 59.0,
    "knee": 37.3,
    "ankle": 21.9,
    "biceps": 32.0,
    "forearm": 27.4,
    "wrist": 17.1
  }
}
```

**Interpretación:** Porcentaje de grasa corporal (típicamente entre 3% y 50%).

---

### 3.4 Car Prices (Regresión)

**Endpoint:** `POST /predictions/car_prices`

```json
{
  "features": {
    "year": 2014,
    "present_price": 5.59,
    "kms_driven": 27000,
    "owner": 0,
    "car_name": "ritz",
    "fuel_type": "Petrol",
    "seller_type": "Dealer",
    "transmission": "Manual"
  }
}
```

**Interpretación:** Precio de venta en lakhs (unidad monetaria india).

---

### 3.5 Telco Churn (Clasificación Binaria)

**Endpoint:** `POST /predictions/telco_churn`

```json
{
  "features": {
    "senior_citizen": 0,
    "tenure": 1,
    "monthly_charges": 29.85,
    "total_charges": 29.85,
    "customer_id": "7590-VHVEG",
    "gender": "Female",
    "partner": "Yes",
    "dependents": "No",
    "phone_service": "No",
    "multiple_lines": "No phone service",
    "internet_service": "DSL",
    "online_security": "No",
    "online_backup": "Yes",
    "device_protection": "No",
    "tech_support": "No",
    "streaming_tv": "No",
    "streaming_movies": "No",
    "contract": "Month-to-month",
    "paperless_billing": "Yes",
    "payment_method": "Electronic check"
  }
}
```

**Interpretación:**
- **0** = Cliente NO abandonará el servicio
- **1** = Cliente SÍ abandonará el servicio

---

### 3.6 Wine Quality (Clasificación Multiclase) ⭐

**Endpoint:** `POST /predictions/wine_quality`

```json
{
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
}
```

**Interpretación:** Calidad del vino en escala de 3 a 9:
- **3-4:** Calidad baja
- **5-6:** Calidad media
- **7-9:** Calidad alta

---

### 3.7 Stroke Risk (Clasificación Binaria)

**Endpoint:** `POST /predictions/stroke_risk`

```json
{
  "features": {
    "age": 67.0,
    "hypertension": 0,
    "heart_disease": 1,
    "avg_glucose_level": 228.69,
    "bmi": 36.6,
    "gender": "Male",
    "ever_married": "Yes",
    "work_type": "Private",
    "residence_type": "Urban",
    "smoking_status": "formerly smoked"
  }
}
```

**Interpretación:**
- **0** = Sin riesgo de derrame
- **1** = Con riesgo de derrame

---

### 3.8 Hepatitis C (Clasificación Multiclase)

**Endpoint:** `POST /predictions/hepatitis_c`

```json
{
  "features": {
    "age": 32,
    "alb": 38.5,
    "alp": 52.5,
    "alt": 7.7,
    "ast": 22.1,
    "bil": 7.5,
    "che": 6.93,
    "chol": 3.23,
    "crea": 106.0,
    "ggt": 12.1,
    "prot": 69.0,
    "sex": "m"
  }
}
```

**Interpretación:**
- **0:** Blood Donor (donante de sangre)
- **1:** Hepatitis
- **2:** Fibrosis
- **3:** Cirrosis

---

### 3.9 Cirrhosis Status (Clasificación Multiclase)

**Endpoint:** `POST /predictions/cirrhosis_status`

```json
{
  "features": {
    "n_days": 400,
    "age": 21464,
    "bilirubin": 14.5,
    "cholesterol": 261.0,
    "albumin": 2.6,
    "copper": 156.0,
    "alk_phos": 1718.0,
    "sgot": 137.95,
    "tryglicerides": 172.0,
    "platelets": 190.0,
    "prothrombin": 12.2,
    "stage": 4.0,
    "drug": "D-penicillamine",
    "sex": "F",
    "ascites": "Y",
    "hepatomegaly": "Y",
    "spiders": "Y",
    "edema": "Y"
  }
}
```

**Interpretación:**
- **0:** C (Censored - censurado)
- **1:** CL (Censored due to liver transplant)
- **2:** D (Death - fallecimiento)

---

## 4. Interpretación de Resultados

### Estructura de Respuesta Exitosa:

```json
{
  "dataset": "nombre_del_modelo",
  "prediction": <valor_predicho>,
  "confidence": <confianza_0_a_1>,
  "model_type": "regression|classification"
}
```

### Campos Explicados:

- **dataset:** Nombre del modelo usado
- **prediction:** Valor predicho (número o clase)
- **confidence:** Confianza del modelo (0.0 a 1.0)
  - `0.0 - 0.5`: Baja confianza
  - `0.5 - 0.8`: Confianza moderada
  - `0.8 - 1.0`: Alta confianza
- **model_type:** Tipo de predicción

### Códigos de Estado HTTP:

- **200 OK:** Predicción exitosa
- **400 Bad Request:** Datos inválidos
- **422 Unprocessable Entity:** Columnas faltantes o nombres incorrectos
- **500 Internal Server Error:** Error en el servidor (reportar bug)

---

## 5. Troubleshooting

### ❌ Error 422: "Invalid input features"

**Causa:** Columnas faltantes o nombres incorrectos.

**Solución:**
1. Verifica que TODAS las columnas estén presentes
2. Asegúrate de usar `snake_case` en los nombres
3. Compara con los ejemplos de esta guía

**Ejemplo de error común:**
```json
// ❌ INCORRECTO
{
  "features": {
    "pH": 3.0,  // Debe ser "p_h"
    "SeniorCitizen": 0  // Debe ser "senior_citizen"
  }
}

// ✅ CORRECTO
{
  "features": {
    "p_h": 3.0,
    "senior_citizen": 0
  }
}
```

---

### ❌ Error 500: "Unable to serialize"

**Causa:** Error de serialización en el modelo (bug del servidor).

**Estado:** ✅ RESUELTO - Se agregó conversión automática de tipos numpy.

**Si persiste:**
1. Reportar en GitHub Issues
2. Incluir el JSON completo usado
3. Copiar el mensaje de error completo

---

### ❌ Error 404: "Not Found"

**Causa:** Endpoint incorrecto.

**Solución:**
- Verifica que el `dataset_key` sea uno de estos:
  - `bitcoin_price`
  - `avocado_prices`
  - `body_fat`
  - `car_prices`
  - `telco_churn`
  - `wine_quality`
  - `stroke_risk`
  - `hepatitis_c`
  - `cirrhosis_status`

---

### 🔍 Debugging Avanzado

Si encuentras errores, revisa el terminal donde corre la API. Los logs muestran:

```
🔍 Predicción para: wine_quality
📥 Features recibidas: {...}
📊 Tipo de features: <class 'dict'>
📊 Keys: ['fixed_acidity', 'volatile_acidity', ...]
✅ Predicción exitosa: 5 (confianza: 0.47661808811197665)
```

---

## 📝 Checklist de Prueba Completa

Usa esta lista para verificar que todos los modelos funcionan:

- [ ] ✅ Bitcoin Price
- [ ] ✅ Avocado Prices
- [ ] ✅ Body Fat
- [ ] ✅ Car Prices
- [ ] ✅ Telco Churn
- [ ] ✅ Wine Quality
- [ ] ✅ Stroke Risk
- [ ] ✅ Hepatitis C
- [ ] ✅ Cirrhosis Status

---

## 🎯 Prueba Rápida (Quick Test)

Copia este script Python para probar todos los modelos automáticamente:

```python
import requests
import json

API_URL = "http://localhost:8000"

# Ejemplo de wine_quality (el más simple)
def quick_test():
    url = f"{API_URL}/predictions/wine_quality"
    data = {
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
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API funcionando correctamente!")
            print(f"   Calidad del vino: {result['prediction']}")
            print(f"   Confianza: {result['confidence']:.2%}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    quick_test()
```

---

## 🔗 Enlaces Útiles

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc (Documentación alternativa):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 📚 Recursos Adicionales

- **Ejemplos Completos:** Ver `EJEMPLOS_COMPLETOS_PREDICCION.md`
- **Guía de Testing Completa:** Ver `TESTING_GUIDE.md`
- **Repositorio GitHub:** https://github.com/MaikelHR/Proyecto1IA-Jarvis

---

**Última validación:** 13 de octubre de 2025  
**Estado:** ✅ Todos los modelos validados en Swagger UI  
**Versión API:** 1.0.0

---

## 💡 Tips Pro

1. **Usa "Execute" múltiples veces** para ver la consistencia de las predicciones
2. **Modifica valores gradualmente** para entender cómo afectan la predicción
3. **Guarda los JSON que funcionan** como templates para futuras pruebas
4. **Compara confianza** entre diferentes inputs del mismo modelo
5. **Usa Ctrl+F** en Swagger para buscar endpoints rápidamente

---

¡Listo! Ahora puedes probar todos los 9 modelos de Jarvis IA con confianza. 🚀
