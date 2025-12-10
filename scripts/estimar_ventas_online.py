"""
Estimador de Ventas usando Información Online
Busca información de librerías en Google Maps, páginas web, etc.
y calcula estimaciones basadas en indicadores online.
"""

import pandas as pd
import os
from typing import Dict, List
import time

class EstimadorVentasOnline:
    """Estima ventas basándose en información online disponible."""
    
    def __init__(self):
        # Factores de estimación basados en indicadores online
        self.factores = {
            'reseñas_google': {
                'sin_resenas': 0.5,  # Multiplicador si no hay reseñas
                'pocas_1_10': 1.0,    # 1-10 reseñas
                'moderadas_11_50': 1.5,  # 11-50 reseñas
                'muchas_51_100': 2.0,    # 51-100 reseñas
                'muy_muchas_100+': 3.0   # 100+ reseñas
            },
            'presencia_online': {
                'sin_web': 0.8,
                'con_web': 1.5,
                'con_redes_sociales': 2.0,
                'con_ecommerce': 2.5
            },
            'ubicacion': {
                'centro_comercial': 2.0,
                'zona_comercial': 1.5,
                'zona_residencial': 1.0,
                'zona_remota': 0.7
            },
            'antiguedad': {
                'nueva_0_2': 0.8,      # 0-2 años
                'joven_3_5': 1.0,      # 3-5 años
                'establecida_6_10': 1.3,  # 6-10 años
                'antigua_10+': 1.5     # 10+ años
            }
        }
        
        # Base de estimación por tamaño (en USD/mes)
        self.base_ventas = {
            'pequena': 8000,
            'mediana': 25000,
            'grande': 60000
        }
    
    def buscar_google_maps_url(self, nombre: str, canton: str, provincia: str) -> str:
        """Genera URL de búsqueda en Google Maps."""
        query = f"{nombre} {canton} {provincia} Ecuador"
        query_encoded = query.replace(' ', '+')
        return f"https://www.google.com/maps/search/?api=1&query={query_encoded}"
    
    def estimar_por_indicadores(self, registro: pd.Series) -> Dict:
        """Estima ventas basándose en indicadores disponibles."""
        estimacion = {
            'base': 0,
            'factores_aplicados': [],
            'multiplicador_total': 1.0,
            'venta_estimada_mensual': 0,
            'venta_estimada_anual': 0,
            'confianza': 'baja'  # baja, media, alta
        }
        
        # Determinar tamaño base
        if 'CLASIFICACION_TAMANO' in registro.index:
            tamano = registro['CLASIFICACION_TAMANO']
        else:
            # Clasificar por indicadores
            if pd.notna(registro.get('AGENTE_RETENCION')):
                tamano = 'grande'
            elif registro.get('ESTADO_CONTRIBUYENTE') == 'ACTIVO':
                tamano = 'mediana'
            else:
                tamano = 'pequena'
        
        estimacion['base'] = self.base_ventas.get(tamano, 8000)
        
        # Factor 1: Agente de retención
        if pd.notna(registro.get('AGENTE_RETENCION')):
            estimacion['multiplicador_total'] *= 1.5
            estimacion['factores_aplicados'].append('Agente de retención (+50%)')
        
        # Factor 2: Estado activo
        if registro.get('ESTADO_CONTRIBUYENTE') == 'ACTIVO':
            estimacion['multiplicador_total'] *= 1.2
            estimacion['factores_aplicados'].append('Estado activo (+20%)')
        elif 'SUSPENDIDO' in str(registro.get('ESTADO_CONTRIBUYENTE', '')):
            estimacion['multiplicador_total'] *= 0.3
            estimacion['factores_aplicados'].append('Estado suspendido (-70%)')
        
        # Factor 3: Ubicación (cantones grandes)
        canton = str(registro.get('DESCRIPCION_CANTON_EST', '')).upper()
        cantones_grandes = ['MACHALA', 'GUAYAQUIL', 'QUITO', 'CUENCA', 'AMBATO', 'SALINAS']
        if any(c in canton for c in cantones_grandes):
            estimacion['multiplicador_total'] *= 1.3
            estimacion['factores_aplicados'].append(f'Cantón grande ({canton}) (+30%)')
        
        # Factor 4: Antigüedad (si hay fecha de inicio)
        if 'FECHA_INICIO_ACTIVIDADES' in registro.index and pd.notna(registro.get('FECHA_INICIO_ACTIVIDADES')):
            try:
                from datetime import datetime
                fecha_inicio = pd.to_datetime(registro['FECHA_INICIO_ACTIVIDADES'])
                años_operacion = (datetime.now() - fecha_inicio).days / 365
                
                if años_operacion >= 10:
                    estimacion['multiplicador_total'] *= 1.3
                    estimacion['factores_aplicados'].append(f'Antigüedad {años_operacion:.1f} años (+30%)')
                elif años_operacion >= 5:
                    estimacion['multiplicador_total'] *= 1.1
                    estimacion['factores_aplicados'].append(f'Antigüedad {años_operacion:.1f} años (+10%)')
            except:
                pass
        
        # Factor 5: Nombre fantasia (marca establecida)
        if pd.notna(registro.get('NOMBRE_FANTASIA_COMERCIAL')):
            estimacion['multiplicador_total'] *= 1.2
            estimacion['factores_aplicados'].append('Nombre fantasia (+20%)')
        
        # Calcular venta estimada
        estimacion['venta_estimada_mensual'] = estimacion['base'] * estimacion['multiplicador_total']
        estimacion['venta_estimada_anual'] = estimacion['venta_estimada_mensual'] * 12
        
        # Determinar confianza
        num_factores = len(estimacion['factores_aplicados'])
        if num_factores >= 4:
            estimacion['confianza'] = 'alta'
        elif num_factores >= 2:
            estimacion['confianza'] = 'media'
        else:
            estimacion['confianza'] = 'baja'
        
        return estimacion
    
    def generar_urls_busqueda(self, df: pd.DataFrame) -> pd.DataFrame:
        """Genera URLs de búsqueda para cada librería."""
        df_resultado = df.copy()
        
        urls_google_maps = []
        urls_google_busqueda = []
        
        for idx, row in df.iterrows():
            nombre = str(row.get('RAZON_SOCIAL', ''))
            fantasia = str(row.get('NOMBRE_FANTASIA_COMERCIAL', ''))
            canton = str(row.get('DESCRIPCION_CANTON_EST', ''))
            provincia = str(row.get('DESCRIPCION_PROVINCIA_EST', ''))
            
            # Usar nombre fantasia si existe, sino razón social
            nombre_busqueda = fantasia if fantasia != 'N/A' and pd.notna(row.get('NOMBRE_FANTASIA_COMERCIAL')) else nombre
            
            # URL Google Maps
            url_maps = self.buscar_google_maps_url(nombre_busqueda, canton, provincia)
            urls_google_maps.append(url_maps)
            
            # URL Google Búsqueda
            query = f"{nombre_busqueda} {canton} {provincia} librería"
            url_google = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            urls_google_busqueda.append(url_google)
        
        df_resultado['URL_GOOGLE_MAPS'] = urls_google_maps
        df_resultado['URL_GOOGLE_BUSQUEDA'] = urls_google_busqueda
        
        return df_resultado
    
    def procesar_librerias(self, df: pd.DataFrame) -> pd.DataFrame:
        """Procesa todas las librerías y genera estimaciones mejoradas."""
        print("\n📊 Generando estimaciones mejoradas...")
        
        df_resultado = df.copy()
        
        # Generar estimaciones
        estimaciones = []
        for idx, row in df_resultado.iterrows():
            estimacion = self.estimar_por_indicadores(row)
            estimaciones.append(estimacion)
        
        # Agregar columnas de estimación
        df_resultado['ESTIMACION_VENTA_MENSUAL_USD'] = [e['venta_estimada_mensual'] for e in estimaciones]
        df_resultado['ESTIMACION_VENTA_ANUAL_USD'] = [e['venta_estimada_anual'] for e in estimaciones]
        df_resultado['CONFIANZA_ESTIMACION'] = [e['confianza'] for e in estimaciones]
        df_resultado['FACTORES_APLICADOS'] = [', '.join(e['factores_aplicados']) for e in estimaciones]
        
        # Generar URLs de búsqueda
        df_resultado = self.generar_urls_busqueda(df_resultado)
        
        return df_resultado


