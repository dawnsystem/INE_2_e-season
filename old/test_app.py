import pandas as pd
import os

# Probar la carga y procesamiento de datos
folder_path = r"C:\Users\david\Downloads\ine_transformer"

# Cargar archivos
try:
    df_pays_arrivees = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Pays Arrivées.xlsx"), sheet_name=0)
    df_pays_occupation = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Pays Occupation.xlsx"), sheet_name=0)
    df_regions_arrivees = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Régions Arrivées.xlsx"), sheet_name=0)
    df_regions_occupation = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Régions Occupation.xlsx"), sheet_name=0)
    
    print("Archivos cargados correctamente")
    
    # Verificar columnas
    print(f"\nColumnas Pays Arrivées: {list(df_pays_arrivees.columns)}")
    print(f"Columnas Pays Occupation: {list(df_pays_occupation.columns)}")
    
    # Obtener nombres de columnas
    col_pays = df_pays_arrivees.columns[0]
    col_regions = df_regions_arrivees.columns[0]
    
    # Probar filtrado de países
    print(f"\nPrimera columna Pays: '{col_pays}'")
    print(f"Primeros valores: {df_pays_arrivees[col_pays].head().tolist()}")
    
    # Filtrar países (todos excepto España)
    mask_pays = ~df_pays_arrivees[col_pays].str.contains('ESPAÑA|ESPANA|SPAIN', case=False, na=False)
    print(f"\nMáscara países shape: {mask_pays.shape}")
    print(f"DataFrame países shape: {df_pays_arrivees.shape}")
    print(f"Países filtrados: {mask_pays.sum()} de {len(mask_pays)}")
    
    # Probar el filtrado
    pays_arrivees_filtered = df_pays_arrivees.loc[mask_pays].copy()
    print(f"\nPaíses después de filtrar: {pays_arrivees_filtered.shape}")
    
    # Intentar con el segundo dataframe
    print(f"\nDataFrame occupation shape: {df_pays_occupation.shape}")
    pays_occupation_filtered = df_pays_occupation.loc[mask_pays].copy()
    print(f"Occupation después de filtrar: {pays_occupation_filtered.shape}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()