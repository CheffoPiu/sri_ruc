# 🔧 Cómo Habilitar Google Places API

Para que el script `buscar_info_google_places.py` funcione, necesitas habilitar **Places API** en tu proyecto de Google Cloud.

## ⚡ Pasos Rápidos

### 1. Ir a Google Cloud Console
Ve a: **https://console.cloud.google.com/**

### 2. Seleccionar tu Proyecto
- Asegúrate de estar en el mismo proyecto donde tienes la API key de Google Maps

### 3. Habilitar Places API
1. En el menú lateral, ve a **"APIs y servicios"** → **"Biblioteca"**
2. Busca: **"Places API"**
3. Haz clic en **"Places API"** (debería ser el primer resultado)
4. Haz clic en **"HABILITAR"**
5. Espera unos segundos hasta que veas "API habilitada"

### 4. Verificar que esté Habilitada
1. Ve a **"APIs y servicios"** → **"APIs habilitadas"**
2. Deberías ver:
   - ✅ Geocoding API
   - ✅ Maps JavaScript API
   - ✅ **Places API** ← Esta es la nueva

## ✅ Listo

Una vez habilitada, puedes ejecutar:
```bash
python3 buscar_info_google_places.py
```

## 💰 Costos

- **Places API** tiene un crédito gratuito de $200 USD/mes
- Cada búsqueda cuesta aproximadamente $0.032 USD
- Para 62 librerías: ~$2 USD (dentro del crédito gratuito)

## ⚠️ Si tienes problemas

1. **Verifica que la API key tenga acceso a Places API**
   - Ve a "APIs y servicios" → "Credenciales"
   - Haz clic en tu API key
   - Verifica que "Places API" esté en la lista de restricciones (o sin restricciones)

2. **Verifica la facturación**
   - Aunque tengas crédito gratuito, necesitas tener facturación configurada

3. **Revisa los límites**
   - Google tiene límites de rate (búsquedas por segundo)
   - El script incluye pausas para evitar exceder límites

