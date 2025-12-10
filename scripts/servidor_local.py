"""
Servidor local simple para visualizar el mapa en el navegador.
Ejecuta este script y abre la URL que te muestra.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path


def main():
    """Inicia un servidor HTTP local."""
    PORT = 8001  # Cambiado a 8001 para evitar conflictos
    
    # Cambiar al directorio raíz del proyecto primero
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # Verificar qué archivos de mapa existen
    archivos_mapas = []
    if os.path.exists("output/html/mapa_google_maps_filtrado.html"):
        archivos_mapas.append("output/html/mapa_google_maps_filtrado.html")
    if os.path.exists("output/html/mapa_google_maps.html"):
        archivos_mapas.append("output/html/mapa_google_maps.html")
    if os.path.exists("output/html/dashboard_completo.html"):
        archivos_mapas.append("output/html/dashboard_completo.html")
    
    if not archivos_mapas:
        print(f"❌ No se encontraron archivos HTML")
        print("   Ejecuta primero: python3 scripts/generar_mapa_filtrado.py")
        print("   O: python3 scripts/generar_dashboard_completo.py")
        return
    
    # Usar el dashboard si existe, sino el mapa filtrado, sino el normal
    if "dashboard_completo.html" in archivos_mapas:
        archivo_principal = "output/html/dashboard_completo.html"
    else:
        archivo_principal = archivos_mapas[0]
    
    # Crear servidor
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/{archivo_principal}"
            
            print("=" * 60)
            print("🌐 Servidor local iniciado")
            print("=" * 60)
            print(f"📍 URL principal: {url}")
            print(f"📂 Servidor corriendo en: http://localhost:{PORT}/")
            print()
            if len(archivos_mapas) > 1:
                print("📋 Archivos disponibles:")
                for archivo in archivos_mapas:
                    print(f"   • http://localhost:{PORT}/{archivo}")
            print()
            print("💡 Presiona Ctrl+C para detener el servidor")
            print()
            
            # Abrir automáticamente en el navegador
            try:
                webbrowser.open(url)
                print("✅ Abriendo dashboard en tu navegador...")
            except:
                print("⚠️  No se pudo abrir automáticamente. Copia la URL de arriba.")
            
            print()
            print("=" * 60)
            
            # Mantener el servidor corriendo
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ El puerto {PORT} ya está en uso.")
            print(f"   Cierra la aplicación que lo está usando o cambia el puerto.")
        else:
            print(f"❌ Error: {str(e)}")
    except KeyboardInterrupt:
        print("\n\n✅ Servidor detenido")


if __name__ == "__main__":
    main()

