"""
Genera mapa filtrando por códigos CIIU específicos.
Filtra los datos de Excel antes de generar el mapa.
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


class GeneradorMapaFiltrado:
    """Genera mapa filtrando por códigos CIIU y/o provincias."""
    
    def __init__(self, google_api_key: Optional[str] = None, codigos_ciiu: List[str] = None, provincias: List[str] = None):
        """
        Inicializa el generador.
        
        Args:
            google_api_key: API key de Google Maps
            codigos_ciiu: Lista de códigos CIIU para filtrar (opcional)
            provincias: Lista de provincias para filtrar (opcional)
        """
        self.google_api_key = google_api_key
        self.google_client = None
        self.cache_coordenadas = {}
        self.codigos_ciiu = codigos_ciiu or []
        self.provincias = provincias or []
        
        if google_api_key and GOOGLE_MAPS_AVAILABLE:
            try:
                self.google_client = googlemaps.Client(key=google_api_key)
                print("✅ Google Maps API configurada")
            except Exception as e:
                print(f"⚠️  Error al configurar Google Maps: {str(e)}")
    
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
    
    def filtrar_excel(self, archivo_excel: str, codigos_ciiu: List[str] = None, provincias: List[str] = None, estados: List[str] = None) -> pd.DataFrame:
        """
        Lee y filtra un archivo Excel por códigos CIIU y/o provincias.
        
        Args:
            archivo_excel: Ruta al archivo Excel
            codigos_ciiu: Lista de códigos CIIU a filtrar (opcional)
            provincias: Lista de provincias a filtrar (opcional)
            
        Returns:
            DataFrame filtrado
        """
        try:
            print(f"\n📄 Leyendo: {os.path.basename(archivo_excel)}")
            df = pd.read_excel(archivo_excel)
            
            print(f"   Total de filas antes del filtro: {len(df):,}")
            
            # Detectar columna de provincia
            col_provincia = next((col for col in df.columns if 'provincia' in col.lower()), None)
            
            # Aplicar filtros
            df_filtrado = df.copy()
            
            # Filtrar por códigos CIIU si se especifican
            if codigos_ciiu:
                if 'CODIGO_CIIU' not in df.columns:
                    print(f"   ⚠️  No se encontró la columna CODIGO_CIIU")
                    return pd.DataFrame()
                df_filtrado = df_filtrado[df_filtrado['CODIGO_CIIU'].isin(codigos_ciiu)]
                print(f"   Después de filtrar por CIIU: {len(df_filtrado):,} filas")
            
            # Filtrar por provincias si se especifican
            if provincias and col_provincia:
                # Normalizar nombres de provincias (mayúsculas, sin espacios extra)
                provincias_normalizadas = [p.upper().strip() for p in provincias]
                df_filtrado = df_filtrado[
                    df_filtrado[col_provincia].str.upper().str.strip().isin(provincias_normalizadas)
                ]
                print(f"   Después de filtrar por provincia: {len(df_filtrado):,} filas")
            
            # Filtrar por estados si se especifican
            if estados:
                col_estado = next((col for col in df_filtrado.columns if 'estado_contribuyente' in col.lower()), None)
                if col_estado:
                    estados_normalizados = [e.upper().strip() for e in estados]
                    df_filtrado = df_filtrado[
                        df_filtrado[col_estado].astype(str).str.upper().str.strip().isin(estados_normalizados)
                    ]
                    print(f"   Después de filtrar por estado: {len(df_filtrado):,} filas")
            
            print(f"   ✅ Filas después de todos los filtros: {len(df_filtrado):,}")
            
            # Mostrar distribución por código CIIU si hay filtro
            if codigos_ciiu and len(df_filtrado) > 0 and 'CODIGO_CIIU' in df_filtrado.columns:
                print(f"\n   Distribución por código CIIU:")
                distribucion = df_filtrado['CODIGO_CIIU'].value_counts()
                for codigo, cantidad in distribucion.items():
                    print(f"      {codigo}: {cantidad:,} establecimientos")
            
            # Mostrar distribución por provincia si hay filtro
            if provincias and col_provincia and len(df_filtrado) > 0:
                print(f"\n   Distribución por provincia:")
                distribucion = df_filtrado[col_provincia].value_counts()
                for provincia, cantidad in distribucion.items():
                    print(f"      {provincia}: {cantidad:,} establecimientos")
            
            return df_filtrado
            
        except Exception as e:
            print(f"   ❌ Error al leer archivo: {str(e)}")
            return pd.DataFrame()
    
    def procesar_datos_filtrados(self, df: pd.DataFrame) -> List[Dict]:
        """Procesa datos filtrados y agrupa por ubicación."""
        if df.empty:
            return []
        
        # Detectar columnas
        col_ruc = next((col for col in df.columns if 'ruc' in col.lower()), None)
        col_nombre = next((col for col in df.columns if any(x in col.lower() for x in ['razon', 'nombre'])), None)
        col_provincia = next((col for col in df.columns if 'provincia' in col.lower()), None)
        col_canton = next((col for col in df.columns if 'canton' in col.lower()), None)
        col_ciiu = next((col for col in df.columns if 'ciiu' in col.lower()), None)
        col_actividad = next((col for col in df.columns if 'actividad' in col.lower()), None)
        col_estado = next((col for col in df.columns if 'estado_contribuyente' in col.lower()), None)
        
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
                'canton': canton,
                'codigo_ciiu': str(row[col_ciiu]) if col_ciiu and not pd.isna(row[col_ciiu]) else None,
                'actividad': str(row[col_actividad]) if col_actividad and not pd.isna(row[col_actividad]) else None,
                'estado': str(row[col_estado]).strip() if col_estado and not pd.isna(row[col_estado]) else None
            })
        
        print(f"\n   Ubicaciones únicas encontradas: {len(grupos)}")
        
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
                    'establecimientos': establecimientos[:10],  # Solo primeros 10 para el popup
                    'establecimientos_todos': establecimientos,  # TODOS para la tabla
                    'codigos_ciiu': list(set([e.get('codigo_ciiu') for e in establecimientos if e.get('codigo_ciiu')]))
                })
            
            if self.google_client:
                import time
                time.sleep(0.1)
        
        return ubicaciones
    
    def generar_html_google_maps(self, ubicaciones: List[Dict], archivo_salida: str = "mapa_google_maps_filtrado.html"):
        """Genera HTML con Google Maps JavaScript API."""
        ubicaciones_validas = [u for u in ubicaciones if u.get('latitud') and u.get('longitud')]
        
        if not ubicaciones_validas:
            print("❌ No hay ubicaciones con coordenadas válidas.")
            return
        
        if not self.google_api_key:
            print("❌ Se requiere API key de Google Maps.")
            return
        
        print(f"\n🗺️  Generando mapa con {len(ubicaciones_validas)} ubicaciones...")
        
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
                color = '#FF0000'
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
            elif cantidad > 500:
                color = '#FF8800'
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'
            elif cantidad > 100:
                color = '#0000FF'
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            else:
                color = '#00FF00'
                icon_url = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
            
            codigos_texto = ', '.join(ubicacion.get('codigos_ciiu', []))
            
            # Preparar datos completos de establecimientos para la tabla (TODOS los establecimientos)
            establecimientos_completos = []
            # Usar establecimientos_todos si existe, sino usar todos los disponibles
            establecimientos_para_tabla = ubicacion.get('establecimientos_todos', ubicacion.get('establecimientos', []))
            for est in establecimientos_para_tabla:
                estado = est.get('estado', 'N/A')
                # Determinar si está activo o no
                estado_display = estado
                if estado and estado.upper() in ['ACTIVO', 'PASIVO']:
                    estado_display = estado
                elif estado and 'SUSPENDIDO' in estado.upper():
                    estado_display = 'SUSPENDIDO'
                else:
                    estado_display = estado if estado != 'N/A' else 'N/A'
                
                establecimientos_completos.append({
                    'ruc': est.get('ruc', 'N/A'),
                    'nombre': est.get('nombre', 'N/A'),
                    'codigo_ciiu': est.get('codigo_ciiu', 'N/A'),
                    'actividad': est.get('actividad', 'N/A'),
                    'estado': estado_display
                })
            
            marcadores_js.append({
                'lat': ubicacion['latitud'],
                'lng': ubicacion['longitud'],
                'titulo': ubicacion['ubicacion'],
                'cantidad': ubicacion['cantidad'],
                'provincia': ubicacion.get('provincia', 'N/A'),
                'canton': ubicacion.get('canton', 'N/A'),
                'codigos_ciiu': codigos_texto,
                'establecimientos': establecimientos_texto,
                'establecimientos_completos': establecimientos_completos,
                'color': color,
                'icon_url': icon_url
            })
        
        # Obtener lista única de provincias
        provincias_disponibles = sorted(list(set([u.get('provincia') for u in ubicaciones_validas if u.get('provincia')])))
        
        # Obtener lista única de estados de todos los establecimientos
        estados_disponibles = set()
        for ubicacion in ubicaciones_validas:
            for est in ubicacion.get('establecimientos_todos', ubicacion.get('establecimientos', [])):
                estado = est.get('estado')
                if estado and estado != 'N/A':
                    # Normalizar estado
                    estado_upper = estado.upper().strip()
                    if 'SUSPENDIDO' in estado_upper:
                        estados_disponibles.add('SUSPENDIDO')
                    elif estado_upper == 'ACTIVO' or estado_upper == 'PASIVO':
                        estados_disponibles.add(estado_upper)
                    else:
                        estados_disponibles.add(estado)
        estados_disponibles = sorted(list(estados_disponibles))
        
        # Generar HTML
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa de Establecimientos - Filtrado por CIIU</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }}
        
        #header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        #header h1 {{
            font-size: 20px;
            margin: 0;
            margin-right: 20px;
        }}
        
        #header p {{
            font-size: 12px;
            opacity: 0.9;
            margin: 0;
        }}
        
        #map {{
            width: 100%;
            height: 70vh;
            min-height: 500px;
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
        
        #tabla-detalle {{
            background: white;
            padding: 0;
            border-top: 3px solid #667eea;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-in-out, padding 0.4s ease-in-out;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            width: 100%;
        }}
        
        #tabla-detalle.visible {{
            max-height: none;
            padding: 20px;
            overflow-y: visible;
        }}
        
        #contenido-tabla {{
            max-height: 60vh;
            overflow-y: auto;
        }}
        
        #tabla-detalle h3 {{
            margin: 0 0 15px 0;
            color: #333;
            font-size: 18px;
        }}
        
        #tabla-detalle .info-ubicacion {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }}
        
        #tabla-detalle .info-ubicacion p {{
            margin: 5px 0;
            color: #666;
        }}
        
        .tabla-establecimientos {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        .tabla-establecimientos thead {{
            background: #667eea;
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .tabla-establecimientos th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        .tabla-establecimientos td {{
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
        }}
        
        .tabla-establecimientos tbody tr:hover {{
            background: #f9f9f9;
        }}
        
        .tabla-establecimientos tbody tr:nth-child(even) {{
            background: #fafafa;
        }}
        
        .cerrar-tabla {{
            float: right;
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-bottom: 15px;
        }}
        
        .cerrar-tabla:hover {{
            background: #c82333;
        }}
        
        .tabla-header {{
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
        }}
        
        .tabla-header h3 {{
            margin: 0;
            color: #333;
            font-size: 18px;
        }}
        
        .filtro-estado-tabla {{
            margin-bottom: 15px;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }}
        
        .filtro-estado-tabla h4 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #495057;
            font-weight: 600;
        }}
        
        .filtro-estado-opciones {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}
        
        .checkbox-estado-tabla {{
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            background: white;
            border: 1px solid #ced4da;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .checkbox-estado-tabla:hover {{
            border-color: #667eea;
            background: #f0f4ff;
        }}
        
        .checkbox-estado-tabla input[type="checkbox"] {{
            cursor: pointer;
            margin: 0;
        }}
        
        .checkbox-estado-tabla label {{
            cursor: pointer;
            margin: 0;
            font-size: 13px;
            color: #495057;
            user-select: none;
        }}
        
        .checkbox-estado-tabla.activa {{
            background: #667eea;
            border-color: #667eea;
            color: white;
        }}
        
        .checkbox-estado-tabla.activa label {{
            color: white;
        }}
        
        .tabla-establecimientos tbody tr.filtrado-oculto {{
            display: none;
        }}
        
        #filtros {{
            background: white;
            padding: 10px 20px;
            border-bottom: 1px solid #eee;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .filtro-izquierda {{
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .filtro-izquierda h3 {{
            margin: 0;
            font-size: 14px;
            color: #333;
            font-weight: 600;
        }}
        
        .filtro-provincias {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }}
        
        .checkbox-provincia {{
            display: flex;
            align-items: center;
            padding: 6px 12px;
            background: #f5f5f5;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
        }}
        
        .checkbox-provincia:hover {{
            background: #e8e8e8;
        }}
        
        .checkbox-provincia input[type="checkbox"] {{
            margin-right: 6px;
            cursor: pointer;
            width: 16px;
            height: 16px;
        }}
        
        .checkbox-provincia label {{
            cursor: pointer;
            font-size: 13px;
            color: #333;
            margin: 0;
        }}
        
        .checkbox-provincia.activa {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .checkbox-provincia.activa label {{
            color: white;
        }}
        
        .botones-filtro {{
            display: flex;
            gap: 8px;
        }}
        
        .btn-filtro {{
            padding: 6px 15px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            transition: background 0.3s;
            white-space: nowrap;
        }}
        
        .btn-filtro:hover {{
            background: #5568d3;
        }}
        
        .btn-filtro:active {{
            background: #4457c2;
        }}
    </style>
</head>
<body>
    <div id="header">
        <div>
            <h1>📍 Mapa de Establecimientos - Filtrado</h1>
            <p>
                {f"Códigos CIIU: {', '.join(self.codigos_ciiu)}" if self.codigos_ciiu else "Códigos CIIU: Todos"}
            </p>
        </div>
        <div id="filtros">
            <div class="filtro-izquierda">
                <h3>🔍 Provincias:</h3>
                <div class="filtro-provincias">
                    {''.join([f'''
                    <div class="checkbox-provincia activa" data-provincia="{prov}">
                        <input type="checkbox" id="prov_{prov.replace(' ', '_')}" checked onchange="toggleProvincia('{prov}')">
                        <label for="prov_{prov.replace(' ', '_')}">{prov}</label>
                    </div>''' for prov in provincias_disponibles])}
                </div>
            </div>
            <div class="botones-filtro">
                <button class="btn-filtro" onclick="seleccionarTodas()">✅ Todas</button>
                <button class="btn-filtro" onclick="deseleccionarTodas()">❌ Ninguna</button>
            </div>
        </div>
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
    
    <div id="tabla-detalle">
        <button class="cerrar-tabla" onclick="cerrarTabla()" title="Cerrar tabla">✕</button>
        <div class="tabla-header">
            <h3 id="titulo-tabla">Detalle de Establecimientos</h3>
        </div>
        <div id="contenido-tabla"></div>
    </div>
    
    <script>
        let map;
        let todosLosMarcadores = [];
        let marcadoresVisibles = [];
        const provinciasDisponibles = {json.dumps(provincias_disponibles)};
        
        function initMap() {{
            const centro = {{ lat: {lat_centro}, lng: {lon_centro} }};
            
            map = new google.maps.Map(document.getElementById('map'), {{
                zoom: 7,
                center: centro,
                mapTypeId: 'roadmap'
            }});
            
            const marcadores = {json.dumps(marcadores_js)};
            
            // Crear todos los marcadores
            marcadores.forEach(marcador => {{
                const marker = new google.maps.Marker({{
                    position: {{ lat: marcador.lat, lng: marcador.lng }},
                    map: map,
                    title: marcador.titulo + ' (' + marcador.cantidad.toLocaleString() + ' establecimientos)',
                    icon: {{
                        url: marcador.icon_url,
                        scaledSize: new google.maps.Size(32, 32)
                    }},
                    provincia: marcador.provincia
                }});
                
                const infoWindow = new google.maps.InfoWindow({{
                    content: `
                        <div class="info-window">
                            <h3>${{marcador.titulo}}</h3>
                            <p><strong>📍 Establecimientos:</strong> ${{marcador.cantidad.toLocaleString()}}</p>
                            <p><strong>Provincia:</strong> ${{marcador.provincia}}</p>
                            <p><strong>Cantón:</strong> ${{marcador.canton}}</p>
                            <p><strong>Códigos CIIU:</strong> ${{marcador.codigos_ciiu}}</p>
                            <hr>
                            <p><strong>Ejemplos:</strong></p>
                            <div class="establecimientos">${{marcador.establecimientos}}</div>
                        </div>
                    `
                }});
                
                marker.addListener('click', () => {{
                    infoWindow.open(map, marker);
                    mostrarTablaDetalle(marcador);
                }});
                
                todosLosMarcadores.push(marker);
                marcadoresVisibles.push(marker);
            }});
            
            actualizarEstadisticas();
        }}
        
        function toggleProvincia(provincia) {{
            const checkbox = document.getElementById('prov_' + provincia.replace(' ', '_'));
            const div = checkbox.closest('.checkbox-provincia');
            
            if (checkbox.checked) {{
                div.classList.add('activa');
                mostrarProvincia(provincia);
            }} else {{
                div.classList.remove('activa');
                ocultarProvincia(provincia);
            }}
            
            actualizarEstadisticas();
        }}
        
        function mostrarProvincia(provincia) {{
            todosLosMarcadores.forEach(marker => {{
                if (marker.provincia === provincia && !marcadoresVisibles.includes(marker)) {{
                    marker.setMap(map);
                    marcadoresVisibles.push(marker);
                }}
            }});
        }}
        
        function ocultarProvincia(provincia) {{
            todosLosMarcadores.forEach((marker, index) => {{
                if (marker.provincia === provincia) {{
                    marker.setMap(null);
                    const idx = marcadoresVisibles.indexOf(marker);
                    if (idx > -1) {{
                        marcadoresVisibles.splice(idx, 1);
                    }}
                }}
            }});
        }}
        
        function seleccionarTodas() {{
            provinciasDisponibles.forEach(prov => {{
                const checkbox = document.getElementById('prov_' + prov.replace(' ', '_'));
                if (!checkbox.checked) {{
                    checkbox.checked = true;
                    toggleProvincia(prov);
                }}
            }});
        }}
        
        function deseleccionarTodas() {{
            provinciasDisponibles.forEach(prov => {{
                const checkbox = document.getElementById('prov_' + prov.replace(' ', '_'));
                if (checkbox.checked) {{
                    checkbox.checked = false;
                    toggleProvincia(prov);
                }}
            }});
        }}
        
        function actualizarEstadisticas() {{
            const ubicaciones = marcadoresVisibles.length;
            const establecimientos = todosLosMarcadores
                .filter(m => marcadoresVisibles.includes(m))
                .reduce((sum, m) => {{
                    const cantidad = parseInt(m.title.match(/(\d{{1,3}}(?:,\d{{3}})*)/)?.[1]?.replace(/,/g, '') || '0');
                    return sum + cantidad;
                }}, 0);
            
            document.querySelector('.stat-item .number').textContent = ubicaciones;
            document.querySelectorAll('.stat-item .number')[1].textContent = establecimientos.toLocaleString();
        }}
        
        function mostrarTablaDetalle(marcador) {{
            const tablaDetalle = document.getElementById('tabla-detalle');
            const tituloTabla = document.getElementById('titulo-tabla');
            const contenidoTabla = document.getElementById('contenido-tabla');
            
            tituloTabla.textContent = `Detalle de Establecimientos - ${{marcador.titulo}}`;
            
            // Obtener estados únicos de los establecimientos
            const estadosEnTabla = new Set();
            marcador.establecimientos_completos.forEach(est => {{
                const estado = est.estado || 'N/A';
                if (estado !== 'N/A') {{
                    const estadoUpper = estado.toUpperCase().trim();
                    if (estadoUpper.includes('SUSPENDIDO')) {{
                        estadosEnTabla.add('SUSPENDIDO');
                    }} else if (estadoUpper === 'ACTIVO' || estadoUpper === 'PASIVO') {{
                        estadosEnTabla.add(estadoUpper);
                    }} else {{
                        estadosEnTabla.add(estado);
                    }}
                }} else {{
                    estadosEnTabla.add('N/A');
                }}
            }});
            
            const estadosArray = Array.from(estadosEnTabla).sort();
            
            // Generar HTML del filtro de estado
            let filtroEstadosHtml = '';
            if (estadosArray.length > 0) {{
                const checkboxesEstados = estadosArray.map(estado => {{
                    const estadoId = estado.replace(/[^a-zA-Z0-9]/g, '_');
                    return `
                        <div class="checkbox-estado-tabla activa" data-estado-tabla="${{estado}}">
                            <input type="checkbox" id="filtro_estado_${{estadoId}}" checked onchange="filtrarTablaPorEstado()">
                            <label for="filtro_estado_${{estadoId}}">${{estado}}</label>
                        </div>`;
                }}).join('');
                
                filtroEstadosHtml = `
                <div class="filtro-estado-tabla">
                    <h4>🔍 Filtrar por Estado:</h4>
                    <div class="filtro-estado-opciones">
                        ${{checkboxesEstados}}
                    </div>
                </div>`;
            }}
            
            // Guardar el total original para referencia
            const totalOriginal = marcador.cantidad;
            
            let html = `
                <div class="info-ubicacion">
                    <p><strong>📍 Ubicación:</strong> ${{marcador.titulo}}</p>
                    <p><strong>Provincia:</strong> ${{marcador.provincia}}</p>
                    <p><strong>Cantón:</strong> ${{marcador.canton}}</p>
                    <p><strong>Total Establecimientos:</strong> <span id="contador-establecimientos">${{totalOriginal.toLocaleString()}}</span> <span id="contador-filtrado" style="color: #667eea; font-weight: normal;"></span></p>
                    <p><strong>Códigos CIIU:</strong> ${{marcador.codigos_ciiu}}</p>
                </div>
                ${{filtroEstadosHtml}}
                <table class="tabla-establecimientos">
                    <thead>
                        <tr>
                            <th>RUC</th>
                            <th>Nombre / Razón Social</th>
                            <th>Código CIIU</th>
                            <th>Estado</th>
                            <th>Actividad Económica</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            marcador.establecimientos_completos.forEach(est => {{
                // Determinar color del estado
                const estado = est.estado || 'N/A';
                let estadoClass = '';
                let estadoColor = '#666';
                let estadoNormalizado = estado;
                
                // Normalizar estado para el filtro
                const estadoUpper = estado.toUpperCase().trim();
                if (estadoUpper.includes('SUSPENDIDO')) {{
                    estadoClass = 'estado-suspendido';
                    estadoColor = '#dc3545';
                    estadoNormalizado = 'SUSPENDIDO';
                }} else if (estadoUpper === 'ACTIVO' || estadoUpper === 'PASIVO') {{
                    estadoClass = 'estado-activo';
                    estadoColor = '#28a745';
                    estadoNormalizado = estadoUpper;
                }} else {{
                    estadoNormalizado = 'N/A';
                }}
                
                html += `
                    <tr data-estado="${{estadoNormalizado}}">
                        <td>${{est.ruc}}</td>
                        <td>${{est.nombre}}</td>
                        <td>${{est.codigo_ciiu}}</td>
                        <td style="color: ${{estadoColor}}; font-weight: 600;">${{estado}}</td>
                        <td>${{est.actividad}}</td>
                    </tr>
                `;
            }});
            
            html += `
                    </tbody>
                </table>
            `;
            
            contenidoTabla.innerHTML = html;
            tablaDetalle.classList.add('visible');
            
            // Aplicar filtro inicial
            filtrarTablaPorEstado();
        }}
        
        function filtrarTablaPorEstado() {{
            // Obtener estados seleccionados
            const checkboxes = document.querySelectorAll('.checkbox-estado-tabla input[type="checkbox"]');
            const estadosSeleccionados = [];
            
            checkboxes.forEach(checkbox => {{
                const div = checkbox.closest('.checkbox-estado-tabla');
                if (checkbox.checked) {{
                    estadosSeleccionados.push(div.getAttribute('data-estado-tabla'));
                    div.classList.add('activa');
                }} else {{
                    div.classList.remove('activa');
                }}
            }});
            
            // Filtrar filas de la tabla
            const filas = document.querySelectorAll('.tabla-establecimientos tbody tr');
            let filasVisibles = 0;
            
            filas.forEach(fila => {{
                const estadoFila = fila.getAttribute('data-estado');
                if (estadosSeleccionados.includes(estadoFila)) {{
                    fila.classList.remove('filtrado-oculto');
                    filasVisibles++;
                }} else {{
                    fila.classList.add('filtrado-oculto');
                }}
            }});
            
            // Actualizar contador de establecimientos visibles
            const contadorEstablecimientos = document.getElementById('contador-establecimientos');
            const contadorFiltrado = document.getElementById('contador-filtrado');
            const infoUbicacion = document.querySelector('.info-ubicacion');
            
            if (contadorEstablecimientos && infoUbicacion) {{
                // Obtener el total original del texto
                const totalP = infoUbicacion.querySelector('p:nth-child(4)');
                if (totalP) {{
                    // Extraer el número original si existe un atributo data-total
                    // Si no, usar el número de filas totales
                    const totalFilas = document.querySelectorAll('.tabla-establecimientos tbody tr').length;
                    
                    // Actualizar el contador con el número de filas visibles
                    contadorEstablecimientos.textContent = filasVisibles.toLocaleString();
                    
                    // Mostrar información adicional si hay filtro activo
                    if (filasVisibles < totalFilas) {{
                        contadorFiltrado.textContent = `(de ${{totalFilas.toLocaleString()}} total)`;
                        contadorFiltrado.style.display = 'inline';
                    }} else {{
                        contadorFiltrado.textContent = '';
                        contadorFiltrado.style.display = 'none';
                    }}
                }}
            }}
        }}
        
        function cerrarTabla() {{
            const tablaDetalle = document.getElementById('tabla-detalle');
            tablaDetalle.classList.remove('visible');
        }}
        
        // Función global para llamar desde el popup
        window.mostrarTablaDetalle = mostrarTablaDetalle;
        window.filtrarTablaPorEstado = filtrarTablaPorEstado;
    </script>
    
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key={self.google_api_key}&callback=initMap">
    </script>
</body>
</html>
"""
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ Mapa generado: {archivo_salida}")


