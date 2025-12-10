"""
Recalcula las estimaciones de ventas con valores ajustados para Ecuador.
"""

import pandas as pd
import os
from buscar_info_google_places import BuscadorGooglePlaces

def recalcular_estimaciones():
    """Recalcula estimaciones con valores ajustados para Ecuador."""
    
    archivo = "../data/output/librerias_con_info_google.xlsx"
    if not os.path.exists(archivo):
        print(f"❌ No se encontró: {archivo}")
        return
    
    print("📊 Recalculando estimaciones con valores ajustados para Ecuador...")
    
    df = pd.read_excel(archivo)
    
    # Cargar API key (aunque no la usaremos, necesitamos la clase)
    google_api_key = None
    if os.path.exists('../config/google_maps_api_key.txt'):
        with open('../config/google_maps_api_key.txt', 'r') as f:
            google_api_key = f.read().strip()
    
    buscador = BuscadorGooglePlaces(google_api_key)
    
    # Recalcular estimaciones
    estimaciones_nuevas = []
    for _, row in df.iterrows():
        # Crear diccionario con info de Google
        info_google = {
            'encontrado': row.get('ENCONTRADO_GOOGLE', False),
            'numero_resenas': int(row.get('NUMERO_RESENAS', 0)),
            'calificacion': float(row.get('CALIFICACION_GOOGLE', 0)),
            'sitio_web': row.get('SITIO_WEB', ''),
            'tiene_fotos': bool(row.get('TIENE_FOTOS', False)),
            'numero_fotos': int(row.get('NUMERO_FOTOS', 0))
        }
        
        # Calcular nueva estimación
        estimacion = buscador.calcular_estimacion_mejorada(info_google, row)
        estimaciones_nuevas.append(estimacion)
    
    # Actualizar DataFrame
    df['ESTIMACION_VENTA_MENSUAL'] = [e['venta_estimada_mensual'] for e in estimaciones_nuevas]
    df['ESTIMACION_VENTA_ANUAL'] = [e['venta_estimada_anual'] for e in estimaciones_nuevas]
    df['CONFIANZA_ESTIMACION'] = [e['confianza'] for e in estimaciones_nuevas]
    df['RAZON_ESTIMACION'] = [e['razon'] for e in estimaciones_nuevas]
    
    # Guardar
    archivo_salida = "../data/output/librerias_con_info_google.xlsx"
    df.to_excel(archivo_salida, index=False)
    
    # Estadísticas
    print(f"\n✅ Estimaciones recalculadas")
    print(f"   Archivo actualizado: {archivo_salida}")
    
    # Filtrar por provincias
    df_filtrado = df[df['DESCRIPCION_PROVINCIA_EST'].isin(['EL ORO', 'GALAPAGOS'])]
    
    print(f"\n📊 Nuevas estadísticas (El Oro y Galápagos):")
    print(f"   Promedio mensual: ${df_filtrado['ESTIMACION_VENTA_MENSUAL'].mean():,.0f}")
    print(f"   Mediana mensual: ${df_filtrado['ESTIMACION_VENTA_MENSUAL'].median():,.0f}")
    print(f"   Mínimo: ${df_filtrado['ESTIMACION_VENTA_MENSUAL'].min():,.0f}")
    print(f"   Máximo: ${df_filtrado['ESTIMACION_VENTA_MENSUAL'].max():,.0f}")
    print(f"   Total mensual: ${df_filtrado['ESTIMACION_VENTA_MENSUAL'].sum():,.0f}")
    print(f"   Total anual: ${df_filtrado['ESTIMACION_VENTA_ANUAL'].sum():,.0f}")
    
    print(f"\n📈 Top 5 más altas (nuevas estimaciones):")
    top5 = df_filtrado.nlargest(5, 'ESTIMACION_VENTA_MENSUAL')
    for idx, row in top5.iterrows():
        print(f"   ${row['ESTIMACION_VENTA_MENSUAL']:,.0f} - {row['RAZON_SOCIAL'][:40]} ({row['NUMERO_RESENAS']} reseñas)")

if __name__ == "__main__":
    recalcular_estimaciones()

