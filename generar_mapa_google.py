"""
Genera un mapa usando Google Maps JavaScript API directamente.
Solo necesitas la API key de Google Maps (la misma que usaste para geocodificación).
"""

import pandas as pd
import json
import os
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Intentar importar Google Maps para geocodificación
try:
    import googlemaps
    GOOGLE_MAPS_AVAILABLE = True
except ImportError:
    GOOGLE_MAPS_AVAILABLE = False
    print("⚠️  googlemaps no instalado. Instala con: pip install googlemaps")
    print("   Usando geocodificación gratuita como respaldo...")


class GeneradorMapaGoogle:
    """Genera mapa usando Google Maps JavaScript API."""
    
    def __init__(self, google_api_key: Optional[str] = None):
        """
        Inicializa el generador.
        
        Args:
            google_api_key: API key de Google Maps (para geocodificación y mapa)
        """
        self.google_api_key = google_api_key
        self.google_client = None
        self.cache_coordenadas = {}
        
        if google_api_key and GOOGLE_MAPS_AVAILABLE:
            try:
                self.google_client = googlemaps.Client(key=google_api_key)
                print("✅ Google Maps API configurada")
            except Exception as e:
                print(f"⚠️  Error al configurar Google Maps: {str(e)}")
        elif not google_api_key:
            print("⚠️  No se proporcionó API key. El mapa funcionará pero sin geocodificación.")
    
    def geocodificar_ubicacion(self, provincia: str = None, canton: str = None) -> Optional[Tuple[float, float]]:
        """Geocodifica usando Google Maps API."""
        if not self.google_client:
            return None
        
        clave = f"{canton or ''}|{provincia or ''}".strip('|')
        if not clave or clave in self.cache_coordenadas:
            return self.cache_coordenadas.get(clave)
        
        try:
            query = f"{canton}, {provincia}, Ecuador" if canton and provincia else f"{provincia}, Ecuador"
            result = self.google_client.geocode(query)
            
            if result and len(result) > 0:
                location = result[0]['geometry']['location']
                coords = (location['lat'], location['lng'])
                self.cache_coordenadas[clave] = coords
                return coords
        except Exception:
            pass
        
        return None
    
    def procesar_excel(self, archivo_excel: str) -> List[Dict]:
        """Procesa Excel y agrupa por ubicación."""
        try:
            df = pd.read_excel(archivo_excel)
            
            print(f"\n📄 Archivo: {os.path.basename(archivo_excel)}")
            print(f"   Total de filas: {len(df):,}")
            
            # Detectar columnas
            col_ruc = next((col for col in df.columns if 'ruc' in col.lower()), None)
            col_nombre = next((col for col in df.columns if any(x in col.lower() for x in ['razon', 'nombre'])), None)
            col_provincia = next((col for col in df.columns if 'provincia' in col.lower()), None)
            col_canton = next((col for col in df.columns if 'canton' in col.lower()), None)
            
            # Agrupar por ubicación
            grupos = defaultdict(list)
            
            for idx, row in df.iterrows():
                provincia = str(row[col_provincia]).strip() if col_provincia and not pd.isna(row[col_provincia]) else None
                canton = str(row[col_canton]).strip() if col_canton and not pd.isna(row[col_canton]) else None
                
                if canton and provincia:
                    clave = f"{canton}, {provincia}"
                elif provincia:
                    clave = provincia
                else:
                    continue
                
                grupos[clave].append({
                    'ruc': str(row[col_ruc]) if col_ruc and not pd.isna(row[col_ruc]) else None,
                    'nombre': str(row[col_nombre]) if col_nombre and not pd.isna(row[col_nombre]) else None,
                    'provincia': provincia,
                    'canton': canton
                })
            
            print(f"   Ubicaciones únicas: {len(grupos)}")
            
            # Geocodificar cada ubicación única
            ubicaciones = []
            total = len(grupos)
            
            for i, (clave, establecimientos) in enumerate(grupos.items(), 1):
                if i % 10 == 0 or i == 1:
                    print(f"   Geocodificando {i}/{total}: {clave}")
                
                provincia = establecimientos[0].get('provincia')
                canton = establecimientos[0].get('canton')
                
                coordenadas = self.geocodificar_ubicacion(provincia, canton)
                
                ubicaciones.append({
                    'ubicacion': clave,
                    'provincia': provincia,
                    'canton': canton,
                    'latitud': coordenadas[0] if coordenadas else None,
                    'longitud': coordenadas[1] if coordenadas else None,
                    'cantidad': len(establecimientos),
                    'establecimientos': establecimientos[:10]
                })
                
                if self.google_client:
                    import time
                    time.sleep(0.1)  # Rate limiting para Google API
            
            return ubicaciones
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def generar_html_google_maps(self, ubicaciones: List[Dict], archivo_salida: str = "mapa_google_maps.html"):
        """Genera HTML con Google Maps JavaScript API."""
        ubicaciones_validas = [u for u in ubicaciones if u.get('latitud') and u.get('longitud')]
        
        if not ubicaciones_validas:
            print("❌ No hay ubicaciones con coordenadas válidas.")
            return
        
        if not self.google_api_key:
            print("❌ Se requiere API key de Google Maps para generar el mapa.")
            print("   Configura tu API key en 'google_maps_api_key.txt' o como variable de entorno.")
            return
        
        print(f"\n🗺️  Generando mapa Google Maps con {len(ubicaciones_validas)} ubicaciones...")
        
        # Calcular centro
        lat_centro = sum(u['latitud'] for u in ubicaciones_validas) / len(ubicaciones_validas)
        lon_centro = sum(u['longitud'] for u in ubicaciones_validas) / len(ubicaciones_validas)
        
        # Preparar datos para JavaScript
        marcadores_js = []
        for ubicacion in ubicaciones_validas:
            establecimientos_texto = '<br>'.join([
                f"• {est.get('nombre', est.get('ruc', 'N/A'))}" 
                for est in ubicacion.get('establecimientos', [])[:5]
            ])
            
            if ubicacion['cantidad'] > 5:
                establecimientos_texto += f"<br><em>... y {ubicacion['cantidad'] - 5:,} más</em>"
            
            # Determinar color según cantidad
            cantidad = ubicacion['cantidad']
            if cantidad > 1000:
                color = '#FF0000'  # Rojo
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
            elif cantidad > 500:
                color = '#FF8800'  # Naranja
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'
            elif cantidad > 100:
                color = '#0000FF'  # Azul
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            else:
                color = '#00FF00'  # Verde
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
            
            marcadores_js.append({
                'lat': ubicacion['latitud'],
                'lng': ubicacion['longitud'],
                'titulo': ubicacion['ubicacion'],
                'cantidad': ubicacion['cantidad'],
                'provincia': ubicacion.get('provincia', 'N/A'),
                'canton': ubicacion.get('canton', 'N/A'),
                'establecimientos': establecimientos_texto,
                'color': color,
                'icon_url': icon_url
            })
        
        # Generar HTML
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa de Establecimientos - SRI Ecuador</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        
        #header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        #header h1 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
        
        #header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        #map {{
            flex: 1;
            width: 100%;
        }}
        
        .info-window {{
            max-width: 300px;
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .info-window h3 {{
            margin: 0 0 10px 0;
            color: #333;
            font-size: 18px;
        }}
        
        .info-window p {{
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }}
        
        .info-window hr {{
            margin: 10px 0;
            border: none;
            border-top: 1px solid #eee;
        }}
        
        .info-window .establecimientos {{
            margin-top: 10px;
            font-size: 13px;
        }}
        
        #stats {{
            background: white;
            padding: 15px 20px;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }}
        
        .stat-item {{
            text-align: center;
            margin: 5px 15px;
        }}
        
        .stat-item .number {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-item .label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>📍 Mapa de Establecimientos - SRI Ecuador</h1>
        <p>Visualización interactiva de ubicaciones de establecimientos registrados</p>
    </div>
    
    <div id="map"></div>
    
    <div id="stats">
        <div class="stat-item">
            <div class="number">{len(ubicaciones_validas)}</div>
            <div class="label">Ubicaciones</div>
        </div>
        <div class="stat-item">
            <div class="number">{sum(u['cantidad'] for u in ubicaciones_validas):,}</div>
            <div class="label">Establecimientos</div>
        </div>
    </div>
    
    <script>
        // Inicializar mapa
        function initMap() {{
            const centro = {{ lat: {lat_centro}, lng: {lon_centro} }};
            
            const map = new google.maps.Map(document.getElementById('map'), {{
                zoom: 7,
                center: centro,
                mapTypeId: 'roadmap',
                styles: [
                    {{
                        featureType: 'poi',
                        elementType: 'labels',
                        stylers: [{{ visibility: 'off' }}]
                    }}
                ]
            }});
            
            // Agregar marcadores
            const marcadores = {json.dumps(marcadores_js)};
            
            marcadores.forEach(marcador => {{
                const marker = new google.maps.Marker({{
                    position: {{ lat: marcador.lat, lng: marcador.lng }},
                    map: map,
                    title: marcador.titulo + ' (' + marcador.cantidad.toLocaleString() + ' establecimientos)',
                    icon: {{
                        url: marcador.icon_url,
                        scaledSize: new google.maps.Size(32, 32)
                    }}
                }});
                
                const infoWindow = new google.maps.InfoWindow({{
                    content: `
                        <div class="info-window">
                            <h3>${{marcador.titulo}}</h3>
                            <p><strong>📍 Establecimientos:</strong> ${{marcador.cantidad.toLocaleString()}}</p>
                            <p><strong>Provincia:</strong> ${{marcador.provincia}}</p>
                            <p><strong>Cantón:</strong> ${{marcador.canton}}</p>
                            <hr>
                            <p><strong>Ejemplos:</strong></p>
                            <div class="establecimientos">${{marcador.establecimientos}}</div>
                        </div>
                    `
                }});
                
                marker.addListener('click', () => {{
                    infoWindow.open(map, marker);
                }});
            }});
            
            // Agregar control de tipo de mapa
            map.setOptions({{
                mapTypeControl: true,
                mapTypeControlOptions: {{
                    style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
                    position: google.maps.ControlPosition.TOP_RIGHT,
                    mapTypeIds: ['roadmap', 'satellite', 'hybrid', 'terrain']
                }}
            }});
        }}
    </script>
    
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key={self.google_api_key}&callback=initMap">
    </script>
</body>
</html>
"""
        
        # Guardar archivo
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ Mapa Google Maps generado: {archivo_salida}")
        print(f"   Abre el archivo en tu navegador para ver el mapa interactivo")


def main():
    """Función principal."""
    # Obtener API key
    google_api_key = None
    
    if os.path.exists('google_maps_api_key.txt'):
        with open('google_maps_api_key.txt', 'r') as f:
            google_api_key = f.read().strip()
    
    if not google_api_key:
        google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not google_api_key:
        print("❌ No se encontró API key de Google Maps.")
        print("   Crea el archivo 'google_maps_api_key.txt' con tu API key")
        print("   O ejecuta: python3 configurar_api_key.py")
        return
    
    directorio_datos = "datos_excel"
    
    if not os.path.exists(directorio_datos):
        print(f"❌ No existe '{directorio_datos}'")
        return
    
    archivos_excel = [f for f in os.listdir(directorio_datos) 
                     if f.endswith(('.xlsx', '.xls')) and not f.startswith('~')]
    
    if not archivos_excel:
        print(f"❌ No se encontraron archivos Excel")
        return
    
    print(f"📊 Archivos Excel encontrados: {len(archivos_excel)}")
    
    generador = GeneradorMapaGoogle(google_api_key=google_api_key)
    todas_ubicaciones = []
    
    for archivo_excel in archivos_excel:
        ruta_completa = os.path.join(directorio_datos, archivo_excel)
        ubicaciones = generador.procesar_excel(ruta_completa)
        todas_ubicaciones.extend(ubicaciones)
    
    if todas_ubicaciones:
        generador.generar_html_google_maps(todas_ubicaciones, "mapa_google_maps.html")
        
        print(f"\n{'='*60}")
        print("✅ PROCESO COMPLETADO")
        print(f"{'='*60}")
        ubicaciones_con_coords = [u for u in todas_ubicaciones if u.get('latitud')]
        print(f"📍 Ubicaciones: {len(ubicaciones_con_coords)}/{len(todas_ubicaciones)}")
        print(f"📊 Total establecimientos: {sum(u['cantidad'] for u in todas_ubicaciones):,}")
        print(f"\n🌐 Abre 'mapa_google_maps.html' en tu navegador")
    else:
        print("❌ No se procesaron ubicaciones")


if __name__ == "__main__":
    main()

