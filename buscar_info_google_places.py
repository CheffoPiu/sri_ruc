"""
Buscador Automático de Información de Librerías en Google Places
Usa la API de Google Places para obtener reseñas, calificaciones, etc.
"""

import pandas as pd
import os
import time
from typing import Dict, List, Optional
import json

# Intentar importar Google Maps
try:
    import googlemaps
    GOOGLE_MAPS_AVAILABLE = True
except ImportError:
    GOOGLE_MAPS_AVAILABLE = False
    print("⚠️  googlemaps no instalado. Instala con: pip install googlemaps")


class BuscadorGooglePlaces:
    """Busca información de librerías usando Google Places API."""
    
    def __init__(self, google_api_key: Optional[str] = None):
        """Inicializa el buscador."""
        self.google_api_key = google_api_key
        self.google_client = None
        self.cache_resultados = {}
        
        if google_api_key and GOOGLE_MAPS_AVAILABLE:
            try:
                self.google_client = googlemaps.Client(key=google_api_key)
                print("✅ Google Places API configurada")
            except Exception as e:
                print(f"⚠️  Error al configurar Google Maps: {str(e)}")
        else:
            print("⚠️  No se puede usar Google Places API sin API key")
    
    def buscar_libreria(self, nombre: str, canton: str, provincia: str) -> Optional[Dict]:
        """
        Busca una librería en Google Places.
        
        Returns:
            Dict con información encontrada o None
        """
        if not self.google_client:
            return None
        
        # Crear query de búsqueda
        query = f"{nombre} librería {canton} {provincia} Ecuador"
        
        # Verificar cache
        if query in self.cache_resultados:
            return self.cache_resultados[query]
        
        try:
            # Buscar usando Places API
            places_result = self.google_client.places(query=query)
            
            if not places_result.get('results'):
                # Intentar sin "librería" en el query
                query2 = f"{nombre} {canton} {provincia} Ecuador"
                places_result = self.google_client.places(query=query2)
            
            if not places_result.get('results'):
                self.cache_resultados[query] = None
                return None
            
            # Tomar el primer resultado (más relevante)
            place = places_result['results'][0]
            place_id = place.get('place_id')
            
            # Obtener detalles completos
            place_details = self.google_client.place(
                place_id=place_id,
                fields=['name', 'rating', 'user_ratings_total', 'formatted_address', 
                       'website', 'formatted_phone_number', 'photo', 'opening_hours']
            )
            
            resultado = place_details.get('result', {})
            
            # Extraer información relevante
            info = {
                'encontrado': True,
                'nombre_google': resultado.get('name', ''),
                'calificacion': resultado.get('rating', 0),
                'numero_resenas': resultado.get('user_ratings_total', 0),
                'direccion': resultado.get('formatted_address', ''),
                'sitio_web': resultado.get('website', ''),
                'telefono': resultado.get('formatted_phone_number', ''),
                'tiene_fotos': 'photo' in resultado,
                'numero_fotos': 1 if 'photo' in resultado else 0,  # La API devuelve info de foto, no lista
                'abierto_ahora': None,
                'place_id': place_id,
                'url_google_maps': f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            }
            
            # Horarios
            if 'opening_hours' in resultado:
                opening_hours = resultado['opening_hours']
                info['abierto_ahora'] = opening_hours.get('open_now', None)
                info['horarios'] = opening_hours.get('weekday_text', [])
            
            self.cache_resultados[query] = info
            return info
            
        except Exception as e:
            print(f"   ⚠️  Error al buscar '{nombre}': {str(e)}")
            self.cache_resultados[query] = None
            return None
    
    def calcular_estimacion_mejorada(self, info_google: Dict, registro: pd.Series) -> Dict:
        """Calcula estimación mejorada basándose en información de Google."""
        if not info_google or not info_google.get('encontrado'):
            return {
                'venta_estimada_mensual': 0,
                'venta_estimada_anual': 0,
                'confianza': 'muy_baja',
                'razon': 'No encontrado en Google Maps'
            }
        
        # Base según número de reseñas
        num_resenas = info_google.get('numero_resenas', 0)
        calificacion = info_google.get('calificacion', 0)
        tiene_web = bool(info_google.get('sitio_web'))
        tiene_fotos = info_google.get('tiene_fotos', False)
        
        # Determinar tamaño base por reseñas
        if num_resenas == 0:
            base_ventas = 5000  # USD/mes
            confianza = 'baja'
        elif num_resenas < 10:
            base_ventas = 10000
            confianza = 'baja'
        elif num_resenas < 50:
            base_ventas = 25000
            confianza = 'media'
        elif num_resenas < 100:
            base_ventas = 50000
            confianza = 'alta'
        else:
            base_ventas = 80000
            confianza = 'alta'
        
        # Ajustes por calificación
        if calificacion >= 4.5:
            base_ventas *= 1.3
        elif calificacion >= 4.0:
            base_ventas *= 1.1
        elif calificacion < 3.5:
            base_ventas *= 0.8
        
        # Ajuste por sitio web
        if tiene_web:
            base_ventas *= 1.5
            confianza = 'alta' if confianza != 'muy_baja' else 'media'
        
        # Ajuste por fotos (más fotos = más actividad)
        if tiene_fotos:
            num_fotos = info_google.get('numero_fotos', 0)
            if num_fotos > 5:
                base_ventas *= 1.2
        
        # Ajuste por estado del contribuyente
        if registro.get('ESTADO_CONTRIBUYENTE') == 'ACTIVO':
            base_ventas *= 1.2
        elif 'SUSPENDIDO' in str(registro.get('ESTADO_CONTRIBUYENTE', '')):
            base_ventas *= 0.3
        
        return {
            'venta_estimada_mensual': round(base_ventas, 2),
            'venta_estimada_anual': round(base_ventas * 12, 2),
            'confianza': confianza,
            'razon': f'Basado en {num_resenas} reseñas, calificación {calificacion}'
        }


