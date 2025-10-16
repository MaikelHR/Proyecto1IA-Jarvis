import re

def to_snake_case(text):
    """Convert PascalCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Test con Market Cap
test_cases = [
    "Market Cap",
    "Open",
    "High", 
    "Low",
    "Volume"
]

print("Normalización INCORRECTA (orden antiguo):")
print("=" * 50)

for test in test_cases:
    # Orden incorrecto: to_snake_case primero, luego replace
    normalized_bad = to_snake_case(test).replace(' ', '_').lower()
    print(f"{test:15s} -> {normalized_bad}")

print("\n" + "=" * 50)
print("Normalización CORRECTA (orden nuevo):")
print("=" * 50)

for test in test_cases:
    # Orden correcto: replace primero, luego to_snake_case
    temp = test.replace(' ', '_')
    normalized_good = to_snake_case(temp).lower()
    print(f"{test:15s} -> {normalized_good}")
