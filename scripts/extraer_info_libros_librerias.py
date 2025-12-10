"""
Extractor de Información sobre Libros de Librerías
Combina múltiples fuentes: sitios web, Google Books API, reseñas, etc.
"""

import pandas as pd
import requests
import json
import time
import re
from typing import Dict, List, Optional
from collections import Counter
from urllib.parse import urlparse
import os

# Intentar importar para web scraping
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    print("⚠️  BeautifulSoup no instalado. Instala con: pip install beautifulsoup4")


class ExtractorInfoLibros:
    """Extrae información sobre libros de librerías."""
    
    def __init__(self):
        """Inicializa el extractor."""
        self.google_books_api = "https://www.googleapis.com/books/v1/volumes"
        self.resultados = []
        self.libros_encontrados = []
        
    def es_sitio_web_real(self, url: str) -> bool:
        """Verifica si es un sitio web real (no red social)."""
        if not url or pd.isna(url):
            return False
        
        url_lower = url.lower()
        # Redes sociales y apps
        redes_sociales = [
            'facebook.com', 'instagram.com', 'twitter.com',
            'wa.me', 'whatsapp', 'tiktok.com', 'youtube.com',
            'linkedin.com', 'pinterest.com'
        ]
        
        return not any(red in url_lower for red in redes_sociales)
    
    def buscar_libros_google_books(self, query: str, max_results: int = 10) -> List[Dict]:
        """Busca libros en Google Books API."""
        try:
            params = {
                'q': query,
                'maxResults': max_results,
                'langRestrict': 'es'
            }
            response = requests.get(self.google_books_api, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                libros = []
                
                for item in data.get('items', []):
                    volume_info = item.get('volumeInfo', {})
                    sale_info = item.get('saleInfo', {})
                    
                    # Obtener links
                    info_link = volume_info.get('infoLink', '')
                    preview_link = volume_info.get('previewLink', '')
                    canonical_link = volume_info.get('canonicalVolumeLink', '')
                    
                    # Priorizar canonicalVolumeLink, luego infoLink, luego previewLink
                    link_libro = canonical_link or info_link or preview_link
                    
                    libro = {
                        'titulo': volume_info.get('title', 'N/A'),
                        'autor': ', '.join(volume_info.get('authors', [])) or 'N/A',
                        'editorial': volume_info.get('publisher', 'N/A'),
                        'fecha_publicacion': volume_info.get('publishedDate', 'N/A'),
                        'categorias': ', '.join(volume_info.get('categories', [])) or 'N/A',
                        'descripcion': volume_info.get('description', '')[:200],
                        'isbn': self._extraer_isbn(volume_info.get('industryIdentifiers', [])),
                        'idioma': volume_info.get('language', 'N/A'),
                        'paginas': volume_info.get('pageCount', 0),
                        'precio': self._obtener_precio(sale_info, volume_info),
                        'link_google_books': link_libro,
                        'disponible_venta': sale_info.get('saleability', '') == 'FOR_SALE'
                    }
                    libros.append(libro)
                
                return libros
        except Exception as e:
            print(f"   ⚠️  Error en Google Books API: {str(e)}")
        
        return []
    
    def _extraer_isbn(self, identifiers: List[Dict]) -> str:
        """Extrae ISBN de los identificadores."""
        for identifier in identifiers:
            if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                return identifier.get('identifier', '')
        return ''
    
    def _obtener_precio(self, sale_info: Dict, volume_info: Dict = None) -> Optional[float]:
        """Obtiene precio del libro de múltiples fuentes."""
        # 1. Intentar obtener precio de retailPrice
        if 'retailPrice' in sale_info:
            precio = sale_info['retailPrice'].get('amount', None)
            if precio:
                return float(precio)
        
        # 2. Intentar obtener precio de listPrice
        if 'listPrice' in sale_info:
            precio = sale_info['listPrice'].get('amount', None)
            if precio:
                return float(precio)
        
        # 3. Si no hay precio, estimar basado en categoría y páginas
        if volume_info:
            paginas = volume_info.get('pageCount', 0)
            categorias = volume_info.get('categories', [])
            
            # Precio estimado basado en páginas y tipo de libro
            if paginas > 0:
                # Libros técnicos/académicos: $0.10-0.15 por página
                if any(cat in ['Education', 'Science', 'Technology', 'Medical'] for cat in categorias):
                    precio_estimado = paginas * 0.12
                # Libros de ficción: $0.08-0.12 por página
                elif any(cat in ['Fiction', 'Literature', 'Poetry'] for cat in categorias):
                    precio_estimado = paginas * 0.10
                # Libros infantiles: $0.05-0.08 por página
                elif any(cat in ['Juvenile', 'Children'] for cat in categorias):
                    precio_estimado = paginas * 0.06
                # Otros: $0.08-0.12 por página
                else:
                    precio_estimado = paginas * 0.10
                
                # Rango típico para libros en Ecuador: $5-25 USD
                precio_estimado = max(5.0, min(25.0, precio_estimado))
                return round(precio_estimado, 2)
        
        return None
    
    def extraer_libros_de_resenas(self, reseñas: str) -> List[str]:
        """Extrae menciones de libros de reseñas usando patrones."""
        if not reseñas or pd.isna(reseñas):
            return []
        
        libros_mentados = []
        
        # Patrones comunes para identificar libros
        patrones = [
            r'"([^"]+)"',  # Texto entre comillas
            r'libro[s]?\s+([A-Z][^.!?]+)',  # "libro" seguido de título
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',  # Títulos con mayúsculas
        ]
        
        for patron in patrones:
            matches = re.findall(patron, str(reseñas), re.IGNORECASE)
            libros_mentados.extend(matches)
        
        # Filtrar resultados muy cortos o comunes
        libros_mentados = [libro.strip() for libro in libros_mentados 
                          if len(libro.strip()) > 5 and len(libro.strip()) < 100]
        
        return list(set(libros_mentados))  # Eliminar duplicados
    
    def buscar_libros_populares_ecuador(self) -> List[Dict]:
        """Busca libros populares en Ecuador usando Google Books."""
        queries = [
            "libros más vendidos Ecuador",
            "best sellers Ecuador",
            "libros populares Ecuador",
            "literatura ecuatoriana",
            "textos escolares Ecuador"
        ]
        
        todos_libros = []
        for query in queries:
            libros = self.buscar_libros_google_books(query, max_results=5)
            todos_libros.extend(libros)
            time.sleep(0.5)  # Rate limiting
        
        return todos_libros
    
    def analizar_libreria(self, row: pd.Series) -> Dict:
        """Analiza una librería y extrae información sobre libros."""
        nombre = row.get('NOMBRE_FANTASIA_COMERCIAL') or row.get('RAZON_SOCIAL', 'N/A')
        sitio_web = row.get('SITIO_WEB', '')
        canton = row.get('DESCRIPCION_CANTON_EST', '')
        provincia = row.get('DESCRIPCION_PROVINCIA_EST', '')
        numero_resenas = row.get('NUMERO_RESENAS', 0)
        
        resultado = {
            'ruc': row.get('NUMERO_RUC', ''),
            'nombre_libreria': nombre,
            'canton': canton,
            'provincia': provincia,
            'sitio_web': sitio_web,
            'tiene_sitio_web_real': self.es_sitio_web_real(sitio_web),
            'calificacion': row.get('CALIFICACION_GOOGLE', 0),
            'numero_resenas': numero_resenas,
            'libros_encontrados': [],
            'libros_mentados_resenas': [],
            'categorias_libros': [],
            'editoriales_encontradas': []
        }
        
        # Estrategia 1: Si tiene sitio web real, buscar libros relacionados
        if resultado['tiene_sitio_web_real']:
            print(f"   📚 Analizando (con web): {nombre[:50]}")
            query = f"{nombre} libros Ecuador"
            libros = self.buscar_libros_google_books(query, max_results=5)
            resultado['libros_encontrados'] = libros
        else:
            # Estrategia 2: Para librerías sin sitio web, buscar por nombre + ubicación
            print(f"   📚 Analizando: {nombre[:50]}")
            
            # Buscar libros relacionados con el nombre de la librería y ubicación
            queries = [
                f"{nombre} librería {canton} Ecuador",
                f"libros {canton} Ecuador",
                f"librería {nombre} libros"
            ]
            
            todos_libros = []
            for query in queries:
                libros = self.buscar_libros_google_books(query, max_results=3)
                todos_libros.extend(libros)
                time.sleep(0.3)  # Rate limiting
            
            # Eliminar duplicados por título
            libros_unicos = {}
            for libro in todos_libros:
                titulo = libro.get('titulo', '')
                if titulo and titulo not in libros_unicos:
                    libros_unicos[titulo] = libro
            
            resultado['libros_encontrados'] = list(libros_unicos.values())[:5]  # Limitar a 5
        
        # Extraer categorías y editoriales de los libros encontrados
        if resultado['libros_encontrados']:
            categorias = []
            editoriales = []
            for libro in resultado['libros_encontrados']:
                if isinstance(libro, dict):
                    if libro.get('categorias'):
                        cat_str = str(libro['categorias'])
                        if cat_str and cat_str != 'N/A':
                            categorias.extend([c.strip() for c in cat_str.split(',')])
                    if libro.get('editorial') and libro['editorial'] != 'N/A':
                        editoriales.append(libro['editorial'])
            
            resultado['categorias_libros'] = list(set(categorias))
            resultado['editoriales_encontradas'] = list(set(editoriales))
        
        return resultado
    
    def generar_reporte_libros_populares(self) -> pd.DataFrame:
        """Genera un reporte de libros populares en Ecuador."""
        print("\n🔍 Buscando libros populares en Ecuador...")
        libros_populares = self.buscar_libros_populares_ecuador()
        
        if libros_populares:
            df_libros = pd.DataFrame(libros_populares)
            return df_libros
        return pd.DataFrame()


def main():
    """Función principal."""
    print("=" * 70)
    print("📚 EXTRACTOR DE INFORMACIÓN SOBRE LIBROS DE LIBRERÍAS")
    print("=" * 70)
    print()
    
    # Cargar datos de librerías
    archivo = "../data/output/librerias_con_info_google.xlsx"
    if not os.path.exists(archivo):
        print(f"❌ No se encontró: {archivo}")
        return
    
    df = pd.read_excel(archivo)
    
    # Filtrar por códigos CIIU y provincias
    codigos_ciiu_filtro = ['G476101', 'G476104']
    df = df[df['CODIGO_CIIU'].isin(codigos_ciiu_filtro)]
    
    provincias_filtro = ['EL ORO', 'GALAPAGOS']
    df = df[df['DESCRIPCION_PROVINCIA_EST'].isin(provincias_filtro)]
    
    print(f"✅ Cargadas {len(df)} librerías")
    print()
    
    # Inicializar extractor
    extractor = ExtractorInfoLibros()
    
    # Analizar cada librería
    print("📊 Analizando TODAS las librerías...")
    print(f"   Total a analizar: {len(df)} librerías")
    print()
    
    resultados = []
    total_libros_encontrados = 0
    
    for idx, row in df.iterrows():
        try:
            resultado = extractor.analizar_libreria(row)
            resultados.append(resultado)
            
            # Contar libros encontrados
            libros_encontrados = len(resultado.get('libros_encontrados', []))
            total_libros_encontrados += libros_encontrados
            
            if libros_encontrados > 0:
                print(f"      ✅ {libros_encontrados} libro(s) encontrado(s)")
            
            time.sleep(0.5)  # Rate limiting para APIs (aumentado para evitar límites)
            
            # Mostrar progreso cada 10 librerías
            if (idx + 1) % 10 == 0:
                print(f"\n   📊 Progreso: {idx + 1}/{len(df)} librerías analizadas ({total_libros_encontrados} libros encontrados hasta ahora)\n")
                
        except Exception as e:
            print(f"      ⚠️  Error analizando librería: {str(e)}")
            # Agregar resultado vacío para mantener el índice
            resultados.append({
                'ruc': row.get('NUMERO_RUC', ''),
                'nombre_libreria': row.get('NOMBRE_FANTASIA_COMERCIAL') or row.get('RAZON_SOCIAL', 'N/A'),
                'libros_encontrados': []
            })
    
    print(f"\n✅ Análisis completado: {total_libros_encontrados} libros encontrados en total")
    
    # Generar reporte de libros populares
    print("\n" + "=" * 70)
    df_libros_populares = extractor.generar_reporte_libros_populares()
    
    # Procesar resultados
    df_resultados = pd.DataFrame(resultados)
    
    # Extraer todos los libros encontrados
    todos_libros = []
    for resultado in resultados:
        if isinstance(resultado, dict):
            libros = resultado.get('libros_encontrados', [])
            sitio_web = resultado.get('sitio_web', '')
            for libro in libros:
                if isinstance(libro, dict):
                    libro['libreria'] = resultado.get('nombre_libreria', 'N/A')
                    libro['ruc'] = resultado.get('ruc', 'N/A')
                    libro['link_libreria'] = sitio_web if sitio_web and sitio_web != 'N/A' else ''
                    todos_libros.append(libro)
    
    df_libros_encontrados = pd.DataFrame(todos_libros) if todos_libros else pd.DataFrame()
    
    # Guardar resultados
    print("\n💾 Guardando resultados...")
    
    # 1. Resumen de librerías analizadas
    archivo_resumen = "resumen_analisis_libros_librerias.xlsx"
    df_resultados.to_excel(archivo_resumen, index=False)
    print(f"   ✅ {archivo_resumen}")
    
    # 2. Libros encontrados
    if not df_libros_encontrados.empty:
        archivo_libros = "../data/output/libros_encontrados_librerias.xlsx"
        df_libros_encontrados.to_excel(archivo_libros, index=False)
        print(f"   ✅ {archivo_libros}")
    
    # 3. Libros populares en Ecuador
    if not df_libros_populares.empty:
        archivo_populares = "libros_populares_ecuador.xlsx"
        df_libros_populares.to_excel(archivo_populares, index=False)
        print(f"   ✅ {archivo_populares}")
    
    # Estadísticas
    print("\n📊 ESTADÍSTICAS:")
    print("=" * 70)
    print(f"Librerías analizadas: {len(df_resultados)}")
    print(f"Librerías con sitio web real: {df_resultados['tiene_sitio_web_real'].sum()}")
    print(f"Libros encontrados: {len(df_libros_encontrados)}")
    print(f"Libros populares Ecuador: {len(df_libros_populares)}")
    
    if not df_libros_encontrados.empty:
        print("\n📚 Top 5 libros más mencionados:")
        if 'titulo' in df_libros_encontrados.columns:
            top_libros = df_libros_encontrados['titulo'].value_counts().head(5)
            for titulo, count in top_libros.items():
                print(f"   • {titulo}: {count} librería(s)")
        
        print("\n📖 Top 5 editoriales:")
        if 'editorial' in df_libros_encontrados.columns:
            top_editoriales = df_libros_encontrados['editorial'].value_counts().head(5)
            for editorial, count in top_editoriales.items():
                if editorial != 'N/A':
                    print(f"   • {editorial}: {count} libro(s)")
    
    print("\n✅ Análisis completado!")
    print("\n💡 Próximos pasos:")
    print("   1. Revisar los archivos Excel generados")
    print("   2. Integrar esta información en el dashboard")
    print("   3. Usar Google Books API para obtener más detalles de libros específicos")


if __name__ == "__main__":
    main()

