import re

def to_snake_case(text):
    """Convert PascalCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def clean_numeric_value(value):
    """Clean numeric values with commas"""
    if isinstance(value, str):
        cleaned = value.replace(',', '')
        try:
            return float(cleaned)
        except ValueError:
            return value
    return value

# Test PascalCase conversion
print("=" * 60)
print("PRUEBA 1: Conversión PascalCase -> snake_case")
print("=" * 60)
telco_fields = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
    'PhoneService', 'MultipleLines', 'InternetService', 
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
    'TechSupport', 'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod', 
    'MonthlyCharges', 'TotalCharges'
]

for field in telco_fields:
    converted = to_snake_case(field)
    print(f"{field:20s} -> {converted}")

# Test numeric cleaning
print("\n" + "=" * 60)
print("PRUEBA 2: Limpieza de valores numéricos")
print("=" * 60)
numeric_tests = [
    "860,575,000",
    "45,535,800,000",
    "1,234.56",
    "Yes",
    "Male",
    2763.24
]

for test in numeric_tests:
    cleaned = clean_numeric_value(test)
    print(f"{str(test):20s} -> {cleaned} ({type(cleaned).__name__})")
