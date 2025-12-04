"""
Análisis de Librerías - Códigos CIIU G476101 y G476104
Analiza los datos de librerías y proporciona recomendaciones para estimar ventas.
"""

import pandas as pd
import os
from collections import defaultdict
from typing import Dict, List, Tuple
import json

class AnalizadorLibrerias:
    """Analiza datos de librerías y proporciona insights."""
    
    def __init__(self):
        self.codigos_librerias = ['G476101', 'G476104']
        self.descripciones_ciiu = {
            'G476101': 'VENTA AL POR MENOR DE LIBROS DE TODO TIPO EN ESTABLECIMIENTOS ESPECIALIZADOS.',
            'G476102': 'VENTA AL POR MENOR DE PERIÓDICOS EN ESTABLECIMIENTOS ESPECIALIZADOS.',
            'G476103': 'VENTA AL POR MENOR DE ARTÍCULOS DE OFICINA Y PAPELERÍA COMO LÁPICES, BOLÍGRAFOS, PAPEL, ETCÉTERA, EN ESTABLECIMIENTOS ESPECIALIZADOS.',
            'G476104': 'VENTA AL POR MENOR DE LIBROS, PERIODICOS, REVISTAS Y ARTICULOS DE PAPELERIA.'
        }
    
    def cargar_datos(self, directorio: str = "datos_excel") -> pd.DataFrame:
        """Carga todos los archivos Excel y filtra por códigos de librerías."""
        archivos_excel = [f for f in os.listdir(directorio) 
                         if f.endswith(('.xlsx', '.xls')) and not f.startswith('~')]
        
        if not archivos_excel:
            print("❌ No se encontraron archivos Excel")
            return pd.DataFrame()
        
        todos_datos = []
        
        for archivo in archivos_excel:
            ruta = os.path.join(directorio, archivo)
            try:
                df = pd.read_excel(ruta)
                print(f"✅ Cargado: {archivo} ({len(df):,} registros)")
                
                # Filtrar por códigos de librerías
                if 'CODIGO_CIIU' in df.columns:
                    df_filtrado = df[df['CODIGO_CIIU'].isin(self.codigos_librerias)]
                    if not df_filtrado.empty:
                        todos_datos.append(df_filtrado)
                        print(f"   → {len(df_filtrado):,} librerías encontradas")
            except Exception as e:
                print(f"⚠️  Error al leer {archivo}: {str(e)}")
        
        if todos_datos:
            df_completo = pd.concat(todos_datos, ignore_index=True)
            print(f"\n📊 Total de librerías encontradas: {len(df_completo):,}")
            return df_completo
        else:
            return pd.DataFrame()
    
    def analizar_estadisticas(self, df: pd.DataFrame) -> Dict:
        """Genera estadísticas detalladas de las librerías."""
        if df.empty:
            return {}
        
        stats = {
            'total_librerias': len(df),
            'por_codigo_ciiu': {},
            'por_estado': {},
            'por_provincia': {},
            'por_canton': {},
            'activas': 0,
            'suspendidas': 0,
            'pasivas': 0,
            'con_fantasia': 0,
            'agentes_retencion': 0
        }
        
        # Análisis por código CIIU
        if 'CODIGO_CIIU' in df.columns:
            distribucion = df['CODIGO_CIIU'].value_counts()
            for codigo, cantidad in distribucion.items():
                stats['por_codigo_ciiu'][codigo] = {
                    'cantidad': int(cantidad),
                    'porcentaje': round((cantidad / len(df)) * 100, 2),
                    'descripcion': self.descripciones_ciiu.get(codigo, 'N/A')
                }
        
        # Análisis por estado
        if 'ESTADO_CONTRIBUYENTE' in df.columns:
            estados = df['ESTADO_CONTRIBUYENTE'].value_counts()
            for estado, cantidad in estados.items():
                estado_str = str(estado).upper().strip()
                stats['por_estado'][estado_str] = int(cantidad)
                
                if 'ACTIVO' in estado_str:
                    stats['activas'] += int(cantidad)
                elif 'SUSPENDIDO' in estado_str:
                    stats['suspendidas'] += int(cantidad)
                elif 'PASIVO' in estado_str:
                    stats['pasivas'] += int(cantidad)
        
        # Análisis por provincia
        col_provincia = next((col for col in df.columns if 'provincia' in col.lower()), None)
        if col_provincia:
            provincias = df[col_provincia].value_counts()
            for provincia, cantidad in provincias.items():
                stats['por_provincia'][str(provincia)] = int(cantidad)
        
        # Análisis por cantón
        col_canton = next((col for col in df.columns if 'canton' in col.lower()), None)
        if col_canton:
            cantones = df[col_canton].value_counts()
            stats['top_cantones'] = dict(cantones.head(10))
        
        # Análisis de nombre fantasia
        col_fantasia = next((col for col in df.columns if 'fantasia' in col.lower() or 'comercial' in col.lower()), None)
        if col_fantasia:
            stats['con_fantasia'] = int(df[col_fantasia].notna().sum())
        
        # Agentes de retención
        if 'AGENTE_RETENCION' in df.columns:
            stats['agentes_retencion'] = int(df['AGENTE_RETENCION'].notna().sum())
        
        return stats
    
    def identificar_palabras_clave(self, df: pd.DataFrame) -> Dict[str, int]:
        """Identifica palabras clave en nombres que indican si son librerías."""
        palabras_clave = {
            'libreria': 0,
            'libro': 0,
            'papeleria': 0,
            'papel': 0,
            'libros': 0,
            'librería': 0,
            'papelería': 0,
            'book': 0,
            'books': 0,
            'stationery': 0,
            'oficina': 0,
            'escolar': 0,
            'educacion': 0,
            'educación': 0
        }
        
        col_nombre = next((col for col in df.columns if any(x in col.lower() for x in ['razon', 'nombre', 'fantasia'])), None)
        
        if col_nombre:
            nombres = df[col_nombre].astype(str).str.lower()
            for palabra, _ in palabras_clave.items():
                palabras_clave[palabra] = int(nombres.str.contains(palabra, na=False).sum())
        
        return palabras_clave
    
    def generar_recomendaciones(self, stats: Dict) -> List[str]:
        """Genera recomendaciones para obtener más información sobre ventas."""
        recomendaciones = []
        
        recomendaciones.append("📊 FUENTES DE DATOS PARA ESTIMAR VENTAS:")
        recomendaciones.append("")
        
        recomendaciones.append("1. 📋 DATOS DEL SRI (Servicio de Rentas Internas):")
        recomendaciones.append("   • Consultar declaraciones de IVA (Formulario 104)")
        recomendaciones.append("   • Verificar facturación mensual/anual")
        recomendaciones.append("   • Revisar retenciones en la fuente")
        recomendaciones.append("   • Portal: https://srienlinea.sri.gob.ec/")
        recomendaciones.append("")
        
        recomendaciones.append("2. 🏢 REGISTRO MERCANTIL:")
        recomendaciones.append("   • Información financiera de empresas")
        recomendaciones.append("   • Estados financieros anuales")
        recomendaciones.append("   • Portal: https://www.registromercantil.gob.ec/")
        recomendaciones.append("")
        
        recomendaciones.append("3. 📱 ENCUESTAS DIRECTAS:")
        recomendaciones.append("   • Contactar librerías por teléfono/email")
        recomendaciones.append("   • Usar los RUCs para buscar información de contacto")
        recomendaciones.append("   • Preguntar sobre volumen de ventas estimado")
        recomendaciones.append("")
        
        recomendaciones.append("4. 🛒 PLATAFORMAS DE VENTA ONLINE:")
        recomendaciones.append("   • Buscar librerías en Google Maps")
        recomendaciones.append("   • Revisar reseñas y actividad en redes sociales")
        recomendaciones.append("   • Verificar si tienen tienda online")
        recomendaciones.append("")
        
        recomendaciones.append("5. 📈 ESTIMACIONES POR INDICADORES:")
        recomendaciones.append("   • Tamaño del establecimiento (si hay datos de superficie)")
        recomendaciones.append("   • Ubicación (centros comerciales = más ventas)")
        recomendaciones.append("   • Estado del contribuyente (ACTIVO = operando)")
        recomendaciones.append("   • Agente de retención (indica mayor volumen)")
        recomendaciones.append("")
        
        recomendaciones.append("6. 📚 ASOCIACIONES Y GREMIOS:")
        recomendaciones.append("   • Cámara de Comercio de Ecuador")
        recomendaciones.append("   • Asociaciones de libreros")
        recomendaciones.append("   • Solicitar datos agregados del sector")
        recomendaciones.append("")
        
        recomendaciones.append("7. 🔍 VERIFICACIÓN DE LIBRERÍAS REALES:")
        recomendaciones.append("   • Buscar nombres en Google Maps")
        recomendaciones.append("   • Verificar si tienen presencia online")
        recomendaciones.append("   • Revisar si el nombre contiene palabras clave de librería")
        recomendaciones.append("   • Comparar con directorios comerciales")
        
        return recomendaciones
    
    def generar_reporte(self, df: pd.DataFrame, archivo_salida: str = "reporte_librerias.txt"):
        """Genera un reporte completo de análisis."""
        print("\n" + "="*70)
        print("📚 ANÁLISIS DE LIBRERÍAS - CÓDIGOS G476101 y G476104")
        print("="*70)
        
        if df.empty:
            print("\n❌ No se encontraron datos de librerías")
            return
        
        # Estadísticas
        stats = self.analizar_estadisticas(df)
        palabras_clave = self.identificar_palabras_clave(df)
        
        # Generar reporte
        reporte = []
        reporte.append("="*70)
        reporte.append("📚 REPORTE DE ANÁLISIS DE LIBRERÍAS")
        reporte.append("Códigos CIIU: G476101 y G476104")
        reporte.append("="*70)
        reporte.append("")
        
        # Resumen general
        reporte.append("📊 RESUMEN GENERAL")
        reporte.append("-"*70)
        reporte.append(f"Total de establecimientos: {stats['total_librerias']:,}")
        reporte.append(f"Librerías activas: {stats['activas']:,}")
        reporte.append(f"Librerías suspendidas: {stats['suspendidas']:,}")
        reporte.append(f"Librerías pasivas: {stats['pasivas']:,}")
        reporte.append(f"Con nombre fantasia: {stats['con_fantasia']:,}")
        reporte.append(f"Agentes de retención: {stats['agentes_retencion']:,}")
        reporte.append("")
        
        # Por código CIIU
        reporte.append("📋 DISTRIBUCIÓN POR CÓDIGO CIIU")
        reporte.append("-"*70)
        for codigo, info in stats['por_codigo_ciiu'].items():
            reporte.append(f"\n{codigo}: {info['cantidad']:,} establecimientos ({info['porcentaje']}%)")
            reporte.append(f"  Descripción: {info['descripcion']}")
        reporte.append("")
        
        # Por estado
        reporte.append("📊 DISTRIBUCIÓN POR ESTADO")
        reporte.append("-"*70)
        for estado, cantidad in sorted(stats['por_estado'].items(), key=lambda x: x[1], reverse=True):
            porcentaje = (cantidad / stats['total_librerias']) * 100
            reporte.append(f"{estado}: {cantidad:,} ({porcentaje:.1f}%)")
        reporte.append("")
        
        # Por provincia
        if stats['por_provincia']:
            reporte.append("🗺️  DISTRIBUCIÓN POR PROVINCIA")
            reporte.append("-"*70)
            for provincia, cantidad in sorted(stats['por_provincia'].items(), key=lambda x: x[1], reverse=True):
                porcentaje = (cantidad / stats['total_librerias']) * 100
                reporte.append(f"{provincia}: {cantidad:,} ({porcentaje:.1f}%)")
            reporte.append("")
        
        # Top cantones
        if 'top_cantones' in stats:
            reporte.append("🏙️  TOP 10 CANTONES")
            reporte.append("-"*70)
            for canton, cantidad in stats['top_cantones'].items():
                reporte.append(f"{canton}: {cantidad:,}")
            reporte.append("")
        
        # Palabras clave
        reporte.append("🔍 ANÁLISIS DE PALABRAS CLAVE EN NOMBRES")
        reporte.append("-"*70)
        palabras_ordenadas = sorted(palabras_clave.items(), key=lambda x: x[1], reverse=True)
        for palabra, cantidad in palabras_ordenadas:
            if cantidad > 0:
                porcentaje = (cantidad / stats['total_librerias']) * 100
                reporte.append(f"'{palabra}': {cantidad:,} ({porcentaje:.1f}%)")
        reporte.append("")
        
        # Recomendaciones
        recomendaciones = self.generar_recomendaciones(stats)
        reporte.extend(recomendaciones)
        reporte.append("")
        
        # Guardar reporte
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write('\n'.join(reporte))
        
        # Mostrar en consola
        print('\n'.join(reporte))
        print("\n" + "="*70)
        print(f"✅ Reporte guardado en: {archivo_salida}")
        print("="*70)
    
    def exportar_datos_librerias(self, df: pd.DataFrame, archivo_salida: str = "librerias_detalle.xlsx"):
        """Exporta los datos de librerías a Excel para análisis adicional."""
        if df.empty:
            print("❌ No hay datos para exportar")
            return
        
        # Seleccionar columnas relevantes
        columnas_relevantes = [
            'NUMERO_RUC', 'RAZON_SOCIAL', 'NOMBRE_FANTASIA_COMERCIAL',
            'CODIGO_CIIU', 'ACTIVIDAD_ECONOMICA',
            'ESTADO_CONTRIBUYENTE', 'ESTADO_ESTABLECIMIENTO',
            'DESCRIPCION_PROVINCIA_EST', 'DESCRIPCION_CANTON_EST', 'DESCRIPCION_PARROQUIA_EST',
            'AGENTE_RETENCION', 'FECHA_INICIO_ACTIVIDADES'
        ]
        
        columnas_disponibles = [col for col in columnas_relevantes if col in df.columns]
        df_exportar = df[columnas_disponibles].copy()
        
        # Agregar columna de verificación
        col_nombre = next((col for col in df.columns if 'razon' in col.lower() or 'nombre' in col.lower()), None)
        if col_nombre:
            nombres = df[col_nombre].astype(str).str.lower()
            df_exportar['VERIFICACION_LIBRERIA'] = nombres.str.contains(
                'libreria|librería|libro|libros|papeleria|papelería', 
                na=False, regex=True
            )
        
        df_exportar.to_excel(archivo_salida, index=False)
        print(f"✅ Datos exportados a: {archivo_salida}")
        print(f"   Total de registros: {len(df_exportar):,}")


def main():
    """Función principal."""
    analizador = AnalizadorLibrerias()
    
    print("\n🔍 Cargando datos de librerías...")
    df = analizador.cargar_datos()
    
    if not df.empty:
        print("\n📊 Generando análisis...")
        analizador.generar_reporte(df)
        
        print("\n💾 Exportando datos detallados...")
        analizador.exportar_datos_librerias(df)
        
        print("\n✅ Análisis completado!")
        print("\n📝 Próximos pasos:")
        print("   1. Revisa el reporte_librerias.txt para ver estadísticas")
        print("   2. Abre librerias_detalle.xlsx para análisis detallado")
        print("   3. Usa los RUCs para buscar información adicional en el SRI")
    else:
        print("\n❌ No se encontraron librerías con los códigos G476101 o G476104")


if __name__ == "__main__":
    main()

