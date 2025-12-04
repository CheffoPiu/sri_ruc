"""
Generador de Dashboard Completo con Menú y Pestañas
Crea un dashboard interactivo con navegación por pestañas.
"""

import pandas as pd
import json
import os
from datetime import datetime

def generar_dashboard_completo():
    """Genera un dashboard HTML completo con menú y pestañas."""
    
    # Cargar datos
    archivo = "librerias_con_info_google.xlsx"
    if not os.path.exists(archivo):
        print(f"❌ No se encontró: {archivo}")
        return
    
    df = pd.read_excel(archivo)
    encontradas = df[df['ENCONTRADO_GOOGLE'] == True]
    
    # Calcular estadísticas
    total_librerias = len(df)
    total_encontradas = len(encontradas)
    total_resenas = int(encontradas['NUMERO_RESENAS'].sum())
    promedio_resenas = encontradas['NUMERO_RESENAS'].mean()
    promedio_calificacion = encontradas['CALIFICACION_GOOGLE'].mean()
    venta_mensual = df['ESTIMACION_VENTA_MENSUAL'].sum()
    venta_anual = venta_mensual * 12
    
    # Datos para gráficos
    por_provincia = df.groupby('DESCRIPCION_PROVINCIA_EST').agg({
        'NUMERO_RUC': 'count',
        'ESTIMACION_VENTA_MENSUAL': 'sum',
        'NUMERO_RESENAS': 'sum'
    }).round(2).sort_values('ESTIMACION_VENTA_MENSUAL', ascending=False)
    
    top_10 = df.nlargest(10, 'NUMERO_RESENAS')[
        ['RAZON_SOCIAL', 'NOMBRE_FANTASIA_COMERCIAL', 'NUMERO_RESENAS',
         'CALIFICACION_GOOGLE', 'ESTIMACION_VENTA_MENSUAL', 'DESCRIPCION_CANTON_EST', 'URL_GOOGLE_MAPS']
    ]
    
    top_20_ventas = df.nlargest(20, 'ESTIMACION_VENTA_MENSUAL')[
        ['RAZON_SOCIAL', 'NOMBRE_FANTASIA_COMERCIAL', 'NUMERO_RESENAS',
         'CALIFICACION_GOOGLE', 'ESTIMACION_VENTA_MENSUAL', 'DESCRIPCION_CANTON_EST', 'URL_GOOGLE_MAPS']
    ]
    
    # Preparar datos para JavaScript
    provincias_data = []
    for provincia, row in por_provincia.iterrows():
        provincias_data.append({
            'provincia': str(provincia),
            'cantidad': int(float(row['NUMERO_RUC'])),
            'venta_mensual': float(round(row['ESTIMACION_VENTA_MENSUAL'], 2)),
            'resenas': int(float(row['NUMERO_RESENAS']))
        })
    
    top_10_data = []
    for _, row in top_10.iterrows():
        nombre = row['NOMBRE_FANTASIA_COMERCIAL'] if pd.notna(row['NOMBRE_FANTASIA_COMERCIAL']) else row['RAZON_SOCIAL']
        top_10_data.append({
            'nombre': str(nombre)[:60],
            'resenas': int(float(row['NUMERO_RESENAS'])),
            'calificacion': float(round(row['CALIFICACION_GOOGLE'], 1)),
            'venta_mensual': float(round(row['ESTIMACION_VENTA_MENSUAL'], 2)),
            'canton': str(row['DESCRIPCION_CANTON_EST']),
            'url': str(row['URL_GOOGLE_MAPS']) if pd.notna(row['URL_GOOGLE_MAPS']) else ''
        })
    
    top_20_ventas_data = []
    for _, row in top_20_ventas.iterrows():
        nombre = row['NOMBRE_FANTASIA_COMERCIAL'] if pd.notna(row['NOMBRE_FANTASIA_COMERCIAL']) else row['RAZON_SOCIAL']
        top_20_ventas_data.append({
            'nombre': str(nombre)[:60],
            'resenas': int(float(row['NUMERO_RESENAS'])),
            'calificacion': float(round(row['CALIFICACION_GOOGLE'], 1)),
            'venta_mensual': float(round(row['ESTIMACION_VENTA_MENSUAL'], 2)),
            'canton': str(row['DESCRIPCION_CANTON_EST']),
            'url': str(row['URL_GOOGLE_MAPS']) if pd.notna(row['URL_GOOGLE_MAPS']) else ''
        })
    
    # Distribución de reseñas
    distribucion_resenas = {
        '0-10': len(encontradas[(encontradas['NUMERO_RESENAS'] >= 0) & (encontradas['NUMERO_RESENAS'] <= 10)]),
        '11-50': len(encontradas[(encontradas['NUMERO_RESENAS'] > 10) & (encontradas['NUMERO_RESENAS'] <= 50)]),
        '51-100': len(encontradas[(encontradas['NUMERO_RESENAS'] > 50) & (encontradas['NUMERO_RESENAS'] <= 100)]),
        '100+': len(encontradas[encontradas['NUMERO_RESENAS'] > 100])
    }
    
    # Datos para tabla completa
    todas_librerias = df[[
        'NUMERO_RUC', 'RAZON_SOCIAL', 'NOMBRE_FANTASIA_COMERCIAL',
        'DESCRIPCION_CANTON_EST', 'NUMERO_RESENAS', 'CALIFICACION_GOOGLE',
        'ESTIMACION_VENTA_MENSUAL', 'SITIO_WEB', 'URL_GOOGLE_MAPS'
    ]].sort_values('ESTIMACION_VENTA_MENSUAL', ascending=False)
    
    todas_librerias_data = []
    for _, row in todas_librerias.iterrows():
        nombre = row['NOMBRE_FANTASIA_COMERCIAL'] if pd.notna(row['NOMBRE_FANTASIA_COMERCIAL']) else row['RAZON_SOCIAL']
        todas_librerias_data.append({
            'ruc': str(row['NUMERO_RUC']),
            'nombre': str(nombre),
            'canton': str(row['DESCRIPCION_CANTON_EST']),
            'resenas': int(float(row['NUMERO_RESENAS'])) if pd.notna(row['NUMERO_RESENAS']) else 0,
            'calificacion': float(round(row['CALIFICACION_GOOGLE'], 1)) if pd.notna(row['CALIFICACION_GOOGLE']) else 0,
            'venta_mensual': float(round(row['ESTIMACION_VENTA_MENSUAL'], 2)),
            'sitio_web': str(row['SITIO_WEB']) if pd.notna(row['SITIO_WEB']) else '',
            'url': str(row['URL_GOOGLE_MAPS']) if pd.notna(row['URL_GOOGLE_MAPS']) else ''
        })
    
    # Generar HTML
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Completo - Análisis de Librerías</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
            min-height: 100vh;
        }}
        
        .header {{
            background: white;
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 5px;
        }}
        
        .header p {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .tabs {{
            background: white;
            border-bottom: 2px solid #667eea;
            display: flex;
            flex-wrap: wrap;
            padding: 0 30px;
            position: sticky;
            top: 100px;
            z-index: 999;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .tab-button {{
            background: none;
            border: none;
            padding: 15px 25px;
            cursor: pointer;
            font-size: 1em;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            font-weight: 500;
        }}
        
        .tab-button:hover {{
            color: #667eea;
            background: #f5f5f5;
        }}
        
        .tab-button.active {{
            color: #667eea;
            border-bottom-color: #667eea;
            font-weight: 600;
        }}
        
        .tab-content {{
            display: none;
            padding: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        
        .stat-card .icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .chart-card h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.3em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
        }}
        
        .table-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            overflow-x: auto;
        }}
        
        .table-card h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 800px;
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        
        tr:hover {{
            background: #f5f5f5;
        }}
        
        .link-button {{
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.85em;
            display: inline-block;
        }}
        
        .link-button:hover {{
            background: #5568d3;
        }}
        
        .info-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        
        .info-box h3 {{
            color: #856404;
            margin-bottom: 10px;
        }}
        
        .info-box ul {{
            margin-left: 20px;
            color: #856404;
        }}
        
        .search-box {{
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            .tabs {{
                top: 80px;
            }}
            .tab-button {{
                padding: 10px 15px;
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Dashboard - Análisis de Librerías</h1>
        <p>Códigos CIIU: G476101 y G476104 | Fecha: {fecha}</p>
    </div>
    
    <div class="tabs">
        <button class="tab-button active" onclick="mostrarTab('resumen')">📊 Resumen</button>
        <button class="tab-button" onclick="mostrarTab('mapa')">🗺️ Mapa Interactivo</button>
        <button class="tab-button" onclick="mostrarTab('graficos')">📈 Gráficos</button>
        <button class="tab-button" onclick="mostrarTab('top-librerias')">🏆 Top Librerías</button>
        <button class="tab-button" onclick="mostrarTab('todas-librerias')">📋 Todas las Librerías</button>
        <button class="tab-button" onclick="mostrarTab('metodologia')">🔬 Metodología</button>
        <button class="tab-button" onclick="mostrarTab('limitaciones')">⚠️ Limitaciones</button>
    </div>
    
    <!-- TAB: RESUMEN -->
    <div id="resumen" class="tab-content active">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📊</div>
                <div class="number">{total_librerias}</div>
                <div class="label">Librerías Analizadas</div>
            </div>
            <div class="stat-card">
                <div class="icon">✅</div>
                <div class="number">{total_encontradas}</div>
                <div class="label">Encontradas en Google Maps</div>
            </div>
            <div class="stat-card">
                <div class="icon">⭐</div>
                <div class="number">{promedio_calificacion:.2f}</div>
                <div class="label">Calificación Promedio</div>
            </div>
            <div class="stat-card">
                <div class="icon">💬</div>
                <div class="number">{total_resenas:,}</div>
                <div class="label">Total de Reseñas</div>
            </div>
            <div class="stat-card">
                <div class="icon">💰</div>
                <div class="number">${venta_mensual:,.0f}</div>
                <div class="label">Venta Mensual (USD)</div>
            </div>
            <div class="stat-card">
                <div class="icon">📈</div>
                <div class="number">${venta_anual:,.0f}</div>
                <div class="label">Venta Anual (USD)</div>
            </div>
        </div>
        
        <div class="info-box">
            <h3>ℹ️ Información Importante</h3>
            <ul>
                <li>Las estimaciones de ventas están basadas en indicadores de Google Maps (reseñas, calificaciones, presencia online)</li>
                <li>Estas son <strong>estimaciones proyectadas</strong>, no datos históricos reales de ventas</li>
                <li>Las reseñas son el total acumulado hasta hoy, no sabemos las fechas específicas</li>
                <li>Para datos oficiales, consulta el SRI</li>
            </ul>
        </div>
    </div>
    
    <!-- TAB: MAPA -->
    <div id="mapa" class="tab-content">
        <div class="table-card">
            <h2>🗺️ Mapa Interactivo de Librerías</h2>
            <div style="background: #e7f3ff; border-left: 4px solid #2196F3; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                <p style="margin-bottom: 15px; color: #0c5460;">
                    <strong>📍 Mapa completo con todas las librerías</strong>
                </p>
                <p style="margin-bottom: 15px; color: #0c5460;">
                    El mapa muestra la ubicación geográfica de todas las librerías encontradas. 
                    Puedes hacer zoom, hacer clic en los marcadores para ver detalles, y filtrar por provincia o código CIIU.
                </p>
                <a href="mapa_google_maps_filtrado.html" target="_blank" 
                   style="display: inline-block; background: #2196F3; color: white; padding: 12px 25px; 
                          border-radius: 5px; text-decoration: none; font-weight: 600; margin-top: 10px;">
                    🗺️ Abrir Mapa Interactivo
                </a>
            </div>
            
            <div style="background: white; border: 2px dashed #ddd; padding: 40px; text-align: center; border-radius: 10px;">
                <iframe src="mapa_google_maps_filtrado.html" 
                        style="width: 100%; height: 600px; border: none; border-radius: 10px;"
                        title="Mapa de Librerías">
                </iframe>
                <p style="margin-top: 15px; color: #666; font-size: 0.9em;">
                    Si el mapa no se carga, <a href="mapa_google_maps_filtrado.html" target="_blank">haz clic aquí para abrirlo en una nueva pestaña</a>
                </p>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px;">
                <h3 style="color: #333; margin-bottom: 10px;">💡 Características del Mapa:</h3>
                <ul style="margin-left: 20px; line-height: 1.8; color: #666;">
                    <li><strong>Marcadores por ubicación:</strong> Cada marcador representa una ubicación con múltiples librerías</li>
                    <li><strong>Colores por cantidad:</strong> 
                        <span style="color: #FF0000;">🔴 Rojo</span> (>1,000), 
                        <span style="color: #FF8800;">🟠 Naranja</span> (500-1,000), 
                        <span style="color: #0000FF;">🔵 Azul</span> (100-500), 
                        <span style="color: #00FF00;">🟢 Verde</span> (<100)
                    </li>
                    <li><strong>Filtros:</strong> Puedes filtrar por provincia y código CIIU</li>
                    <li><strong>Tabla detallada:</strong> Haz clic en un marcador para ver todos los establecimientos de esa ubicación</li>
                    <li><strong>Estadísticas:</strong> El mapa muestra el total de ubicaciones y establecimientos</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- TAB: GRÁFICOS -->
    <div id="graficos" class="tab-content">
        <div class="charts-grid">
            <div class="chart-card">
                <h2>📊 Ventas por Provincia</h2>
                <div class="chart-container">
                    <canvas id="chartProvincias"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>📈 Distribución de Reseñas</h2>
                <div class="chart-container">
                    <canvas id="chartResenas"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>🏙️ Cantidad de Librerías por Provincia</h2>
                <div class="chart-container">
                    <canvas id="chartCantidad"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>⭐ Top 10 Librerías por Reseñas</h2>
                <div class="chart-container">
                    <canvas id="chartTop10"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- TAB: TOP LIBRERÍAS -->
    <div id="top-librerias" class="tab-content">
        <div class="table-card">
            <h2>🏆 Top 10 Librerías por Reseñas</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>Reseñas</th>
                        <th>Calificación</th>
                        <th>Venta Mensual (USD)</th>
                        <th>Cantón</th>
                        <th>Ver en Maps</th>
                    </tr>
                </thead>
                <tbody id="tablaTop10">
                </tbody>
            </table>
        </div>
        
        <div class="table-card">
            <h2>💰 Top 20 Librerías por Ventas Estimadas</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>Reseñas</th>
                        <th>Calificación</th>
                        <th>Venta Mensual (USD)</th>
                        <th>Cantón</th>
                        <th>Ver en Maps</th>
                    </tr>
                </thead>
                <tbody id="tablaTop20Ventas">
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- TAB: TODAS LAS LIBRERÍAS -->
    <div id="todas-librerias" class="tab-content">
        <div class="search-box">
            <input type="text" id="buscarLibreria" placeholder="🔍 Buscar librería por nombre, RUC o cantón..." onkeyup="filtrarTabla()">
        </div>
        <div class="table-card">
            <h2>📋 Todas las Librerías ({len(df)} total)</h2>
            <table>
                <thead>
                    <tr>
                        <th>RUC</th>
                        <th>Nombre</th>
                        <th>Cantón</th>
                        <th>Reseñas</th>
                        <th>Calificación</th>
                        <th>Venta Mensual (USD)</th>
                        <th>Sitio Web</th>
                        <th>Ver en Maps</th>
                    </tr>
                </thead>
                <tbody id="tablaTodas">
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- TAB: METODOLOGÍA -->
    <div id="metodologia" class="tab-content">
        <div class="table-card">
            <h2>🔬 Metodología del Análisis</h2>
            <h3 style="margin-top: 20px; color: #667eea;">1. Fuente de Datos</h3>
            <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                <li><strong>Datos del SRI:</strong> RUCs, razones sociales, estados, ubicaciones</li>
                <li><strong>Google Maps API:</strong> Reseñas, calificaciones, presencia online</li>
                <li><strong>Filtro:</strong> Solo librerías con estado ACTIVO</li>
            </ul>
            
            <h3 style="margin-top: 30px; color: #667eea;">2. Proceso de Búsqueda</h3>
            <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                <li>Búsqueda automática en Google Places API usando nombre y ubicación</li>
                <li>58 de 62 librerías encontradas (93.5%)</li>
                <li>Obtención de reseñas, calificaciones, sitio web, teléfono</li>
            </ul>
            
            <h3 style="margin-top: 30px; color: #667eea;">3. Cálculo de Estimaciones</h3>
            <p style="margin-top: 10px; line-height: 1.8;">
                Las estimaciones se basan en múltiples indicadores:
            </p>
            <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                <li><strong>Número de reseñas:</strong> Más reseñas = más actividad = más ventas estimadas</li>
                <li><strong>Calificación:</strong> Mejor calificación = más confianza = más ventas</li>
                <li><strong>Sitio web:</strong> Presencia online = más alcance = más ventas</li>
                <li><strong>Estado del contribuyente:</strong> ACTIVO = operando = más ventas</li>
            </ul>
            
            <h3 style="margin-top: 30px; color: #667eea;">4. Fórmula de Estimación</h3>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 10px;">
                <p><strong>Base según reseñas:</strong></p>
                <ul style="margin-left: 20px; margin-top: 5px;">
                    <li>0-10 reseñas → $5,000-15,000 USD/mes</li>
                    <li>11-50 reseñas → $15,000-40,000 USD/mes</li>
                    <li>51-100 reseñas → $40,000-80,000 USD/mes</li>
                    <li>100+ reseñas → $80,000-150,000 USD/mes</li>
                </ul>
                <p style="margin-top: 10px;"><strong>Ajustes:</strong></p>
                <ul style="margin-left: 20px; margin-top: 5px;">
                    <li>Calificación 4.5+ → +30%</li>
                    <li>Calificación 4.0-4.5 → +10%</li>
                    <li>Con sitio web → +50%</li>
                    <li>Estado ACTIVO → +20%</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- TAB: LIMITACIONES -->
    <div id="limitaciones" class="tab-content">
        <div class="table-card">
            <h2>⚠️ Limitaciones y Consideraciones</h2>
            
            <div class="info-box" style="margin-top: 20px;">
                <h3>📅 Sobre las Fechas de las Reseñas</h3>
                <ul>
                    <li>Las reseñas son el <strong>total acumulado</strong> hasta hoy</li>
                    <li><strong>NO tenemos fechas específicas</strong> de cada reseña</li>
                    <li>No sabemos si son de este mes, este año, o de varios años</li>
                    <li>Son una "foto" del estado actual, no un historial</li>
                </ul>
            </div>
            
            <div class="info-box" style="margin-top: 20px;">
                <h3>💰 Sobre las Estimaciones de Ventas</h3>
                <ul>
                    <li>Son <strong>proyecciones mensuales/anuales</strong> basadas en el estado actual</li>
                    <li><strong>NO son datos históricos reales</strong> de ventas</li>
                    <li>No corresponden a un período específico (diciembre 2024, etc.)</li>
                    <li>Son estimaciones de lo que <strong>podría</strong> vender mensualmente</li>
                </ul>
            </div>
            
            <div class="info-box" style="margin-top: 20px;">
                <h3>📊 Otras Limitaciones</h3>
                <ul>
                    <li>4 librerías no fueron encontradas en Google Maps</li>
                    <li>Las reseñas pueden no reflejar ventas directamente</li>
                    <li>Algunas librerías pueden tener muchas reseñas pero pocas ventas (o viceversa)</li>
                    <li>Las estimaciones pueden estar sobreestimadas o subestimadas</li>
                    <li>Para datos reales, se requiere consultar el SRI o las librerías directamente</li>
                </ul>
            </div>
            
            <div style="background: #d1ecf1; border-left: 4px solid #0c5460; padding: 20px; border-radius: 5px; margin-top: 20px;">
                <h3 style="color: #0c5460; margin-bottom: 10px;">💡 Recomendaciones</h3>
                <ul style="margin-left: 20px; color: #0c5460; line-height: 1.8;">
                    <li>Consultar el SRI para obtener datos oficiales de facturación</li>
                    <li>Contactar directamente a las librerías para validar estimaciones</li>
                    <li>Usar estas estimaciones como referencia comparativa, no como valores exactos</li>
                    <li>Actualizar periódicamente con nuevos datos</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        // Datos
        const provinciasData = {json.dumps(provincias_data, ensure_ascii=False)};
        const top10Data = {json.dumps(top_10_data, ensure_ascii=False)};
        const top20VentasData = {json.dumps(top_20_ventas_data, ensure_ascii=False)};
        const todasLibreriasData = {json.dumps(todas_librerias_data, ensure_ascii=False)};
        const distribucionResenas = {json.dumps(distribucion_resenas, ensure_ascii=False)};
        
        // Navegación de pestañas
        function mostrarTab(tabId) {{
            // Ocultar todas las pestañas
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Remover active de todos los botones
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Mostrar la pestaña seleccionada
            document.getElementById(tabId).classList.add('active');
            
            // Activar el botón correspondiente
            event.target.classList.add('active');
            
            // Inicializar gráficos si es necesario
            if (tabId === 'graficos') {{
                inicializarGraficos();
            }}
        }}
        
        // Inicializar gráficos
        let charts = {{}};
        function inicializarGraficos() {{
            if (charts.provincias) return; // Ya están inicializados
            
            const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a'];
            
            // Gráfico de Ventas por Provincia
            const ctxProvincias = document.getElementById('chartProvincias').getContext('2d');
            charts.provincias = new Chart(ctxProvincias, {{
                type: 'bar',
                data: {{
                    labels: provinciasData.map(p => p.provincia),
                    datasets: [{{
                        label: 'Venta Mensual (USD)',
                        data: provinciasData.map(p => p.venta_mensual),
                        backgroundColor: colors[0],
                        borderColor: colors[0],
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return '$' + context.parsed.y.toLocaleString('es-ES', {{maximumFractionDigits: 0}}) + ' USD';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return '$' + value.toLocaleString('es-ES', {{maximumFractionDigits: 0}});
                                }}
                            }}
                        }}
                    }}
                }}
            }});
            
            // Gráfico de Distribución de Reseñas
            const ctxResenas = document.getElementById('chartResenas').getContext('2d');
            charts.resenas = new Chart(ctxResenas, {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(distribucionResenas),
                    datasets: [{{
                        data: Object.values(distribucionResenas),
                        backgroundColor: colors.slice(0, 4),
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom' }}
                    }}
                }}
            }});
            
            // Gráfico de Cantidad por Provincia
            const ctxCantidad = document.getElementById('chartCantidad').getContext('2d');
            charts.cantidad = new Chart(ctxCantidad, {{
                type: 'pie',
                data: {{
                    labels: provinciasData.map(p => p.provincia),
                    datasets: [{{
                        data: provinciasData.map(p => p.cantidad),
                        backgroundColor: colors,
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom' }}
                    }}
                }}
            }});
            
            // Gráfico Top 10
            const ctxTop10 = document.getElementById('chartTop10').getContext('2d');
            charts.top10 = new Chart(ctxTop10, {{
                type: 'bar',
                data: {{
                    labels: top10Data.map(l => l.nombre.substring(0, 20) + '...'),
                    datasets: [{{
                        label: 'Reseñas',
                        data: top10Data.map(l => l.resenas),
                        backgroundColor: colors[1],
                        borderColor: colors[1],
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ beginAtZero: true }}
                    }}
                }}
            }});
        }}
        
        // Llenar tablas
        function llenarTablas() {{
            // Tabla Top 10
            const tablaTop10 = document.getElementById('tablaTop10');
            top10Data.forEach((lib, index) => {{
                const row = tablaTop10.insertRow();
                row.insertCell(0).textContent = index + 1;
                row.insertCell(1).textContent = lib.nombre;
                row.insertCell(2).textContent = lib.resenas.toLocaleString();
                row.insertCell(3).innerHTML = '⭐ ' + lib.calificacion;
                row.insertCell(4).textContent = '$' + lib.venta_mensual.toLocaleString('es-ES', {{maximumFractionDigits: 0}});
                row.insertCell(5).textContent = lib.canton;
                const cellLink = row.insertCell(6);
                if (lib.url) {{
                    const link = document.createElement('a');
                    link.href = lib.url;
                    link.target = '_blank';
                    link.className = 'link-button';
                    link.textContent = 'Ver';
                    cellLink.appendChild(link);
                }}
            }});
            
            // Tabla Top 20 Ventas
            const tablaTop20Ventas = document.getElementById('tablaTop20Ventas');
            top20VentasData.forEach((lib, index) => {{
                const row = tablaTop20Ventas.insertRow();
                row.insertCell(0).textContent = index + 1;
                row.insertCell(1).textContent = lib.nombre;
                row.insertCell(2).textContent = lib.resenas.toLocaleString();
                row.insertCell(3).innerHTML = '⭐ ' + lib.calificacion;
                row.insertCell(4).textContent = '$' + lib.venta_mensual.toLocaleString('es-ES', {{maximumFractionDigits: 0}});
                row.insertCell(5).textContent = lib.canton;
                const cellLink = row.insertCell(6);
                if (lib.url) {{
                    const link = document.createElement('a');
                    link.href = lib.url;
                    link.target = '_blank';
                    link.className = 'link-button';
                    link.textContent = 'Ver';
                    cellLink.appendChild(link);
                }}
            }});
            
            // Tabla Todas las Librerías
            const tablaTodas = document.getElementById('tablaTodas');
            todasLibreriasData.forEach((lib) => {{
                const row = tablaTodas.insertRow();
                row.insertCell(0).textContent = lib.ruc;
                row.insertCell(1).textContent = lib.nombre;
                row.insertCell(2).textContent = lib.canton;
                row.insertCell(3).textContent = lib.resenas.toLocaleString();
                row.insertCell(4).innerHTML = lib.calificacion > 0 ? '⭐ ' + lib.calificacion : '-';
                row.insertCell(5).textContent = '$' + lib.venta_mensual.toLocaleString('es-ES', {{maximumFractionDigits: 0}});
                const cellWeb = row.insertCell(6);
                if (lib.sitio_web) {{
                    const link = document.createElement('a');
                    link.href = lib.sitio_web;
                    link.target = '_blank';
                    link.textContent = 'Web';
                    link.className = 'link-button';
                    cellWeb.appendChild(link);
                }} else {{
                    cellWeb.textContent = '-';
                }}
                const cellLink = row.insertCell(7);
                if (lib.url) {{
                    const link = document.createElement('a');
                    link.href = lib.url;
                    link.target = '_blank';
                    link.className = 'link-button';
                    link.textContent = 'Maps';
                    cellLink.appendChild(link);
                }} else {{
                    cellLink.textContent = '-';
                }}
            }});
        }}
        
        // Filtrar tabla
        function filtrarTabla() {{
            const input = document.getElementById('buscarLibreria');
            const filter = input.value.toLowerCase();
            const table = document.getElementById('tablaTodas');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 0; i < rows.length; i++) {{
                const row = rows[i];
                const text = row.textContent.toLowerCase();
                if (text.indexOf(filter) > -1) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }}
        }}
        
        // Inicializar al cargar
        window.onload = function() {{
            llenarTablas();
            inicializarGraficos();
        }};
    </script>
</body>
</html>
"""
    
    # Guardar archivo
    archivo_salida = "dashboard_completo.html"
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard completo generado: {archivo_salida}")
    print(f"\n🌐 Para verlo:")
    print(f"   1. Abre el archivo: {archivo_salida}")
    print(f"   2. O ejecuta: python3 servidor_local.py")
    print(f"   3. Luego abre: http://localhost:8000/{archivo_salida}")
    print(f"\n📋 Pestañas disponibles:")
    print(f"   • Resumen - Métricas principales")
    print(f"   • Gráficos - Visualizaciones interactivas")
    print(f"   • Top Librerías - Las mejores por reseñas y ventas")
    print(f"   • Todas las Librerías - Lista completa con búsqueda")
    print(f"   • Metodología - Cómo se hizo el análisis")
    print(f"   • Limitaciones - Aclaraciones importantes")


if __name__ == "__main__":
    generar_dashboard_completo()

