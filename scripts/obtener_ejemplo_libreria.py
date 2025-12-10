"""Script rápido para obtener ejemplos de librerías activas"""
import pandas as pd

df = pd.read_excel('../data/output/librerias_detalle.xlsx')
activas = df[df['ESTADO_CONTRIBUYENTE'] == 'ACTIVO'].head(5)

print('='*70)
print('EJEMPLOS DE LIBRERÍAS ACTIVAS PARA CONSULTAR EN SRI')
print('='*70)

for idx, row in activas.iterrows():
    print(f'\n📚 Ejemplo {idx + 1}:')
    print(f'   RUC: {row["NUMERO_RUC"]}')
    print(f'   Nombre: {row["RAZON_SOCIAL"]}')
    print(f'   Provincia: {row["DESCRIPCION_PROVINCIA_EST"]}')
    print(f'   Cantón: {row["DESCRIPCION_CANTON_EST"]}')
    print(f'   Código CIIU: {row["CODIGO_CIIU"]}')
    if pd.notna(row.get('NOMBRE_FANTASIA_COMERCIAL')):
        print(f'   Nombre Fantasía: {row["NOMBRE_FANTASIA_COMERCIAL"]}')
    print('-'*70)

print('\n✅ Usa cualquiera de estos RUCs para el ejemplo en la guía')

