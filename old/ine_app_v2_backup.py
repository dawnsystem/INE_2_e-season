# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from datetime import datetime
import traceback

class INEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("INE - Encuestas de Ocupación")
        self.root.geometry("1400x800")
        
        # Variables para almacenar los dataframes
        self.df_pays_arrivees = None
        self.df_pays_occupation = None
        self.df_regions_arrivees = None
        self.df_regions_occupation = None
        self.df_combined = None
        
        # Lista de regiones españolas (simplificada y normalizada)
        self.regiones_espana = [
            'andaluc', 'aragon', 'aragón', 'asturias', 'baleares', 'balears', 'canarias', 'cantabria',
            'castilla', 'mancha', 'catalu', 'valencia', 'extremadura',
            'galicia', 'madrid', 'murcia', 'navarra', 'vasco', 'euskadi', 'rioja',
            'ceuta', 'melilla', 'almeria', 'almería', 'cadiz', 'cádiz', 'cordoba', 'córdoba', 
            'granada', 'huelva', 'jaen', 'jaén', 'malaga', 'málaga', 'sevilla',
            'huesca', 'teruel', 'zaragoza', 'albacete', 'ciudad real', 'cuenca', 'guadalajara', 
            'toledo', 'avila', 'ávila', 'burgos', 'leon', 'león', 'palencia', 'salamanca', 
            'segovia', 'soria', 'valladolid', 'zamora', 'barcelona', 'girona', 'gerona', 
            'lleida', 'lerida', 'tarragona', 'alicante', 'alacant', 'castellon', 'castelló',
            'badajoz', 'caceres', 'cáceres', 'coruña', 'lugo', 'ourense', 'orense', 'pontevedra',
            'alava', 'álava', 'araba', 'guipuzcoa', 'gipuzkoa', 'vizcaya', 'bizkaia', 
            'palmas', 'tenerife', 'espagne', 'espana', 'españa', 'spain'
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el peso de las filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="INE - Procesador de Encuestas de Ocupación", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # Frame para botones de tipo de cuestionario
        type_frame = ttk.LabelFrame(main_frame, text="Tipo de Cuestionario", padding="10")
        type_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(type_frame, text="Cargar archivos manualmente (uno por uno)", 
                   command=self.load_weekly_files, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(type_frame, text="Cargar archivos desde carpeta (automático)", 
                   command=self.auto_load_files, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(type_frame, text="Cuestionario Mensual (Próximamente)", 
                   state='disabled', width=30).pack(side=tk.LEFT, padx=5)
        
        # Frame para la tabla
        table_frame = ttk.LabelFrame(main_frame, text="Datos Procesados", padding="10")
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Crear Treeview con scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        tree_scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar estilo para el Treeview con cuadrícula visible
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       rowheight=28,
                       borderwidth=2,
                       relief='solid',
                       fieldbackground='white')
        style.configure("Custom.Treeview.Heading", 
                       background="#d0d0d0",
                       foreground="black",
                       borderwidth=2,
                       relief='raised',
                       font=('Arial', 9, 'bold'))
        style.map("Custom.Treeview.Heading",
                 background=[('active', '#c0c0c0')])
        
        self.tree = ttk.Treeview(table_frame, 
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set,
                                 style="Custom.Treeview")
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para alternar colores de filas
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='#f5f5f5')
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, pady=10)
        
        self.export_button = ttk.Button(action_frame, text="Exportar a Excel", 
                                        command=self.export_to_excel, state='disabled')
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Limpiar Datos", 
                   command=self.clear_data).pack(side=tk.LEFT, padx=5)
        
        # Label de estado
        self.status_label = ttk.Label(main_frame, text="Esperando carga de archivos...", 
                                      foreground="blue")
        self.status_label.grid(row=4, column=0, pady=5)
        
    def auto_load_files(self):
        """Cargar automáticamente los archivos desde una carpeta seleccionada"""
        try:
            # Solicitar carpeta al usuario
            folder_path = filedialog.askdirectory(
                title="Seleccionar carpeta con los archivos Excel del INE"
            )
            
            if not folder_path:
                self.status_label.config(text="Carga cancelada", foreground="red")
                return
            
            # Diccionario para almacenar archivos encontrados
            files_dict = {
                'pays_arrivees': None,
                'pays_occupation': None,
                'regions_arrivees': None,
                'regions_occupation': None
            }
            
            files_info = []
            
            # Buscar archivos Excel en la carpeta
            excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls'))]
            
            if len(excel_files) < 4:
                messagebox.showwarning("Advertencia", 
                    f"Se encontraron solo {len(excel_files)} archivos Excel.\nSe esperan 4 archivos.")
                return
            
            # Analizar cada archivo para determinar su tipo
            for file in excel_files:
                file_lower = file.lower()
                file_path = os.path.join(folder_path, file)
                
                # Detectar tipo de archivo por palabras clave
                is_pays = 'pay' in file_lower or 'país' in file_lower or 'pais' in file_lower
                is_region = 'region' in file_lower or 'région' in file_lower or 'provincia' in file_lower
                is_arrivee = 'arriv' in file_lower or 'llegada' in file_lower
                is_occupation = 'occupation' in file_lower or 'ocupac' in file_lower or 'pernoc' in file_lower
                
                # Si no se puede determinar por el nombre, intentar por el contenido
                if not (is_pays or is_region):
                    try:
                        df_temp = pd.read_excel(file_path, sheet_name=0, nrows=5)
                        first_col = str(df_temp.columns[0]).lower()
                        
                        if 'pay' in first_col or 'país' in first_col:
                            is_pays = True
                        elif 'region' in first_col or 'région' in first_col:
                            is_region = True
                    except:
                        pass
                
                # Asignar archivo según su tipo detectado
                if is_pays and is_arrivee and not files_dict['pays_arrivees']:
                    files_dict['pays_arrivees'] = file_path
                    files_info.append(f"✓ Pays Arrivées: {file}")
                elif is_pays and is_occupation and not files_dict['pays_occupation']:
                    files_dict['pays_occupation'] = file_path
                    files_info.append(f"✓ Pays Occupation: {file}")
                elif is_region and is_arrivee and not files_dict['regions_arrivees']:
                    files_dict['regions_arrivees'] = file_path
                    files_info.append(f"✓ Régions Arrivées: {file}")
                elif is_region and is_occupation and not files_dict['regions_occupation']:
                    files_dict['regions_occupation'] = file_path
                    files_info.append(f"✓ Régions Occupation: {file}")
            
            # Verificar que se encontraron los 4 tipos de archivos
            missing = []
            if not files_dict['pays_arrivees']:
                missing.append("Pays Arrivées")
            if not files_dict['pays_occupation']:
                missing.append("Pays Occupation")
            if not files_dict['regions_arrivees']:
                missing.append("Régions Arrivées")
            if not files_dict['regions_occupation']:
                missing.append("Régions Occupation")
            
            if missing:
                msg = "No se pudieron identificar los siguientes archivos:\n" + "\n".join(missing)
                msg += "\n\nAsegúrese de que los nombres de archivo contengan:"
                msg += "\n- 'Pays' o 'País' para archivos de países"
                msg += "\n- 'Region' o 'Région' para archivos de regiones"
                msg += "\n- 'Arriv' o 'Llegada' para archivos de llegadas"
                msg += "\n- 'Occupation' o 'Ocupación' para archivos de ocupación"
                messagebox.showwarning("Archivos faltantes", msg)
                return
            
            # Confirmar con el usuario
            confirm_msg = "Se identificaron los siguientes archivos:\n\n" + "\n".join(files_info)
            confirm_msg += "\n\n¿Desea continuar con estos archivos?"
            
            if not messagebox.askyesno("Confirmar archivos", confirm_msg):
                self.status_label.config(text="Carga cancelada por el usuario", foreground="orange")
                return
            
            # Cargar los archivos
            self.status_label.config(text="Cargando archivos...", foreground="blue")
            self.root.update()
            
            self.df_pays_arrivees = pd.read_excel(files_dict['pays_arrivees'], sheet_name=0)
            self.df_pays_occupation = pd.read_excel(files_dict['pays_occupation'], sheet_name=0)
            self.df_regions_arrivees = pd.read_excel(files_dict['regions_arrivees'], sheet_name=0)
            self.df_regions_occupation = pd.read_excel(files_dict['regions_occupation'], sheet_name=0)
            
            self.status_label.config(text="Archivos cargados correctamente", foreground="green")
            
            # Procesar los datos
            self.process_weekly_data()
            
        except Exception as e:
            error_msg = f"Error al cargar archivos: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="Error en la carga", foreground="red")
            
    def load_weekly_files(self):
        """Cargar los 4 archivos Excel para el cuestionario semanal"""
        try:
            # Pedir al usuario que seleccione los 4 archivos
            file_types = [
                ("Pays Arrivées", "Llegadas por País"),
                ("Pays Occupation", "Ocupación por País"),
                ("Régions Arrivées", "Llegadas por Región"),
                ("Régions Occupation", "Ocupación por Región")
            ]
            
            files = {}
            for file_key, description in file_types:
                file_path = filedialog.askopenfilename(
                    title=f"Seleccionar archivo: {description}",
                    filetypes=[("Excel files", "*.xlsx *.xls")]
                )
                if not file_path:
                    self.status_label.config(text="Carga cancelada", foreground="red")
                    return
                files[file_key] = file_path
            
            # Cargar los archivos
            self.status_label.config(text="Cargando archivos...", foreground="blue")
            self.root.update()
            
            self.df_pays_arrivees = pd.read_excel(files["Pays Arrivées"], sheet_name=0)
            self.df_pays_occupation = pd.read_excel(files["Pays Occupation"], sheet_name=0)
            self.df_regions_arrivees = pd.read_excel(files["Régions Arrivées"], sheet_name=0)
            self.df_regions_occupation = pd.read_excel(files["Régions Occupation"], sheet_name=0)
            
            # Procesar los datos
            self.process_weekly_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivos: {str(e)}\n\n{traceback.format_exc()}")
            self.status_label.config(text="Error en la carga", foreground="red")
    
    def is_spanish_region(self, name):
        """Verificar si un nombre corresponde a una región española"""
        if pd.isna(name):
            return False
        
        name_lower = str(name).lower().strip()
        
        # Verificar si contiene alguna palabra clave de región española
        for region in self.regiones_espana:
            if region in name_lower:
                return True
        
        # Verificar si NO contiene palabras de otros países
        foreign_keywords = ['france', 'francia', 'itali', 'allemagne', 'alemania', 
                          'portugal', 'england', 'inglaterra', 'belgium', 'belgica']
        for keyword in foreign_keywords:
            if keyword in name_lower:
                return False
        
        return False
    
    def process_weekly_data(self):
        """Procesar los datos semanales según las reglas especificadas"""
        try:
            self.status_label.config(text="Procesando datos...", foreground="blue")
            self.root.update()
            
            # Obtener nombres de columnas
            col_pays = self.df_pays_arrivees.columns[0]
            col_regions = self.df_regions_arrivees.columns[0]
            
            print(f"Columna países: {col_pays}")
            print(f"Columna regiones: {col_regions}")
            
            # Filtrar países (todos excepto España)
            mask_pays = ~self.df_pays_arrivees[col_pays].str.contains(
                'ESPAÑA|ESPANA|SPAIN|ESPAGNE', case=False, na=False
            )
            pays_arrivees_filtered = self.df_pays_arrivees.loc[mask_pays].copy()
            pays_occupation_filtered = self.df_pays_occupation.loc[mask_pays].copy()
            
            # Agrupar y sumar filas duplicadas de países
            jour_cols = [f'Jour {i}' for i in range(1, 8)]
            pays_arrivees_filtered = pays_arrivees_filtered.groupby(col_pays, as_index=False)[jour_cols].sum()
            pays_occupation_filtered = pays_occupation_filtered.groupby(col_pays, as_index=False)[jour_cols].sum()
            
            print(f"Países únicos después de agrupar: {len(pays_arrivees_filtered)}")
            
            # Filtrar regiones (solo España)
            mask_regions = self.df_regions_arrivees[col_regions].apply(self.is_spanish_region)
            regions_arrivees_filtered = self.df_regions_arrivees.loc[mask_regions].copy()
            regions_occupation_filtered = self.df_regions_occupation.loc[mask_regions].copy()
            
            # Agrupar y sumar filas duplicadas de regiones
            regions_arrivees_filtered = regions_arrivees_filtered.groupby(col_regions, as_index=False)[jour_cols].sum()
            regions_occupation_filtered = regions_occupation_filtered.groupby(col_regions, as_index=False)[jour_cols].sum()
            
            print(f"Regiones únicas después de agrupar: {len(regions_arrivees_filtered)}")
            
            # Crear listas separadas para regiones y países
            data_regions = []
            data_countries = []
            
            # Procesar datos de regiones españolas (ahora ya están agrupadas y sin duplicados)
            for idx, row in regions_arrivees_filtered.iterrows():
                zona = row[col_regions]
                # Saltar si la zona está vacía o es NaN
                if pd.isna(zona) or str(zona).strip() == '':
                    continue
                row_data = {'Zona': zona, 'Tipo': 'Region'}
                
                # Buscar la fila correspondiente en occupation (ahora debe ser única)
                occ_row = regions_occupation_filtered[regions_occupation_filtered[col_regions] == zona]
                
                for day in range(1, 8):
                    col_name = f'Jour {day}'
                    if col_name in regions_arrivees_filtered.columns:
                        llegadas = row[col_name]
                        
                        if not occ_row.empty:
                            pernoctaciones = occ_row.iloc[0][col_name]
                        else:
                            pernoctaciones = 0
                        
                        row_data[f'Llegadas Día {day}'] = int(llegadas) if pd.notna(llegadas) else 0
                        row_data[f'Pernoctaciones Día {day}'] = int(pernoctaciones) if pd.notna(pernoctaciones) else 0
                
                data_regions.append(row_data)
            
            # Procesar datos de países (ahora ya están agrupados y sin duplicados)
            for idx, row in pays_arrivees_filtered.iterrows():
                zona = row[col_pays]
                # Saltar si la zona está vacía o es NaN
                if pd.isna(zona) or str(zona).strip() == '':
                    continue
                row_data = {'Zona': zona, 'Tipo': 'Pais'}
                
                # Buscar la fila correspondiente en occupation (ahora debe ser única)
                occ_row = pays_occupation_filtered[pays_occupation_filtered[col_pays] == zona]
                
                for day in range(1, 8):
                    col_name = f'Jour {day}'
                    if col_name in pays_arrivees_filtered.columns:
                        llegadas = row[col_name]
                        
                        if not occ_row.empty:
                            pernoctaciones = occ_row.iloc[0][col_name]
                        else:
                            pernoctaciones = 0
                        
                        row_data[f'Llegadas Día {day}'] = int(llegadas) if pd.notna(llegadas) else 0
                        row_data[f'Pernoctaciones Día {day}'] = int(pernoctaciones) if pd.notna(pernoctaciones) else 0
                
                data_countries.append(row_data)
            
            # Ordenar regiones y países alfabéticamente por separado
            # Convertir None/NaN a string vacío para evitar errores de comparación
            data_regions = sorted(data_regions, key=lambda x: str(x['Zona']) if x['Zona'] is not None else '')
            data_countries = sorted(data_countries, key=lambda x: str(x['Zona']) if x['Zona'] is not None else '')
            
            # Combinar: primero regiones, luego países
            data_combined = data_regions + data_countries
            
            # Crear DataFrame final
            self.df_combined = pd.DataFrame(data_combined)
            
            # Eliminar la columna 'Tipo' que solo se usó para ordenar
            if 'Tipo' in self.df_combined.columns:
                self.df_combined = self.df_combined.drop('Tipo', axis=1)
            
            # Filtrar líneas de totales y filas sin datos
            # Primero filtrar líneas que contengan "total" en el nombre de la zona
            mask_not_total = ~self.df_combined['Zona'].str.contains('total|TOTAL|Total', case=False, na=False)
            self.df_combined = self.df_combined[mask_not_total]
            
            # Luego filtrar filas que tienen al menos un valor mayor que 0
            # Crear una máscara para las columnas numéricas
            numeric_columns = [col for col in self.df_combined.columns if col != 'Zona']
            
            # Verificar si al menos una columna numérica tiene un valor > 0
            mask_has_data = (self.df_combined[numeric_columns] > 0).any(axis=1)
            
            # Filtrar el DataFrame
            self.df_combined = self.df_combined[mask_has_data].reset_index(drop=True)
            
            # Contar cuántas se filtraron
            total_before = len(data_combined)
            total_after = len(self.df_combined)
            filtered_count = total_before - total_after
            
            print(f"Zonas con datos: {total_after} de {total_before} (filtradas {filtered_count} zonas sin actividad)")
            
            # Mostrar en la tabla
            self.display_data()
            
            status_msg = f"Datos procesados: {total_after} zonas con actividad"
            if filtered_count > 0:
                status_msg += f" ({filtered_count} zonas sin datos fueron ocultadas)"
            self.status_label.config(text=status_msg, foreground="green")
            self.export_button.config(state='normal')
            
        except Exception as e:
            error_msg = f"Error al procesar datos: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="Error en el procesamiento", foreground="red")
    
    def display_data(self):
        """Mostrar los datos en el Treeview"""
        # Limpiar tabla existente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.df_combined is None or self.df_combined.empty:
            return
        
        # Configurar columnas
        columns = list(self.df_combined.columns)
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # Configurar encabezados con iconos y anchos
        for col in columns:
            # Personalizar títulos de columnas
            if col == 'Zona':
                display_text = 'Zona'
                self.tree.heading(col, text=display_text)
                self.tree.column(col, width=200, minwidth=150)
            elif 'Llegadas' in col:
                # Extraer el número del día
                day_num = col.split()[-1]
                display_text = f"↘️ {day_num}"
                self.tree.heading(col, text=display_text)
                self.tree.column(col, width=50, minwidth=40, anchor='center')
            elif 'Pernoctaciones' in col:
                # Extraer el número del día
                day_num = col.split()[-1]
                display_text = f"🌙 {day_num}"
                self.tree.heading(col, text=display_text)
                self.tree.column(col, width=50, minwidth=40, anchor='center')
            else:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=80, minwidth=60)
        
        # Insertar datos con alternancia de colores para mejor visualización
        for idx, row in self.df_combined.iterrows():
            values = [row[col] for col in columns]
            # Alternar colores de filas
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=values, tags=(tag,))
    
    def export_to_excel(self):
        """Exportar los datos a Excel"""
        if self.df_combined is None or self.df_combined.empty:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        try:
            # Pedir ubicación para guardar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"INE_Procesado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if file_path:
                self.df_combined.to_excel(file_path, index=False, sheet_name='Datos INE')
                messagebox.showinfo("Éxito", f"Archivo exportado correctamente:\n{file_path}")
                self.status_label.config(text="Exportación completada", foreground="green")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def clear_data(self):
        """Limpiar todos los datos cargados"""
        self.df_pays_arrivees = None
        self.df_pays_occupation = None
        self.df_regions_arrivees = None
        self.df_regions_occupation = None
        self.df_combined = None
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.export_button.config(state='disabled')
        self.status_label.config(text="Esperando carga de archivos...", foreground="blue")

def main():
    root = tk.Tk()
    app = INEApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()