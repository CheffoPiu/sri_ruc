# 🎯 Ejemplo Práctico: Consultar una Librería en el SRI

## 📚 Librería de Ejemplo

Usaremos esta librería real de tus datos:

```
┌─────────────────────────────────────────────────────────────┐
│  RUC: 1709303281001                                         │
│  Nombre: ARMIJOS CONZA JOSE DARIO                           │
│  Nombre Fantasía: DISTRIBUIDORA DE LIBROS CULTECSA          │
│  Provincia: EL ORO                                          │
│  Cantón: MACHALA                                             │
│  Código CIIU: G476101                                        │
│  Estado: ACTIVO ✅                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Pasos para Consultar (Paso a Paso)

### Paso 1: Abrir el Portal del SRI

1. Abre tu navegador (Chrome, Firefox, Safari, etc.)
2. Ve a esta dirección: **https://srienlinea.sri.gob.ec/**
3. Verás la página principal del SRI

---

### Paso 2: Buscar la Opción de Consulta de RUC

En la página principal, busca alguna de estas opciones:

- 🔍 **"Consulta de RUC"**
- 🔍 **"Consultas"** → **"RUC"**
- 🔍 Un campo de búsqueda que diga "Ingrese RUC"
- 🔍 Menú superior con opción "Consultas"

**💡 Tip**: Si no encuentras, busca en Google: `SRI consulta RUC Ecuador` y haz clic en el primer resultado.

---

### Paso 3: Ingresar el RUC

1. En el campo de búsqueda, escribe: **`1709303281001`**
2. Haz clic en **"Consultar"** o presiona **Enter**

---

### Paso 4: Ver los Resultados (Información Pública)

Después de consultar, deberías ver algo como esto:

```
╔═══════════════════════════════════════════════════════════╗
║  CONSULTA DE RUC                                          ║
╠═══════════════════════════════════════════════════════════╣
║  RUC: 1709303281001                                       ║
║  Razón Social: ARMIJOS CONZA JOSE DARIO                   ║
║  Nombre Comercial: DISTRIBUIDORA DE LIBROS CULTECSA       ║
║  Estado: ACTIVO ✅                                        ║
║  Actividad: VENTA AL POR MENOR DE LIBROS...              ║
║  Provincia: EL ORO                                        ║
║  Cantón: MACHALA                                          ║
║  Dirección: [dirección registrada]                        ║
║  Fecha Inicio: [fecha]                                    ║
╚═══════════════════════════════════════════════════════════╝
```

**✅ Esto confirma que:**
- La librería existe
- Está activa
- Tiene el código CIIU correcto (G476101 = librería)

---

### Paso 5: Buscar Información de Facturación (Requiere Login)

Para ver **ventas y facturación**, necesitas iniciar sesión:

#### 5.1. Crear Cuenta (si no tienes)

1. Busca **"Registro"** o **"Crear cuenta"** en la página
2. Completa el formulario:
   - Cédula/RUC
   - Email
   - Contraseña
   - Datos personales
3. Verifica tu email
4. Activa tu cuenta

#### 5.2. Iniciar Sesión

1. Haz clic en **"Iniciar Sesión"** o **"Login"**
2. Ingresa tu usuario y contraseña
3. Completa la verificación (captcha, si aplica)

---

### Paso 6: Consultar Declaraciones de IVA

Una vez dentro de tu cuenta:

1. Busca en el menú:
   - **"Declaraciones"**
   - **"IVA"**
   - **"Formulario 104"**
   - **"Consultas"** → **"Declaraciones"**

2. Selecciona **"Consultar declaraciones de terceros"** o similar

3. Ingresa el RUC: **`1709303281001`**

4. Selecciona el período (ej: últimos 12 meses)

5. Haz clic en **"Consultar"**

---

### Paso 7: Interpretar los Resultados

Si tienes acceso, verás algo como:

```
╔═══════════════════════════════════════════════════════════╗
║  DECLARACIONES DE IVA - ÚLTIMOS 12 MESES                 ║
╠═══════════════════════════════════════════════════════════╣
║  Período        │ Base Imponible │ IVA Cobrado            ║
╠═══════════════════════════════════════════════════════════╣
║  Enero 2024     │ $15,000        │ $1,800                ║
║  Febrero 2024  │ $18,000        │ $2,160                ║
║  Marzo 2024    │ $20,000        │ $2,400                ║
║  ...            │ ...            │ ...                    ║
║  Diciembre 2024 │ $22,000        │ $2,640                ║
╠═══════════════════════════════════════════════════════════╣
║  TOTAL ANUAL    │ $240,000       │ $28,800               ║
╚═══════════════════════════════════════════════════════════╝
```

---

### Paso 8: Calcular Ventas Estimadas

**Fórmula simple**:
```
Ventas = Base Imponible / 0.12
```

**Ejemplo**:
- Si Base Imponible anual = $240,000
- Ventas estimadas = $240,000 / 0.12 = **$2,000,000 USD/año**

O simplemente usa la **Base Imponible** como referencia de ventas (es lo que declaran).

---

## 📝 Registro de Datos

Crea una tabla como esta para registrar:

| RUC | Nombre | Base Imponible (Mes) | Base Imponible (Año) | Ventas Estimadas (Año) |
|-----|--------|---------------------|---------------------|----------------------|
| 1709303281001 | DISTRIBUIDORA DE LIBROS CULTECSA | $20,000 | $240,000 | $2,000,000 |

---

## ⚠️ Posibles Limitaciones

### Escenario 1: No puedes ver facturación
- **Razón**: Datos protegidos por privacidad
- **Solución**: 
  - Contacta directamente a la librería
  - Solicita datos agregados al SRI
  - Usa las estimaciones como referencia

### Escenario 2: Solo ves datos agregados
- **Razón**: El SRI protege información individual
- **Solución**: 
  - Trabaja con promedios del sector
  - Usa datos de múltiples librerías para promediar

### Escenario 3: Necesitas permisos especiales
- **Razón**: Para ver facturación de terceros se requieren permisos
- **Solución**: 
  - Si eres estudiante/investigador, contacta al SRI
  - Explica que es para investigación académica
  - Pueden darte acceso o datos agregados

---

## 🎯 Resumen Rápido

```
1. Ve a: https://srienlinea.sri.gob.ec/
2. Busca "Consulta de RUC"
3. Ingresa: 1709303281001
4. Ver información básica ✅
5. Inicia sesión (si quieres ver facturación)
6. Busca "Declaraciones IVA"
7. Consulta base imponible
8. Calcula ventas estimadas
```

---

## 📊 Otros Ejemplos para Probar

Si quieres probar con otras librerías:

| RUC | Nombre Fantasía | Prioridad |
|-----|----------------|-----------|
| 701355687001 | LIBRERIA DEL SALTO | 🔴 Alta |
| 106019201001 | BAZAR CORAZON DE MARIA | 🔴 Alta |
| 703500124001 | EDICIONES CULTURALES HERMANDAD | 🔴 Alta |
| 1717293870001 | IKU | 🔴 Alta |

**💡 Tip**: Ejecuta `python3 ejemplo_consulta_sri.py` para ver todas las librerías activas con sus RUCs.

---

## ✅ Checklist

- [ ] Accedí al portal del SRI
- [ ] Consulté el RUC 1709303281001
- [ ] Vi la información básica (estado, actividad)
- [ ] Creé cuenta en el SRI (si no tenía)
- [ ] Inicié sesión
- [ ] Busqué declaraciones de IVA
- [ ] Obtuve base imponible (si disponible)
- [ ] Calculé ventas estimadas
- [ ] Registré los datos

---

**🎉 ¡Listo!** Ahora puedes repetir este proceso con otras librerías de tu lista.

