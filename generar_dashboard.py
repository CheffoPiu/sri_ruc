"""
Generador de Dashboard Interactivo HTML
Crea un dashboard visual con gráficos y tablas interactivas.
"""

import pandas as pd
import json
import os
from datetime import datetime

def generar_dashboard_html():
    """Genera un dashboard HTML interactivo con gráficos."""
    
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
         'CALIFICACION_GOOGLE', 'ESTIMACION_VENTA_MENSUAL', 'DESCRIPCION_CANTON_EST']
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
            'nombre': str(nombre)[:50],
            'resenas': int(float(row['NUMERO_RESENAS'])),
            'calificacion': float(round(row['CALIFICACION_GOOGLE'], 1)),
            'venta_mensual': float(round(row['ESTIMACION_VENTA_MENSUAL'], 2)),
            'canton': str(row['DESCRIPCION_CANTON_EST'])
        })
    
    # Distribución de reseñas
    distribucion_resenas = {
        '0-10': len(encontradas[(encontradas['NUMERO_RESENAS'] >= 0) & (encontradas['NUMERO_RESENAS'] <= 10)]),
        '11-50': len(encontradas[(encontradas['NUMERO_RESENAS'] > 10) & (encontradas['NUMERO_RESENAS'] <= 50)]),
        '51-100': len(encontradas[(encontradas['NUMERO_RESENAS'] > 50) & (encontradas['NUMERO_RESENAS'] <= 100)]),
        '100+': len(encontradas[encontradas['NUMERO_RESENAS'] > 100])
    }
    
    # Generar HTML
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Análisis de Librerías</title>
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
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
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
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            color: #666;
            font-size: 1em;
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
            font-size: 1.5em;
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
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        
        tr:hover {{
            background: #f5f5f5;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}
        
        .badge-high {{
            background: #28a745;
            color: white;
        }}
        
        .badge-medium {{
            background: #ffc107;
            color: #333;
        }}
        
        .badge-low {{
            background: #dc3545;
            color: white;
        }}
        
        .footer {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            color: #666;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Dashboard - Análisis de Librerías</h1>
            <p>Códigos CIIU: G476101 y G476104 | Fecha: {fecha}</p>
        </div>
        
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
        
        <div class="table-card">
            <h2>🏆 Top 10 Librerías</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>Reseñas</th>
                        <th>Calificación</th>
                        <th>Venta Mensual (USD)</th>
                        <th>Cantón</th>
                    </tr>
                </thead>
                <tbody id="tablaTop10">
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>⚠️ <strong>Nota:</strong> Las estimaciones de ventas están basadas en indicadores de Google Maps (reseñas, calificaciones, presencia online).</p>
            <p>Estas son estimaciones y deben validarse con datos oficiales del SRI.</p>
        </div>
    </div>
    
    <script>
        // Datos
        const provinciasData = {json.dumps(provincias_data, ensure_ascii=False)};
        const top10Data = {json.dumps(top_10_data, ensure_ascii=False)};
        const distribucionResenas = {json.dumps(distribucion_resenas, ensure_ascii=False)};
        
        // Colores
        const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a'];
        
        // Gráfico de Ventas por Provincia
        const ctxProvincias = document.getElementById('chartProvincias').getContext('2d');
        new Chart(ctxProvincias, {{
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
        new Chart(ctxResenas, {{
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
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Gráfico de Cantidad por Provincia
        const ctxCantidad = document.getElementById('chartCantidad').getContext('2d');
        new Chart(ctxCantidad, {{
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
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Gráfico Top 10
        const ctxTop10 = document.getElementById('chartTop10').getContext('2d');
        new Chart(ctxTop10, {{
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
                    x: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        
        // Llenar tabla
        const tabla = document.getElementById('tablaTop10');
        top10Data.forEach((lib, index) => {{
            const row = tabla.insertRow();
            row.insertCell(0).textContent = index + 1;
            row.insertCell(1).textContent = lib.nombre;
            row.insertCell(2).textContent = lib.resenas.toLocaleString();
            row.insertCell(3).innerHTML = '⭐ ' + lib.calificacion;
            row.insertCell(4).textContent = '$' + lib.venta_mensual.toLocaleString('es-ES', {{maximumFractionDigits: 0}});
            row.insertCell(5).textContent = lib.canton;
        }});
    </script>
</body>
</html>
"""
    
    # Guardar archivo
    archivo_salida = "dashboard_librerias.html"
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard generado: {archivo_salida}")
    print(f"\n🌐 Para verlo:")
    print(f"   1. Abre el archivo: {archivo_salida}")
    print(f"   2. O ejecuta: python3 servidor_local.py")
    print(f"   3. Luego abre: http://localhost:8000/{archivo_salida}")


if __name__ == "__main__":
    generar_dashboard_html()

