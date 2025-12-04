# 📊 Guía para Obtener Información de Ventas de Librerías

## 🎯 Objetivo
Obtener datos reales o estimaciones precisas de cuántos libros venden las librerías con códigos CIIU **G476101** y **G476104**.

---

## 📋 Fuentes de Datos Disponibles

### 1. 🏛️ SRI (Servicio de Rentas Internas) - **MÁS CONFIABLE**

#### ¿Qué información puedes obtener?
- ✅ **Facturación mensual/anual** (declaraciones de IVA)
- ✅ **Volumen de ventas** (Formulario 104)
- ✅ **Retenciones en la fuente** (indica volumen de operaciones)
- ✅ **Estado de declaraciones** (si están al día)

#### ¿Cómo acceder?
1. **Portal SRI en línea**: https://srienlinea.sri.gob.ec/
2. **Consulta por RUC**: Ingresa el número de RUC de cada librería
3. **Solicitar información**: Puedes solicitar reportes agregados del sector

#### Datos que ya tienes:
- ✅ RUC de cada librería (en `librerias_detalle.xlsx`)
- ✅ Estado del contribuyente (ACTIVO/PASIVO/SUSPENDIDO)
- ✅ Agente de retención (indica mayor volumen)

#### Pasos recomendados:
```python
# 1. Filtrar librerías activas
librerias_activas = df[df['ESTADO_CONTRIBUYENTE'] == 'ACTIVO']

# 2. Priorizar agentes de retención (mayor volumen)
agentes_retencion = df[df['AGENTE_RETENCION'].notna()]

# 3. Consultar en SRI usando los RUCs
```

---

### 2. 🏢 Registro Mercantil

#### ¿Qué información puedes obtener?
- ✅ **Estados financieros anuales**
- ✅ **Capital social** (indica tamaño del negocio)
- ✅ **Información de socios y representantes**
- ✅ **Historial de la empresa**

#### ¿Cómo acceder?
- Portal: https://www.registromercantil.gob.ec/
- Búsqueda por RUC o razón social
- Algunos datos son públicos, otros requieren registro

---

### 3. 📱 Encuestas Directas

#### Ventajas:
- ✅ Datos directos de la fuente
- ✅ Información actualizada
- ✅ Puedes hacer preguntas específicas

#### Desventajas:
- ⚠️ Requiere tiempo y recursos
- ⚠️ No todas las librerías responderán
- ⚠️ Pueden no querer compartir información

#### ¿Cómo hacerlo?
1. **Obtener contactos**:
   - Usar los RUCs para buscar en Google
   - Buscar en Google Maps por nombre
   - Buscar en redes sociales

2. **Preguntas sugeridas**:
   - ¿Cuántos libros venden aproximadamente al mes?
   - ¿Cuál es su facturación mensual estimada?
   - ¿Cuántos empleados tienen?
   - ¿Qué tipo de libros venden más?

3. **Herramientas**:
   - Google Maps (buscar por nombre)
   - Facebook/Instagram (buscar páginas comerciales)
   - Directorios telefónicos online

---

### 4. 🛒 Google Maps y Redes Sociales

#### ¿Qué información puedes obtener?
- ✅ **Ubicación física** (verificar si existe)
- ✅ **Reseñas y calificaciones** (indica actividad)
- ✅ **Fotos del establecimiento** (ver tamaño)
- ✅ **Horarios de atención** (indica operación)
- ✅ **Número de teléfono** (para contactar)

#### Pasos:
1. Buscar por nombre de la librería en Google Maps
2. Revisar reseñas (más reseñas = más actividad)
3. Ver fotos para estimar tamaño
4. Verificar si tiene página web o redes sociales

---

### 5. 📈 Estimaciones por Indicadores (Ya implementado)

Ya tienes un script que estima ventas basándose en:
- ✅ Estado del contribuyente (ACTIVO = operando)
- ✅ Agente de retención (mayor volumen)
- ✅ Ubicación (cantones grandes = más ventas)
- ✅ Nombre fantasia (marca establecida)

**Archivo generado**: `librerias_con_estimaciones.xlsx`

---

## 🔍 Verificación: ¿Son realmente librerías?

### Métodos de verificación:

1. **Análisis de nombres**:
   - Buscar palabras clave: "librería", "libro", "papelería"
   - Ya implementado en el análisis

2. **Búsqueda en Google Maps**:
   - Buscar por nombre + ubicación
   - Ver fotos del establecimiento
   - Leer reseñas

3. **Verificar actividad económica**:
   - Revisar columna `ACTIVIDAD_ECONOMICA` en los datos
   - Debe mencionar libros, papelería, etc.

4. **Contacto directo**:
   - Llamar o visitar el establecimiento
   - Verificar qué productos venden

---

## 📊 Estrategia Recomendada

