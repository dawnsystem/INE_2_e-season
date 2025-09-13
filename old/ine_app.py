import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from datetime import datetime
import openpyxl

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
        
        # Lista de regiones españolas conocidas
        self.regiones_espana = [
            'Andalucía', 'Aragón', 'Asturias', 'Baleares', 'Canarias', 'Cantabria',
            'Castilla y León', 'Castilla-La Mancha', 'Cataluña', 'Valencia', 'Extremadura',
            'Galicia', 'Madrid', 'Murcia', 'Navarra', 'País Vasco', 'La Rioja',
            'Ceuta', 'Melilla', 'Almería', 'Cádiz', 'Córdoba', 'Granada', 'Huelva',
            'Jaén', 'Málaga', 'Sevilla', 'Huesca', 'Teruel', 'Zaragoza', 'Albacete',
            'Ciudad Real', 'Cuenca', 'Guadalajara', 'Toledo', 'Ávila', 'Burgos',
            'León', 'Palencia', 'Salamanca', 'Segovia', 'Soria', 'Valladolid', 'Zamora',
            'Barcelona', 'Girona', 'Lleida', 'Tarragona', 'Alicante', 'Castellón',
            'Badajoz', 'Cáceres', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra',
            'Álava', 'Guipúzcoa', 'Vizcaya', 'Las Palmas', 'Santa Cruz de Tenerife'
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
        
        ttk.Button(type_frame, text="Cuestionario Semanal - Apartados 2 y 3", 
                   command=self.load_weekly_files, width=30).pack(side=tk.LEFT, padx=5)
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
        
        self.tree = ttk.Treeview(table_frame, 
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
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
        
    def validate_dataframe_structure(self, df, name):
        """Validar que el DataFrame tenga la estructura esperada"""
        if df is None or df.empty:
            raise ValueError(f"El archivo {name} está vacío")
        
        # Verificar que tenga al menos 8 columnas (1 de zona + 7 días)
        if len(df.columns) < 8:
            raise ValueError(f"El archivo {name} no tiene las columnas esperadas (se esperan 8, hay {len(df.columns)})")
        
        # Verificar que las columnas de días existan
        for day in range(1, 8):
            col_name = f'Jour {day}'
            if col_name not in df.columns:
                raise ValueError(f"El archivo {name} no tiene la columna '{col_name}'")
        
        return True
    
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
            
            # Validar estructura de los archivos
            self.validate_dataframe_structure(self.df_pays_arrivees, "Pays Arrivées")
            self.validate_dataframe_structure(self.df_pays_occupation, "Pays Occupation")
            self.validate_dataframe_structure(self.df_regions_arrivees, "Régions Arrivées")
            self.validate_dataframe_structure(self.df_regions_occupation, "Régions Occupation")
            
            # Procesar los datos
            self.process_weekly_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivos: {str(e)}")
            self.status_label.config(text="Error en la carga", foreground="red")
    
    def process_weekly_data(self):
        """Procesar los datos semanales según las reglas especificadas"""
        try:
            self.status_label.config(text="Procesando datos...", foreground="blue")
            self.root.update()
            
            # Obtener nombres de columnas
            col_pays = self.df_pays_arrivees.columns[0]
            col_regions = self.df_regions_arrivees.columns[0]
            
            # Filtrar países (todos excepto España)
            mask_pays = ~self.df_pays_arrivees[col_pays].str.contains('ESPAÑA|ESPANA|SPAIN', 
                                                                       case=False, na=False)
            pays_arrivees_filtered = self.df_pays_arrivees[mask_pays].copy()
            # Usar loc para evitar warning de reindexación
            pays_occupation_filtered = self.df_pays_occupation.loc[mask_pays].copy()
            
            # Filtrar regiones (solo España)
            # Normalizar nombres para comparación
            def normalize_name(name):
                if pd.isna(name):
                    return ""
                return str(name).lower().strip()
            
            # Crear lista normalizada de regiones españolas
            regiones_espana_norm = [normalize_name(r) for r in self.regiones_espana]
            
            # Filtrar regiones
            mask_regions = self.df_regions_arrivees[col_regions].apply(
                lambda x: normalize_name(x) in regiones_espana_norm or 
                         any(norm in normalize_name(x) for norm in regiones_espana_norm)
            )
            
            regions_arrivees_filtered = self.df_regions_arrivees.loc[mask_regions].copy()
            regions_occupation_filtered = self.df_regions_occupation.loc[mask_regions].copy()
            
            # Crear DataFrame combinado
            data_combined = []
            
            # Añadir datos de países
            for idx, row in pays_arrivees_filtered.iterrows():
                zona = row[col_pays]
                row_data = {'Zona': zona}
                
                for day in range(1, 8):
                    col_name = f'Jour {day}'
                    if col_name in pays_arrivees_filtered.columns:
                        llegadas = row[col_name]
                        # Buscar la fila correspondiente en occupation por el nombre del país
                        occupation_row = pays_occupation_filtered[pays_occupation_filtered.iloc[:, 0] == zona]
                        if not occupation_row.empty:
                            pernoctaciones = occupation_row.iloc[0][col_name]
                        else:
                            pernoctaciones = 0
                        row_data[f'Llegadas Día {day}'] = llegadas
                        row_data[f'Pernoctaciones Día {day}'] = pernoctaciones
                
                data_combined.append(row_data)
            
            # Añadir datos de regiones
            for idx, row in regions_arrivees_filtered.iterrows():
                zona = row[col_regions]
                row_data = {'Zona': zona}
                
                # Buscar el índice correspondiente en occupation
                idx_occupation = regions_occupation_filtered[
                    regions_occupation_filtered[col_regions] == zona
                ].index
                
                if len(idx_occupation) > 0:
                    idx_occ = idx_occupation[0]
                    for day in range(1, 8):
                        col_name = f'Jour {day}'
                        if col_name in regions_arrivees_filtered.columns:
                            llegadas = row[col_name]
                            pernoctaciones = regions_occupation_filtered.loc[idx_occ, col_name]
                            row_data[f'Llegadas Día {day}'] = llegadas
                            row_data[f'Pernoctaciones Día {day}'] = pernoctaciones
                
                data_combined.append(row_data)
            
            # Crear DataFrame final
            self.df_combined = pd.DataFrame(data_combined)
            
            # Mostrar en la tabla
            self.display_data()
            
            self.status_label.config(text=f"Datos procesados: {len(self.df_combined)} zonas", 
                                   foreground="green")
            self.export_button.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar datos: {str(e)}")
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
        
        # Configurar encabezados y anchos
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'Zona':
                self.tree.column(col, width=200, minwidth=150)
            else:
                self.tree.column(col, width=120, minwidth=80)
        
        # Insertar datos
        for idx, row in self.df_combined.iterrows():
            values = [row[col] for col in columns]
            self.tree.insert('', 'end', values=values)
    
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