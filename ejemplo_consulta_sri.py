"""
Script para generar una lista de librerías activas con sus RUCs
para facilitar la consulta manual en el SRI
"""

import pandas as pd

def generar_lista_consulta_sri():
    """Genera una lista de librerías activas para consultar en el SRI."""
    
    # Cargar datos
    df = pd.read_excel('librerias_detalle.xlsx')
    
    # Filtrar solo activas
    activas = df[df['ESTADO_CONTRIBUYENTE'] == 'ACTIVO'].copy()
    
    # Ordenar por tamaño (si tienen estimaciones)
    if 'CLASIFICACION_TAMANO' in activas.columns:
        orden_tamano = {'grande': 1, 'mediana': 2, 'pequena': 3}
        activas['orden'] = activas['CLASIFICACION_TAMANO'].map(orden_tamano)
        activas = activas.sort_values('orden', na_position='last')
    
    print("="*80)
    print("📋 LISTA DE LIBRERÍAS ACTIVAS PARA CONSULTAR EN EL SRI")
    print("="*80)
    print(f"\nTotal de librerías activas: {len(activas)}")
    print("\n" + "="*80)
    
    # Generar lista numerada
    lista_consulta = []
    
    for idx, (_, row) in enumerate(activas.iterrows(), 1):
        ruc = str(row['NUMERO_RUC'])
        nombre = str(row['RAZON_SOCIAL'])
        fantasia = str(row.get('NOMBRE_FANTASIA_COMERCIAL', 'N/A'))
        provincia = str(row['DESCRIPCION_PROVINCIA_EST'])
        canton = str(row['DESCRIPCION_CANTON_EST'])
        codigo = str(row['CODIGO_CIIU'])
        
        # Prioridad sugerida
        prioridad = "🔴 ALTA" if idx <= 20 else "🟡 MEDIA" if idx <= 40 else "🟢 BAJA"
        
        print(f"\n{idx}. {prioridad}")
        print(f"   RUC: {ruc}")
        print(f"   Nombre: {nombre}")
        if fantasia != 'N/A' and pd.notna(row.get('NOMBRE_FANTASIA_COMERCIAL')):
            print(f"   Fantasía: {fantasia}")
        print(f"   Ubicación: {canton}, {provincia}")
        print(f"   Código CIIU: {codigo}")
        print(f"   URL consulta: https://srienlinea.sri.gob.ec/ (buscar RUC: {ruc})")
        print("-"*80)
        
        lista_consulta.append({
            'Numero': idx,
            'Prioridad': prioridad,
            'RUC': ruc,
            'Razon_Social': nombre,
            'Nombre_Fantasia': fantasia if fantasia != 'N/A' else '',
            'Provincia': provincia,
            'Canton': canton,
            'Codigo_CIIU': codigo,
            'Base_Imponible_Mes': '',  # Para llenar manualmente
            'Base_Imponible_Anual': '',  # Para llenar manualmente
            'Ventas_Estimadas_Anual': ''  # Para llenar manualmente
        })
    
    # Exportar a Excel para facilitar el registro
    df_consulta = pd.DataFrame(lista_consulta)
    archivo_salida = 'lista_consulta_sri.xlsx'
    df_consulta.to_excel(archivo_salida, index=False)
    
    print(f"\n✅ Lista exportada a: {archivo_salida}")
    print("   Puedes usar este archivo para registrar los datos que obtengas del SRI")
    print("\n💡 Recomendación: Empieza con las primeras 20 (prioridad ALTA)")
    
    return df_consulta

if __name__ == "__main__":
    generar_lista_consulta_sri()

