"""
Estimador de Ventas para Librerías
Proporciona estimaciones de ventas basadas en indicadores disponibles.
"""

import pandas as pd
import os
from typing import Dict, List

class EstimadorVentasLibrerias:
    """Estima ventas de librerías basándose en indicadores."""
    
    def __init__(self):
        # Rangos de estimación basados en estudios del sector
        # Estos son valores aproximados que pueden ajustarse
        self.rangos_ventas = {
            'pequena': {
                'min': 5000,  # USD/mes
                'max': 15000,
                'promedio': 10000,
                'descripcion': 'Librería pequeña (local pequeño, pocos empleados)'
            },
            'mediana': {
                'min': 15000,
                'max': 50000,
                'promedio': 30000,
                'descripcion': 'Librería mediana (local mediano, varios empleados)'
            },
            'grande': {
                'min': 50000,
                'max': 150000,
                'promedio': 80000,
                'descripcion': 'Librería grande (local grande, cadena, centro comercial)'
            }
        }
    
    def clasificar_libreria(self, registro: pd.Series) -> str:
        """Clasifica una librería en pequeña, mediana o grande basándose en indicadores."""
        # Indicadores que sugieren librería grande
        indicadores_grande = 0
        indicadores_mediana = 0
        
        # Agente de retención (indica mayor volumen de operaciones)
        if pd.notna(registro.get('AGENTE_RETENCION')):
            indicadores_grande += 2
        
        # Estado activo (operando actualmente)
        estado = str(registro.get('ESTADO_CONTRIBUYENTE', '')).upper()
        if 'ACTIVO' in estado:
            indicadores_mediana += 1
        elif 'SUSPENDIDO' in estado:
            return 'pequena'  # Si está suspendida, probablemente pequeña o cerrada
        
        # Nombre fantasia (indica marca establecida)
        if pd.notna(registro.get('NOMBRE_FANTASIA_COMERCIAL')):
            indicadores_mediana += 1
        
        # Ubicación en cantones grandes (más población = más ventas potenciales)
        canton = str(registro.get('DESCRIPCION_CANTON_EST', '')).upper()
        cantones_grandes = ['MACHALA', 'GUAYAQUIL', 'QUITO', 'CUENCA', 'AMBATO']
        if any(c in canton for c in cantones_grandes):
            indicadores_grande += 1
        
        # Clasificación
        if indicadores_grande >= 2:
            return 'grande'
        elif indicadores_mediana >= 1 or indicadores_grande >= 1:
            return 'mediana'
        else:
            return 'pequena'
    
    def estimar_ventas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Agrega estimaciones de ventas al DataFrame."""
        df_resultado = df.copy()
        
        # Clasificar cada librería
        clasificaciones = []
        estimaciones_mensuales = []
        estimaciones_anuales = []
        
        for idx, row in df.iterrows():
            clasificacion = self.clasificar_libreria(row)
            clasificaciones.append(clasificacion)
            
            rango = self.rangos_ventas[clasificacion]
            estimaciones_mensuales.append(rango['promedio'])
            estimaciones_anuales.append(rango['promedio'] * 12)
        
        df_resultado['CLASIFICACION_TAMANO'] = clasificaciones
        df_resultado['ESTIMACION_VENTAS_MENSUAL_USD'] = estimaciones_mensuales
        df_resultado['ESTIMACION_VENTAS_ANUAL_USD'] = estimaciones_anuales
        
        # Agregar rangos
        rangos_min_mensual = []
        rangos_max_mensual = []
        for clasif in clasificaciones:
            rango = self.rangos_ventas[clasif]
            rangos_min_mensual.append(rango['min'])
            rangos_max_mensual.append(rango['max'])
        
        df_resultado['ESTIMACION_MIN_MENSUAL_USD'] = rangos_min_mensual
        df_resultado['ESTIMACION_MAX_MENSUAL_USD'] = rangos_max_mensual
        
        return df_resultado
    
    def generar_resumen_estimaciones(self, df: pd.DataFrame) -> Dict:
        """Genera un resumen de las estimaciones."""
        if 'CLASIFICACION_TAMANO' not in df.columns:
            df = self.estimar_ventas(df)
        
        resumen = {
            'total_librerias': len(df),
            'por_tamano': {},
            'ventas_totales_estimadas': {}
        }
        
        # Por tamaño
        distribucion = df['CLASIFICACION_TAMANO'].value_counts()
        for tamano, cantidad in distribucion.items():
            librerias_tamano = df[df['CLASIFICACION_TAMANO'] == tamano]
            venta_promedio = librerias_tamano['ESTIMACION_VENTAS_MENSUAL_USD'].mean()
            venta_total_mensual = librerias_tamano['ESTIMACION_VENTAS_MENSUAL_USD'].sum()
            venta_total_anual = librerias_tamano['ESTIMACION_VENTAS_ANUAL_USD'].sum()
            
            resumen['por_tamano'][tamano] = {
                'cantidad': int(cantidad),
                'venta_promedio_mensual': round(venta_promedio, 2),
                'venta_total_mensual': round(venta_total_mensual, 2),
                'venta_total_anual': round(venta_total_anual, 2)
            }
        
        # Totales
        resumen['ventas_totales_estimadas'] = {
            'mensual_promedio': round(df['ESTIMACION_VENTAS_MENSUAL_USD'].sum(), 2),
            'anual_promedio': round(df['ESTIMACION_VENTAS_ANUAL_USD'].sum(), 2),
            'mensual_min': round(df['ESTIMACION_MIN_MENSUAL_USD'].sum(), 2),
            'mensual_max': round(df['ESTIMACION_MAX_MENSUAL_USD'].sum(), 2)
        }
        
        return resumen
    
    def exportar_con_estimaciones(self, df: pd.DataFrame, archivo_salida: str = "librerias_con_estimaciones.xlsx"):
        """Exporta los datos con estimaciones de ventas."""
        df_con_estimaciones = self.estimar_ventas(df)
        
        # Ordenar por estimación de ventas (mayor a menor)
        df_con_estimaciones = df_con_estimaciones.sort_values(
            'ESTIMACION_VENTAS_MENSUAL_USD', 
            ascending=False
        )
        
        df_con_estimaciones.to_excel(archivo_salida, index=False)
        print(f"✅ Datos con estimaciones exportados a: {archivo_salida}")
        return df_con_estimaciones


def main():
    """Función principal."""
    print("\n" + "="*70)
    print("💰 ESTIMADOR DE VENTAS PARA LIBRERÍAS")
    print("="*70)
    
    # Cargar datos de librerías
    archivo_librerias = "librerias_detalle.xlsx"
    
    if not os.path.exists(archivo_librerias):
        print(f"\n❌ No se encontró el archivo: {archivo_librerias}")
        print("   Ejecuta primero: python3 analizar_librerias.py")
        return
    
    print(f"\n📂 Cargando datos de: {archivo_librerias}")
    df = pd.read_excel(archivo_librerias)
    print(f"   Total de librerías: {len(df):,}")
    
    # Estimar ventas
    estimador = EstimadorVentasLibrerias()
    print("\n📊 Generando estimaciones de ventas...")
    df_con_estimaciones = estimador.exportar_con_estimaciones(df)
    
    # Generar resumen
    print("\n📈 Generando resumen de estimaciones...")
    resumen = estimador.generar_resumen_estimaciones(df_con_estimaciones)
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE ESTIMACIONES DE VENTAS")
    print("="*70)
    print(f"\nTotal de librerías analizadas: {resumen['total_librerias']:,}")
    
    print("\n📊 DISTRIBUCIÓN POR TAMAÑO:")
    print("-"*70)
    for tamano, info in resumen['por_tamano'].items():
        print(f"\n{tamano.upper()}:")
        print(f"  Cantidad: {info['cantidad']:,} librerías")
        print(f"  Venta promedio mensual: ${info['venta_promedio_mensual']:,.2f} USD")
        print(f"  Venta total mensual: ${info['venta_total_mensual']:,.2f} USD")
        print(f"  Venta total anual: ${info['venta_total_anual']:,.2f} USD")
    
    print("\n💰 ESTIMACIONES TOTALES DEL SECTOR:")
    print("-"*70)
    totales = resumen['ventas_totales_estimadas']
    print(f"Venta total mensual (promedio): ${totales['mensual_promedio']:,.2f} USD")
    print(f"Venta total anual (promedio): ${totales['anual_promedio']:,.2f} USD")
    print(f"Rango mensual: ${totales['mensual_min']:,.2f} - ${totales['mensual_max']:,.2f} USD")
    
    print("\n" + "="*70)
    print("⚠️  IMPORTANTE: Estas son ESTIMACIONES basadas en indicadores")
    print("   Para datos reales, consulta las fuentes recomendadas en el reporte")
    print("="*70)
    
    print("\n✅ Proceso completado!")
    print(f"   Revisa: librerias_con_estimaciones.xlsx")


if __name__ == "__main__":
    main()

