# 🔍 DIAGNÓSTICO - Modelos No Se Cargan

## 🚨 Problema Actual

Los modelos no se muestran en la página web del frontend.

---

## 🧪 PRUEBAS A REALIZAR

### **Prueba 1: Página de Test (PRIMERO ESTO)**

He creado una página de diagnóstico. Ábrela en tu navegador:

```
http://localhost:8080/test-models.html
```

**Esta página:**
- ✅ Verifica la conexión con el backend
- ✅ Carga los modelos y los muestra
- ✅ Muestra todos los logs de la consola
- ✅ Te dirá exactamente qué está fallando

**Toma captura de pantalla de esta página y mándamela**

---

### **Prueba 2: Consola del Navegador**

1. Abre la página principal: `http://localhost:8080`
2. Presiona **F12** para abrir las herramientas de desarrollo
3. Ve a la pestaña **"Console"**
4. Presiona **Ctrl + F5** para recargar sin cache
5. Mira los mensajes que aparecen

**Deberías ver:**
```
🔄 Iniciando carga de modelos...
📡 API URL: http://localhost:8000/predictions/datasets
📥 Response status: 200
📥 Response ok: true
✅ Modelos recibidos: 9
📊 Datos de modelos: [...]
🔨 Creando elementos de modelo...
  1. Precio histórico de Bitcoin (bitcoin_price)
  2. Precios de aguacate por región (avocado_prices)
  ...
✅ Elementos de modelo creados: 9
🎯 Auto-seleccionando primer modelo: ...
```

**Si ves errores rojos, cópialos y mándamelos**

---

### **Prueba 3: Verificar Backend Directamente**

Abre una terminal PowerShell y ejecuta:

```powershell
# Test 1: Health check
curl http://localhost:8000/health

# Test 2: Ver modelos
curl http://localhost:8000/predictions/datasets

# Test 3: Ver keys de modelos
curl http://localhost:8000/predictions/datasets | ConvertFrom-Json | ForEach-Object { Write-Host "$($_.key) - $($_.name)" }
```

**Deberías ver 9 modelos listados**

---

### **Prueba 4: Limpiar Cache del Navegador**

El navegador puede tener la versión antigua cacheada:

#### **Opción A: Recarga Forzada**
```
Ctrl + Shift + R    (Chrome/Edge)
Ctrl + F5           (Todos los navegadores)
Shift + F5          (Firefox)
```

#### **Opción B: Limpiar Cache Completo**

**Chrome/Edge:**
1. F12 → Click derecho en el botón de recarga → "Empty Cache and Hard Reload"

**Firefox:**
1. Ctrl + Shift + Delete
2. Selecciona "Cache"
3. Click en "Limpiar ahora"

#### **Opción C: Modo Incógnito**
```
Ctrl + Shift + N    (Chrome/Edge)
Ctrl + Shift + P    (Firefox)
```

Luego abre: `http://localhost:8080` en la ventana incógnita

---

### **Prueba 5: Verificar que los Archivos Están Actualizados**

En PowerShell, desde la carpeta del proyecto:

```powershell
# Ver última modificación de app.js
Get-Item "frontend/app.js" | Select-Object Name, LastWriteTime

# Buscar "console.log" en app.js para confirmar que tiene los cambios
Select-String -Path "frontend/app.js" -Pattern "🔄 Iniciando carga de modelos"
```

**Deberías ver:**
```
frontend\app.js:94:    console.log('🔄 Iniciando carga de modelos...');
```

Si NO aparece, significa que el archivo no se actualizó.

---

## 🔧 SOLUCIONES PASO A PASO

### **Solución 1: Reiniciar Todo**

```powershell
# Terminal 1: Backend
# Presiona Ctrl+C para detener
cd backend
python start_api.py

# Terminal 2: Frontend
# Presiona Ctrl+C para detener
cd frontend
python -m http.server 8080

# Navegador: Recarga con Ctrl+Shift+R
```

---

### **Solución 2: Verificar Puerto Correcto**

Asegúrate de estar usando:
- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:8080

Si abres `http://localhost:8000` verás la API, NO el frontend.

---

### **Solución 3: Verificar CORS**

Si ves error de CORS en la consola:

```
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:8080' 
has been blocked by CORS policy
```

**Entonces necesitas verificar el backend:**

```powershell
# En backend/api/main.py debe tener esto:
Select-String -Path "backend/api/main.py" -Pattern "CORSMiddleware"
```

---

### **Solución 4: Usar Navegador Diferente**

Si usas Chrome, prueba en:
- Firefox
- Edge
- Opera

A veces un navegador tiene problemas de cache específicos.

---

## 📊 CHECKLIST DE VERIFICACIÓN

Marca lo que ya verificaste:

- [ ] Backend está corriendo en puerto 8000
- [ ] Frontend está corriendo en puerto 8080
- [ ] `curl http://localhost:8000/health` funciona
- [ ] `curl http://localhost:8000/predictions/datasets` muestra 9 modelos
- [ ] Abriste `http://localhost:8080/test-models.html`
- [ ] La página de test muestra los modelos
- [ ] Recargaste con Ctrl+Shift+R
- [ ] Abriste la consola del navegador (F12)
- [ ] Limpiaste el cache del navegador
- [ ] Probaste en modo incógnito
- [ ] Los archivos frontend/app.js tienen la última modificación
- [ ] Verificaste que el archivo tiene los console.log nuevos

---

## 🆘 ÚLTIMA OPCIÓN: REINICIO COMPLETO

Si nada funciona:

```powershell
# 1. Detener todo (Ctrl+C en ambas terminales)

# 2. Cerrar el navegador COMPLETAMENTE

# 3. Reiniciar Backend
cd D:\TEC\IA\Proyecto1IA-Jarvis\backend
python start_api.py

# 4. Reiniciar Frontend (en otra terminal)
cd D:\TEC\IA\Proyecto1IA-Jarvis\frontend
python -m http.server 8080

# 5. Abrir navegador en MODO INCÓGNITO
# Chrome: Ctrl+Shift+N
# Firefox: Ctrl+Shift+P

# 6. Ir a http://localhost:8080

# 7. Abrir consola (F12) ANTES de que cargue la página

# 8. Ver qué mensajes aparecen
```

---

## 📸 LO QUE NECESITO QUE ME MANDES

Para ayudarte mejor, necesito:

1. ✅ **Captura de pantalla** de `http://localhost:8080/test-models.html`
2. ✅ **Captura de pantalla** de la consola del navegador (F12)
3. ✅ **Output** de este comando:
   ```powershell
   curl http://localhost:8000/predictions/datasets
   ```
4. ✅ **Output** de este comando:
   ```powershell
   Select-String -Path "frontend/app.js" -Pattern "🔄"
   ```

---

## 🎯 SIGUIENTE PASO

**AHORA MISMO:**
1. Abre `http://localhost:8080/test-models.html`
2. Toma captura de pantalla
3. Dime qué ves

Eso me dirá exactamente qué está fallando.

---

**¡Vamos a resolverlo juntos! 🚀**
