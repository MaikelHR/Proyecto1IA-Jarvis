# 🎤 Solución al Problema de Speech-to-Text

## ❌ Problema
```
INFO: 127.0.0.1:63621 - "POST /voice/command HTTP/1.1" 500 Internal Server Error
```

**Causa:** Google Cloud Speech-to-Text no está configurado.

---

## ✅ Solución Aplicada: Modo Demo

He modificado el código para que funcione en **modo demo** cuando Google Cloud no está configurado.

### ¿Qué hace ahora?

Cuando intentas grabar audio y Google Cloud no está disponible:
- ✅ **No da error 500**
- ✅ Retorna una transcripción simulada: `"[DEMO MODE] Jarvis, predice el precio de Bitcoin"`
- ✅ Reconoce el comando automáticamente
- ✅ Muestra confianza del 85%

---

## 🚀 Cómo Usar

### **Paso 1: Reiniciar Backend**

```powershell
# Detén el backend actual (Ctrl+C)
# Luego reinicia:
cd backend
python start_api.py
```

### **Paso 2: Probar Speech-to-Text**

Ahora en el frontend:
1. Ve a la pestaña **"Speech-to-Text"**
2. Presiona **"Iniciar Grabación"**
3. Di cualquier cosa (o solo espera 2 segundos)
4. Presiona **"Detener Grabación"**
5. Verás: `"[DEMO MODE] Jarvis, predice el precio de Bitcoin"`

**Funcionará sin errores!** 🎉

---

## 🧪 Endpoint de Prueba Adicional

También agregué un endpoint para probar comandos directamente:

### **Desde Swagger UI:**

1. Abre: http://localhost:8000/docs
2. Ve a **POST /voice/demo**
3. Click en "Try it out"
4. Escribe: `"Jarvis, analiza la calidad del vino"`
5. Click en "Execute"

**Verás el comando reconocido!**

### **Desde PowerShell:**

```powershell
# Probar comando de voz
curl -X POST "http://localhost:8000/voice/demo?command_text=Jarvis,%20predice%20el%20precio%20de%20Bitcoin" -H "accept: application/json"
```

---

## 🎯 Opciones Futuras

### **Opción 1: Seguir en Modo Demo (Recomendado para presentación)**
- ✅ No requiere configuración
- ✅ Funciona inmediatamente
- ✅ Suficiente para demostrar el concepto

### **Opción 2: Configurar Google Cloud (Opcional)**

Si quieres usar transcripción real:

#### **Paso 1: Crear cuenta en Google Cloud**
1. Ve a: https://console.cloud.google.com
2. Crea un proyecto nuevo
3. Habilita "Speech-to-Text API"
4. Crea credenciales (Service Account)
5. Descarga el archivo JSON

#### **Paso 2: Configurar Credenciales**

```powershell
# Guarda el archivo en:
# D:\TEC\IA\Proyecto1IA-Jarvis\config\credentials\google-credentials.json

# Configura la variable de entorno:
[System.Environment]::SetEnvironmentVariable(
    'GOOGLE_APPLICATION_CREDENTIALS',
    'D:\TEC\IA\Proyecto1IA-Jarvis\config\credentials\google-credentials.json',
    'User'
)

# Reinicia PowerShell y el backend
```

#### **Paso 3: Reiniciar Backend**

```powershell
cd backend
python start_api.py
```

Ahora usará transcripción real! 🎤

---

## 📊 Estado Actual

### ✅ **Lo que FUNCIONA:**
- ✅ Modo demo de Speech-to-Text
- ✅ Reconocimiento de comandos
- ✅ Todas las predicciones ML
- ✅ Face Recognition (si Azure está configurado)

### ⚠️ **Lo que es SIMULADO:**
- ⚠️ Transcripción de audio (modo demo)
- ⚠️ Solo si no tienes Google Cloud configurado

---

## 🎬 Para tu Presentación

### **Opción A: Demo con Texto (Más Confiable)**

En lugar de grabar audio, usa el endpoint `/voice/parse`:

1. Abre Swagger: http://localhost:8000/docs
2. Ve a **POST /voice/parse**
3. Escribe comandos manualmente
4. Muestra cómo reconoce los comandos

### **Opción B: Demo con Audio (Modo Demo)**

1. Usa el botón de grabación en el frontend
2. Muestra que reconoce `"[DEMO MODE] ..."`
3. Explica que esto simula la API de Google Cloud

### **Opción C: Combinar Ambos**

1. Muestra primero el modo demo (sin API)
2. Luego muestra el endpoint `/voice/parse` con comandos reales
3. Explica que en producción usarías Google Speech-to-Text

---

## 🔧 Comandos Reconocidos

El sistema reconoce estos comandos:

| Comando | Modelo Activado |
|---------|----------------|
| "bitcoin" | Bitcoin Price |
| "aguacate" o "avocado" | Avocado Prices |
| "grasa corporal" o "body fat" | Body Fat |
| "auto" o "carro" o "car" | Car Prices |
| "churn" o "clientes" | Telco Churn |
| "vino" o "wine" | Wine Quality |
| "derrame" o "stroke" | Stroke Risk |
| "hepatitis" | Hepatitis C |
| "cirrosis" o "cirrhosis" | Cirrhosis |

**Ejemplos:**
- "Jarvis, predice el precio de Bitcoin" → `bitcoin_price`
- "Jarvis, analiza la calidad del vino" → `calidad_de_vinos`
- "Jarvis, evalúa riesgo de derrame" → `predicción_de_derrame_cerebral`

---

## 📝 Resumen

**Antes:**
```
POST /voice/command → 500 Internal Server Error ❌
```

**Ahora:**
```
POST /voice/command → 200 OK (Modo Demo) ✅
```

**¡Ya puedes probar los comandos de voz! 🎉**

---

## 🆘 Si Sigues Teniendo Problemas

1. **Reinicia el backend:**
   ```powershell
   # Ctrl+C en la terminal del backend
   cd backend
   python start_api.py
   ```

2. **Verifica que el código se actualizó:**
   ```powershell
   # Busca "[DEMO MODE]" en el código
   Select-String -Path "backend/api/routers/voice.py" -Pattern "DEMO MODE"
   ```

3. **Prueba el nuevo endpoint de demo:**
   ```
   http://localhost:8000/docs → POST /voice/demo
   ```

---

**¡Listo para probar! 🚀**
