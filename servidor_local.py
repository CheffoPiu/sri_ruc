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
    
    # Verificar qué archivos de mapa existen
    archivos_mapas = []
    if os.path.exists("mapa_google_maps_filtrado.html"):
        archivos_mapas.append("mapa_google_maps_filtrado.html")
    if os.path.exists("mapa_google_maps.html"):
        archivos_mapas.append("mapa_google_maps.html")
    
    if not archivos_mapas:
        print(f"❌ No se encontraron archivos de mapa")
        print("   Ejecuta primero: python3 generar_mapa_filtrado.py")
        print("   O: python3 generar_mapa_google.py")
        return
    
    # Usar el mapa filtrado si existe, sino el normal
    archivo_mapa = archivos_mapas[0]
    
    # Cambiar al directorio del script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Crear servidor
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/{archivo_mapa}"
            
            print("=" * 60)
            print("🌐 Servidor local iniciado")
            print("=" * 60)
            print(f"📍 URL del mapa principal: {url}")
            print(f"📂 Servidor corriendo en: http://localhost:{PORT}/")
            print()
            if len(archivos_mapas) > 1:
                print("📋 Mapas disponibles:")
                for mapa in archivos_mapas:
                    print(f"   • http://localhost:{PORT}/{mapa}")
            print()
            print("💡 Presiona Ctrl+C para detener el servidor")
            print()
            
            # Abrir automáticamente en el navegador
            try:
                webbrowser.open(url)
                print("✅ Abriendo mapa en tu navegador...")
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

