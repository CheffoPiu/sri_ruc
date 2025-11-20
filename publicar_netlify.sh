#!/bin/bash
# Script para publicar el mapa en Netlify fácilmente

echo "🌐 Publicador de Mapa en Netlify"
echo "=================================="
echo ""

# Verificar que existe el archivo HTML
if [ ! -f "mapa_google_maps_filtrado.html" ]; then
    echo "❌ Error: No se encontró 'mapa_google_maps_filtrado.html'"
    echo "   Ejecuta primero: python3 generar_mapa_filtrado.py"
    exit 1
fi

echo "✅ Archivo encontrado: mapa_google_maps_filtrado.html"
echo ""
echo "📋 Instrucciones:"
echo "1. Ve a https://www.netlify.com/"
echo "2. Inicia sesión o crea una cuenta (gratis)"
echo "3. En la página principal, verás un área para arrastrar archivos"
echo "4. Arrastra este archivo HTML o la carpeta completa"
echo "5. ¡Listo! Netlify te dará una URL automáticamente"
echo ""
echo "💡 Tip: Puedes cambiar el nombre del sitio en:"
echo "   Site settings → Change site name"
echo ""
echo "🔒 IMPORTANTE: Antes de publicar, restringe tu API key:"
echo "   1. Ve a Google Cloud Console → Credentials"
echo "   2. Haz clic en tu API key"
echo "   3. Agrega restricción HTTP referrer: https://*.netlify.app/*"
echo ""

# Verificar si Netlify CLI está instalado
if command -v netlify &> /dev/null; then
    echo "✅ Netlify CLI detectado"
    read -p "¿Quieres publicar ahora con CLI? (s/n): " respuesta
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        echo ""
        echo "🚀 Publicando en Netlify..."
        netlify deploy --prod --dir . --open
    else
        echo ""
        echo "📝 Abriendo Netlify en el navegador..."
        open "https://app.netlify.com/drop" 2>/dev/null || xdg-open "https://app.netlify.com/drop" 2>/dev/null || echo "Abre manualmente: https://app.netlify.com/drop"
    fi
else
    echo "💡 Tip: Instala Netlify CLI para publicar desde terminal:"
    echo "   npm install -g netlify-cli"
    echo ""
    echo "📝 Abriendo Netlify en el navegador..."
    open "https://app.netlify.com/drop" 2>/dev/null || xdg-open "https://app.netlify.com/drop" 2>/dev/null || echo "Abre manualmente: https://app.netlify.com/drop"
fi