def procesar_librerias_con_google():
    """Procesa librerías y busca información en Google Places."""
    print("="*70)
    print("🔍 BUSCADOR AUTOMÁTICO DE INFORMACIÓN EN GOOGLE PLACES")
    print("="*70)
    
    # Cargar API key
    google_api_key = None
    if os.path.exists('google_maps_api_key.txt'):
        with open('google_maps_api_key.txt', 'r') as f:
            google_api_key = f.read().strip()
    
    if not google_api_key:
        print("\n❌ No se encontró API key de Google Maps")
        print("   Asegúrate de tener el archivo 'google_maps_api_key.txt'")
        print("   Y que la API key tenga habilitada 'Places API'")
        return
    
    # Verificar que Places API esté disponible
    if not GOOGLE_MAPS_AVAILABLE:
        print("\n❌ googlemaps no está instalado")
        print("   Instala con: pip install googlemaps")
        return
    
    # Cargar datos
    archivo = "librerias_detalle.xlsx"
    if not os.path.exists(archivo):
        print(f"\n❌ No se encontró: {archivo}")
        return
    
    print(f"\n📂 Cargando datos de: {archivo}")
    df = pd.read_excel(archivo)
    
    # Filtrar solo activas
    activas = df[df['ESTADO_CONTRIBUYENTE'] == 'ACTIVO'].copy()
    print(f"   Librerías activas: {len(activas):,}")
    
    # Inicializar buscador
    buscador = BuscadorGooglePlaces(google_api_key)
    
    if not buscador.google_client:
        print("\n❌ No se pudo inicializar Google Places API")
        print("   Verifica que tu API key tenga habilitada 'Places API'")
        print("   Ve a: https://console.cloud.google.com/apis/library/places-backend.googleapis.com")
        return
    
    print("\n🔍 Buscando información en Google Places...")
    print("   (Esto puede tomar varios minutos)")
    print()
    
    # Procesar cada librería
    resultados_google = []
    estimaciones_mejoradas = []
    
    total = len(activas)
    encontrados = 0
    
    for idx, (_, row) in enumerate(activas.iterrows(), 1):
        nombre = str(row.get('RAZON_SOCIAL', ''))
        fantasia = str(row.get('NOMBRE_FANTASIA_COMERCIAL', ''))
        canton = str(row.get('DESCRIPCION_CANTON_EST', ''))
        provincia = str(row.get('DESCRIPCION_PROVINCIA_EST', ''))
        
        # Usar nombre fantasia si existe
        nombre_busqueda = fantasia if fantasia != 'N/A' and pd.notna(row.get('NOMBRE_FANTASIA_COMERCIAL')) else nombre
        
        print(f"[{idx}/{total}] Buscando: {nombre_busqueda[:50]}...", end=' ')
        
        # Buscar en Google Places
        info_google = buscador.buscar_libreria(nombre_busqueda, canton, provincia)
        
        if info_google and info_google.get('encontrado'):
            encontrados += 1
            print(f"✅ Encontrado ({info_google.get('numero_resenas', 0)} reseñas)")
        else:
            print("❌ No encontrado")
        
        resultados_google.append(info_google if info_google else {})
        
        # Calcular estimación mejorada
        estimacion = buscador.calcular_estimacion_mejorada(
            info_google if info_google else {}, 
            row
        )
        estimaciones_mejoradas.append(estimacion)
        
        # Rate limiting (evitar exceder límites de API)
        time.sleep(0.2)  # 200ms entre búsquedas
    
    # Agregar resultados al DataFrame
    print("\n📊 Procesando resultados...")
    
    # Crear columnas con información de Google
    activas['ENCONTRADO_GOOGLE'] = [r.get('encontrado', False) if r else False for r in resultados_google]
    activas['NOMBRE_GOOGLE'] = [r.get('nombre_google', '') if r else '' for r in resultados_google]
    activas['CALIFICACION_GOOGLE'] = [r.get('calificacion', 0) if r else 0 for r in resultados_google]
    activas['NUMERO_RESENAS'] = [r.get('numero_resenas', 0) if r else 0 for r in resultados_google]
    activas['DIRECCION_GOOGLE'] = [r.get('direccion', '') if r else '' for r in resultados_google]
    activas['SITIO_WEB'] = [r.get('sitio_web', '') if r else '' for r in resultados_google]
    activas['TELEFONO_GOOGLE'] = [r.get('telefono', '') if r else '' for r in resultados_google]
    activas['TIENE_FOTOS'] = [r.get('tiene_fotos', False) if r else False for r in resultados_google]
    activas['NUMERO_FOTOS'] = [r.get('numero_fotos', 0) if r else 0 for r in resultados_google]
    activas['URL_GOOGLE_MAPS'] = [r.get('url_google_maps', '') if r else '' for r in resultados_google]
    
    # Agregar estimaciones mejoradas
    activas['ESTIMACION_VENTA_MENSUAL'] = [e['venta_estimada_mensual'] for e in estimaciones_mejoradas]
    activas['ESTIMACION_VENTA_ANUAL'] = [e['venta_estimada_anual'] for e in estimaciones_mejoradas]
    activas['CONFIANZA_ESTIMACION'] = [e['confianza'] for e in estimaciones_mejoradas]
    activas['RAZON_ESTIMACION'] = [e['razon'] for e in estimaciones_mejoradas]
    
    # Ordenar por estimación
    activas = activas.sort_values('ESTIMACION_VENTA_MENSUAL', ascending=False)
    
    # Exportar
    archivo_salida = "librerias_con_info_google.xlsx"
    activas.to_excel(archivo_salida, index=False)
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("✅ PROCESO COMPLETADO")
    print("="*70)
    print(f"\n📊 Resultados:")
    print(f"   Total procesadas: {total}")
    print(f"   Encontradas en Google: {encontrados} ({encontrados/total*100:.1f}%)")
    print(f"   No encontradas: {total - encontrados}")
    
    # Estadísticas de reseñas
    encontradas = activas[activas['ENCONTRADO_GOOGLE'] == True]
    if len(encontradas) > 0:
        print(f"\n📈 Estadísticas de librerías encontradas:")
        print(f"   Promedio de reseñas: {encontradas['NUMERO_RESENAS'].mean():.1f}")
        print(f"   Promedio de calificación: {encontradas['CALIFICACION_GOOGLE'].mean():.2f}")
        print(f"   Con sitio web: {encontradas['SITIO_WEB'].notna().sum()}")
        print(f"   Con fotos: {encontradas['TIENE_FOTOS'].sum()}")
    
    # Estimaciones totales
    print(f"\n💰 Estimaciones de ventas:")
    print(f"   Venta total mensual estimada: ${activas['ESTIMACION_VENTA_MENSUAL'].sum():,.2f} USD")
    print(f"   Venta total anual estimada: ${activas['ESTIMACION_VENTA_ANUAL'].sum():,.2f} USD")
    
    print(f"\n📁 Archivo generado: {archivo_salida}")
    print("\n💡 Revisa el archivo Excel para ver toda la información obtenida")


if __name__ == "__main__":
    procesar_librerias_con_google()

