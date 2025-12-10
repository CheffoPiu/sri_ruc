"""
Script para actualizar la ubicación de un RUC específico
"""
import pandas as pd
from urllib.parse import quote

def actualizar_ubicacion_ruc(ruc: str, nueva_direccion: str):
    """Actualiza la ubicación de un RUC específico."""
    archivo = "../data/output/librerias_con_info_google.xlsx"
    
    # Cargar datos
    df = pd.read_excel(archivo)
    
    # Buscar el RUC
    ruc_str = str(ruc)
    mask = df['NUMERO_RUC'].astype(str) == ruc_str
    
    if not mask.any():
        print(f"❌ RUC {ruc} no encontrado en el archivo")
        return False
    
    # Actualizar ubicación
    print(f"✅ RUC {ruc} encontrado. Actualizando ubicación...")
    
    # Parsear la nueva dirección: GALAPAGOS / SANTA CRUZ / PUERTO AYORA / FLOREANA S/N Y CUCUVE
    partes = nueva_direccion.split(' / ')
    if len(partes) >= 3:
        provincia = partes[0].strip()
        canton = partes[1].strip()
        parroquia = partes[2].strip()
        direccion_especifica = partes[3].strip() if len(partes) > 3 else ''
    else:
        print("⚠️  Formato de dirección no reconocido")
        return False
    
    # Actualizar columnas de ubicación
    df.loc[mask, 'DESCRIPCION_PROVINCIA_EST'] = provincia
    df.loc[mask, 'DESCRIPCION_CANTON_EST'] = canton
    df.loc[mask, 'DESCRIPCION_PARROQUIA_EST'] = parroquia
    
    # Actualizar dirección de Google con la dirección específica
    if direccion_especifica:
        direccion_completa = f"{direccion_especifica}, {parroquia}, {canton}, {provincia}, Ecuador"
        df.loc[mask, 'DIRECCION_GOOGLE'] = direccion_completa
    
    # Generar nuevo URL de Google Maps con la ubicación correcta
    for idx in df[mask].index:
        nombre = str(df.loc[idx, 'NOMBRE_FANTASIA_COMERCIAL']) if pd.notna(df.loc[idx, 'NOMBRE_FANTASIA_COMERCIAL']) else str(df.loc[idx, 'RAZON_SOCIAL'])
        nombre_para_maps = nombre.replace(' ', '+')
        
        if direccion_especifica:
            query = f"{direccion_especifica}+{parroquia}+{canton}+{provincia}+Ecuador"
        else:
            query = f"{nombre_para_maps}+{parroquia}+{canton}+{provincia}+Ecuador"
        
        url_maps = f"https://www.google.com/maps/search/?api=1&query={quote(query)}"
        df.loc[idx, 'URL_GOOGLE_MAPS'] = url_maps
        print(f"   URL actualizado: {url_maps}")
    
    # Guardar archivo
    df.to_excel(archivo, index=False)
    print(f"\n✅ Ubicación actualizada y guardada en: {archivo}")
    
    # Mostrar resumen
    filas_actualizadas = df[mask]
    print(f"\n📋 Registros actualizados:")
    for idx, row in filas_actualizadas.iterrows():
        print(f"   - {row['NOMBRE_FANTASIA_COMERCIAL'] if pd.notna(row['NOMBRE_FANTASIA_COMERCIAL']) else row['RAZON_SOCIAL']}")
        print(f"     Ubicación: {parroquia}, {canton}, {provincia}")
        if direccion_especifica:
            print(f"     Dirección: {direccion_especifica}")
    
    return True

if __name__ == "__main__":
    ruc = "1704491362001"
    direccion = "GALAPAGOS / SANTA CRUZ / PUERTO AYORA / FLOREANA S/N Y CUCUVE"
    
    print("="*70)
    print("📍 ACTUALIZAR UBICACIÓN DE RUC")
    print("="*70)
    print(f"\nRUC: {ruc}")
    print(f"Nueva ubicación: {direccion}\n")
    
    actualizar_ubicacion_ruc(ruc, direccion)
