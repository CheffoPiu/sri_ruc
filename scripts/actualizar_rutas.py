"""
Script para actualizar rutas en todos los archivos Python después de reorganizar
"""
import os
import re
import glob

# Mapeo de rutas antiguas a nuevas
RUTAS = {
    # Archivos de datos
    '../data/output/librerias_con_info_google.xlsx': '../data/output/librerias_con_info_google.xlsx',
    '../data/output/librerias_detalle.xlsx': '../data/output/librerias_detalle.xlsx',
    '../data/output/libros_encontrados_librerias.xlsx': '../data/output/libros_encontrados_librerias.xlsx',
    '../data/output/estadisticas_libros.json': '../data/output/estadisticas_libros.json',
    '../config/google_maps_api_key.txt': '../config/google_maps_api_key.txt',
    
    # Archivos HTML de salida
    '../output/html/dashboard_completo.html': '../output/html/dashboard_completo.html',
    '../output/html/mapa_google_maps_filtrado.html': '../output/html/mapa_google_maps_filtrado.html',
    '../output/html/mapa_google_maps.html': '../output/html/mapa_google_maps.html',
    
    # Carpetas
    '../data/input/datos_excel/': '../data/input/datos_excel/',
}

def actualizar_archivo(archivo):
    """Actualiza las rutas en un archivo."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        contenido_original = contenido
        
        # Reemplazar rutas
        for ruta_antigua, ruta_nueva in RUTAS.items():
            # Reemplazar rutas simples
            contenido = contenido.replace(f'"{ruta_antigua}"', f'"{ruta_nueva}"')
            contenido = contenido.replace(f"'{ruta_antigua}'", f"'{ruta_nueva}'")
            
            # Reemplazar en os.path.exists, os.path.join, etc.
            contenido = re.sub(
                rf'os\.path\.(exists|join|isfile)\s*\(\s*["\']?{re.escape(ruta_antigua)}["\']?\s*\)',
                lambda m: m.group(0).replace(ruta_antigua, ruta_nueva),
                contenido
            )
            
            # Reemplazar en pd.read_excel, open, etc.
            contenido = re.sub(
                rf'(pd\.read_excel|open|json\.(load|dump))\s*\(\s*["\']?{re.escape(ruta_antigua)}["\']?\s*',
                lambda m: m.group(0).replace(ruta_antigua, ruta_nueva),
                contenido
            )
        
        if contenido != contenido_original:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
            return True
        return False
    except Exception as e:
        print(f"   ⚠️  Error en {archivo}: {e}")
        return False

def main():
    """Actualiza todas las rutas."""
    print("=" * 70)
    print("🔄 ACTUALIZANDO RUTAS EN SCRIPTS")
    print("=" * 70)
    print()
    
    # Buscar todos los archivos Python
    scripts = glob.glob('*.py')
    
    actualizados = 0
    for script in scripts:
        print(f"📝 Procesando: {script}...", end=' ')
        if actualizar_archivo(script):
            print("✅ Actualizado")
            actualizados += 1
        else:
            print("⏭️  Sin cambios")
    
    print()
    print(f"✅ {actualizados} archivo(s) actualizado(s)")

if __name__ == "__main__":
    main()

