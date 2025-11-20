# 🌐 Cómo Ejecutar el Servidor Local

## 📋 Pasos para Ejecutar el Servidor

### 1. Abre tu terminal

Abre la terminal en la carpeta del proyecto:
```bash
cd /Users/danilo/Documents/Universidad/Noveno/Legislacion/sri_ruc
```

### 2. Verifica que no haya otro servidor corriendo

```bash
lsof -i :8000
```

Si muestra algo, detén el proceso:
```bash
pkill -f servidor_local.py
```

### 3. Ejecuta el servidor

```bash
python3 servidor_local.py
```

### 4. Verás algo como esto:

```
============================================================
🌐 Servidor local iniciado
============================================================
📍 URL del mapa principal: http://localhost:8000/mapa_google_maps_filtrado.html
📂 Servidor corriendo en: http://localhost:8000/

💡 Presiona Ctrl+C para detener el servidor
```

### 5. Abre el mapa en tu navegador

Copia y pega esta URL:
```
http://localhost:8000/mapa_google_maps_filtrado.html
```

### 6. Para detener el servidor

Presiona `Ctrl+C` en la terminal donde está corriendo.

---

## 🔧 Solución de Problemas

### Error: "El puerto 8000 ya está en uso"

**Solución 1: Detener el proceso**
```bash
pkill -f servidor_local.py
```

**Solución 2: Encontrar y detener el proceso manualmente**
```bash
lsof -i :8000
# Verás algo como: Python  75969  danilo  ...
# Luego ejecuta:
kill 75969
```

**Solución 3: Usar otro puerto**

Edita `servidor_local.py` y cambia:
```python
PORT = 8000  # Cambia a 8001, 8080, etc.
```

---

## ✅ Verificación Rápida

Para verificar que el servidor está corriendo:

```bash
curl http://localhost:8000/mapa_google_maps_filtrado.html
```

Si devuelve código HTML, el servidor está funcionando.

---

## 📱 URLs Disponibles

- **Mapa filtrado**: http://localhost:8000/mapa_google_maps_filtrado.html
- **Mapa completo**: http://localhost:8000/mapa_google_maps.html
- **Lista de archivos**: http://localhost:8000/

---

## 💡 Tips

- **Mantén la terminal abierta** mientras usas el mapa
- **No cierres la terminal** o el servidor se detendrá
- **Presiona Ctrl+C** cuando termines de usar el mapa

