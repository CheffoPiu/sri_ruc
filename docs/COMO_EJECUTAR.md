# 🚀 Cómo Ejecutar el Dashboard desde la Terminal

## ⚡ Opción 1: Servidor Local (Recomendado)

### Paso 1: Abrir la terminal
Abre tu terminal (Terminal.app en Mac, o la terminal de tu sistema).

### Paso 2: Ir al directorio del proyecto
```bash
cd /Users/danilo/Documents/Universidad/Noveno/Legislacion/sri_ruc
```

### Paso 3: Ejecutar el servidor
```bash
python3 servidor_local.py
```

### Paso 4: Abrir en el navegador
El servidor se abrirá automáticamente, o puedes ir a:
- **Dashboard completo**: http://localhost:8001/dashboard_completo.html
- **Mapa interactivo**: http://localhost:8001/mapa_google_maps_filtrado.html

### Para detener el servidor:
Presiona `Ctrl + C` en la terminal

---

## ⚡ Opción 2: Abrir Directamente (Sin servidor)

### Desde la terminal:
```bash
cd /Users/danilo/Documents/Universidad/Noveno/Legislacion/sri_ruc
open dashboard_completo.html
```

O en Linux:
```bash
xdg-open dashboard_completo.html
```

---

## 📋 Comandos Rápidos

### Ver el dashboard completo:
```bash
cd /Users/danilo/Documents/Universidad/Noveno/Legislacion/sri_ruc
python3 servidor_local.py
```
Luego abre: http://localhost:8001/dashboard_completo.html

### Ver solo el mapa:
```bash
cd /Users/danilo/Documents/Universidad/Noveno/Legislacion/sri_ruc
python3 servidor_local.py
```
Luego abre: http://localhost:8001/mapa_google_maps_filtrado.html

---

## 🔧 Si tienes problemas

### Error: "puerto ya en uso"
```bash
# Buscar qué está usando el puerto 8001
lsof -i :8001

# O usar otro puerto (edita servidor_local.py y cambia PORT = 8001 a otro número)
```

### Error: "python3 no encontrado"
```bash
# Usa python en lugar de python3
python servidor_local.py
```

### El mapa no carga
- Asegúrate de tener tu API key de Google Maps configurada
- Verifica que `mapa_google_maps_filtrado.html` existe
- Revisa la consola del navegador (F12) para ver errores

---

## 📁 Archivos Disponibles

Una vez que ejecutes el servidor, puedes acceder a:

- ✅ `dashboard_completo.html` - Dashboard con todas las pestañas
- ✅ `mapa_google_maps_filtrado.html` - Mapa interactivo
- ✅ `dashboard_librerias.html` - Dashboard simple (versión anterior)

---

## 💡 Tips

1. **Mantén el servidor corriendo** mientras navegas por el dashboard
2. **No cierres la terminal** hasta que termines de usar el dashboard
3. **Usa Ctrl+C** para detener el servidor cuando termines
4. **El servidor se abre automáticamente** en tu navegador predeterminado

---

## ✅ Checklist

- [ ] Terminal abierta
- [ ] En el directorio correcto
- [ ] Servidor ejecutándose
- [ ] Navegador abierto con el dashboard

