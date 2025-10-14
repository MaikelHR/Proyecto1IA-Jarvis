# 📚 Ejemplos Completos de Predicción - Jarvis IA API

> **Última actualización:** 13 de octubre de 2025  
> **Estado:** ✅ Validado con los 9 modelos funcionando

Esta guía contiene ejemplos completos y validados para hacer predicciones con cada uno de los 9 modelos de Machine Learning disponibles en Jarvis IA API.

## ⚠️ IMPORTANTE: Convención de Nombres

**Todos los modelos esperan nombres de columnas en formato `snake_case`** debido al preprocesamiento automático de scikit-learn durante el entrenamiento:

- ✅ Correcto: `fixed_acidity`, `senior_citizen`, `p_h`
- ❌ Incorrecto: `fixedAcidity`, `SeniorCitizen`, `pH`

---

## 📊 Índice de Modelos

1. [Bitcoin Price](#1-bitcoin-price)
2. [Avocado Prices](#2-avocado-prices)
3. [Body Fat](#3-body-fat)
4. [Car Prices](#4-car-prices)
5. [Telco Churn](#5-telco-churn)
6. [Wine Quality](#6-wine-quality)
7. [Stroke Risk](#7-stroke-risk)
8. [Hepatitis C](#8-hepatitis-c)
9. [Cirrhosis Status](#9-cirrhosis-status)

---

## 1. Bitcoin Price

**Descripción:** Predicción del precio histórico de Bitcoin  
**Endpoint:** `POST /predictions/bitcoin_price`  
**Tipo de predicción:** Regresión (precio en USD)

### Columnas Requeridas (8):
```json
["open", "high", "low", "volume", "market_cap", "lag_1", "lag_7", "rolling_mean_7"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "bitcoin_price",
  "prediction": 2875.34,
  "confidence": 0.89,
  "model_type": "regression"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/bitcoin_price" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 2. Avocado Prices

**Descripción:** Predicción de precios de aguacate por región  
**Endpoint:** `POST /predictions/avocado_prices`  
**Tipo de predicción:** Regresión (precio promedio en USD)

### Columnas Requeridas (12):
```json
["total_volume", "col_4046", "col_4225", "col_4770", "total_bags", 
 "small_bags", "large_bags", "xlarge_bags", "year", "date", "type", "region"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "avocado_prices",
  "prediction": 1.33,
  "confidence": 0.82,
  "model_type": "regression"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/avocado_prices" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 3. Body Fat

**Descripción:** Predicción del porcentaje de grasa corporal  
**Endpoint:** `POST /predictions/body_fat`  
**Tipo de predicción:** Regresión (porcentaje de grasa corporal)

### Columnas Requeridas (14):
```json
["density", "age", "weight", "height", "neck", "chest", "abdomen", 
 "hip", "thigh", "knee", "ankle", "biceps", "forearm", "wrist"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "body_fat",
  "prediction": 12.3,
  "confidence": 0.99,
  "model_type": "regression"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/body_fat" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 4. Car Prices

**Descripción:** Predicción del valor de automóviles usados  
**Endpoint:** `POST /predictions/car_prices`  
**Tipo de predicción:** Regresión (precio en lakhs - unidad india)

### Columnas Requeridas (8):
```json
["year", "present_price", "kms_driven", "owner", "car_name", 
 "fuel_type", "seller_type", "transmission"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "car_prices",
  "prediction": 3.95,
  "confidence": 0.96,
  "model_type": "regression"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/car_prices" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 5. Telco Churn

**Descripción:** Predicción de churn de clientes de telecomunicaciones  
**Endpoint:** `POST /predictions/telco_churn`  
**Tipo de predicción:** Clasificación binaria (0 = No churn, 1 = Churn)

### Columnas Requeridas (20):
```json
["senior_citizen", "tenure", "monthly_charges", "total_charges", "customer_id",
 "gender", "partner", "dependents", "phone_service", "multiple_lines",
 "internet_service", "online_security", "online_backup", "device_protection",
 "tech_support", "streaming_tv", "streaming_movies", "contract",
 "paperless_billing", "payment_method"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "telco_churn",
  "prediction": 0,
  "confidence": 0.76,
  "model_type": "classification",
  "interpretation": "Cliente NO abandonará el servicio"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/telco_churn" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 6. Wine Quality

**Descripción:** Predicción de la calidad de vinos  
**Endpoint:** `POST /predictions/wine_quality`  
**Tipo de predicción:** Clasificación multiclase (calidad de 3 a 9)

### Columnas Requeridas (12):
```json
["fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
 "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
 "p_h", "sulphates", "alcohol", "type"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "wine_quality",
  "prediction": 5,
  "confidence": 0.48,
  "model_type": "classification",
  "interpretation": "Calidad media (escala 3-9)"
}
```

### cURL:
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

---

## 7. Stroke Risk

**Descripción:** Predicción del riesgo de derrame cerebral  
**Endpoint:** `POST /predictions/stroke_risk`  
**Tipo de predicción:** Clasificación binaria (0 = Sin riesgo, 1 = Con riesgo)

### Columnas Requeridas (10):
```json
["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi",
 "gender", "ever_married", "work_type", "residence_type", "smoking_status"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "stroke_risk",
  "prediction": 1,
  "confidence": 0.73,
  "model_type": "classification",
  "interpretation": "Alto riesgo de derrame cerebral"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/stroke_risk" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 8. Hepatitis C

**Descripción:** Diagnóstico de hepatitis C  
**Endpoint:** `POST /predictions/hepatitis_c`  
**Tipo de predicción:** Clasificación multiclase

### Columnas Requeridas (12):
```json
["age", "alb", "alp", "alt", "ast", "bil", "che", "chol",
 "crea", "ggt", "prot", "sex"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "hepatitis_c",
  "prediction": 0,
  "confidence": 0.91,
  "model_type": "classification",
  "interpretation": "Categoría: Blood Donor (0=Donante, 1=Hepatitis, 2=Fibrosis, 3=Cirrosis)"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/hepatitis_c" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 9. Cirrhosis Status

**Descripción:** Predicción del estatus clínico de cirrosis  
**Endpoint:** `POST /predictions/cirrhosis_status`  
**Tipo de predicción:** Clasificación multiclase

### Columnas Requeridas (18):
```json
["n_days", "age", "bilirubin", "cholesterol", "albumin", "copper",
 "alk_phos", "sgot", "tryglicerides", "platelets", "prothrombin", "stage",
 "drug", "sex", "ascites", "hepatomegaly", "spiders", "edema"]
```

### Ejemplo de Request:
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

### Ejemplo de Response:
```json
{
  "dataset": "cirrhosis_status",
  "prediction": 2,
  "confidence": 0.68,
  "model_type": "classification",
  "interpretation": "Estatus: D (0=C: Censored, 1=CL: Censored due to liver tx, 2=D: Death)"
}
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predictions/cirrhosis_status" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 🧪 Testing con Python

```python
import requests
import json

# Configuración
API_URL = "http://localhost:8000"

# Ejemplo: Wine Quality
def test_wine_quality():
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
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Predicción: {result['prediction']}")
        print(f"📊 Confianza: {result['confidence']:.2%}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_wine_quality()
```

---

## 📝 Notas Importantes

### Tipos de Datos
- **Numéricos:** int, float (según columna)
- **Categóricos:** string (valores específicos del dataset)
- **Booleanos:** 0/1 o "Yes"/"No" según dataset

### Validaciones
- Todas las columnas son obligatorias
- Los nombres deben estar en `snake_case`
- Los valores categóricos deben coincidir con los del entrenamiento
- Los valores numéricos deben estar en rangos razonables

### Errores Comunes
1. **422 Unprocessable Entity:** Columnas faltantes o nombres incorrectos
2. **400 Bad Request:** Valores fuera de rango o tipo incorrecto
3. **500 Internal Server Error:** Error en el modelo (reportar bug)

---

## 🔗 Enlaces Útiles

- **API Docs (Swagger):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Repositorio:** https://github.com/MaikelHR/Proyecto1IA-Jarvis

---

**Última validación:** 13 de octubre de 2025  
**Estado:** ✅ Todos los modelos operativos  
**Versión API:** 1.0.0
