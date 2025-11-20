# ⚙️ Configuración de Filtros

## 📝 Cómo Configurar los Filtros

Abre el archivo `generar_mapa_filtrado.py` y busca la sección de **CONFIGURACIÓN DE FILTROS** (alrededor de la línea 440).

## 🔧 Opciones Disponibles

### 1. Códigos CIIU

```python
CODIGOS_CIIU = ['G476101', 'G476102', 'G476103', 'G476104']
```

- **Con filtro**: Solo muestra establecimientos con estos códigos
- **Sin filtro**: `CODIGOS_CIIU = []` → Muestra todos los códigos

### 2. Provincias a Visualizar

```python
PROVINCIAS_A_VISUALIZAR = []
```

**IMPORTANTE**: 
- Cada archivo Excel se filtra **automáticamente** por su propia provincia
- El archivo `SRI_RUC_El_Oro.xlsx` solo procesa datos de **EL ORO**
- El archivo `SRI_RUC_Galapagos.xlsx` solo procesa datos de **GALAPAGOS**

Esta opción controla qué provincias aparecen en el **mapa final**:

#### Opciones:

**Mostrar TODAS las provincias:**
```python
PROVINCIAS_A_VISUALIZAR = []  # Vacío = todas
```

**Mostrar SOLO El Oro:**
```python
PROVINCIAS_A_VISUALIZAR = ['EL ORO']
```

**Mostrar SOLO Galápagos:**
```python
PROVINCIAS_A_VISUALIZAR = ['GALAPAGOS']
```

**Mostrar ambas:**
```python
PROVINCIAS_A_VISUALIZAR = ['EL ORO', 'GALAPAGOS']
```

## 📋 Ejemplos de Configuración

### Ejemplo 1: Solo El Oro con códigos CIIU
```python
CODIGOS_CIIU = ['G476101', 'G476102', 'G476103', 'G476104']
PROVINCIAS_A_VISUALIZAR = ['EL ORO']
```

### Ejemplo 2: Solo Galápagos con códigos CIIU
```python
CODIGOS_CIIU = ['G476101', 'G476102', 'G476103', 'G476104']
PROVINCIAS_A_VISUALIZAR = ['GALAPAGOS']
```

### Ejemplo 3: Ambas provincias, todos los códigos CIIU
```python
CODIGOS_CIIU = []  # Sin filtro
PROVINCIAS_A_VISUALIZAR = ['EL ORO', 'GALAPAGOS']
```

### Ejemplo 4: Solo El Oro, sin filtro de CIIU
```python
CODIGOS_CIIU = []  # Sin filtro
PROVINCIAS_A_VISUALIZAR = ['EL ORO']
```

## 🎯 Cómo Funciona

1. **Detección automática**: El script detecta la provincia de cada archivo Excel por su nombre
2. **Filtrado por archivo**: Cada Excel se filtra por su propia provincia + códigos CIIU
3. **Filtrado final**: Si especificas `PROVINCIAS_A_VISUALIZAR`, solo esas provincias aparecen en el mapa

## ✅ Recomendación

Para empezar, usa:
```python
CODIGOS_CIIU = ['G476101', 'G476102', 'G476103', 'G476104']
PROVINCIAS_A_VISUALIZAR = []  # Ver todas
```

Luego cambia `PROVINCIAS_A_VISUALIZAR` según lo que quieras visualizar.

