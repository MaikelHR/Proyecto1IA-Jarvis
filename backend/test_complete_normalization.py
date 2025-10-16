import re

def to_snake_case(text):
    """Convert PascalCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def normalize_key(key):
    """Nueva lógica de normalización"""
    if key == "pH":
        return "p_h"
    elif key.startswith("4"):
        return f"col_{key}"
    elif ' ' in key:
        # Simple case: "Market Cap" -> "market_cap"
        return key.lower().replace(' ', '_')
    else:
        # PascalCase: "PaperlessBilling" -> "paperless_billing"
        return to_snake_case(key)

# Pruebas completas
print("=" * 70)
print("PRUEBA COMPLETA DE NORMALIZACIÓN")
print("=" * 70)

test_cases = [
    # Bitcoin (con espacios)
    ("Open", "open"),
    ("High", "high"),
    ("Low", "low"),
    ("Volume", "volume"),
    ("Market Cap", "market_cap"),  # ¡CRÍTICO!
    
    # Telco (PascalCase)
    ("gender", "gender"),
    ("SeniorCitizen", "senior_citizen"),
    ("PaperlessBilling", "paperless_billing"),
    ("MonthlyCharges", "monthly_charges"),
    ("PhoneService", "phone_service"),
    
    # Wine (casos especiales)
    ("pH", "p_h"),
    ("fixed acidity", "fixed_acidity"),
    ("citric acid", "citric_acid"),
    
    # Avocado (números)
    ("4046", "col_4046"),
    ("4225", "col_4225"),
    ("Total Volume", "total_volume"),
]

errors = []
for input_key, expected in test_cases:
    result = normalize_key(input_key)
    status = "✅" if result == expected else "❌"
    print(f"{status} {input_key:20s} -> {result:25s} (esperado: {expected})")
    
    if result != expected:
        errors.append((input_key, expected, result))

print("\n" + "=" * 70)
if errors:
    print(f"❌ {len(errors)} ERRORES ENCONTRADOS:")
    for inp, exp, got in errors:
        print(f"   {inp}: esperado '{exp}', obtenido '{got}'")
else:
    print("✅ TODOS LOS TESTS PASARON")
print("=" * 70)
