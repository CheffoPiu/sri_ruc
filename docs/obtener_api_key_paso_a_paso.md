# 🔑 Guía Paso a Paso: Obtener Google Maps API Key

## ⚡ Resumen Rápido

1. Ir a Google Cloud Console
2. Crear proyecto
3. Habilitar Geocoding API
4. Configurar facturación
5. Crear API key
6. Guardar la API key

**Tiempo estimado: 10-15 minutos**

---

## 📋 PASO 1: Acceder a Google Cloud Console

1. Abre tu navegador y ve a: **https://console.cloud.google.com/**
2. Inicia sesión con tu cuenta de Google (la misma que usas para Gmail)
3. Si es tu primera vez, acepta los términos y condiciones

**✅ Listo cuando veas:** La pantalla principal de Google Cloud Console

---

## 📋 PASO 2: Crear un Nuevo Proyecto

1. En la parte **superior** de la pantalla, verás un selector de proyectos (dice "Seleccionar proyecto" o el nombre de un proyecto)
2. Haz clic en ese selector
3. Haz clic en el botón **"NUEVO PROYECTO"** (arriba a la derecha)
4. Completa el formulario:
   - **Nombre del proyecto:** `SRI RUC Mapper` (o cualquier nombre que prefieras)
   - **Organización:** Déjalo como está (si aparece)
5. Haz clic en **"CREAR"**
6. Espera unos segundos (verás una notificación cuando esté listo)
7. Selecciona el proyecto recién creado desde el selector de proyectos

**✅ Listo cuando veas:** El nombre de tu proyecto en la parte superior

---

## 📋 PASO 3: Habilitar la Geocoding API

1. En el menú lateral izquierdo (☰), busca y haz clic en **"APIs y servicios"**
2. En el submenú, haz clic en **"Biblioteca"**
3. En la barra de búsqueda, escribe: **"Geocoding API"**
4. Haz clic en **"Geocoding API"** (debería ser el primer resultado)
5. Haz clic en el botón azul **"HABILITAR"**
6. Espera unos segundos hasta que veas "API habilitada"

**✅ Listo cuando veas:** "API habilitada" o el botón cambia a "ADMINISTRAR"

---

## 📋 PASO 4: Configurar Facturación

⚠️ **IMPORTANTE:** Google requiere una cuenta de facturación, PERO:
- Tienes **$200 USD GRATIS** cada mes
- Con tus datos usarás menos de **$1 USD**
- **NO se te cobrará nada** a menos que excedas los $200 mensuales

### Pasos:

1. En el menú lateral, busca y haz clic en **"Facturación"**
2. Si no tienes una cuenta de facturación:
   - Haz clic en **"VINCULAR UNA CUENTA DE FACTURACIÓN"**
   - Completa el formulario:
     - **Nombre de la cuenta:** Tu nombre o nombre de tu organización
     - **País:** Ecuador
     - **Tipo de cuenta:** Individual o Empresa (según corresponda)
   - Haz clic en **"CONTINUAR"**
3. Agrega un método de pago:
   - Selecciona **"Tarjeta de crédito o débito"**
   - Completa los datos de tu tarjeta
   - Haz clic en **"INICIAR PRUEBA GRATUITA"**
4. Vincula la cuenta de facturación a tu proyecto:
   - Selecciona tu proyecto: **"SRI RUC Mapper"**
   - Haz clic en **"VINCULAR"**

**✅ Listo cuando veas:** "Cuenta de facturación vinculada" o el estado cambia a "Activa"

---

## 📋 PASO 5: Crear la API Key

1. En el menú lateral, ve a **"APIs y servicios"** > **"Credenciales"**
2. En la parte superior, haz clic en **"+ CREAR CREDENCIALES"**
3. Selecciona **"Clave de API"** del menú desplegable
4. Se creará una API key automáticamente y verás un cuadro de diálogo
5. **⚠️ IMPORTANTE:** Copia la API key ahora (se verá algo como: `AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - Haz clic en el ícono de copiar o selecciona todo y copia (Cmd+C / Ctrl+C)
6. Haz clic en **"CERRAR"**

**✅ Listo cuando tengas:** Tu API key copiada (empieza con "AIza")

---

## 📋 PASO 6: Restringir la API Key (RECOMENDADO - Seguridad)

Esto es opcional pero recomendado para proteger tu API key:

1. En la lista de "Claves de API", haz clic en la API key que acabas de crear
2. En la sección **"Restricciones de API"**:
   - Selecciona **"Restringir clave"**
   - En la lista, marca solo **"Geocoding API"**
3. En **"Restricciones de aplicación"**:
   - Puedes dejarlo en **"Ninguna"** por ahora (o restringir por IP si lo deseas)
4. Haz clic en **"GUARDAR"** (arriba)

**✅ Listo cuando veas:** "Restricciones actualizadas"

---

## 📋 PASO 7: Guardar la API Key en tu Proyecto

Tienes dos opciones:

### Opción A: Usar el script (Más fácil) ⭐

Ejecuta en la terminal:
```bash
python3 configurar_api_key.py
```

Luego pega tu API key cuando te la pida.

### Opción B: Crear archivo manualmente

1. En la carpeta del proyecto, crea un archivo llamado: `google_maps_api_key.txt`
2. Abre el archivo con un editor de texto
3. Pega tu API key (solo la clave, sin espacios ni comillas)
4. Guarda el archivo

**✅ Listo cuando tengas:** El archivo `google_maps_api_key.txt` con tu API key

---

## ✅ Verificación Final

Ejecuta el script:
```bash
python3 generar_mapa_google.py
```

Si ves el mensaje: **"✅ Google Maps API configurada"**, ¡todo está funcionando perfectamente!

---

## 💰 Costos

- **Crédito gratuito:** $200 USD/mes
- **Costo por 1,000 geocodificaciones:** $5 USD
- **Tu uso estimado:** ~100 ubicaciones = **$0.50 USD**
- **Resultado:** **Completamente GRATIS** (dentro del crédito)

---

## 🔒 Seguridad

- ✅ El archivo `google_maps_api_key.txt` está en `.gitignore` (no se subirá a git)
- ✅ Si compartes tu código, NO incluyas la API key
- ✅ Si expones tu API key por error, ve a Google Cloud Console y elimina/regenera la clave

---

## ❓ Problemas Comunes

### "Error al configurar Google Maps API"
- Verifica que copiaste la API key completa
- Asegúrate de que la Geocoding API esté habilitada
- Verifica que la facturación esté activa

### "API key not valid"
- Verifica que no hay espacios al inicio/final
- Asegúrate de que copiaste la clave completa
- Verifica que la API key no esté restringida de forma incorrecta

### "Quota exceeded"
- Has excedido el límite (muy poco probable)
- Espera hasta el próximo mes o actualiza tu plan

---

## 🎉 ¡Listo!

Ahora puedes generar mapas interactivos con Google Maps. Ejecuta:

```bash
python3 generar_mapa_google.py
```

Y disfruta de tu mapa interactivo! 🗺️

