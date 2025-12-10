# 📁 Estructura Organizada del Proyecto

## ✅ Organización Completada

El proyecto ha sido reorganizado en la siguiente estructura:

```
sri_ruc/
├── scripts/                    # 17 scripts Python
│   ├── generar_dashboard_completo.py
│   ├── generar_mapa_filtrado.py
│   ├── buscar_info_google_places.py
│   ├── extraer_info_libros_librerias.py
│   ├── analizar_libros_dashboard.py
│   ├── servidor_local.py
│   └── ...
│
├── docs/                       # 18 archivos de documentación
│   ├── README.md
│   ├── GUIA_*.md
│   ├── ACLARACION_*.md
│   └── ...
│
├── data/
│   ├── input/                  # Datos de entrada
│   │   └── datos_excel/       # Archivos Excel del SRI
│   └── output/                 # Datos generados
│       ├── *.xlsx             # Archivos Excel generados
│       └── *.json             # Archivos JSON
│
├── output/
│   └── html/                   # Dashboards y mapas HTML
│       ├── dashboard_completo.html
│       └── mapa_google_maps_filtrado.html
│
├── config/                     # Configuración
│   └── google_maps_api_key.txt
│
├── README.md                   # Documentación principal
└── requirements.txt            # Dependencias
```

## 🔄 Cambios Realizados

1. ✅ **Scripts movidos** a `scripts/`
2. ✅ **Documentación movida** a `docs/`
3. ✅ **Datos organizados** en `data/input/` y `data/output/`
4. ✅ **HTML generados** en `output/html/`
5. ✅ **Configuración** en `config/`
6. ✅ **Rutas actualizadas** en todos los scripts (17 archivos)

## 📝 Notas Importantes

- Todos los scripts ahora usan rutas relativas desde `scripts/`
- Los datos de entrada deben estar en `data/input/datos_excel/`
- Los resultados se generan en `output/html/` y `data/output/`
- Ejecutar scripts desde la carpeta `scripts/` o ajustar rutas según necesidad

## 🚀 Uso

```bash
# Desde la raíz del proyecto
cd scripts
python3 generar_dashboard_completo.py

# O desde cualquier lugar
python3 scripts/generar_dashboard_completo.py
```