def detectar_provincia_archivo(nombre_archivo: str) -> Optional[str]:
    """Detecta la provincia basándose en el nombre del archivo."""
    nombre_upper = nombre_archivo.upper()
    
    if 'ORO' in nombre_upper:
        return 'EL ORO'
    elif 'GALAPAGOS' in nombre_upper or 'GALÁPAGOS' in nombre_upper:
        return 'GALAPAGOS'
    elif 'PICHINCHA' in nombre_upper:
        return 'PICHINCHA'
    elif 'GUAYAS' in nombre_upper:
        return 'GUAYAS'
    elif 'MANABI' in nombre_upper or 'MANABÍ' in nombre_upper:
        return 'MANABI'
    elif 'AZUAY' in nombre_upper:
        return 'AZUAY'
    elif 'LOJA' in nombre_upper:
        return 'LOJA'
    elif 'TUNGURAHUA' in nombre_upper:
        return 'TUNGURAHUA'
    elif 'IMBABURA' in nombre_upper:
        return 'IMBABURA'
    elif 'ESMERALDAS' in nombre_upper:
        return 'ESMERALDAS'
    elif 'LOS RIOS' in nombre_upper or 'LOS RÍOS' in nombre_upper:
        return 'LOS RIOS'
    elif 'BOLIVAR' in nombre_upper or 'BOLÍVAR' in nombre_upper:
        return 'BOLIVAR'
    elif 'COTOPAXI' in nombre_upper:
        return 'COTOPAXI'
    elif 'CHIMBORAZO' in nombre_upper:
        return 'CHIMBORAZO'
    elif 'CAÑAR' in nombre_upper or 'CANAR' in nombre_upper:
        return 'CAÑAR'
    elif 'MORONA SANTIAGO' in nombre_upper:
        return 'MORONA SANTIAGO'
    elif 'NAPO' in nombre_upper:
        return 'NAPO'
    elif 'ORELLANA' in nombre_upper:
        return 'ORELLANA'
    elif 'PASTAZA' in nombre_upper:
        return 'PASTAZA'
    elif 'SUCUMBIOS' in nombre_upper:
        return 'SUCUMBIOS'
    elif 'ZAMORA CHINCHIPE' in nombre_upper:
        return 'ZAMORA CHINCHIPE'
    elif 'SANTA ELENA' in nombre_upper:
        return 'SANTA ELENA'
    elif 'SANTO DOMINGO' in nombre_upper:
        return 'SANTO DOMINGO DE LOS TSACHILAS'
    elif 'CARCHI' in nombre_upper:
        return 'CARCHI'
    
    return None


