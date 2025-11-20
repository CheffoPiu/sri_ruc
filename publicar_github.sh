#!/bin/bash
# Script para publicar el mapa en GitHub Pages

echo "🌐 Publicador de Mapa en GitHub Pages"
echo "======================================"
echo ""

# Verificar que existe el archivo HTML
if [ ! -f "mapa_google_maps_filtrado.html" ]; then
    echo "❌ Error: No se encontró 'mapa_google_maps_filtrado.html'"
    echo "   Ejecuta primero: python3 generar_mapa_filtrado.py"
    exit 1
fi

echo "✅ Archivo encontrado: mapa_google_maps_filtrado.html"
echo ""

# Verificar si git está inicializado
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    echo "✅ Repositorio inicializado"
    echo ""
fi

# Verificar .gitignore
if [ ! -f ".gitignore" ]; then
    echo "📝 Creando .gitignore..."
    cat > .gitignore << 'EOF'
# API Keys (NUNCA subir)
google_maps_api_key.txt

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# Archivos temporales
*.log
.DS_Store
EOF
    echo "✅ .gitignore creado"
    echo ""
fi

# Verificar que el API key no se va a subir
if grep -q "google_maps_api_key.txt" .gitignore; then
    echo "✅ API key protegido en .gitignore"
else
    echo "⚠️  Agregando API key a .gitignore..."
    echo "google_maps_api_key.txt" >> .gitignore
fi
echo ""

# Agregar archivos
echo "📤 Agregando archivos a Git..."
git add mapa_google_maps_filtrado.html .gitignore

# Verificar si hay cambios
if git diff --staged --quiet; then
    echo "ℹ️  No hay cambios nuevos para subir"
else
    echo "💾 Creando commit..."
    git commit -m "Publicar mapa interactivo de establecimientos SRI"
    echo "✅ Commit creado"
fi
echo ""

# Verificar si hay un remote configurado
if git remote | grep -q "origin"; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ Remote configurado: $REMOTE_URL"
    echo ""
    echo "📤 Subiendo a GitHub..."
    git branch -M main 2>/dev/null
    git push -u origin main
    echo ""
    echo "✅ Archivos subidos a GitHub"
    echo ""
    echo "🔧 Ahora activa GitHub Pages:"
    echo "   1. Ve a tu repositorio en GitHub"
    echo "   2. Settings → Pages (en el menú lateral)"
    echo "   3. Source: 'Deploy from a branch'"
    echo "   4. Branch: 'main' / '/ (root)'"
    echo "   5. Folder: '/ (root)'"
    echo "   6. Save"
    echo ""
    echo "🌐 Tu URL será:"
    REPO_NAME=$(basename -s .git "$REMOTE_URL" 2>/dev/null || echo "TU_REPOSITORIO")
    echo "   https://$(echo $REMOTE_URL | sed 's/.*github.com[:/]\([^/]*\)\/\([^/]*\).*/\1.github.io\/\2/' | sed 's/\.git$//')/mapa_google_maps_filtrado.html"
else
    echo "📋 Pasos para configurar GitHub:"
    echo ""
    echo "1. Crea un repositorio en GitHub:"
    echo "   - Ve a: https://github.com/new"
    echo "   - Nombre: sri-ruc-mapa (o el que prefieras)"
    echo "   - Marca 'Public' (necesario para GitHub Pages gratis)"
    echo "   - NO inicialices con README, .gitignore o licencia"
    echo "   - Haz clic en 'Create repository'"
    echo ""
    echo "2. Conecta este repositorio local con GitHub:"
    echo "   git remote add origin https://github.com/TU_USUARIO/sri-ruc-mapa.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. Activa GitHub Pages:"
    echo "   - Ve a Settings → Pages"
    echo "   - Source: 'Deploy from a branch'"
    echo "   - Branch: 'main' / '/ (root)'"
    echo "   - Save"
    echo ""
    echo "4. Tu URL será:"
    echo "   https://TU_USUARIO.github.io/sri-ruc-mapa/mapa_google_maps_filtrado.html"
    echo ""
    read -p "¿Ya creaste el repositorio en GitHub? (s/n): " respuesta
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        read -p "Ingresa la URL de tu repositorio (ej: https://github.com/usuario/sri-ruc-mapa.git): " repo_url
        if [ ! -z "$repo_url" ]; then
            git remote add origin "$repo_url"
            git branch -M main
            git push -u origin main
            echo ""
            echo "✅ ¡Listo! Ahora activa GitHub Pages en Settings → Pages"
        fi
    else
        echo ""
        echo "💡 Cuando crees el repositorio, ejecuta:"
        echo "   git remote add origin https://github.com/TU_USUARIO/sri-ruc-mapa.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
    fi
fi

echo ""
echo "🔒 IMPORTANTE: Antes de compartir, restringe tu API key:"
echo "   1. Ve a Google Cloud Console → Credentials"
echo "   2. Haz clic en tu API key"
echo "   3. Agrega restricción HTTP referrer: https://*.github.io/*"
echo "   4. Guarda"
echo ""

