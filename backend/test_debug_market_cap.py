import re

def to_snake_case(text):
    """Convert PascalCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Debuggeando Market_Cap
test = "Market_Cap"
print(f"Input: {test}")

s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', test)
print(f"After first regex: {s1}")  # Market__Cap (agrega _ antes de Cap)

s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
print(f"After second regex: {s2}")  # Market__Cap (ya tiene _)

final = s2.lower()
print(f"After lowercase: {final}")  # market__cap

print("\n" + "=" * 50)
print("Solución: Primero lowercase, LUEGO replace espacios")
print("=" * 50)

test2 = "Market Cap"
print(f"Input: {test2}")

# Nuevo enfoque: lowercase + replace spaces + to_snake_case
step1 = test2.lower()  # "market cap"
print(f"After lowercase: {step1}")

step2 = step1.replace(' ', '_')  # "market_cap"
print(f"After replace spaces: {step2}")

# Ya está en minúsculas, no necesita to_snake_case
print(f"Final: {step2}")