### Fase 1: Análisis Inicial (✅ COMPLETADO)
- [x] Identificar librerías con códigos G476101 y G476104
- [x] Generar estadísticas básicas
- [x] Clasificar por tamaño (pequeña/mediana/grande)
- [x] Generar estimaciones iniciales

### Fase 2: Verificación (🔄 EN PROGRESO)
1. **Priorizar librerías**:
   - Empezar con las ACTIVAS
   - Priorizar agentes de retención
   - Enfocarse en cantones grandes

2. **Verificar en Google Maps**:
   - Buscar cada librería
   - Verificar si existe físicamente
   - Revisar reseñas y actividad

3. **Crear lista de verificación**:
   - Librería verificada: ✅
   - Librería no encontrada: ❌
   - Necesita más investigación: ⚠️

### Fase 3: Obtención de Datos Reales
1. **Consultar SRI** (para datos oficiales):
   - Usar RUCs para consultar declaraciones
   - Obtener facturación real

2. **Encuestas** (para datos directos):
   - Contactar librerías prioritarias
   - Hacer preguntas específicas

3. **Análisis de redes sociales**:
   - Revisar actividad en Facebook/Instagram
   - Estimar volumen por engagement

---

## 🛠️ Scripts Disponibles

### 1. `analizar_librerias.py`
- Analiza los datos de librerías
- Genera estadísticas
- Exporta datos detallados

**Ejecutar**: `python3 analizar_librerias.py`

**Resultados**:
- `reporte_librerias.txt` - Reporte completo
- `librerias_detalle.xlsx` - Datos detallados

### 2. `estimar_ventas_librerias.py`
- Estima ventas basándose en indicadores
- Clasifica por tamaño
- Genera rangos de estimación

**Ejecutar**: `python3 estimar_ventas_librerias.py`

**Resultados**:
- `librerias_con_estimaciones.xlsx` - Datos con estimaciones

### 3. `generar_mapa_filtrado.py`
- Genera mapa interactivo
- Filtra por códigos CIIU
- Visualiza ubicaciones

**Ejecutar**: `python3 generar_mapa_filtrado.py`

**Resultados**:
- `mapa_google_maps_filtrado.html` - Mapa interactivo

---

## 📝 Próximos Pasos Sugeridos

### Opción A: Verificación Rápida (Recomendado)
1. Abrir `librerias_con_estimaciones.xlsx`
2. Filtrar por librerías ACTIVAS y GRANDES
3. Buscar cada una en Google Maps
4. Verificar si realmente son librerías
5. Actualizar el Excel con resultados

### Opción B: Consulta SRI (Más preciso)
1. Obtener acceso al portal SRI
2. Consultar declaraciones de IVA por RUC
3. Obtener facturación real
4. Comparar con estimaciones

### Opción C: Encuesta Directa (Más completo)
1. Seleccionar muestra representativa (ej: 20-30 librerías)
2. Buscar contactos en Google Maps/redes sociales
3. Contactar por teléfono/email
4. Hacer preguntas sobre ventas
5. Extrapolar resultados a toda la población

---

## ⚠️ Limitaciones y Consideraciones

1. **Datos del SRI**:
   - Solo muestran facturación declarada
   - Puede haber subdeclaración
   - No distingue entre libros y otros productos

2. **Estimaciones**:
   - Son aproximaciones basadas en indicadores
   - Pueden variar significativamente
   - Útiles para análisis comparativo

3. **Verificación**:
   - Algunas librerías pueden haber cerrado
   - Algunas pueden haber cambiado de actividad
   - Necesitas verificar caso por caso

---

## 📊 Resumen de Datos Actuales

Según el análisis realizado:

- **Total de librerías**: 260 establecimientos
- **G476101**: 255 (98.08%) - Librerías especializadas
- **G476104**: 5 (1.92%) - Librerías con papelería
- **Activas**: 62 (23.8%)
- **Suspendidas**: 143 (55.0%)
- **Pasivas**: 55 (21.2%)

**Provincias principales**:
- El Oro: 219 (84.2%)
- Galápagos: 14 (5.4%)
- Guayas: 10 (3.8%)

**Cantones principales**:
- Machala: 140
- Pasaje: 41
- Santa Rosa: 11

---

## 🎯 Recomendación Final

Para tu dashboard, te recomiendo:

1. **Usar las estimaciones** como punto de partida
2. **Verificar las librerías activas** en Google Maps
3. **Consultar SRI** para las librerías más grandes (agentes de retención)
4. **Hacer encuestas** a una muestra pequeña para validar

Esto te dará:
- ✅ Datos estimados para todas las librerías
- ✅ Datos verificados para las más importantes
- ✅ Validación de que realmente son librerías
- ✅ Información suficiente para tu investigación

---

## 📞 Contacto y Recursos

- **SRI en línea**: https://srienlinea.sri.gob.ec/
- **Registro Mercantil**: https://www.registromercantil.gob.ec/
- **Google Maps**: https://maps.google.com/

---

**Última actualización**: Generado automáticamente por el análisis de datos

