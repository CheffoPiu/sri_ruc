# 📚 Dashboard de Análisis de Librerías - SRI Ecuador

Dashboard interactivo para análisis de librerías en las provincias de El Oro y Galápagos, basado en datos del SRI y Google Maps API.

## 📁 Estructura del Proyecto

```
sri_ruc/
├── scripts/              # Scripts Python principales
│   ├── generar_dashboard_completo.py
│   ├── generar_mapa_filtrado.py
│   ├── buscar_info_google_places.py
│   ├── extraer_info_libros_librerias.py
│   └── ...
├── docs/                 # Documentación
│   ├── README.md
│   ├── GUIA_*.md
│   └── ...
├── data/                 # Datos
│   ├── input/           # Datos de entrada (Excel del SRI)
│   └── output/          # Datos generados (Excel, JSON)
├── output/              # Resultados
│   └── html/            # Dashboards y mapas HTML
├── config/              # Configuración
│   └── google_maps_api_key.txt
└── requirements.txt     # Dependencias Python
```

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key de Google Maps

```bash
cd scripts
python3 configurar_api_key.py
```

O crea manualmente `config/google_maps_api_key.txt` con tu API key.

### 3. Ejecutar scripts principales

```bash
cd scripts

# Generar mapa interactivo
python3 generar_mapa_filtrado.py

# Extraer información de libros
python3 extraer_info_libros_librerias.py

# Generar dashboard completo
python3 generar_dashboard_completo.py
```

### 4. Visualizar resultados

```bash
# Desde la raíz del proyecto
python3 scripts/servidor_local.py
```

Luego abre: http://localhost:8000/output/html/dashboard_completo.html

## 📊 Características

- ✅ Dashboard interactivo con múltiples pestañas
- ✅ Mapa interactivo de Google Maps
- ✅ Análisis de libros por librería
- ✅ Estimaciones de ventas basadas en datos reales
- ✅ Gráficos y visualizaciones profesionales
- ✅ Clasificación formal/informal (natural vs jurídica)

## 📖 Documentación

Consulta la carpeta `docs/` para guías detalladas sobre:
- Configuración de APIs
- Consultas al SRI
- Publicación online
- Metodología del análisis

## 🔧 Requisitos

- Python 3.7+
- Google Maps API Key (con Places API y Geocoding API habilitadas)
- Dependencias en `requirements.txt`

## 📝 Notas

- Los datos de entrada deben estar en `data/input/datos_excel/`
- Los resultados se generan en `output/html/` y `data/output/`
- Las estimaciones de ventas están basadas en datos reales calibrados

