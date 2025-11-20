# 🚀 Guía Paso a Paso: Publicar en GitHub Pages

## ✅ Sí, cualquiera podrá ver el mapa una vez publicado

GitHub Pages es perfecto para tu proyecto. Aquí está la guía completa:

---

## 📋 Paso 1: Crear Repositorio en GitHub

1. **Ve a GitHub:**
   - Abre: https://github.com/new
   - Si no tienes cuenta, créala gratis en: https://github.com/signup

2. **Crea el repositorio:**
   - **Repository name:** `sri-ruc-mapa` (o el nombre que prefieras)
   - **Description:** "Mapa interactivo de establecimientos SRI" (opcional)
   - **Visibilidad:** ✅ **Marca "Public"** (necesario para GitHub Pages gratis)
   - **NO marques:**
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
   - Haz clic en **"Create repository"**

---

## 📤 Paso 2: Subir el Archivo a GitHub

### Opción A: Usar el Script Automático (Recomendado)

```bash
./publicar_github.sh
```

El script te guiará paso a paso.

### Opción B: Manual

```bash
# 1. Inicializar Git (si no lo has hecho)
git init

# 2. Agregar archivos (el .gitignore ya protege tu API key)
git add mapa_google_maps_filtrado.html .gitignore

# 3. Crear commit
git commit -m "Publicar mapa interactivo de establecimientos SRI"

# 4. Conectar con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/sri-ruc-mapa.git

# 5. Subir
git branch -M main
git push -u origin main
```

**Nota:** Si te pide usuario y contraseña:
- Usuario: Tu usuario de GitHub
- Contraseña: Usa un **Personal Access Token** (no tu contraseña)
  - Crea uno en: https://github.com/settings/tokens
  - Permisos: `repo`

---

## 🌐 Paso 3: Activar GitHub Pages

1. **Ve a tu repositorio en GitHub:**
   - Abre: `https://github.com/TU_USUARIO/sri-ruc-mapa`

2. **Ve a Settings:**
   - Haz clic en **"Settings"** (en el menú superior del repositorio)

3. **Activa Pages:**
   - En el menú lateral izquierdo, haz clic en **"Pages"**
   - En **"Source"**, selecciona:
     - **Branch:** `main`
     - **Folder:** `/ (root)`
   - Haz clic en **"Save"**

4. **Espera unos minutos:**
   - GitHub procesará tu sitio (puede tomar 1-2 minutos)
   - Verás un mensaje verde cuando esté listo

---

## 🔗 Paso 4: Tu URL Pública

Tu mapa estará disponible en:

```
https://TU_USUARIO.github.io/sri-ruc-mapa/mapa_google_maps_filtrado.html
```

**Ejemplo:**
- Si tu usuario es `danilo123`
- Tu URL será: `https://danilo123.github.io/sri-ruc-mapa/mapa_google_maps_filtrado.html`

---

## 🔒 Paso 5: Proteger tu API Key (OBLIGATORIO)

⚠️ **IMPORTANTE:** Tu API key está en el HTML. Debes restringirla por dominio.

### Restringir API Key en Google Cloud:

1. **Ve a Google Cloud Console:**
   - https://console.cloud.google.com/
   - Selecciona tu proyecto

2. **Ve a Credentials:**
   - En el menú lateral: **APIs & Services** → **Credentials**
   - Haz clic en tu **API key**

3. **Configurar restricciones:**
   
   **a) Application restrictions:**
   - Selecciona **"HTTP referrers (web sites)"**
   - Haz clic en **"ADD AN ITEM"**
   - Agrega:
     ```
     https://*.github.io/*
     http://localhost:*
     ```
   - Guarda
   
   **b) API restrictions:**
   - Selecciona **"Restrict key"**
   - Marca solo:
     - ✅ Maps JavaScript API
     - ✅ Geocoding API
   - Guarda

4. **Verificar:**
   - El mapa debe funcionar en tu URL de GitHub
   - El mapa NO debe funcionar en otros sitios (protección activa)

---

## ✅ Verificar que Funciona

1. Abre tu URL en el navegador:
   ```
   https://TU_USUARIO.github.io/sri-ruc-mapa/mapa_google_maps_filtrado.html
   ```

2. Deberías ver:
   - ✅ El mapa cargado
   - ✅ Los marcadores visibles
   - ✅ Los controles de filtro funcionando

3. Comparte la URL con quien quieras:
   - ✅ Cualquiera puede ver el mapa
   - ✅ No necesitan cuenta de GitHub
   - ✅ Funciona en cualquier dispositivo

---

## 🔄 Actualizar el Mapa

Si generas un nuevo mapa:

```bash
# 1. Regenerar el mapa
python3 generar_mapa_filtrado.py

# 2. Subir cambios
git add mapa_google_maps_filtrado.html
git commit -m "Actualizar mapa con nuevos datos"
git push

# 3. GitHub Pages se actualiza automáticamente (1-2 minutos)
```

---

## 🎨 Personalizar la URL

Puedes cambiar el nombre del repositorio:

1. Ve a Settings → General
2. Cambia el nombre del repositorio
3. Tu nueva URL será: `https://TU_USUARIO.github.io/NUEVO_NOMBRE/mapa_google_maps_filtrado.html`

---

## ❓ Problemas Comunes

### El mapa no carga
- ✅ Verifica que el API key esté restringido correctamente
- ✅ Verifica que las APIs estén habilitadas (Maps JavaScript API, Geocoding API)
- ✅ Revisa la consola del navegador (F12) para ver errores

### Error 404
- ✅ Verifica que el archivo se llamó `mapa_google_maps_filtrado.html`
- ✅ Verifica que GitHub Pages esté activado
- ✅ Espera 1-2 minutos después de activar Pages

### No puedo hacer push
- ✅ Verifica que tengas permisos en el repositorio
- ✅ Usa un Personal Access Token en lugar de contraseña
- ✅ Verifica que el repositorio sea público

---

## 📊 Ventajas de GitHub Pages

✅ **Gratis** - Sin costo  
✅ **URL permanente** - No expira  
✅ **HTTPS incluido** - Seguro  
✅ **Fácil de actualizar** - Solo hacer push  
✅ **Profesional** - Bueno para proyectos académicos  
✅ **Compartible** - Cualquiera puede ver el mapa  

---

## 🎯 Resumen Rápido

1. ✅ Crea repositorio público en GitHub
2. ✅ Sube `mapa_google_maps_filtrado.html`
3. ✅ Activa GitHub Pages en Settings
4. ✅ Restringe tu API key por dominio
5. ✅ Comparte tu URL: `https://TU_USUARIO.github.io/sri-ruc-mapa/mapa_google_maps_filtrado.html`

---

¿Necesitas ayuda? Ejecuta `./publicar_github.sh` y te guiará paso a paso.