def main():
    """Función principal."""
    print("="*70)
    print("🌐 ESTIMADOR DE VENTAS USANDO INFORMACIÓN ONLINE")
    print("="*70)
    
    # Cargar datos
    archivo = "../data/output/librerias_detalle.xlsx"
    if not os.path.exists(archivo):
        print(f"\n❌ No se encontró: {archivo}")
        print("   Ejecuta primero: python3 analizar_librerias.py")
        return
    
    print(f"\n📂 Cargando datos de: {archivo}")
    df = pd.read_excel(archivo)
    print(f"   Total de librerías: {len(df):,}")
    
    # Filtrar solo activas para mejor estimación
    activas = df[df['ESTADO_CONTRIBUYENTE'] == 'ACTIVO'].copy()
    print(f"   Librerías activas: {len(activas):,}")
    
    # Procesar
    estimador = EstimadorVentasOnline()
    df_resultado = estimador.procesar_librerias(activas)
    
    # Ordenar por estimación (mayor a menor)
    df_resultado = df_resultado.sort_values('ESTIMACION_VENTA_MENSUAL_USD', ascending=False)
    
    # Exportar
    archivo_salida = "librerias_con_estimaciones_online.xlsx"
    df_resultado.to_excel(archivo_salida, index=False)
    
    print(f"\n✅ Datos exportados a: {archivo_salida}")
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE ESTIMACIONES")
    print("="*70)
    print(f"\nTotal de librerías analizadas: {len(df_resultado):,}")
    print(f"Venta total mensual estimada: ${df_resultado['ESTIMACION_VENTA_MENSUAL_USD'].sum():,.2f} USD")
    print(f"Venta total anual estimada: ${df_resultado['ESTIMACION_VENTA_ANUAL_USD'].sum():,.2f} USD")
    
    print("\n📈 Top 10 librerías por estimación:")
    print("-"*70)
    for idx, (_, row) in enumerate(df_resultado.head(10).iterrows(), 1):
        nombre = row.get('NOMBRE_FANTASIA_COMERCIAL', row.get('RAZON_SOCIAL', 'N/A'))
        venta_mensual = row['ESTIMACION_VENTA_MENSUAL_USD']
        confianza = row['CONFIANZA_ESTIMACION']
        print(f"{idx}. {nombre[:50]}")
        print(f"   Venta estimada: ${venta_mensual:,.2f} USD/mes | Confianza: {confianza}")
    
    print("\n" + "="*70)
    print("💡 PRÓXIMOS PASOS:")
    print("="*70)
    print("1. Abre el archivo Excel generado")
    print("2. Usa las columnas URL_GOOGLE_MAPS para buscar cada librería")
    print("3. Revisa reseñas, fotos, y presencia online")
    print("4. Ajusta las estimaciones manualmente según lo que encuentres")
    print("5. Registra información adicional (reseñas, presencia web, etc.)")
    print("\n⚠️  Estas son ESTIMACIONES mejoradas, no datos reales")
    print("   Úsalas como referencia y valida con búsquedas online")


if __name__ == "__main__":
    main()

