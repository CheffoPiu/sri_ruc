"""
Análisis de Libros para Dashboard
Genera estadísticas y visualizaciones sobre libros de librerías
"""

import pandas as pd
import json
import os
from collections import Counter
from typing import Dict, List

def analizar_libros_para_dashboard():
    """Genera análisis de libros para integrar en el dashboard."""
    
    print("=" * 70)
    print("📚 ANÁLISIS DE LIBROS PARA DASHBOARD")
    print("=" * 70)
    print()
    
    # Cargar datos
    archivos = {
        'libros_encontrados': 'libros_encontrados_librerias.xlsx',
        'libros_populares': 'libros_populares_ecuador.xlsx',
        'resumen_librerias': 'resumen_analisis_libros_librerias.xlsx'
    }
    
    datos = {}
    for nombre, archivo in archivos.items():
        if os.path.exists(archivo):
            datos[nombre] = pd.read_excel(archivo)
            print(f"✅ Cargado: {archivo} ({len(datos[nombre])} registros)")
        else:
            print(f"⚠️  No encontrado: {archivo}")
            datos[nombre] = pd.DataFrame()
    
    print()
    
    # Análisis de libros encontrados
    estadisticas = {}
    
    if not datos['libros_encontrados'].empty:
        df_libros = datos['libros_encontrados']
        
        # Top libros
        if 'titulo' in df_libros.columns:
            top_libros = df_libros['titulo'].value_counts().head(10).to_dict()
            estadisticas['top_libros'] = top_libros
        
        # Top editoriales
        if 'editorial' in df_libros.columns:
            top_editoriales = df_libros[df_libros['editorial'] != 'N/A']['editorial'].value_counts().head(10).to_dict()
            estadisticas['top_editoriales'] = top_editoriales
        
        # Top autores
        if 'autor' in df_libros.columns:
            autores = []
            for autor_str in df_libros['autor'].dropna():
                if autor_str and autor_str != 'N/A':
                    autores.extend([a.strip() for a in str(autor_str).split(',')])
            top_autores = Counter(autores).most_common(10)
            estadisticas['top_autores'] = {autor: count for autor, count in top_autores}
        
        # Categorías
        if 'categorias' in df_libros.columns:
            categorias = []
            for cat_str in df_libros['categorias'].dropna():
                if cat_str and cat_str != 'N/A':
                    categorias.extend([c.strip() for c in str(cat_str).split(',')])
            top_categorias = Counter(categorias).most_common(10)
            estadisticas['top_categorias'] = {cat: count for cat, count in top_categorias}
        
        # Precios promedio
        if 'precio' in df_libros.columns:
            precios = df_libros['precio'].dropna()
            if len(precios) > 0:
                estadisticas['precio_promedio'] = float(precios.mean())
                estadisticas['precio_min'] = float(precios.min())
                estadisticas['precio_max'] = float(precios.max())
    
    # Análisis de libros populares
    if not datos['libros_populares'].empty:
        df_populares = datos['libros_populares']
        
        if 'titulo' in df_populares.columns:
            libros_populares_lista = df_populares['titulo'].head(20).tolist()
            estadisticas['libros_populares_ecuador'] = libros_populares_lista
    
    # Librerías con información de libros
    if not datos['resumen_librerias'].empty:
        df_resumen = datos['resumen_librerias']
        estadisticas['total_librerias_analizadas'] = len(df_resumen)
    
    # Contar librerías que realmente tienen libros encontrados
    if not datos['libros_encontrados'].empty:
        df_libros = datos['libros_encontrados']
        if 'libreria' in df_libros.columns:
            librerias_unicas_con_libros = df_libros['libreria'].nunique()
            estadisticas['librerias_con_info_libros'] = librerias_unicas_con_libros
        else:
            estadisticas['librerias_con_info_libros'] = 0
    elif not datos['resumen_librerias'].empty:
        # Fallback: contar las que tienen sitio web si no hay datos de libros
        df_resumen = datos['resumen_librerias']
        librerias_con_libros = df_resumen[df_resumen['tiene_sitio_web_real'] == True]
        estadisticas['librerias_con_info_libros'] = len(librerias_con_libros)
    
    # Guardar estadísticas en JSON para el dashboard
    archivo_json = "estadisticas_libros.json"
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(estadisticas, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Estadísticas guardadas en: {archivo_json}")
    print()
    
    # Mostrar resumen
    print("📊 RESUMEN DE ESTADÍSTICAS:")
    print("=" * 70)
    
    if 'top_libros' in estadisticas:
        print(f"\n📚 Top 5 Libros más encontrados:")
        for i, (libro, count) in enumerate(list(estadisticas['top_libros'].items())[:5], 1):
            print(f"   {i}. {libro}: {count} librería(s)")
    
    if 'top_editoriales' in estadisticas:
        print(f"\n📖 Top 5 Editoriales:")
        for i, (editorial, count) in enumerate(list(estadisticas['top_editoriales'].items())[:5], 1):
            print(f"   {i}. {editorial}: {count} libro(s)")
    
    if 'top_autores' in estadisticas:
        print(f"\n✍️  Top 5 Autores:")
        for i, (autor, count) in enumerate(list(estadisticas['top_autores'].items())[:5], 1):
            print(f"   {i}. {autor}: {count} libro(s)")
    
    if 'precio_promedio' in estadisticas:
        print(f"\n💰 Precios:")
        print(f"   Promedio: ${estadisticas['precio_promedio']:.2f} USD")
        print(f"   Mínimo: ${estadisticas['precio_min']:.2f} USD")
        print(f"   Máximo: ${estadisticas['precio_max']:.2f} USD")
    
    if 'librerias_con_info_libros' in estadisticas:
        print(f"\n🏪 Librerías:")
        print(f"   Con información de libros: {estadisticas['librerias_con_info_libros']}")
        print(f"   Total analizadas: {estadisticas['total_librerias_analizadas']}")
    
    print()
    print("✅ Análisis completado!")
    print("\n💡 Estos datos están listos para integrarse en el dashboard")


if __name__ == "__main__":
    analizar_libros_para_dashboard()

