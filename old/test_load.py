import pandas as pd
import os
import traceback

# Simular el proceso de carga
folder_path = r"C:\Users\david\Downloads\ine_transformer"

try:
    # Cargar archivos
    df_pays_arrivees = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Pays Arrivées.xlsx"), sheet_name=0)
    df_pays_occupation = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Pays Occupation.xlsx"), sheet_name=0)
    df_regions_arrivees = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Régions Arrivées.xlsx"), sheet_name=0)
    df_regions_occupation = pd.read_excel(os.path.join(folder_path, "INE-08_08_2025-Régions Occupation.xlsx"), sheet_name=0)
    
    print("Archivos cargados correctamente")
    
    # Obtener nombres de columnas
    col_pays = df_pays_arrivees.columns[0]
    col_regions = df_regions_arrivees.columns[0]
    
    print(f"Columna países: {col_pays}")
    print(f"Columna regiones: {col_regions}")
    
    # Filtrar países
    mask_pays = ~df_pays_arrivees[col_pays].str.contains(
        'ESPAÑA|ESPANA|SPAIN|ESPAGNE', case=False, na=False
    )
    pays_arrivees_filtered = df_pays_arrivees[mask_pays].copy()
    pays_occupation_filtered = df_pays_occupation[mask_pays].copy()
    
    print(f"Países filtrados: {len(pays_arrivees_filtered)}")
    
    # Crear listas separadas
    data_regions = []
    data_countries = []
    
    # Procesar un país de ejemplo
    for idx, row in pays_arrivees_filtered.head(2).iterrows():
        zona = row[col_pays]
        row_data = {'Zona': zona, 'Tipo': 'Pais'}
        
        for day in range(1, 8):
            col_name = f'Jour {day}'
            if col_name in pays_arrivees_filtered.columns:
                llegadas = row[col_name]
                # Buscar la fila correspondiente en occupation
                occ_row = pays_occupation_filtered[pays_occupation_filtered[col_pays] == zona]
                if not occ_row.empty:
                    pernoctaciones = occ_row.iloc[0][col_name]
                else:
                    pernoctaciones = 0
                
                row_data[f'Llegadas Día {day}'] = int(llegadas) if pd.notna(llegadas) else 0
                row_data[f'Pernoctaciones Día {day}'] = int(pernoctaciones) if pd.notna(pernoctaciones) else 0
        
        data_countries.append(row_data)
        print(f"Procesado país: {zona}")
    
    # Ordenar
    data_countries = sorted(data_countries, key=lambda x: x['Zona'])
    print(f"Países ordenados: {len(data_countries)}")
    
    # Crear DataFrame
    df_combined = pd.DataFrame(data_countries)
    print(f"DataFrame creado con {len(df_combined)} filas")
    
    # Eliminar columna Tipo
    if 'Tipo' in df_combined.columns:
        df_combined = df_combined.drop('Tipo', axis=1)
        print("Columna 'Tipo' eliminada")
    
    print("\nPrimeras columnas del DataFrame final:")
    print(df_combined.columns.tolist())
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()