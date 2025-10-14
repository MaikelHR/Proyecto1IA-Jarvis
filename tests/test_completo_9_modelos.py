"""
Script de prueba completa para los 9 modelos de Jarvis IA API.
Prueba cada modelo con datos reales y genera un reporte detallado.
"""
import requests
import json
from datetime import datetime
from typing import Dict, Any, Tuple

# Configuración
API_URL = "http://localhost:8000"
TIMEOUT = 30  # segundos

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Imprime un encabezado formateado."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

def print_section(text: str):
    """Imprime una sección."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}📊 {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.END}")

def test_model(dataset_key: str, features: Dict[str, Any], description: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Prueba un modelo específico y retorna el resultado.
    
    Returns:
        Tuple[bool, Dict]: (success, response_data)
    """
    url = f"{API_URL}/predictions/{dataset_key}"
    
    try:
        print(f"\n{Colors.YELLOW}🔄 Probando: {Colors.BOLD}{dataset_key}{Colors.END}")
        print(f"   {description}")
        
        response = requests.post(
            url,
            json={"features": features},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"{Colors.GREEN}✅ ÉXITO{Colors.END}")
            print(f"   Predicción: {Colors.BOLD}{result.get('prediction', 'N/A')}{Colors.END}")
            
            # Formatear confianza solo si existe
            confidence = result.get('confidence')
            if confidence is not None:
                print(f"   Confianza: {Colors.BOLD}{confidence:.2%}{Colors.END}")
            else:
                print(f"   Confianza: {Colors.BOLD}N/A{Colors.END}")
            
            print(f"   Tipo: {result.get('model_type', 'N/A')}")
            return True, result
        else:
            print(f"{Colors.RED}❌ ERROR {response.status_code}{Colors.END}")
            print(f"   {response.text}")
            return False, {"error": response.text, "status_code": response.status_code}
            
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}❌ TIMEOUT - El servidor tardó más de {TIMEOUT}s en responder{Colors.END}")
        return False, {"error": "Timeout"}
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ ERROR DE CONEXIÓN - ¿Está corriendo la API en {API_URL}?{Colors.END}")
        return False, {"error": "Connection error"}
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR INESPERADO: {e}{Colors.END}")
        return False, {"error": str(e)}

def check_api_health() -> bool:
    """Verifica que la API esté funcionando."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"{Colors.GREEN}✅ API funcionando correctamente{Colors.END}")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Modelos cargados: {data.get('models_loaded', 0)}")
            print(f"   Azure Face configurado: {data.get('azure_face_configured', False)}")
            return True
        else:
            print(f"{Colors.RED}❌ API respondió con código {response.status_code}{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ No se pudo conectar a la API: {e}{Colors.END}")
        print(f"{Colors.YELLOW}💡 Asegúrate de que la API esté corriendo: python start_api.py{Colors.END}")
        return False

def main():
    """Función principal que ejecuta todas las pruebas."""
    print_header("🤖 JARVIS IA - PRUEBA COMPLETA DE LOS 9 MODELOS")
    
    # Verificar que la API esté funcionando
    print_section("1. Verificación de la API")
    if not check_api_health():
        print(f"\n{Colors.RED}❌ La API no está disponible. Abortando pruebas.{Colors.END}")
        return
    
    # Definir pruebas para cada modelo
    tests = [
        {
            "dataset_key": "bitcoin_price",
            "description": "Predicción del precio histórico de Bitcoin",
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
        {
            "dataset_key": "avocado_prices",
            "description": "Predicción de precios de aguacate por región",
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
        {
            "dataset_key": "body_fat",
            "description": "Predicción del porcentaje de grasa corporal",
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
        {
            "dataset_key": "car_prices",
            "description": "Predicción del valor de automóviles usados",
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
        {
            "dataset_key": "telco_churn",
            "description": "Predicción de churn de clientes de telecomunicaciones",
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
        {
            "dataset_key": "wine_quality",
            "description": "Predicción de la calidad de vinos",
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
        {
            "dataset_key": "stroke_risk",
            "description": "Predicción del riesgo de derrame cerebral",
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
        {
            "dataset_key": "hepatitis_c",
            "description": "Diagnóstico de hepatitis C",
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
        {
            "dataset_key": "cirrhosis_status",
            "description": "Predicción del estatus clínico de cirrosis",
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
    ]
    
    # Ejecutar pruebas
    print_section("2. Probando los 9 modelos")
    
    results = []
    for i, test in enumerate(tests, 1):
        print(f"\n{Colors.BOLD}[{i}/9]{Colors.END}")
        success, data = test_model(
            test["dataset_key"],
            test["features"],
            test["description"]
        )
        results.append({
            "model": test["dataset_key"],
            "success": success,
            "data": data
        })
    
    # Generar reporte final
    print_section("3. Reporte Final")
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print(f"\n{Colors.BOLD}Resumen:{Colors.END}")
    print(f"  {Colors.GREEN}✅ Exitosas: {successful}/9{Colors.END}")
    print(f"  {Colors.RED}❌ Fallidas: {failed}/9{Colors.END}")
    print(f"  {Colors.CYAN}📊 Tasa de éxito: {(successful/9)*100:.1f}%{Colors.END}")
    
    if failed > 0:
        print(f"\n{Colors.YELLOW}⚠️  Modelos con errores:{Colors.END}")
        for result in results:
            if not result["success"]:
                print(f"  - {result['model']}: {result['data'].get('error', 'Unknown error')}")
    
    # Guardar reporte en JSON
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(results),
        "successful": successful,
        "failed": failed,
        "success_rate": (successful/9)*100,
        "results": results
    }
    
    report_file = "test_report_9_modelos.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Colors.CYAN}📄 Reporte guardado en: {report_file}{Colors.END}")
    
    # Resultado final
    print_header("✅ PRUEBA COMPLETA FINALIZADA" if successful == 9 else "⚠️ PRUEBA COMPLETA FINALIZADA CON ERRORES")
    
    return successful == 9

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
