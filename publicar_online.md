# 🌐 Cómo Publicar tu Mapa en una URL Pública

Tienes varias opciones para compartir tu mapa en internet. El archivo a publicar es: **`mapa_google_maps_filtrado.html`**

---

## 🚀 Opción 1: Netlify (GRATIS - MÁS FÁCIL) ⭐ RECOMENDADO

### Pasos:

1. **Ve a Netlify:**
   - Abre: https://www.netlify.com/
   - Haz clic en "Sign up" (gratis)
   - Regístrate con GitHub, Google o email

2. **Arrastra y suelta:**
   - En la página principal de Netlify, verás un área que dice "Want to deploy a new site without connecting to Git? Drag and drop your site output folder here"
   - **Arrastra el archivo** `mapa_google_maps_filtrado.html` directamente
   - O crea una carpeta, pon el HTML ahí, y arrastra la carpeta

3. **¡Listo!**
   - Netlify te dará una URL automáticamente
   - Ejemplo: `https://random-name-12345.netlify.app/mapa_google_maps_filtrado.html`
   - Puedes cambiar el nombre en: Site settings → Change site name

- ✅ **Ventaja:** Súper fácil, URL automática, HTTPS incluido
- ✅ **Tiempo:** 2 minutos
- ✅ **URL personalizada:** Puedes configurar un dominio personalizado después

### Script Automático (Opcional):

```bash
# Si tienes Node.js instalado, puedes usar Netlify CLI
npm install -g netlify-cli
netlify deploy --prod --dir . --open
```

---

## 🌍 Opción 2: GitHub Pages (GRATIS - Buena para proyectos)

### Pasos:

1. **Crea un repositorio en GitHub:**
   - Ve a: https://github.com/new
   - Nombre: `sri-ruc-mapa` (o el que prefieras)
   - Marca "Public" (necesario para GitHub Pages gratis)
   - Haz clic en "Create repository"

2. **Sube tu archivo:**
   ```bash
   # Inicializar git (si no lo has hecho)
   git init
   
   # Agregar archivo (IMPORTANTE: NO agregues google_maps_api_key.txt)
   git add mapa_google_maps_filtrado.html
   git add .gitignore  # Para asegurar que el API key no se suba
   
   # Commit
   git commit -m "Agregar mapa interactivo de establecimientos"
   
   # Conectar con GitHub (reemplaza TU_USUARIO)
   git remote add origin https://github.com/TU_USUARIO/sri-ruc-mapa.git
   
   # Subir
   git branch -M main
   git push -u origin main
   ```

3. **Activar GitHub Pages:**
   - Ve a tu repositorio en GitHub
   - Settings → Pages (en el menú lateral)
   - Source: "Deploy from a branch"
   - Branch: `main` / `/ (root)`
   - Folder: `/ (root)`
   - Save

4. **Tu URL será:**
   ```
   https://TU_USUARIO.github.io/sri-ruc-mapa/mapa_google_maps_filtrado.html
   ```

- ✅ **Ventaja:** Gratis, URL pública permanente, bueno para proyectos
- ⚠️ **Nota:** NO subas el archivo `google_maps_api_key.txt` (ya está en .gitignore)

---

## 🌐 Opción 3: Vercel (GRATIS - Rápido)

### Pasos:

1. **Instala Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **En la carpeta del proyecto:**
   ```bash
   vercel
   ```

3. **Sigue las instrucciones en pantalla**

- ✅ **Ventaja:** Rápido, buena performance, HTTPS automático
- ✅ **URL ejemplo:** `https://sri-ruc-mapa.vercel.app/mapa_google_maps_filtrado.html`

---

## 🌐 Opción 4: Surge.sh (GRATIS - Simple)

### Pasos:

1. **Instala Surge:**
   ```bash
   npm install -g surge
   ```

2. **Publica:**
   ```bash
   surge
   # Te pedirá email y contraseña (primera vez)
   # Proyecto: . (punto para carpeta actual)
   # Dominio: elige uno o usa el sugerido
   ```

- ✅ **Ventaja:** Muy simple, URL inmediata
- ✅ **URL ejemplo:** `https://tu-mapa.surge.sh/mapa_google_maps_filtrado.html`

---

## 🔒 Seguridad - IMPORTANTE ⚠️

### Tu API Key está en el HTML

El archivo HTML contiene tu API key de Google Maps (esto es normal para Google Maps API). **DEBES restringir tu API key por dominio** para evitar uso no autorizado.

### Restringir API Key por Dominio (OBLIGATORIO):

1. **Ve a Google Cloud Console:**
   - https://console.cloud.google.com/
   - Selecciona tu proyecto

2. **Ve a Credenciales:**
   - APIs & Services → Credentials
   - Haz clic en tu API key

3. **Configura restricciones:**
   - En "Application restrictions" → Selecciona "HTTP referrers (web sites)"
   - Haz clic en "ADD AN ITEM"
   - Agrega tus dominios:
     - `https://*.netlify.app/*` (si usas Netlify)
     - `https://*.github.io/*` (si usas GitHub Pages)
     - `https://*.vercel.app/*` (si usas Vercel)
     - `https://*.surge.sh/*` (si usas Surge)
   - También agrega `http://localhost:*` para desarrollo local
   - Guarda

4. **Restringir APIs:**
   - En "API restrictions" → "Restrict key"
   - Selecciona solo:
     - Maps JavaScript API
     - Geocoding API
   - Guarda

### Verificar que funciona:

- ✅ El mapa debe funcionar en tu URL pública
- ✅ El mapa NO debe funcionar en otros sitios (protección activa)

---

## 📊 Comparación Rápida

| Opción | Dificultad | Costo | URL Pública | Tiempo | Recomendado |
|--------|------------|-------|-------------|--------|-------------|
| **Netlify** | ⭐ Muy Fácil | Gratis | ✅ Sí | 2 min | ⭐⭐⭐⭐⭐ |
| **GitHub Pages** | ⭐⭐ Media | Gratis | ✅ Sí | 5 min | ⭐⭐⭐⭐ |
| **Vercel** | ⭐⭐ Media | Gratis | ✅ Sí | 3 min | ⭐⭐⭐⭐ |
| **Surge.sh** | ⭐⭐ Media | Gratis | ✅ Sí | 3 min | ⭐⭐⭐ |

---

## 🎯 Recomendación

**Para empezar rápido:** **Netlify** (arrastra y suelta, 2 minutos)

**Para proyectos académicos:** **GitHub Pages** (bueno para documentar el proyecto)

---

## ✅ Checklist Antes de Publicar

- [ ] El archivo `mapa_google_maps_filtrado.html` está generado
- [ ] Has restringido tu API key por dominio en Google Cloud Console
- [ ] Has agregado los dominios de tu servicio de hosting a las restricciones
- [ ] Has probado que el mapa funciona localmente
- [ ] NO vas a subir `google_maps_api_key.txt` (está en .gitignore)

---

## ❓ ¿Necesitas ayuda?

Si tienes problemas con alguna opción, dime cuál prefieres y te ayudo paso a paso.

