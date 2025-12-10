"""
Script de ayuda para configurar la API key de Google Maps.
Ejecuta este script para guardar tu API key de forma segura.
"""

import os


def main():
    print("=" * 60)
    print("🔑 Configuración de Google Maps API Key")
    print("=" * 60)
    print()
    print("📖 Para obtener tu API key, sigue estos pasos:")
    print()
    print("   1. Ve a: https://console.cloud.google.com/")
    print("   2. Crea un proyecto nuevo")
    print("   3. Habilita 'Geocoding API'")
    print("   4. Configura facturación (tienes $200 USD gratis/mes)")
    print("   5. Crea una API key en 'Credenciales'")
    print()
    print("   📄 Guía completa: obtener_api_key_paso_a_paso.md")
    print()
    
    # Verificar si ya existe
    if os.path.exists('../config/google_maps_api_key.txt'):
        print("⚠️  Ya existe un archivo '../config/google_maps_api_key.txt'")
        respuesta = input("¿Deseas sobrescribirlo? (s/n): ").lower()
        if respuesta != 's':
            print("Operación cancelada.")
            return
        print()
    
    # Solicitar API key
    print("Pega tu API key de Google Maps aquí:")
    print("(La API key se verá algo como: AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)")
    print()
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No se ingresó ninguna API key.")
        return
    
    if not api_key.startswith('AIza'):
        print("⚠️  Advertencia: La API key de Google Maps generalmente comienza con 'AIza'")
        respuesta = input("¿Continuar de todas formas? (s/n): ").lower()
        if respuesta != 's':
            print("Operación cancelada.")
            return
    
    # Guardar en archivo
    try:
        with open('../config/google_maps_api_key.txt', 'w') as f:
            f.write(api_key)
        
        # Establecer permisos restrictivos (solo lectura para el dueño)
        os.chmod('../config/google_maps_api_key.txt', 0o600)
        
        print()
        print("✅ API key guardada exitosamente en '../config/google_maps_api_key.txt'")
        print("   El archivo tiene permisos restrictivos para mayor seguridad.")
        print()
        print("Ahora puedes ejecutar:")
        print("   python3 generar_mapa_final.py")
        print()
        
    except Exception as e:
        print(f"❌ Error al guardar la API key: {str(e)}")


if __name__ == "__main__":
    main()

