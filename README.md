# 📚 Dashboard de Análisis de Librerías - SRI Ecuador

Dashboard interactivo para análisis de librerías en las provincias de El Oro y Galápagos.

## 📁 Estructura del Proyecto

```
sri_ruc/
├── scripts/              # Scripts Python principales
├── docs/                 # Documentación
├── data/                 # Datos (input/output)
├── output/               # Resultados HTML
├── config/               # Configuración
└── requirements.txt      # Dependencias
```

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key
cd scripts
python3 configurar_api_key.py

# Generar dashboard
python3 generar_dashboard_completo.py

# Visualizar
cd ..
python3 scripts/servidor_local.py
# Abre: http://localhost:8000/output/html/dashboard_completo.html
```

## 📖 Documentación

Ver carpeta `docs/` para guías detalladas.

