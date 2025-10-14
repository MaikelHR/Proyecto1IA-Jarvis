"""
Genera ejemplos completos y realistas para todos los 9 modelos
basados en datos reales de los CSVs.
"""
import json

# Ejemplos completos basados en los datos reales de los CSVs
ejemplos_completos = {
    "bitcoin_price": {
        "description": "Predicción del precio histórico de Bitcoin",
        "endpoint": "/predictions/bitcoin_price",
        "columns": ["open", "high", "low", "volume", "market_cap", "lag_1", "lag_7", "rolling_mean_7"],
        "example": {
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
        },
        "expected_output": "Precio predicho (float) y confianza del modelo"
    },
    
    "avocado_prices": {
        "description": "Predicción de precios de aguacate por región",
        "endpoint": "/predictions/avocado_prices",
        "columns": ["total_volume", "col_4046", "col_4225", "col_4770", "total_bags", 
                   "small_bags", "large_bags", "xlarge_bags", "year", "date", "type", "region"],
        "example": {
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
        },
        "expected_output": "Precio promedio predicho (float) y confianza del modelo"
    },
    
    "body_fat": {
        "description": "Predicción del porcentaje de grasa corporal",
        "endpoint": "/predictions/body_fat",
        "columns": ["density", "age", "weight", "height", "neck", "chest", "abdomen", 
                   "hip", "thigh", "knee", "ankle", "biceps", "forearm", "wrist"],
        "example": {
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
        },
        "expected_output": "Porcentaje de grasa corporal predicho (float) y confianza del modelo"
    },
    
    "car_prices": {
        "description": "Predicción del valor de automóviles usados",
        "endpoint": "/predictions/car_prices",
        "columns": ["year", "present_price", "kms_driven", "owner", "car_name", 
                   "fuel_type", "seller_type", "transmission"],
        "example": {
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
        },
        "expected_output": "Precio del automóvil predicho (float) y confianza del modelo"
    },
    
    "telco_churn": {
        "description": "Predicción de churn de clientes de telecomunicaciones",
        "endpoint": "/predictions/telco_churn",
        "columns": ["senior_citizen", "tenure", "monthly_charges", "total_charges", "customer_id",
                   "gender", "partner", "dependents", "phone_service", "multiple_lines",
                   "internet_service", "online_security", "online_backup", "device_protection",
                   "tech_support", "streaming_tv", "streaming_movies", "contract",
                   "paperless_billing", "payment_method"],
        "example": {
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
        },
        "expected_output": "Predicción de churn (0 = No, 1 = Yes) y probabilidad"
    },
    
    "wine_quality": {
        "description": "Predicción de la calidad de vinos",
        "endpoint": "/predictions/wine_quality",
        "columns": ["fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
                   "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
                   "p_h", "sulphates", "alcohol", "type"],
        "example": {
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
        },
        "expected_output": "Calidad del vino predicha (int de 3 a 9) y confianza del modelo"
    },
    
    "stroke_risk": {
        "description": "Predicción del riesgo de derrame cerebral",
        "endpoint": "/predictions/stroke_risk",
        "columns": ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi",
                   "gender", "ever_married", "work_type", "residence_type", "smoking_status"],
        "example": {
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
        },
        "expected_output": "Riesgo de derrame (0 = No, 1 = Sí) y probabilidad"
    },
    
    "hepatitis_c": {
        "description": "Diagnóstico de hepatitis C",
        "endpoint": "/predictions/hepatitis_c",
        "columns": ["age", "alb", "alp", "alt", "ast", "bil", "che", "chol",
                   "crea", "ggt", "prot", "sex"],
        "example": {
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
        },
        "expected_output": "Categoría diagnóstica (0=Blood Donor, 1=Hepatitis, 2=Fibrosis, 3=Cirrhosis) y confianza"
    },
    
    "cirrhosis_status": {
        "description": "Predicción del estatus clínico de cirrosis",
        "endpoint": "/predictions/cirrhosis_status",
        "columns": ["n_days", "age", "bilirubin", "cholesterol", "albumin", "copper",
                   "alk_phos", "sgot", "tryglicerides", "platelets", "prothrombin", "stage",
                   "drug", "sex", "ascites", "hepatomegaly", "spiders", "edema"],
        "example": {
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
        },
        "expected_output": "Estatus clínico (C=Censored, CL=Censored due to liver tx, D=Death) y probabilidad"
    }
}

# Guardar los ejemplos completos
output_file = 'ejemplos_prediccion_completos.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(ejemplos_completos, f, indent=2, ensure_ascii=False)

print("=" * 80)
print("✅ EJEMPLOS COMPLETOS GENERADOS")
print("=" * 80)
print(f"\n📄 Archivo generado: {output_file}")
print(f"📊 Total de modelos: {len(ejemplos_completos)}")
print("\n📋 Modelos incluidos:")
for i, (key, info) in enumerate(ejemplos_completos.items(), 1):
    print(f"  {i}. {key}: {info['description']}")
    print(f"     Endpoint: {info['endpoint']}")
    print(f"     Columnas: {len(info['columns'])}")

print("\n" + "=" * 80)
print("✅ Los ejemplos están listos para actualizar la documentación")
print("=" * 80)
