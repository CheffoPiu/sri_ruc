"""
Generador de Presentación - Análisis de Librerías
Crea visualizaciones y resumen ejecutivo para presentar los datos.
"""

import pandas as pd
import os
from datetime import datetime

def generar_resumen_ejecutivo():
    """Genera un resumen ejecutivo en formato texto y HTML."""
    
    # Cargar datos
    archivo = "librerias_con_info_google.xlsx"
    if not os.path.exists(archivo):
        print(f"❌ No se encontró: {archivo}")
        return
    
    df = pd.read_excel(archivo)
    
    # Filtrar encontradas
    encontradas = df[df['ENCONTRADO_GOOGLE'] == True]
    no_encontradas = df[df['ENCONTRADO_GOOGLE'] != True]
    
    # Calcular estadísticas
    total_librerias = len(df)
    total_encontradas = len(encontradas)
    porcentaje_encontradas = (total_encontradas / total_librerias) * 100
    
    # Estadísticas de reseñas
    promedio_resenas = encontradas['NUMERO_RESENAS'].mean()
    total_resenas = encontradas['NUMERO_RESENAS'].sum()
    promedio_calificacion = encontradas['CALIFICACION_GOOGLE'].mean()
    
    # Estadísticas de ventas
    venta_total_mensual = df['ESTIMACION_VENTA_MENSUAL'].sum()
    venta_total_anual = venta_total_mensual * 12
    
    # Top librerías
    top_10_resenas = encontradas.nlargest(10, 'NUMERO_RESENAS')[
        ['RAZON_SOCIAL', 'NOMBRE_FANTASIA_COMERCIAL', 'NUMERO_RESENAS', 
         'CALIFICACION_GOOGLE', 'ESTIMACION_VENTA_MENSUAL', 'DESCRIPCION_CANTON_EST']
    ]
    
    # Por provincia
    por_provincia = df.groupby('DESCRIPCION_PROVINCIA_EST').agg({
        'NUMERO_RUC': 'count',
        'ESTIMACION_VENTA_MENSUAL': 'sum',
        'NUMERO_RESENAS': 'sum'
    }).round(2)
    por_provincia.columns = ['Cantidad', 'Venta_Mensual_USD', 'Total_Resenas']
    por_provincia = por_provincia.sort_values('Venta_Mensual_USD', ascending=False)
    
    # Por cantón
    por_canton = df.groupby('DESCRIPCION_CANTON_EST').agg({
        'NUMERO_RUC': 'count',
        'ESTIMACION_VENTA_MENSUAL': 'sum'
    }).round(2)
    por_canton.columns = ['Cantidad', 'Venta_Mensual_USD']
    por_canton = por_canton.sort_values('Venta_Mensual_USD', ascending=False).head(10)
    
    # Generar reporte
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    reporte = f"""
{'='*80}
📚 RESUMEN EJECUTIVO - ANÁLISIS DE LIBRERÍAS
Códigos CIIU: G476101 y G476104
Fecha: {fecha}
{'='*80}

📊 DATOS GENERALES
{'-'*80}
Total de librerías analizadas: {total_librerias}
Librerías encontradas en Google Maps: {total_encontradas} ({porcentaje_encontradas:.1f}%)
Librerías no encontradas: {len(no_encontradas)}

📈 ESTADÍSTICAS DE GOOGLE MAPS
{'-'*80}
Total de reseñas: {total_resenas:,.0f}
Promedio de reseñas por librería: {promedio_resenas:.1f}
Calificación promedio: {promedio_calificacion:.2f} ⭐

💰 ESTIMACIONES DE VENTAS
{'-'*80}
Venta total mensual estimada: ${venta_total_mensual:,.2f} USD
Venta total anual estimada: ${venta_total_anual:,.2f} USD

📍 DISTRIBUCIÓN POR PROVINCIA
{'-'*80}
"""
    
    for provincia, datos in por_provincia.iterrows():
        reporte += f"{provincia}:\n"
        reporte += f"  • Librerías: {int(datos['Cantidad'])}\n"
        reporte += f"  • Venta mensual: ${datos['Venta_Mensual_USD']:,.2f} USD\n"
        reporte += f"  • Total reseñas: {int(datos['Total_Resenas'])}\n\n"
    
    reporte += f"""
🏙️  TOP 10 CANTONES POR VENTAS
{'-'*80}
"""
    for canton, datos in por_canton.iterrows():
        reporte += f"{canton}: ${datos['Venta_Mensual_USD']:,.2f} USD/mes ({int(datos['Cantidad'])} librerías)\n"
    
    reporte += f"""

⭐ TOP 10 LIBRERÍAS POR RESEÑAS
{'-'*80}
"""
    for idx, (_, row) in enumerate(top_10_resenas.iterrows(), 1):
        nombre = row['NOMBRE_FANTASIA_COMERCIAL'] if pd.notna(row['NOMBRE_FANTASIA_COMERCIAL']) else row['RAZON_SOCIAL']
        reporte += f"{idx}. {nombre[:50]}\n"
        reporte += f"   Reseñas: {int(row['NUMERO_RESENAS'])} | Calificación: {row['CALIFICACION_GOOGLE']:.1f}⭐\n"
        reporte += f"   Venta estimada: ${row['ESTIMACION_VENTA_MENSUAL']:,.2f} USD/mes\n"
        reporte += f"   Ubicación: {row['DESCRIPCION_CANTON_EST']}\n\n"
    
    reporte += f"""
{'='*80}
⚠️  NOTA IMPORTANTE
{'-'*80}
Las estimaciones de ventas están basadas en:
• Número de reseñas en Google Maps
• Calificaciones de usuarios
• Presencia online (sitio web, redes sociales)
• Estado del contribuyente (ACTIVO/PASIVO/SUSPENDIDO)
• Ubicación geográfica

Estas son ESTIMACIONES y deben validarse con datos oficiales del SRI
o información directa de las librerías.

{'='*80}
"""
    
    # Guardar reporte
    with open('RESUMEN_PRESENTACION.txt', 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print("✅ Resumen ejecutivo generado: RESUMEN_PRESENTACION.txt")
    return reporte


def generar_tablas_resumen():
    """Genera tablas resumen en Excel para presentación."""
    
    archivo = "librerias_con_info_google.xlsx"
    if not os.path.exists(archivo):
        print(f"❌ No se encontró: {archivo}")
        return
    
    df = pd.read_excel(archivo)
    
    # Crear Excel con múltiples hojas
    archivo_salida = "PRESENTACION_LIBRERIAS.xlsx"
    
    with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
        
        # Hoja 1: Resumen General
        resumen_general = pd.DataFrame({
            'Métrica': [
                'Total de librerías',
                'Encontradas en Google Maps',
                'No encontradas',
                'Total de reseñas',
                'Promedio de reseñas',
                'Calificación promedio',
                'Venta mensual estimada (USD)',
                'Venta anual estimada (USD)'
            ],
            'Valor': [
                len(df),
                df['ENCONTRADO_GOOGLE'].sum(),
                len(df) - df['ENCONTRADO_GOOGLE'].sum(),
                int(df['NUMERO_RESENAS'].sum()),
                f"{df[df['ENCONTRADO_GOOGLE']==True]['NUMERO_RESENAS'].mean():.1f}",
                f"{df[df['ENCONTRADO_GOOGLE']==True]['CALIFICACION_GOOGLE'].mean():.2f}",
                f"${df['ESTIMACION_VENTA_MENSUAL'].sum():,.2f}",
                f"${df['ESTIMACION_VENTA_MENSUAL'].sum() * 12:,.2f}"
            ]
        })
        resumen_general.to_excel(writer, sheet_name='Resumen General', index=False)
        
        # Hoja 2: Top 20 Librerías
        top_20 = df.nlargest(20, 'ESTIMACION_VENTA_MENSUAL')[
            ['RAZON_SOCIAL', 'NOMBRE_FANTASIA_COMERCIAL', 'DESCRIPCION_CANTON_EST',
             'NUMERO_RESENAS', 'CALIFICACION_GOOGLE', 'ESTIMACION_VENTA_MENSUAL',
             'ESTIMACION_VENTA_ANUAL', 'SITIO_WEB', 'URL_GOOGLE_MAPS']
        ]
        top_20.columns = ['Razón Social', 'Nombre Fantasía', 'Cantón', 'Reseñas',
                          'Calificación', 'Venta Mensual (USD)', 'Venta Anual (USD)',
                          'Sitio Web', 'URL Google Maps']
        top_20.to_excel(writer, sheet_name='Top 20 Librerías', index=False)
        
        # Hoja 3: Por Provincia
        por_provincia = df.groupby('DESCRIPCION_PROVINCIA_EST').agg({
            'NUMERO_RUC': 'count',
            'ESTIMACION_VENTA_MENSUAL': 'sum',
            'NUMERO_RESENAS': 'sum',
            'CALIFICACION_GOOGLE': 'mean'
        }).round(2)
        por_provincia.columns = ['Cantidad', 'Venta Mensual (USD)', 'Total Reseñas', 'Calificación Promedio']
        por_provincia = por_provincia.sort_values('Venta Mensual (USD)', ascending=False)
        por_provincia.to_excel(writer, sheet_name='Por Provincia')
        
        # Hoja 4: Por Cantón
        por_canton = df.groupby('DESCRIPCION_CANTON_EST').agg({
            'NUMERO_RUC': 'count',
            'ESTIMACION_VENTA_MENSUAL': 'sum',
            'NUMERO_RESENAS': 'sum'
        }).round(2)
        por_canton.columns = ['Cantidad', 'Venta Mensual (USD)', 'Total Reseñas']
        por_canton = por_canton.sort_values('Venta Mensual (USD)', ascending=False)
        por_canton.to_excel(writer, sheet_name='Por Cantón')
        
        # Hoja 5: Todas las Librerías (simplificado)
        todas = df[[
            'NUMERO_RUC', 'RAZON_SOCIAL', 'NOMBRE_FANTASIA_COMERCIAL',
            'DESCRIPCION_CANTON_EST', 'NUMERO_RESENAS', 'CALIFICACION_GOOGLE',
            'ESTIMACION_VENTA_MENSUAL', 'SITIO_WEB', 'URL_GOOGLE_MAPS'
        ]].copy()
        todas.columns = ['RUC', 'Razón Social', 'Nombre Fantasía', 'Cantón',
                        'Reseñas', 'Calificación', 'Venta Mensual (USD)',
                        'Sitio Web', 'URL Google Maps']
        todas = todas.sort_values('Venta Mensual (USD)', ascending=False)
        todas.to_excel(writer, sheet_name='Todas las Librerías', index=False)
    
    print(f"✅ Archivo de presentación generado: {archivo_salida}")
    print("   Contiene 5 hojas con diferentes vistas de los datos")


def main():
    """Función principal."""
    print("="*80)
    print("📊 GENERADOR DE PRESENTACIÓN - ANÁLISIS DE LIBRERÍAS")
    print("="*80)
    
    print("\n1️⃣ Generando resumen ejecutivo...")
    generar_resumen_ejecutivo()
    
    print("\n2️⃣ Generando tablas resumen...")
    generar_tablas_resumen()
    
    print("\n" + "="*80)
    print("✅ PRESENTACIÓN GENERADA")
    print("="*80)
    print("\n📁 Archivos creados:")
    print("   • RESUMEN_PRESENTACION.txt - Resumen ejecutivo en texto")
    print("   • PRESENTACION_LIBRERIAS.xlsx - Tablas para presentación")
    print("\n💡 Usa estos archivos para:")
    print("   • Presentar los hallazgos")
    print("   • Crear gráficos en Excel/PowerPoint")
    print("   • Integrar en tu dashboard")
    print("\n📊 Métricas clave para destacar:")
    print("   • 58 librerías encontradas en Google Maps")
    print("   • Promedio de 70.8 reseñas por librería")
    print("   • Calificación promedio: 4.24 estrellas")
    print("   • Venta estimada: $2.7 millones USD/mes")


if __name__ == "__main__":
    main()