def main():
    """Función principal."""
    # ============================================
    # CONFIGURACIÓN DE FILTROS
    # ============================================
    
    # Códigos CIIU a filtrar (deja vacío [] para no filtrar por CIIU)
    CODIGOS_CIIU = ['G476101', 'G476102', 'G476103', 'G476104']
    
    # Provincias a VISUALIZAR en el mapa final
    # IMPORTANTE: Cada Excel se filtra automáticamente por su propia provincia
    # Esta opción solo controla qué provincias aparecen en el mapa final
    
    # Opciones:
    # [] = Mostrar TODAS las provincias procesadas (recomendado)
    # ['EL ORO'] = Mostrar SOLO El Oro
    # ['GALAPAGOS'] = Mostrar SOLO Galápagos
    # ['EL ORO', 'GALAPAGOS'] = Mostrar ambas
    
    PROVINCIAS_A_VISUALIZAR = []  # Cambia esto para filtrar qué ver en el mapa
    
    # Estados del contribuyente a filtrar
    # Opciones: [] = Todos los estados
    # ['ACTIVO'] = Solo activos
    # ['SUSPENDIDO'] = Solo suspendidos
    # ['PASIVO'] = Solo pasivos
    # ['ACTIVO', 'PASIVO'] = Activos y pasivos (sin suspendidos)
    ESTADOS_FILTRAR = []  # Cambia esto para filtrar por estado
    
    # ============================================
    
    print("=" * 60)
    print("🗺️  Generador de Mapa Filtrado")
    print("=" * 60)
    
    if CODIGOS_CIIU:
        print(f"\n📋 Códigos CIIU a filtrar:")
        for codigo in CODIGOS_CIIU:
            print(f"   • {codigo}")
    else:
        print(f"\n📋 Códigos CIIU: Sin filtro (todos)")
    
    if PROVINCIAS_A_VISUALIZAR:
        print(f"\n👁️  Provincias a VISUALIZAR en el mapa:")
        for provincia in PROVINCIAS_A_VISUALIZAR:
            print(f"   • {provincia}")
    else:
        print(f"\n👁️  Provincias a visualizar: Todas las procesadas")
    
    if ESTADOS_FILTRAR:
        print(f"\n📊 Estados a filtrar:")
        for estado in ESTADOS_FILTRAR:
            print(f"   • {estado}")
    else:
        print(f"\n📊 Estados: Sin filtro (todos)")
    
    # Obtener API key
    google_api_key = None
    
    if os.path.exists('google_maps_api_key.txt'):
        with open('google_maps_api_key.txt', 'r') as f:
            google_api_key = f.read().strip()
    
    if not google_api_key:
        google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not google_api_key:
        print("\n❌ No se encontró API key de Google Maps.")
        print("   Crea el archivo 'google_maps_api_key.txt' con tu API key")
        return
    
    directorio_datos = "datos_excel"
    
    if not os.path.exists(directorio_datos):
        print(f"\n❌ No existe '{directorio_datos}'")
        return
    
    archivos_excel = [f for f in os.listdir(directorio_datos) 
                     if f.endswith(('.xlsx', '.xls')) and not f.startswith('~')]
    
    if not archivos_excel:
        print(f"\n❌ No se encontraron archivos Excel")
        return
    
    print(f"\n📊 Archivos Excel encontrados: {len(archivos_excel)}")
    
    generador = GeneradorMapaFiltrado(
        google_api_key=google_api_key, 
        codigos_ciiu=CODIGOS_CIIU if CODIGOS_CIIU else None,
        provincias=None  # No filtrar por provincia aquí, lo haremos por archivo
    )
    todas_ubicaciones = []
    
    # Procesar cada archivo Excel
    for archivo_excel in archivos_excel:
        ruta_completa = os.path.join(directorio_datos, archivo_excel)
        
        # Detectar provincia del archivo
        provincia_archivo = detectar_provincia_archivo(archivo_excel)
        
        if provincia_archivo:
            print(f"\n🔍 Archivo '{archivo_excel}' → Provincia detectada: {provincia_archivo}")
        else:
            print(f"\n⚠️  No se pudo detectar la provincia del archivo '{archivo_excel}'")
            print(f"   Procesando sin filtro de provincia...")
        
        # Filtrar por códigos CIIU, provincia del archivo y estados
        df_filtrado = generador.filtrar_excel(
            ruta_completa, 
            codigos_ciiu=CODIGOS_CIIU if CODIGOS_CIIU else None,
            provincias=[provincia_archivo] if provincia_archivo else None,
            estados=ESTADOS_FILTRAR if ESTADOS_FILTRAR else None
        )
        
        if not df_filtrado.empty:
            # Procesar datos filtrados
            ubicaciones = generador.procesar_datos_filtrados(df_filtrado)
            todas_ubicaciones.extend(ubicaciones)
    
    # Filtrar por provincias a visualizar si se especificaron
    if PROVINCIAS_A_VISUALIZAR and todas_ubicaciones:
        print(f"\n🔍 Filtrando ubicaciones para visualizar solo: {', '.join(PROVINCIAS_A_VISUALIZAR)}")
        provincias_normalizadas = [p.upper().strip() for p in PROVINCIAS_A_VISUALIZAR]
        todas_ubicaciones = [
            u for u in todas_ubicaciones 
            if u.get('provincia', '').upper().strip() in provincias_normalizadas
        ]
        print(f"   Ubicaciones después del filtro de visualización: {len(todas_ubicaciones)}")
    
    if todas_ubicaciones:
        # Actualizar códigos CIIU y provincias para el título del mapa
        generador.codigos_ciiu = CODIGOS_CIIU if CODIGOS_CIIU else []
        generador.provincias = PROVINCIAS_A_VISUALIZAR if PROVINCIAS_A_VISUALIZAR else []
        
        generador.generar_html_google_maps(todas_ubicaciones, "mapa_google_maps_filtrado.html")
        
        print(f"\n{'='*60}")
        print("✅ PROCESO COMPLETADO")
        print(f"{'='*60}")
        ubicaciones_con_coords = [u for u in todas_ubicaciones if u.get('latitud')]
        print(f"📍 Ubicaciones: {len(ubicaciones_con_coords)}/{len(todas_ubicaciones)}")
        print(f"📊 Total establecimientos filtrados: {sum(u['cantidad'] for u in todas_ubicaciones):,}")
        print(f"\n🌐 Abre 'mapa_google_maps_filtrado.html' en tu navegador")
    else:
        print("\n❌ No se encontraron establecimientos con los códigos CIIU especificados")


if __name__ == "__main__":
    main()

