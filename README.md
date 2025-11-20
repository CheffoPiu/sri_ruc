# 🗺️ Generador de Mapas - SRI Ecuador

Genera mapas interactivos con las ubicaciones de establecimientos registrados en el SRI de Ecuador usando Google Maps.

## 📦 Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🔑 Configuración de Google Maps API

### Paso 1: Obtener API Key

Sigue la guía paso a paso en: **`obtener_api_key_paso_a_paso.md`**

Resumen rápido:
1. Ve a https://console.cloud.google.com/
2. Crea un proyecto nuevo
3. Habilita **Geocoding API** y **Maps JavaScript API**
4. Configura facturación (tienes $200 USD gratis/mes)
5. Crea una API key

### Paso 2: Guardar API Key

Ejecuta:
```bash
python3 configurar_api_key.py
```

O crea manualmente el archivo `google_maps_api_key.txt` con tu API key.

## 🚀 Uso

### 1. Coloca tus archivos Excel

Coloca tus archivos Excel (.xlsx o .xls) en la carpeta `datos_excel/`

El script detectará automáticamente las columnas:
- **RUC** (o NUMERO_RUC)
- **Nombre/Razón Social** (o RAZON_SOCIAL)
- **Provincia** (o DESCRIPCION_PROVINCIA_EST)
- **Cantón** (o DESCRIPCION_CANTON_EST)

### 2. Generar el mapa

```bash
python3 generar_mapa_google.py
```

Esto generará: `mapa_google_maps.html`

### 3. Visualizar el mapa

**Opción A: Servidor local**
```bash
python3 servidor_local.py
```
Abre: http://localhost:8000/mapa_google_maps.html

**Opción B: Abrir directamente**
Haz doble clic en `mapa_google_maps.html` para abrirlo en tu navegador.

**Opción C: Publicar online**
Ver guía en: `publicar_online.md` (GitHub Pages, Netlify, etc.)

## 📊 Características del Mapa

- ✅ **Interactivo**: Zoom, arrastre, clic en marcadores
- ✅ **Colores por cantidad**: 
  - 🔴 Rojo: >1,000 establecimientos
  - 🟠 Naranja: 500-1,000
  - 🔵 Azul: 100-500
  - 🟢 Verde: <100
- ✅ **Información detallada**: Al hacer clic verás nombre, cantidad y ejemplos
- ✅ **Vista satelital**: Cambia entre mapa y satelital
- ✅ **Estadísticas**: Total de ubicaciones y establecimientos

## 💰 Costos

- **Crédito gratuito**: $200 USD/mes
- **Geocoding API**: $5 USD por 1,000 solicitudes
- **Maps JavaScript API**: $7 USD por 1,000 cargas
- **Tu uso estimado**: Menos de $1 USD (dentro del crédito gratuito)

## 📁 Estructura del Proyecto

```
sri_ruc/
├── datos_excel/              # Coloca tus archivos Excel aquí
├── generar_mapa_google.py    # Script principal
├── configurar_api_key.py     # Configurar API key
├── servidor_local.py         # Servidor local para visualizar
├── google_maps_api_key.txt   # Tu API key (no subir a git)
├── obtener_api_key_paso_a_paso.md  # Guía para obtener API key
├── publicar_online.md        # Guía para publicar en internet
└── README.md                 # Este archivo
```

## 🔒 Seguridad

- ⚠️ **NUNCA** subas `google_maps_api_key.txt` a repositorios públicos
- El archivo ya está en `.gitignore`
- Si expones tu API key, ve a Google Cloud Console y elimina/regenera la clave

## ❓ Problemas Comunes

### "ApiNotActivatedMapError"
- Habilita **Maps JavaScript API** en Google Cloud Console
- Verifica que ambas APIs estén habilitadas: Geocoding API y Maps JavaScript API

### "Error al configurar Google Maps API"
- Verifica que la API key sea correcta
- Asegúrate de que las APIs estén habilitadas
- Verifica que la facturación esté activa

### "API key not valid"
- Verifica que copiaste la clave completa
- Asegúrate de que no hay espacios al inicio/final

## 📚 Documentación Adicional

- `obtener_api_key_paso_a_paso.md` - Guía detallada para obtener API key
- `publicar_online.md` - Cómo publicar el mapa en internet

## 🎉 ¡Listo!

Ahora puedes generar mapas interactivos con todas las ubicaciones de tus establecimientos.
