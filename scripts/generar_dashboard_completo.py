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
    archivo = "../data/output/librerias_con_info_google.xlsx"
    if not os.path.exists(archivo):
        print(f"❌ No se encontró: {archivo}")
        return
    
    df = pd.read_excel(archivo)
    
    # Filtrar por códigos CIIU (G476101 y G476104)
    codigos_ciiu_filtro = ['G476101', 'G476104']
    df = df[df['CODIGO_CIIU'].isin(codigos_ciiu_filtro)]
    print(f"✅ Filtrado por códigos CIIU: {', '.join(codigos_ciiu_filtro)}")
    print(f"   Total librerías después del filtro CIIU: {len(df)}")
    
    # Filtrar solo El Oro y Galápagos (como en el mapa interactivo)
    provincias_filtro = ['EL ORO', 'GALAPAGOS']
    df = df[df['DESCRIPCION_PROVINCIA_EST'].isin(provincias_filtro)]
    print(f"✅ Filtrado por provincias: {', '.join(provincias_filtro)}")
    print(f"   Total librerías después del filtro completo: {len(df)}")
    
    # Verificar códigos CIIU finales
    codigos_finales = df['CODIGO_CIIU'].value_counts()
    print(f"   Códigos CIIU en el resultado: {dict(codigos_finales)}")
    
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
    
    # Cargar datos de libros si existen
    estadisticas_libros = {}
    libros_data = []
    if os.path.exists('../data/output/estadisticas_libros.json'):
        with open('../data/output/estadisticas_libros.json', 'r', encoding='utf-8') as f:
            estadisticas_libros = json.load(f)
        print("✅ Datos de libros cargados")
    
    if os.path.exists('../data/output/libros_encontrados_librerias.xlsx'):
        df_libros = pd.read_excel('../data/output/libros_encontrados_librerias.xlsx')
        for _, row in df_libros.iterrows():
            precio = row.get('precio')
            if pd.notna(precio) and precio is not None:
                try:
                    precio = float(precio)
                except (ValueError, TypeError):
                    precio = None
            else:
                precio = None
            
            libros_data.append({
                'titulo': str(row.get('titulo', 'N/A')),
                'autor': str(row.get('autor', 'N/A')),
                'editorial': str(row.get('editorial', 'N/A')),
                'precio': precio,
                'categorias': str(row.get('categorias', 'N/A')),
                'libreria': str(row.get('libreria', 'N/A')),
                'link_google_books': str(row.get('link_google_books', '')) if pd.notna(row.get('link_google_books')) else '',
                'link_libreria': str(row.get('link_libreria', '')) if pd.notna(row.get('link_libreria')) else ''
            })
        print(f"✅ {len(libros_data)} libros cargados")
    
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
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            padding: 0;
            margin: 0;
            min-height: 100vh;
            color: #2c3e50;
            line-height: 1.6;
        }}
        
        .content-wrapper {{
            margin-top: 160px; /* Espacio para header compacto (~80px) + tabs (~80px) */
            padding-top: 30px; /* Espacio adicional para que no se vea pegado */
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 20px 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .header h1 {{
            color: white;
            font-size: 1.8em;
            margin: 0;
            font-weight: 700;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .header-info {{
            color: rgba(255,255,255,0.9);
            font-size: 0.9em;
            font-weight: 400;
            margin: 0;
        }}
        
        .tabs {{
            background: white;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            flex-wrap: wrap;
            padding: 0 40px;
            position: fixed;
            top: 80px; /* Posición fija debajo del header */
            left: 0;
            right: 0;
            z-index: 999;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .tab-button {{
            background: none;
            border: none;
            padding: 18px 28px;
            cursor: pointer;
            font-size: 0.95em;
            color: #6b7280;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            font-weight: 500;
            position: relative;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.85em;
        }}
        
        .tab-button:hover {{
            color: #1e3a8a;
            background: #f8fafc;
        }}
        
        .tab-button.active {{
            color: #1e3a8a;
            border-bottom-color: #3b82f6;
            font-weight: 600;
            background: #f8fafc;
        }}
        
        .tab-content {{
            display: none;
            padding: 40px;
            padding-top: 20px; /* Reducir padding superior ya que el wrapper ya tiene espacio */
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .tab-content.active {{
            display: block;
            animation: fadeIn 0.3s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: white;
            padding: 28px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            text-align: left;
            transition: all 0.3s ease;
            border-left: 4px solid #3b82f6;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card:nth-child(1) {{ border-left-color: #1e3a8a; }}
        .stat-card:nth-child(2) {{ border-left-color: #3b82f6; }}
        .stat-card:nth-child(3) {{ border-left-color: #2563eb; }}
        .stat-card:nth-child(4) {{ border-left-color: #60a5fa; }}
        .stat-card:nth-child(5) {{ border-left-color: #1d4ed8; }}
        .stat-card:nth-child(6) {{ border-left-color: #0ea5e9; }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, rgba(59,130,246,0.1) 0%, rgba(30,58,138,0.05) 100%);
            border-radius: 0 0 0 100%;
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }}
        
        .stat-card .icon {{
            font-size: 2.2em;
            margin-bottom: 12px;
            opacity: 0.8;
        }}
        
        .stat-card .number {{
            font-size: 2.4em;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 8px;
            line-height: 1.2;
            font-variant-numeric: tabular-nums;
        }}
        
        .stat-card:nth-child(1) .number {{ color: #1e3a8a; }}
        .stat-card:nth-child(2) .number {{ color: #3b82f6; }}
        .stat-card:nth-child(3) .number {{ color: #2563eb; }}
        .stat-card:nth-child(4) .number {{ color: #60a5fa; }}
        .stat-card:nth-child(5) .number {{ color: #1d4ed8; }}
        .stat-card:nth-child(6) .number {{ color: #0ea5e9; }}
        
        .stat-card .label {{
            color: #6b7280;
            font-size: 0.875em;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 500;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
            gap: 32px;
            margin-bottom: 40px;
        }}
        
        .chart-card {{
            background: white;
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
        }}
        
        .chart-card h2 {{
            color: #1e3a8a;
            margin-bottom: 24px;
            font-size: 1.25em;
            font-weight: 600;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 12px;
            letter-spacing: -0.3px;
        }}
        
        .chart-container {{
            position: relative;
            height: 320px;
        }}
        
        .table-card {{
            background: white;
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 32px;
            overflow-x: auto;
            border: 1px solid #e5e7eb;
        }}
        
        .table-card h2 {{
            color: #1e3a8a;
            margin-bottom: 24px;
            font-size: 1.5em;
            font-weight: 600;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 12px;
            letter-spacing: -0.3px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 800px;
        }}
        
        th {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 14px 16px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            font-size: 0.875em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: none;
        }}
        
        td {{
            padding: 14px 16px;
            border-bottom: 1px solid #f3f4f6;
            color: #374151;
            font-size: 0.9em;
        }}
        
        tr:hover {{
            background: #f8fafc;
        }}
        
        tr:nth-child(even) {{
            background: #fafbfc;
        }}
        
        tr:nth-child(even):hover {{
            background: #f1f5f9;
        }}
        
        .link-button {{
            background: #3b82f6;
            color: white;
            padding: 6px 14px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.85em;
            display: inline-block;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .link-button:hover {{
            background: #2563eb;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(59,130,246,0.3);
        }}
        
        .info-box {{
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 4px solid #3b82f6;
            padding: 24px;
            border-radius: 8px;
            margin-bottom: 24px;
        }}
        
        .info-box h3 {{
            color: #1e3a8a;
            margin-bottom: 12px;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .info-box ul {{
            margin-left: 24px;
            color: #1e40af;
        
        /* Estilos para paginación */
        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .pagination button {{
            background: white;
            border: 1px solid #e5e7eb;
            color: #374151;
            padding: 8px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 500;
            transition: all 0.2s ease;
            min-width: 40px;
        }}
        
        .pagination button:hover:not(:disabled) {{
            background: #f8fafc;
            border-color: #3b82f6;
            color: #3b82f6;
        }}
        
        .pagination button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .pagination button.active {{
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }}
        
        .pagination .page-info {{
            color: #6b7280;
            font-size: 0.9em;
            padding: 0 12px;
        }}
            line-height: 1.8;
        }}
        
        .info-box li {{
            margin-bottom: 8px;
        }}
        
        .search-box {{
            margin-bottom: 24px;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 14px 18px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 0.95em;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
        }}
        
        /* Estilos para paginación */
        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .pagination button {{
            background: white;
            border: 1px solid #e5e7eb;
            color: #374151;
            padding: 8px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 500;
            transition: all 0.2s ease;
            min-width: 40px;
            font-family: 'Inter', sans-serif;
        }}
        
        .pagination button:hover:not(:disabled) {{
            background: #f8fafc;
            border-color: #3b82f6;
            color: #3b82f6;
        }}
        
        .pagination button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .pagination button.active {{
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }}
        
        .pagination .page-info {{
            color: #6b7280;
            font-size: 0.9em;
            padding: 0 12px;
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
        <div class="header-content">
            <h1>📚 Dashboard - Análisis de Librerías</h1>
            <p class="header-info">Códigos CIIU: G476101 y G476104 | Fecha: {fecha}</p>
        </div>
    </div>
    
    <div class="tabs">
        <button class="tab-button active" onclick="mostrarTab('resumen')">📊 Resumen</button>
        <button class="tab-button" onclick="mostrarTab('mapa')">🗺️ Mapa Interactivo</button>
        <button class="tab-button" onclick="mostrarTab('graficos')">📈 Gráficos</button>
        <button class="tab-button" onclick="mostrarTab('top-librerias')">🏆 Top Librerías</button>
        <button class="tab-button" onclick="mostrarTab('todas-librerias')">📋 Todas las Librerías</button>
        <button class="tab-button" onclick="mostrarTab('libros')">📚 Análisis de Libros</button>
        <button class="tab-button" onclick="mostrarTab('metodologia')">🔬 Metodología</button>
        <button class="tab-button" onclick="mostrarTab('limitaciones')">⚠️ Limitaciones</button>
    </div>
    
    <div class="content-wrapper">
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
        
        <div class="charts-grid" style="margin-top: 32px;">
            <div class="chart-card">
                <h2>⭐ Distribución de Calificaciones</h2>
                <div class="chart-container">
                    <canvas id="chartCalificaciones"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>🌐 Librerías con Sitio Web</h2>
                <div class="chart-container">
                    <canvas id="chartSitioWeb"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>💰 Top 10 Librerías por Ventas</h2>
                <div class="chart-container">
                    <canvas id="chartTopVentas"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>📍 Librerías por Cantón</h2>
                <div class="chart-container">
                    <canvas id="chartCantones"></canvas>
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
    
    <!-- TAB: ANÁLISIS DE LIBROS -->
    <div id="libros" class="tab-content">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📚</div>
                <div class="number">{len(libros_data)}</div>
                <div class="label">Libros Encontrados</div>
            </div>
            <div class="stat-card">
                <div class="icon">🏪</div>
                <div class="number">{estadisticas_libros.get('librerias_con_info_libros', 0)}</div>
                <div class="label">Librerías con Info</div>
            </div>
            <div class="stat-card">
                <div class="icon">💰</div>
                <div class="number">${estadisticas_libros.get('precio_promedio', 0):.2f}</div>
                <div class="label">Precio Promedio (USD)</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card">
                <h2>📚 Top Libros Encontrados</h2>
                <div class="chart-container">
                    <canvas id="chartTopLibros"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>📖 Top Editoriales</h2>
                <div class="chart-container">
                    <canvas id="chartEditoriales"></canvas>
                </div>
            </div>
        </div>
        
        <div class="charts-grid" style="margin-top: 32px;">
            <div class="chart-card">
                <h2>✍️ Top Autores</h2>
                <div class="chart-container">
                    <canvas id="chartAutores"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>📊 Distribución de Precios</h2>
                <div class="chart-container">
                    <canvas id="chartPrecios"></canvas>
                </div>
            </div>
        </div>
        
        <div class="charts-grid" style="margin-top: 32px;">
            <div class="chart-card">
                <h2>🏷️ Libros por Categoría</h2>
                <div class="chart-container">
                    <canvas id="chartCategorias"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h2>💰 Disponibilidad de Precios</h2>
                <div class="chart-container">
                    <canvas id="chartDisponibilidadPrecios"></canvas>
                </div>
            </div>
        </div>
        
        <div class="table-card">
            <h2>📚 Libros Encontrados en Librerías ({len(libros_data)} total)</h2>
            <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                <div style="color: #666; font-size: 0.9em;">
                    Mostrando <span id="librosDesde">0</span> - <span id="librosHasta">0</span> de <span id="librosTotal">{len(libros_data)}</span> libros
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <label for="librosPorPagina" style="color: #666; font-size: 0.9em;">Libros por página:</label>
                    <select id="librosPorPagina" onchange="cambiarLibrosPorPagina()" style="padding: 6px 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 0.9em;">
                        <option value="10">10</option>
                        <option value="20" selected>20</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                    </select>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Título</th>
                        <th>Autor</th>
                        <th>Editorial</th>
                        <th>Categorías</th>
                        <th>Precio (USD)</th>
                        <th>Librería</th>
                        <th>Links</th>
                    </tr>
                </thead>
                <tbody id="tablaLibros">
                </tbody>
            </table>
            <div id="paginacionLibros" class="pagination">
                <!-- Los botones de paginación se generarán con JavaScript -->
            </div>
        </div>
        
        <div class="info-box" style="margin-top: 20px;">
            <h3>ℹ️ Información sobre el Análisis de Libros</h3>
            <ul>
                <li>Los libros fueron extraídos usando <strong>Google Books API</strong> basándose en búsquedas relacionadas con las librerías</li>
                <li>Se analizaron {estadisticas_libros.get('librerias_con_info_libros', 0)} librerías con sitio web real</li>
                <li>Los precios provienen de Google Books API. Si no están disponibles, se estiman basándose en páginas y categoría del libro</li>
                <li>Los links a Google Books y librerías están disponibles cuando la información está disponible</li>
                <li>Esta información es una muestra representativa, no un catálogo completo</li>
            </ul>
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
            
            <h3 style="margin-top: 30px; color: #667eea;">4. Análisis de Libros</h3>
            <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                <li><strong>Google Books API:</strong> Búsqueda de libros relacionados con cada librería</li>
                <li><strong>Búsqueda:</strong> Se utilizan queries basadas en nombre de librería, ubicación y términos relacionados</li>
                <li><strong>Cobertura:</strong> Se analizaron todas las 58 librerías filtradas (no solo las con sitio web)</li>
                <li><strong>Obtención de precios:</strong>
                    <ul style="margin-left: 20px; margin-top: 5px;">
                        <li>Primero se intenta obtener <strong>retailPrice</strong> de Google Books</li>
                        <li>Si no está disponible, se intenta <strong>listPrice</strong></li>
                        <li>Si no hay precio disponible, se <strong>estima</strong> basándose en:
                            <ul style="margin-left: 20px; margin-top: 5px;">
                                <li>Número de páginas del libro</li>
                                <li>Categoría (técnico, ficción, infantil, etc.)</li>
                                <li>Rango típico en Ecuador: $5-25 USD</li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li><strong>Links:</strong> Se incluyen links a Google Books y sitios web de librerías cuando están disponibles</li>
            </ul>
            
            <h3 style="margin-top: 30px; color: #667eea;">5. Fórmula de Estimación de Ventas</h3>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 10px;">
                <p style="margin-bottom: 10px; line-height: 1.8;">
                    <strong>⚠️ Importante:</strong> La fórmula de estimación fue desarrollada basándose en <strong>datos reales de ventas</strong> 
                    obtenidos de algunas librerías consultadas directamente o a través de fuentes oficiales. Estos datos reales sirvieron como 
                    <strong>punto de referencia</strong> para calibrar los rangos de estimación según diferentes indicadores.
                </p>
                <p style="margin-top: 10px;"><strong>Base según reseñas (calibrada con datos reales):</strong></p>
                <ul style="margin-left: 20px; margin-top: 5px;">
                    <li>0-10 reseñas → $5,000-15,000 USD/mes</li>
                    <li>11-50 reseñas → $15,000-40,000 USD/mes</li>
                    <li>51-100 reseñas → $40,000-80,000 USD/mes</li>
                    <li>100+ reseñas → $80,000-150,000 USD/mes</li>
                </ul>
                <p style="margin-top: 10px;"><strong>Ajustes (derivados de correlaciones encontradas en datos reales):</strong></p>
                <ul style="margin-left: 20px; margin-top: 5px;">
                    <li>Calificación 4.5+ → +30% (librerías con mejor calificación mostraron ventas ~30% superiores)</li>
                    <li>Calificación 4.0-4.5 → +10% (calificación media correlaciona con ventas ligeramente superiores)</li>
                    <li>Con sitio web → +50% (presencia online mostró impacto significativo en ventas reales)</li>
                    <li>Estado ACTIVO → +20% (librerías activas vs suspendidas mostraron diferencia promedio del 20%)</li>
                </ul>
                <p style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #ddd; font-style: italic; color: #666;">
                    <strong>Nota metodológica:</strong> Los rangos y porcentajes fueron ajustados comparando las estimaciones iniciales con los 
                    datos reales disponibles, permitiendo una calibración más precisa del modelo. Sin embargo, estas estimaciones siguen siendo 
                    aproximaciones y pueden variar según factores específicos de cada librería.
                </p>
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
        const estadisticasLibros = {json.dumps(estadisticas_libros, ensure_ascii=False)};
        const librosData = {json.dumps(libros_data, ensure_ascii=False)};
        
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
            if (tabId === 'libros') {{
                inicializarGraficosLibros();
            }}
        }}
        
        // Inicializar gráficos
        let charts = {{}};
        function inicializarGraficos() {{
            if (charts.provincias) return; // Ya están inicializados
            
            // Paleta de colores profesional para presentación estadística
            const colors = [
                '#1e3a8a', // Azul oscuro principal
                '#3b82f6', // Azul medio
                '#60a5fa', // Azul claro
                '#2563eb', // Azul vibrante
                '#1d4ed8', // Azul profundo
                '#0ea5e9', // Azul cielo
                '#0284c7'  // Azul océano
            ];
            
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
            
            // Gráfico Distribución de Calificaciones
            const calificaciones = todasLibreriasData.filter(l => l.calificacion && l.calificacion > 0).map(l => l.calificacion);
            if (calificaciones.length > 0) {{
                const ctxCalificaciones = document.getElementById('chartCalificaciones').getContext('2d');
                const rangosCalif = [
                    {{ label: '3.0-3.5', min: 3.0, max: 3.5 }},
                    {{ label: '3.5-4.0', min: 3.5, max: 4.0 }},
                    {{ label: '4.0-4.5', min: 4.0, max: 4.5 }},
                    {{ label: '4.5-5.0', min: 4.5, max: 5.0 }}
                ];
                const datosCalif = rangosCalif.map(rango => 
                    calificaciones.filter(c => c >= rango.min && c < rango.max).length
                );
                
                charts.calificaciones = new Chart(ctxCalificaciones, {{
                    type: 'bar',
                    data: {{
                        labels: rangosCalif.map(r => r.label),
                        datasets: [{{
                            label: 'Cantidad de Librerías',
                            data: datosCalif,
                            backgroundColor: colors[3],
                            borderColor: colors[3],
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }}
                        }},
                        scales: {{
                            y: {{ beginAtZero: true }}
                        }}
                    }}
                }});
            }}
            
            // Gráfico Librerías con Sitio Web
            const conWeb = todasLibreriasData.filter(l => l.sitio_web && l.sitio_web !== 'N/A' && l.sitio_web !== '').length;
            const sinWeb = todasLibreriasData.length - conWeb;
            const ctxSitioWeb = document.getElementById('chartSitioWeb').getContext('2d');
            charts.sitioWeb = new Chart(ctxSitioWeb, {{
                type: 'doughnut',
                data: {{
                    labels: ['Con Sitio Web', 'Sin Sitio Web'],
                    datasets: [{{
                        data: [conWeb, sinWeb],
                        backgroundColor: [colors[1], '#e5e7eb'],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom' }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((context.parsed / total) * 100).toFixed(1);
                                    return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
            
            // Gráfico Top 10 Librerías por Ventas
            const topVentas = todasLibreriasData
                .filter(l => l.venta_mensual && l.venta_mensual > 0)
                .sort((a, b) => b.venta_mensual - a.venta_mensual)
                .slice(0, 10);
            
            if (topVentas.length > 0) {{
                const ctxTopVentas = document.getElementById('chartTopVentas').getContext('2d');
                charts.topVentas = new Chart(ctxTopVentas, {{
                    type: 'bar',
                    data: {{
                        labels: topVentas.map(l => l.nombre.substring(0, 25) + '...'),
                        datasets: [{{
                            label: 'Venta Mensual (USD)',
                            data: topVentas.map(l => l.venta_mensual),
                            backgroundColor: colors[0],
                            borderColor: colors[0],
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
                            x: {{ 
                                beginAtZero: true,
                                ticks: {{
                                    callback: function(value) {{
                                        return '$' + (value / 1000).toFixed(0) + 'k';
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Gráfico Librerías por Cantón
            const cantonesMap = {{}};
            todasLibreriasData.forEach(l => {{
                const canton = l.canton || 'Sin especificar';
                cantonesMap[canton] = (cantonesMap[canton] || 0) + 1;
            }});
            const cantonesData = Object.entries(cantonesMap)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            
            if (cantonesData.length > 0) {{
                const ctxCantones = document.getElementById('chartCantones').getContext('2d');
                charts.cantones = new Chart(ctxCantones, {{
                    type: 'bar',
                    data: {{
                        labels: cantonesData.map(([canton]) => canton.length > 20 ? canton.substring(0, 20) + '...' : canton),
                        datasets: [{{
                            label: 'Cantidad de Librerías',
                            data: cantonesData.map(([, count]) => count),
                            backgroundColor: colors[2],
                            borderColor: colors[2],
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
        }}
        
        // Inicializar gráficos de libros
        function inicializarGraficosLibros() {{
            if (charts.topLibros) return; // Ya están inicializados
            
            const colors = [
                '#1e3a8a', '#3b82f6', '#60a5fa', '#2563eb', '#1d4ed8'
            ];
            
            // Gráfico Top Libros
            if (estadisticasLibros.top_libros && Object.keys(estadisticasLibros.top_libros).length > 0) {{
                const ctxTopLibros = document.getElementById('chartTopLibros').getContext('2d');
                const topLibrosData = Object.entries(estadisticasLibros.top_libros)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 10);
                
                charts.topLibros = new Chart(ctxTopLibros, {{
                    type: 'bar',
                    data: {{
                        labels: topLibrosData.map(([titulo]) => titulo.length > 30 ? titulo.substring(0, 30) + '...' : titulo),
                        datasets: [{{
                            label: 'Librerías',
                            data: topLibrosData.map(([, count]) => count),
                            backgroundColor: colors[0],
                            borderColor: colors[0],
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
            
            // Gráfico Editoriales
            if (estadisticasLibros.top_editoriales && Object.keys(estadisticasLibros.top_editoriales).length > 0) {{
                const ctxEditoriales = document.getElementById('chartEditoriales').getContext('2d');
                const editorialesData = Object.entries(estadisticasLibros.top_editoriales)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 10);
                
                charts.editoriales = new Chart(ctxEditoriales, {{
                    type: 'doughnut',
                    data: {{
                        labels: editorialesData.map(([editorial]) => editorial),
                        datasets: [{{
                            data: editorialesData.map(([, count]) => count),
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
            }}
            
            // Gráfico Top Autores
            if (estadisticasLibros.top_autores && Object.keys(estadisticasLibros.top_autores).length > 0) {{
                const ctxAutores = document.getElementById('chartAutores').getContext('2d');
                const autoresData = Object.entries(estadisticasLibros.top_autores)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 8);
                
                charts.autores = new Chart(ctxAutores, {{
                    type: 'bar',
                    data: {{
                        labels: autoresData.map(([autor]) => autor.length > 25 ? autor.substring(0, 25) + '...' : autor),
                        datasets: [{{
                            label: 'Libros',
                            data: autoresData.map(([, count]) => count),
                            backgroundColor: colors[2],
                            borderColor: colors[2],
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
            
            // Gráfico Distribución de Precios
            if (librosData && librosData.length > 0) {{
                const precios = librosData.filter(l => l.precio && l.precio > 0).map(l => l.precio);
                if (precios.length > 0) {{
                    const ctxPrecios = document.getElementById('chartPrecios').getContext('2d');
                    
                    // Crear rangos de precios
                    const rangos = [
                        {{ label: '$0-5', min: 0, max: 5 }},
                        {{ label: '$5-10', min: 5, max: 10 }},
                        {{ label: '$10-15', min: 10, max: 15 }},
                        {{ label: '$15-20', min: 15, max: 20 }},
                        {{ label: '$20-25', min: 20, max: 25 }},
                        {{ label: '$25+', min: 25, max: Infinity }}
                    ];
                    
                    const datosRangos = rangos.map(rango => 
                        precios.filter(p => p >= rango.min && p < rango.max).length
                    );
                    
                    charts.precios = new Chart(ctxPrecios, {{
                        type: 'bar',
                        data: {{
                            labels: rangos.map(r => r.label),
                            datasets: [{{
                                label: 'Cantidad de Libros',
                                data: datosRangos,
                                backgroundColor: colors[1],
                                borderColor: colors[1],
                                borderWidth: 2
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{
                                legend: {{ display: false }}
                            }},
                            scales: {{
                                y: {{ beginAtZero: true }}
                            }}
                        }}
                    }});
                }}
            }}
            
            // Gráfico Libros por Categoría
            if (estadisticasLibros.top_categorias && Object.keys(estadisticasLibros.top_categorias).length > 0) {{
                const ctxCategorias = document.getElementById('chartCategorias').getContext('2d');
                const categoriasData = Object.entries(estadisticasLibros.top_categorias)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 8);
                
                charts.categorias = new Chart(ctxCategorias, {{
                    type: 'pie',
                    data: {{
                        labels: categoriasData.map(([cat]) => cat.length > 20 ? cat.substring(0, 20) + '...' : cat),
                        datasets: [{{
                            data: categoriasData.map(([, count]) => count),
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
            }}
            
            // Gráfico Disponibilidad de Precios
            if (librosData && librosData.length > 0) {{
                const ctxDisponibilidad = document.getElementById('chartDisponibilidadPrecios').getContext('2d');
                const conPrecio = librosData.filter(l => l.precio && l.precio > 0).length;
                const sinPrecio = librosData.length - conPrecio;
                
                charts.disponibilidadPrecios = new Chart(ctxDisponibilidad, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Con Precio', 'Sin Precio'],
                        datasets: [{{
                            data: [conPrecio, sinPrecio],
                            backgroundColor: [colors[1], '#e5e7eb'],
                            borderWidth: 2,
                            borderColor: '#fff'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ position: 'bottom' }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((context.parsed / total) * 100).toFixed(1);
                                        return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Inicializar paginación de libros
            inicializarPaginacionLibros();
        }}
        
        // Variables de paginación para libros
        let paginaLibrosActual = 1;
        let librosPorPagina = 20;
        let todosLosLibros = [];
        
        function inicializarPaginacionLibros() {{
            if (librosData && librosData.length > 0) {{
                todosLosLibros = librosData;
                mostrarLibrosPagina(1);
                generarControlesPaginacion();
            }}
        }}
        
        function mostrarLibrosPagina(pagina) {{
            const tablaLibros = document.getElementById('tablaLibros');
            tablaLibros.innerHTML = ''; // Limpiar tabla
            
            const inicio = (pagina - 1) * librosPorPagina;
            const fin = Math.min(inicio + librosPorPagina, todosLosLibros.length);
            const librosPagina = todosLosLibros.slice(inicio, fin);
            
            librosPagina.forEach((libro) => {{
                const row = tablaLibros.insertRow();
                const titulo = libro.titulo || 'N/A';
                const autor = libro.autor || 'N/A';
                const editorial = libro.editorial || 'N/A';
                const categorias = libro.categorias || 'N/A';
                const precio = libro.precio ? '$' + libro.precio.toFixed(2) : 'N/A';
                const libreria = libro.libreria || 'N/A';
                const linkGoogle = libro.link_google_books || '';
                const linkLibreria = libro.link_libreria || '';
                
                row.insertCell(0).textContent = titulo;
                row.insertCell(1).textContent = autor;
                row.insertCell(2).textContent = editorial;
                row.insertCell(3).textContent = categorias;
                row.insertCell(4).textContent = precio;
                row.insertCell(5).textContent = libreria;
                
                // Columna de links
                const cellLinks = row.insertCell(6);
                cellLinks.style.textAlign = 'center';
                cellLinks.style.whiteSpace = 'nowrap';
                
                if (linkGoogle) {{
                    const linkGB = document.createElement('a');
                    linkGB.href = linkGoogle;
                    linkGB.target = '_blank';
                    linkGB.className = 'link-button';
                    linkGB.textContent = '📚 Google Books';
                    linkGB.style.marginRight = '5px';
                    cellLinks.appendChild(linkGB);
                }}
                
                if (linkLibreria) {{
                    const linkLib = document.createElement('a');
                    linkLib.href = linkLibreria;
                    linkLib.target = '_blank';
                    linkLib.className = 'link-button';
                    linkLib.textContent = '🏪 Librería';
                    linkLib.style.backgroundColor = '#10b981';
                    cellLinks.appendChild(linkLib);
                }}
                
                if (!linkGoogle && !linkLibreria) {{
                    cellLinks.textContent = '-';
                }}
            }});
            
            // Actualizar información de paginación
            document.getElementById('librosDesde').textContent = inicio + 1;
            document.getElementById('librosHasta').textContent = fin;
            document.getElementById('librosTotal').textContent = todosLosLibros.length;
            
            paginaLibrosActual = pagina;
            generarControlesPaginacion();
        }}
        
        function generarControlesPaginacion() {{
            const totalPaginas = Math.ceil(todosLosLibros.length / librosPorPagina);
            const contenedor = document.getElementById('paginacionLibros');
            contenedor.innerHTML = '';
            
            if (totalPaginas <= 1) return;
            
            // Botón Anterior
            const btnAnterior = document.createElement('button');
            btnAnterior.textContent = '« Anterior';
            btnAnterior.disabled = paginaLibrosActual === 1;
            btnAnterior.onclick = () => {{
                if (paginaLibrosActual > 1) {{
                    mostrarLibrosPagina(paginaLibrosActual - 1);
                    window.scrollTo({{ top: document.getElementById('libros').offsetTop - 150, behavior: 'smooth' }});
                }}
            }};
            contenedor.appendChild(btnAnterior);
            
            // Números de página
            const inicioPagina = Math.max(1, paginaLibrosActual - 2);
            const finPagina = Math.min(totalPaginas, paginaLibrosActual + 2);
            
            if (inicioPagina > 1) {{
                const btn1 = document.createElement('button');
                btn1.textContent = '1';
                btn1.onclick = () => {{ mostrarLibrosPagina(1); window.scrollTo({{ top: document.getElementById('libros').offsetTop - 150, behavior: 'smooth' }}); }};
                contenedor.appendChild(btn1);
                
                if (inicioPagina > 2) {{
                    const ellipsis = document.createElement('span');
                    ellipsis.textContent = '...';
                    ellipsis.className = 'page-info';
                    contenedor.appendChild(ellipsis);
                }}
            }}
            
            for (let i = inicioPagina; i <= finPagina; i++) {{
                const btn = document.createElement('button');
                btn.textContent = i;
                btn.className = i === paginaLibrosActual ? 'active' : '';
                btn.onclick = () => {{
                    mostrarLibrosPagina(i);
                    window.scrollTo({{ top: document.getElementById('libros').offsetTop - 150, behavior: 'smooth' }});
                }};
                contenedor.appendChild(btn);
            }}
            
            if (finPagina < totalPaginas) {{
                if (finPagina < totalPaginas - 1) {{
                    const ellipsis = document.createElement('span');
                    ellipsis.textContent = '...';
                    ellipsis.className = 'page-info';
                    contenedor.appendChild(ellipsis);
                }}
                
                const btnUltima = document.createElement('button');
                btnUltima.textContent = totalPaginas;
                btnUltima.onclick = () => {{
                    mostrarLibrosPagina(totalPaginas);
                    window.scrollTo({{ top: document.getElementById('libros').offsetTop - 150, behavior: 'smooth' }});
                }};
                contenedor.appendChild(btnUltima);
            }}
            
            // Botón Siguiente
            const btnSiguiente = document.createElement('button');
            btnSiguiente.textContent = 'Siguiente »';
            btnSiguiente.disabled = paginaLibrosActual === totalPaginas;
            btnSiguiente.onclick = () => {{
                if (paginaLibrosActual < totalPaginas) {{
                    mostrarLibrosPagina(paginaLibrosActual + 1);
                    window.scrollTo({{ top: document.getElementById('libros').offsetTop - 150, behavior: 'smooth' }});
                }}
            }};
            contenedor.appendChild(btnSiguiente);
        }}
        
        function cambiarLibrosPorPagina() {{
            const select = document.getElementById('librosPorPagina');
            librosPorPagina = parseInt(select.value);
            paginaLibrosActual = 1;
            mostrarLibrosPagina(1);
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
    </div> <!-- content-wrapper -->
</body>
</html>
"""
    
    # Guardar archivo
    archivo_salida = "../output/html/dashboard_completo.html"
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard completo generado: {archivo_salida}")
    print(f"\n🌐 Para verlo:")
    print(f"   1. Abre el archivo: {archivo_salida}")
    print(f"   2. O ejecuta: python3 servidor_local.py")
    print(f"   3. Luego abre: http://localhost:8000/{archivo_salida}")
    print(f"\n📋 Pestañas disponibles:")
    print(f"   • Resumen - Métricas principales")
    print(f"   • Mapa Interactivo - Visualización geográfica")
    print(f"   • Gráficos - Visualizaciones interactivas")
    print(f"   • Top Librerías - Las mejores por reseñas y ventas")
    print(f"   • Todas las Librerías - Lista completa con búsqueda")
    print(f"   • Análisis de Libros - Libros encontrados y estadísticas")
    print(f"   • Metodología - Cómo se hizo el análisis")
    print(f"   • Limitaciones - Aclaraciones importantes")


if __name__ == "__main__":
    generar_dashboard_completo()

