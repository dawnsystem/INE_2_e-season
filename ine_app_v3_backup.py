# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from datetime import datetime
import traceback
import re
import json

class INEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("INE - Encuestas de Ocupación")
        self.root.geometry("1400x800")
        
        # Archivo de historial
        self.history_file = "historial_exportaciones.json"
        self.load_history()
        
        # Variables para almacenar los dataframes - Primera pestaña
        self.df_pays_arrivees = None
        self.df_pays_occupation = None
        self.df_regions_arrivees = None
        self.df_regions_occupation = None
        self.df_combined = None
        
        # Variables para segunda pestaña
        self.df_emplacements = None
        self.df_alojamientos = None
        
        # Variables para tercera pestaña - Precios
        self.df_export_alojamientos = None
        self.df_pricing = None
        
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
        
        # Mostrar disclaimer al inicio
        if not self.show_disclaimer():
            self.root.destroy()
            return
        
        self.setup_ui()
    
    def show_disclaimer(self):
        """Mostrar disclaimer legal al iniciar la aplicación"""
        disclaimer_window = tk.Toplevel(self.root)
        disclaimer_window.title("Aviso Legal - Lea Atentamente")
        disclaimer_window.geometry("700x550")
        disclaimer_window.resizable(False, False)
        
        # Centrar la ventana
        disclaimer_window.transient(self.root)
        disclaimer_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(disclaimer_window, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="AVISO LEGAL Y EXENCIÓN DE RESPONSABILIDAD",
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Texto del disclaimer
        disclaimer_text = """Este software es una herramienta de uso interno y personal, desarrollada 
exclusivamente para facilitar el procesamiento de datos de encuestas INE.

AL UTILIZAR ESTE SOFTWARE, USTED ACEPTA Y RECONOCE QUE:

• Esta aplicación se proporciona "TAL CUAL", sin garantías de ningún tipo,
  expresas o implícitas.

• El autor NO se hace responsable de la exactitud, fiabilidad, integridad
  o validez de los datos procesados.

• El usuario asume TODA la responsabilidad por el uso de esta herramienta
  y sus resultados.

• NO está destinada para uso comercial, profesional o de presentación oficial.

• Los resultados generados NO han sido validados, verificados ni aprobados
  por ninguna entidad oficial.

• El autor queda completamente EXENTO de cualquier responsabilidad civil,
  penal, administrativa o de cualquier índole derivada del uso, mal uso
  o imposibilidad de uso de este software.

• Cualquier error, omisión o inexactitud en los datos es responsabilidad
  exclusiva del usuario.

Este software es estrictamente de USO PRIVADO E INTERNO. 
El usuario es el ÚNICO responsable de verificar la exactitud y validez 
de todos los datos antes de su presentación a cualquier organismo oficial.

Al hacer clic en "Aceptar", confirma que ha leído, entendido y aceptado
todos los términos de este aviso legal."""
        
        # Área de texto con scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        text_widget = tk.Text(text_frame, wrap='word', width=80, height=20,
                             font=('Arial', 10), bg='#f5f5f5')
        text_widget.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.insert('1.0', disclaimer_text)
        text_widget.config(state='disabled')  # Solo lectura
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        # Variable para almacenar la respuesta
        self.disclaimer_accepted = False
        
        def accept_disclaimer():
            self.disclaimer_accepted = True
            disclaimer_window.destroy()
        
        def reject_disclaimer():
            self.disclaimer_accepted = False
            disclaimer_window.destroy()
        
        # Botones
        reject_button = ttk.Button(button_frame, text="Rechazar y Salir",
                                  command=reject_disclaimer, width=20)
        reject_button.pack(side='left', padx=5)
        
        accept_button = ttk.Button(button_frame, text="Aceptar y Continuar",
                                  command=accept_disclaimer, width=20)
        accept_button.pack(side='right', padx=5)
        
        # Hacer que la ventana sea modal y esperar respuesta
        self.root.wait_window(disclaimer_window)
        
        return self.disclaimer_accepted
        
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
        
        ttk.Button(type_frame, text="Cargar archivos desde carpeta (automático)", 
                   command=self.auto_load_files, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(type_frame, text="Cuestionario Mensual", 
                   command=self.open_monthly_questionnaire, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(type_frame, text="Ver Historial", 
                   command=self.open_history_window, width=25).pack(side=tk.LEFT, padx=5)
        
        # Crear Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Primera pestaña - Apartados 2 y 3
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Apartados 2 y 3 - Llegadas y Pernoctaciones")
        self.setup_tab1()
        
        # Segunda pestaña - Apartado 4
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Apartado 4 - Alojamientos Ocupados")
        self.setup_tab2()
        
        # Tercera pestaña - Apartado 6
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Apartado 6 - Precios")
        self.setup_tab3()
        
        # Inicialmente deshabilitar segunda y tercera pestaña
        self.notebook.tab(1, state='disabled')
        self.notebook.tab(2, state='disabled')
        
        # Label de estado general
        self.status_label = ttk.Label(main_frame, text="Esperando carga de archivos...", 
                                      foreground="blue")
        self.status_label.grid(row=3, column=0, pady=5)
    
    def setup_tab1(self):
        """Configurar primera pestaña - Apartados 2 y 3"""
        # Frame para la tabla
        table_frame = ttk.LabelFrame(self.tab1, text="Datos Procesados", padding="10")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview con scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
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
        self.tree.pack(fill='both', expand=True)
        
        # Configurar tags para alternar colores de filas
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='#f5f5f5')
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(self.tab1)
        action_frame.pack(pady=10)
        
        self.export_button = ttk.Button(action_frame, text="Exportar Todo a Excel", 
                                        command=self.export_all_to_excel, state='disabled')
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Limpiar Datos", 
                   command=self.clear_data).pack(side=tk.LEFT, padx=5)
    
    def setup_tab2(self):
        """Configurar segunda pestaña - Apartado 4"""
        # Frame para la tabla
        table_frame = ttk.LabelFrame(self.tab2, text="Alojamientos Ocupados", padding="10")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview con scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree2 = ttk.Treeview(table_frame, 
                                  yscrollcommand=tree_scroll_y.set,
                                  xscrollcommand=tree_scroll_x.set,
                                  style="Custom.Treeview",
                                  height=10)
        self.tree2.pack(fill='both', expand=True)
        
        # Configurar tags para alternar colores de filas
        self.tree2.tag_configure('oddrow', background='white')
        self.tree2.tag_configure('evenrow', background='#f5f5f5')
        
        tree_scroll_y.config(command=self.tree2.yview)
        tree_scroll_x.config(command=self.tree2.xview)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(self.tab2)
        action_frame.pack(pady=10)
        
        self.export_button2 = ttk.Button(action_frame, text="Exportar Todo a Excel", 
                                         command=self.export_all_to_excel, state='disabled')
        self.export_button2.pack(side=tk.LEFT, padx=5)
        
        # Label informativo
        info_label = ttk.Label(self.tab2, 
                              text="Los datos de alojamientos se cargarán automáticamente si se encuentra el archivo 'Emplacements'",
                              foreground="gray")
        info_label.pack(pady=5)
    
    def setup_tab3(self):
        """Configurar tercera pestaña - Apartado 6 Precios"""
        # Frame para la tabla
        table_frame = ttk.LabelFrame(self.tab3, text="Distribución de Precios por Tipo de Alojamiento", padding="10")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview con scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree3 = ttk.Treeview(table_frame, 
                                  yscrollcommand=tree_scroll_y.set,
                                  style="Custom.Treeview",
                                  height=5)
        self.tree3.pack(fill='both', expand=True)
        
        # Configurar tags para alternar colores de filas
        self.tree3.tag_configure('oddrow', background='white')
        self.tree3.tag_configure('evenrow', background='#f5f5f5')
        self.tree3.tag_configure('total', background='#e0e0e0', font=('Arial', 10, 'bold'))
        
        tree_scroll_y.config(command=self.tree3.yview)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(self.tab3)
        action_frame.pack(pady=10)
        
        self.export_button3 = ttk.Button(action_frame, text="Exportar Todo a Excel", 
                                         command=self.export_all_to_excel, state='disabled')
        self.export_button3.pack(side=tk.LEFT, padx=5)
        
        # Label informativo
        info_label = ttk.Label(self.tab3, 
                              text="Los porcentajes se calculan automáticamente basándose en la ocupación semanal total",
                              foreground="gray")
        info_label.pack(pady=5)
    
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
                'regions_occupation': None,
                'emplacements': None,  # Nuevo archivo
                'export_alojamientos': None  # Archivo para precios
            }
            
            files_info = []
            
            # Buscar archivos Excel en la carpeta
            excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls'))]
            
            if len(excel_files) < 4:
                messagebox.showwarning("Advertencia", 
                    f"Se encontraron solo {len(excel_files)} archivos Excel.\nSe esperan al menos 4 archivos.")
                return
            
            # Analizar cada archivo para determinar su tipo
            for file in excel_files:
                file_lower = file.lower()
                file_path = os.path.join(folder_path, file)
                
                # Detectar archivo de Emplacements
                if 'emplacement' in file_lower:
                    files_dict['emplacements'] = file_path
                    files_info.append(f"✓ Emplacements: {file}")
                    continue
                
                # Detectar archivo Export_Alojamientos
                if 'export' in file_lower and 'alojamiento' in file_lower:
                    files_dict['export_alojamientos'] = file_path
                    files_info.append(f"✓ Export Alojamientos: {file}")
                    continue
                
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
            
            # Verificar que se encontraron los 4 archivos básicos
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
            if files_dict['emplacements']:
                confirm_msg += "\n\n✅ Se encontró archivo de Emplacements - Se habilitará la pestaña de Alojamientos"
            else:
                confirm_msg += "\n\n⚠️ No se encontró archivo de Emplacements - Solo se procesarán Apartados 2 y 3"
            confirm_msg += "\n\n¿Desea continuar?"
            
            if not messagebox.askyesno("Confirmar archivos", confirm_msg):
                self.status_label.config(text="Carga cancelada por el usuario", foreground="orange")
                return
            
            # Cargar los archivos básicos
            self.status_label.config(text="Cargando archivos...", foreground="blue")
            self.root.update()
            
            self.df_pays_arrivees = pd.read_excel(files_dict['pays_arrivees'], sheet_name=0)
            self.df_pays_occupation = pd.read_excel(files_dict['pays_occupation'], sheet_name=0)
            self.df_regions_arrivees = pd.read_excel(files_dict['regions_arrivees'], sheet_name=0)
            self.df_regions_occupation = pd.read_excel(files_dict['regions_occupation'], sheet_name=0)
            
            # Cargar archivo de Emplacements si existe
            if files_dict['emplacements']:
                self.df_emplacements = pd.read_excel(files_dict['emplacements'], sheet_name=0)
                self.notebook.tab(1, state='normal')  # Habilitar segunda pestaña
                self.process_emplacements_data()
            
            # Procesar precios si tenemos el archivo de Emplacements
            # (no necesitamos Export_Alojamientos para los cálculos)
            if files_dict['emplacements']:
                self.notebook.tab(2, state='normal')  # Habilitar tercera pestaña
                self.process_pricing_data()
            
            # Cargar archivo Export_Alojamientos si existe (para referencia futura)
            if files_dict['export_alojamientos']:
                self.df_export_alojamientos = pd.read_excel(files_dict['export_alojamientos'], sheet_name=0)
            
            self.status_label.config(text="Archivos cargados correctamente", foreground="green")
            
            # Procesar los datos
            self.process_weekly_data()
            
        except Exception as e:
            error_msg = f"Error al cargar archivos: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="Error en la carga", foreground="red")
    
    def process_emplacements_data(self):
        """Procesar datos de alojamientos ocupados"""
        try:
            if self.df_emplacements is None:
                return
            
            # Obtener columna de categorías (segunda columna)
            col_category = self.df_emplacements.columns[1]
            
            # Inicializar diccionario para totales
            totales = {
                '4.1.1 Parcelas larga duración': [0] * 7,
                '4.1.2 Resto parcelas': [0] * 7,
                '4.2 Bungalows y similares': [0] * 7,
                '4.3 Caravanas': [0] * 7,
                '4.4 Zona sin parcelar': [0] * 7
            }
            
            # Procesar cada fila
            for idx, row in self.df_emplacements.iterrows():
                categoria = str(row[col_category]).upper() if pd.notna(row[col_category]) else ''
                
                # Determinar tipo de alojamiento
                if 'PARCELA RESIDENTE' in categoria:
                    tipo = '4.1.1 Parcelas larga duración'
                elif 'PARCELA' in categoria and 'RESIDENTE' not in categoria:
                    tipo = '4.1.2 Resto parcelas'
                elif categoria:  # Todo lo demás que no sea vacío
                    tipo = '4.2 Bungalows y similares'
                else:
                    continue
                
                # Sumar valores de cada día
                for day in range(1, 8):
                    col_name = f'Jour {day}'
                    if col_name in self.df_emplacements.columns:
                        valor = row[col_name]
                        if pd.notna(valor):
                            totales[tipo][day-1] += int(valor)
            
            # Crear DataFrame con los totales
            data = []
            for tipo, valores in totales.items():
                row_data = {'Tipo de Alojamiento': tipo}
                for day in range(1, 8):
                    row_data[f'Día {day}'] = valores[day-1]
                data.append(row_data)
            
            self.df_alojamientos = pd.DataFrame(data)
            
            # Mostrar en la tabla
            self.display_alojamientos()
            self.export_button2.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar alojamientos: {str(e)}")
    
    def display_alojamientos(self):
        """Mostrar datos de alojamientos en la segunda pestaña"""
        # Limpiar tabla existente
        for item in self.tree2.get_children():
            self.tree2.delete(item)
        
        if self.df_alojamientos is None or self.df_alojamientos.empty:
            return
        
        # Configurar columnas
        columns = list(self.df_alojamientos.columns)
        self.tree2['columns'] = columns
        self.tree2['show'] = 'headings'
        
        # Configurar encabezados con iconos
        for col in columns:
            if col == 'Tipo de Alojamiento':
                self.tree2.heading(col, text=col)
                self.tree2.column(col, width=250, minwidth=200)
            elif 'Día' in col:
                day_num = col.split()[-1]
                display_text = f"🏠 {day_num}"
                self.tree2.heading(col, text=display_text)
                self.tree2.column(col, width=80, minwidth=60, anchor='center')
            else:
                self.tree2.heading(col, text=col)
                self.tree2.column(col, width=100, minwidth=80)
        
        # Insertar datos con alternancia de colores
        for idx, row in self.df_alojamientos.iterrows():
            values = [row[col] for col in columns]
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree2.insert('', 'end', values=values, tags=(tag,))
    
    def process_pricing_data(self):
        """Procesar datos de precios basados en ocupación semanal"""
        try:
            if self.df_emplacements is None:
                return
            
            # La columna Catégorie del archivo Emplacements contiene el tipo de alojamiento
            col_category = 'Catégorie' if 'Catégorie' in self.df_emplacements.columns else self.df_emplacements.columns[1]
            
            # Inicializar contadores para toda la semana
            total_camping = 0
            total_residente = 0
            total_bungalow = 0
            
            # Procesar ocupación de cada día
            for day in range(1, 8):
                col_name = f'Jour {day}'
                if col_name in self.df_emplacements.columns:
                    for idx, row in self.df_emplacements.iterrows():
                        categoria = str(row[col_category]).upper() if pd.notna(row[col_category]) else ''
                        ocupacion = row[col_name]
                        
                        if pd.notna(ocupacion) and ocupacion > 0:
                            # Determinar el tipo basándose en la categoría
                            if 'PARCELA RESIDENTE' in categoria:
                                total_residente += int(ocupacion)
                            elif 'PARCELA' in categoria:
                                total_camping += int(ocupacion)
                            elif categoria and categoria != 'NAN':
                                # Todo lo demás (bungalows, mobil-homes, etc.)
                                total_bungalow += int(ocupacion)
            
            # Calcular total general
            total_general = total_camping + total_residente + total_bungalow
            
            # Calcular porcentajes
            if total_general > 0:
                pct_camping = (total_camping / total_general) * 100
                pct_residente = (total_residente / total_general) * 100
                pct_bungalow = (total_bungalow / total_general) * 100
            else:
                pct_camping = pct_residente = pct_bungalow = 0
            
            # Crear DataFrame con los resultados
            data = [
                {
                    'Tipo de Tarifa': 'Tarifa normal: Tarifa aplicada a clientes ocasionales o de paso',
                    'Porcentaje': f'{pct_camping:.1f}%'
                },
                {
                    'Tipo de Tarifa': 'Tarifas especiales: Precios para estancias largas. Mas de un mes',
                    'Porcentaje': f'{pct_residente:.1f}%'
                },
                {
                    'Tipo de Tarifa': 'Bungalows, mobilhomes o similares',
                    'Porcentaje': f'{pct_bungalow:.1f}%'
                },
                {
                    'Tipo de Tarifa': 'TOTAL',
                    'Porcentaje': '100.0%'
                }
            ]
            
            self.df_pricing = pd.DataFrame(data)
            
            # Mostrar en la tabla
            self.display_pricing()
            self.export_button3.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar precios: {str(e)}")
    
    def display_pricing(self):
        """Mostrar datos de precios en la tercera pestaña"""
        # Limpiar tabla existente
        for item in self.tree3.get_children():
            self.tree3.delete(item)
        
        if self.df_pricing is None or self.df_pricing.empty:
            return
        
        # Configurar columnas
        columns = list(self.df_pricing.columns)
        self.tree3['columns'] = columns
        self.tree3['show'] = 'headings'
        
        # Configurar encabezados
        self.tree3.heading('Tipo de Tarifa', text='Tipo de Tarifa')
        self.tree3.column('Tipo de Tarifa', width=500, minwidth=400)
        
        self.tree3.heading('Porcentaje', text='Porcentaje')
        self.tree3.column('Porcentaje', width=150, minwidth=100, anchor='center')
        
        # Insertar datos
        for idx, row in self.df_pricing.iterrows():
            values = [row[col] for col in columns]
            if 'TOTAL' in row['Tipo de Tarifa']:
                tag = 'total'
            else:
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree3.insert('', 'end', values=values, tags=(tag,))
    
    def export_pricing(self):
        """Exportar datos de precios a Excel"""
        if self.df_pricing is None or self.df_pricing.empty:
            messagebox.showwarning("Advertencia", "No hay datos de precios para exportar")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"INE_Precios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if file_path:
                # Remover la fila de TOTAL para el export
                df_export = self.df_pricing[self.df_pricing['Tipo de Tarifa'] != 'TOTAL'].copy()
                df_export.to_excel(file_path, index=False, sheet_name='Precios INE')
                messagebox.showinfo("Éxito", f"Archivo exportado correctamente:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def export_alojamientos(self):
        """Exportar datos de alojamientos a Excel"""
        if self.df_alojamientos is None or self.df_alojamientos.empty:
            messagebox.showwarning("Advertencia", "No hay datos de alojamientos para exportar")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"INE_Alojamientos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if file_path:
                self.df_alojamientos.to_excel(file_path, index=False, sheet_name='Alojamientos INE')
                messagebox.showinfo("Éxito", f"Archivo exportado correctamente:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    # El resto de métodos siguen igual que en la versión anterior
    def load_weekly_files(self):
        """Cargar los 4 archivos Excel para el cuestionario semanal"""
        try:
            # Este método sigue igual que en la versión anterior
            # pero sin la funcionalidad de Emplacements
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
    
    def export_all_to_excel(self):
        """Exportar todos los datos disponibles a un único archivo Excel con múltiples hojas"""
        # Verificar qué datos están disponibles
        has_data = False
        sheets_to_export = {}
        
        if self.df_combined is not None and not self.df_combined.empty:
            sheets_to_export['Llegadas y Pernoctaciones'] = self.df_combined
            has_data = True
            
        if self.df_alojamientos is not None and not self.df_alojamientos.empty:
            sheets_to_export['Alojamientos Ocupados'] = self.df_alojamientos
            has_data = True
            
        if self.df_pricing is not None and not self.df_pricing.empty:
            # Excluir la fila de TOTAL para el export
            df_pricing_export = self.df_pricing[self.df_pricing['Tipo de Tarifa'] != 'TOTAL'].copy()
            sheets_to_export['Precios'] = df_pricing_export
            has_data = True
        
        if not has_data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        try:
            # Pedir ubicación para guardar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"INE_Completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if file_path:
                # Crear Excel con múltiples hojas
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    for sheet_name, df in sheets_to_export.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Informar qué se exportó
                exported_sheets = ', '.join(sheets_to_export.keys())
                
                # Guardar en historial con los datos reales de los DataFrames
                datos_historial = {
                    "pestanas": list(sheets_to_export.keys()),
                    "regiones": [],
                    "paises": [],
                    "ocupacion": [],
                    "precios": []
                }
                
                # Guardar datos de llegadas/pernoctaciones (combinados en df_combined)
                if self.df_combined is not None and not self.df_combined.empty:
                    # Separar datos de regiones y países desde df_combined
                    # Los datos de regiones son donde Zona no es un país
                    # Los datos de países son donde Zona es un país
                    for _, row in self.df_combined.iterrows():
                        # Convertir fila a lista de valores
                        valores = row.tolist()
                        # Determinar si es región o país basado en algún criterio
                        # Por ahora guardamos todo en regiones ya que df_combined tiene todos mezclados
                        datos_historial["regiones"].append(valores)
                
                # Guardar datos de ocupación
                if self.df_alojamientos is not None and not self.df_alojamientos.empty:
                    for _, row in self.df_alojamientos.iterrows():
                        datos_historial["ocupacion"].append(row.tolist())
                
                # Guardar datos de precios
                if self.df_pricing is not None and not self.df_pricing.empty:
                    # Excluir la fila de TOTAL
                    df_pricing_sin_total = self.df_pricing[self.df_pricing['Tipo de Tarifa'] != 'TOTAL']
                    for _, row in df_pricing_sin_total.iterrows():
                        datos_historial["precios"].append(row.tolist())
                
                self.add_to_history("Semanal", file_path, datos_historial, 
                                   f"Pestañas: {exported_sheets}")
                
                messagebox.showinfo("Éxito", 
                    f"Archivo exportado correctamente:\n{file_path}\n\nHojas exportadas:\n{exported_sheets}")
                self.status_label.config(text="Exportación completada", foreground="green")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
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
        self.df_emplacements = None
        self.df_alojamientos = None
        self.df_export_alojamientos = None
        self.df_pricing = None
        
        # Limpiar tablas
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.tree2.get_children():
            self.tree2.delete(item)
        
        self.export_button.config(state='disabled')
        self.export_button2.config(state='disabled')
        self.export_button3.config(state='disabled')
        self.notebook.tab(1, state='disabled')  # Deshabilitar segunda pestaña
        self.notebook.tab(2, state='disabled')  # Deshabilitar tercera pestaña
        self.status_label.config(text="Esperando carga de archivos...", foreground="blue")

    def load_weekly_data_from_history(self, datos):
        """Cargar datos semanales desde el historial"""
        try:
            print(f"DEBUG: Cargando datos desde historial. Keys disponibles: {datos.keys()}")
            
            # Si los árboles no existen, no podemos cargar datos
            if not hasattr(self, 'regiones_tree') or not hasattr(self, 'paises_tree'):
                print("DEBUG: Los árboles de regiones/países no existen aún")
                # Los árboles ya deberían existir desde __init__, si no existen hay un problema
                messagebox.showwarning("Advertencia", 
                    "No se pueden cargar los datos. Reinicie la aplicación.")
                return
            
            # Limpiar tablas actuales
            if hasattr(self, 'regiones_tree'):
                for item in self.regiones_tree.get_children():
                    self.regiones_tree.delete(item)
            
            if hasattr(self, 'paises_tree'):
                for item in self.paises_tree.get_children():
                    self.paises_tree.delete(item)
            
            if hasattr(self, 'ocupacion_tree'):
                for item in self.ocupacion_tree.get_children():
                    self.ocupacion_tree.delete(item)
            
            if hasattr(self, 'precios_tree'):
                for item in self.precios_tree.get_children():
                    self.precios_tree.delete(item)
            
            # Variable para rastrear si faltan árboles
            missing_trees = False
            
            # Cargar datos de regiones
            if 'regiones' in datos and len(datos['regiones']) > 0:
                if hasattr(self, 'regiones_tree'):
                    print(f"DEBUG: Cargando {len(datos['regiones'])} regiones")
                    for row in datos['regiones']:
                        self.regiones_tree.insert('', 'end', values=row)
                else:
                    print("DEBUG: El árbol de regiones no existe aún")
                    missing_trees = True
            else:
                print("DEBUG: No hay datos de regiones en el historial")
            
            # Cargar datos de países
            if 'paises' in datos and len(datos['paises']) > 0:
                if hasattr(self, 'paises_tree'):
                    print(f"DEBUG: Cargando {len(datos['paises'])} países")
                    for row in datos['paises']:
                        self.paises_tree.insert('', 'end', values=row)
                else:
                    print("DEBUG: El árbol de países no existe aún")
                    missing_trees = True
            else:
                print("DEBUG: No hay datos de países en el historial")
            
            # Cargar datos de ocupación si existen
            if 'ocupacion' in datos and len(datos['ocupacion']) > 0:
                if hasattr(self, 'ocupacion_tree'):
                    print(f"DEBUG: Cargando {len(datos['ocupacion'])} registros de ocupación")
                    for row in datos['ocupacion']:
                        self.ocupacion_tree.insert('', 'end', values=row)
                else:
                    print("DEBUG: El árbol de ocupación no existe aún")
                    missing_trees = True
            else:
                print("DEBUG: No hay datos de ocupación en el historial")
            
            # Cargar datos de precios si existen
            if 'precios' in datos and len(datos['precios']) > 0:
                if hasattr(self, 'precios_tree'):
                    print(f"DEBUG: Cargando {len(datos['precios'])} registros de precios")
                    for row in datos['precios']:
                        self.precios_tree.insert('', 'end', values=row)
                else:
                    print("DEBUG: El árbol de precios no existe aún")
                    missing_trees = True
            else:
                print("DEBUG: No hay datos de precios en el historial")
            
            # Habilitar pestañas si hay datos
            if 'ocupacion' in datos and len(datos['ocupacion']) > 0:
                self.notebook.tab(1, state='normal')
            if 'precios' in datos and len(datos['precios']) > 0:
                self.notebook.tab(2, state='normal')
            
            # Mostrar mensaje si faltan árboles
            if missing_trees:
                messagebox.showinfo(
                    "Carga parcial de datos",
                    "Los datos del historial están guardados correctamente.\n\n" +
                    "Para visualizar todos los datos:\n" +
                    "1. Vaya a la pestaña 'Cargar Archivos'\n" +
                    "2. Cargue los archivos Excel correspondientes\n" +
                    "3. Luego podrá ver todos los datos del historial"
                )
            
            # Actualizar estado
            self.status_label.config(text="Datos cargados desde historial", foreground="green")
            print("DEBUG: Datos cargados exitosamente")
            
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def open_monthly_questionnaire_with_data(self, datos):
        """Abrir ventana mensual con datos precargados desde historial"""
        try:
            print(f"DEBUG: Abriendo ventana mensual con datos: {datos}")
            
            monthly_window = tk.Toplevel(self.root)
            monthly_window.title("INE - Cuestionario Mensual (Datos desde Historial)")
            monthly_window.geometry("600x400")
            monthly_window.resizable(False, False)
            
            # Hacer la ventana modal
            monthly_window.transient(self.root)
            monthly_window.grab_set()
            
            # Frame principal
            main_frame = ttk.Frame(monthly_window, padding="20")
            main_frame.pack(fill='both', expand=True)
            
            # Título
            title_label = ttk.Label(main_frame, 
                                   text="Cuestionario Mensual INE - Datos Cargados",
                                   font=('Arial', 14, 'bold'))
            title_label.pack(pady=(0, 20))
            
            # Label de estado
            status_label = ttk.Label(main_frame, text="Datos cargados desde historial", 
                                    foreground="green")
            status_label.pack(pady=5)
            
            # Frame para resultados
            results_frame = ttk.LabelFrame(main_frame, text="Resultados INE Mensual", padding="15")
            results_frame.pack(fill='both', expand=True, pady=10)
            
            # Cargar valores desde datos
            viajeros = datos.get('viajeros', 0)
            pernoctaciones = datos.get('pernoctaciones', 0)
            parcelas = datos.get('parcelas', 0)
            
            print(f"DEBUG: Valores cargados - V:{viajeros}, P:{pernoctaciones}, Pa:{parcelas}")
            
            # Labels para mostrar resultados
            ttk.Label(results_frame, 
                     text=f"1. Viajeros: {viajeros:,}".replace(',', '.'),
                     font=('Arial', 12)).pack(pady=8, anchor='w')
            ttk.Label(results_frame, 
                     text=f"2. Pernoctaciones: {pernoctaciones:,}".replace(',', '.'),
                     font=('Arial', 12)).pack(pady=8, anchor='w')
            ttk.Label(results_frame, 
                     text=f"3. Parcelas totales ocupadas: {parcelas:,}".replace(',', '.'),
                     font=('Arial', 12)).pack(pady=8, anchor='w')
            
            # Crear variable local para resultados
            monthly_results_local = {
                'Viajeros': viajeros,
                'Pernoctaciones': pernoctaciones,
                'Parcelas totales ocupadas': parcelas
            }
            
            def export_monthly_results():
                """Re-exportar resultados mensuales"""
                nonlocal monthly_results_local
                try:
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".xlsx",
                        filetypes=[("Excel files", "*.xlsx")],
                        initialfile=f"INE_Mensual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    )
                    
                    if file_path:
                        # Crear DataFrame con los resultados
                        df_results = pd.DataFrame([
                            {'Concepto': 'Viajeros', 'Valor': monthly_results_local['Viajeros']},
                            {'Concepto': 'Pernoctaciones', 'Valor': monthly_results_local['Pernoctaciones']},
                            {'Concepto': 'Parcelas totales ocupadas', 'Valor': monthly_results_local['Parcelas totales ocupadas']}
                        ])
                        
                        # Exportar a Excel
                        df_results.to_excel(file_path, index=False, sheet_name='INE Mensual')
                        
                        # Añadir al historial
                        self.add_to_history(
                            tipo="Mensual",
                            archivo=file_path,
                            datos_exportados={
                                'viajeros': monthly_results_local['Viajeros'],
                                'pernoctaciones': monthly_results_local['Pernoctaciones'],
                                'parcelas': monthly_results_local['Parcelas totales ocupadas']
                            },
                            resumen=f"V:{monthly_results_local['Viajeros']} P:{monthly_results_local['Pernoctaciones']} Pa:{monthly_results_local['Parcelas totales ocupadas']}"
                        )
                        
                        messagebox.showinfo("Éxito", f"Resultados re-exportados correctamente:\n{file_path}")
                
                except Exception as e:
                    messagebox.showerror("Error", f"Error al exportar: {str(e)}")
            
            # Frame para botones
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(pady=10, side='bottom')
            
            # Botón para re-exportar
            ttk.Button(button_frame, text="Re-exportar a Excel", 
                      command=export_monthly_results).pack(side='left', padx=5)
            
            # Botón cerrar
            ttk.Button(button_frame, text="Cerrar", 
                      command=monthly_window.destroy).pack(side='left', padx=5)
        
        except Exception as e:
            print(f"Error en open_monthly_questionnaire_with_data: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al abrir ventana mensual: {str(e)}")
    
    def open_monthly_questionnaire(self):
        """Abrir ventana para el cuestionario mensual"""
        monthly_window = tk.Toplevel(self.root)
        monthly_window.title("INE - Cuestionario Mensual")
        monthly_window.geometry("600x400")
        monthly_window.resizable(False, False)
        
        # Hacer la ventana modal
        monthly_window.transient(self.root)
        monthly_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(monthly_window, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="Cuestionario Mensual INE",
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Variables para almacenar datos (NO usar self aquí porque estamos en una función local)
        monthly_data = None
        
        # Label de estado
        status_label = ttk.Label(main_frame, text="Seleccione el archivo de estadísticas mensuales", 
                                foreground="blue")
        status_label.pack(pady=10)
        
        # Frame para resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados INE Mensual", padding="15")
        results_frame.pack(fill='both', expand=True, pady=20)
        
        # Labels para mostrar resultados
        result_labels = {
            'viajeros': ttk.Label(results_frame, text="1. Viajeros: -", font=('Arial', 12)),
            'pernoctaciones': ttk.Label(results_frame, text="2. Pernoctaciones: -", font=('Arial', 12)),
            'parcelas': ttk.Label(results_frame, text="3. Parcelas totales ocupadas: -", font=('Arial', 12))
        }
        
        for label in result_labels.values():
            label.pack(pady=8, anchor='w')
        
        # Botón exportar (inicialmente deshabilitado)
        export_btn = ttk.Button(button_frame, text="Exportar Resultados", state='disabled')
        
        def load_monthly_file():
            """Cargar y procesar archivo mensual"""
            try:
                file_path = filedialog.askopenfilename(
                    title="Seleccionar archivo de estadísticas mensuales",
                    filetypes=[("Excel files", "*.xlsx *.xls")],
                    initialdir=os.path.dirname(os.path.abspath(__file__))
                )
                
                if not file_path:
                    return
                
                # Verificar que sea un archivo de estadísticas mensuales
                if 'statistiques pour le mois' not in os.path.basename(file_path).lower():
                    response = messagebox.askyesno("Advertencia", 
                        "El archivo no parece ser de estadísticas mensuales.\n¿Desea continuar de todos modos?")
                    if not response:
                        return
                
                # Cargar archivo
                status_label.config(text="Procesando archivo...", foreground="orange")
                monthly_window.update()
                
                df = pd.read_excel(file_path)
                
                # Verificar columnas necesarias
                required_cols = ['Nb de personnes', 'Nb de nuit', 'Nb de places']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    messagebox.showerror("Error", 
                        f"El archivo no contiene las columnas necesarias:\n{', '.join(missing_cols)}")
                    return
                
                # Calcular resultados
                viajeros = int(df['Nb de personnes'].sum())
                pernoctaciones = int((df['Nb de nuit'] * df['Nb de personnes']).sum())
                parcelas_ocupadas = int(df['Nb de places'].sum())
                
                # Guardar resultados en variable no-local
                nonlocal monthly_data
                monthly_data = {
                    'Viajeros': viajeros,
                    'Pernoctaciones': pernoctaciones,
                    'Parcelas totales ocupadas': parcelas_ocupadas
                }
                
                # Actualizar labels
                result_labels['viajeros'].config(
                    text=f"1. Viajeros: {viajeros:,}".replace(',', '.'))
                result_labels['pernoctaciones'].config(
                    text=f"2. Pernoctaciones: {pernoctaciones:,}".replace(',', '.'))
                result_labels['parcelas'].config(
                    text=f"3. Parcelas totales ocupadas: {parcelas_ocupadas:,}".replace(',', '.'))
                
                # Habilitar botón exportar
                export_btn.config(state='normal')
                
                # Extraer mes del nombre del archivo
                filename = os.path.basename(file_path)
                import re
                match = re.search(r'mois de (\w+) (\d+)', filename)
                if match:
                    mes = match.group(1)
                    año = match.group(2)
                    status_label.config(text=f"Datos procesados para {mes} {año}", foreground="green")
                else:
                    status_label.config(text="Datos procesados correctamente", foreground="green")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar archivo:\n{str(e)}")
                status_label.config(text="Error en el procesamiento", foreground="red")
        
        def export_monthly_results():
            """Exportar resultados mensuales a Excel"""
            nonlocal monthly_data
            print(f"DEBUG: Iniciando exportación mensual")
            print(f"DEBUG: monthly_data = {monthly_data}")
            
            if not monthly_data:
                print("DEBUG: No hay resultados mensuales para exportar")
                messagebox.showwarning("Advertencia", "No hay resultados mensuales para exportar")
                return
            
            try:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    initialfile=f"INE_Mensual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                )
                
                if file_path:
                    print(f"DEBUG: Exportando a {file_path}")
                    # Crear DataFrame con los resultados
                    df_results = pd.DataFrame([
                        {'Concepto': 'Viajeros', 'Valor': monthly_data['Viajeros']},
                        {'Concepto': 'Pernoctaciones', 'Valor': monthly_data['Pernoctaciones']},
                        {'Concepto': 'Parcelas totales ocupadas', 'Valor': monthly_data['Parcelas totales ocupadas']}
                    ])
                    
                    print(f"DEBUG: DataFrame creado:\n{df_results}")
                    
                    # Exportar a Excel
                    df_results.to_excel(file_path, index=False, sheet_name='INE Mensual')
                    print(f"DEBUG: Excel guardado exitosamente")
                    
                    # Añadir al historial
                    self.add_to_history(
                        tipo="Mensual",
                        archivo=file_path,
                        datos_exportados={
                            'viajeros': monthly_data['Viajeros'],
                            'pernoctaciones': monthly_data['Pernoctaciones'],
                            'parcelas': monthly_data['Parcelas totales ocupadas']
                        },
                        resumen=f"V:{monthly_data['Viajeros']} P:{monthly_data['Pernoctaciones']} Pa:{monthly_data['Parcelas totales ocupadas']}"
                    )
                    print(f"DEBUG: Añadido al historial")
                    
                    messagebox.showinfo("Éxito", f"Resultados exportados correctamente:\n{file_path}")
            
            except Exception as e:
                print(f"DEBUG ERROR al exportar: {str(e)}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
        
        # Configurar botones
        ttk.Button(button_frame, text="Cargar Archivo Mensual", 
                  command=load_monthly_file, width=25).pack(side=tk.LEFT, padx=5)
        export_btn.config(command=export_monthly_results)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón cerrar
        ttk.Button(button_frame, text="Cerrar", 
                  command=monthly_window.destroy, width=15).pack(side=tk.LEFT, padx=5)

    def load_history(self):
        """Cargar historial desde archivo JSON"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = {"exportaciones": []}
        except Exception as e:
            print(f"Error cargando historial: {e}")
            self.history = {"exportaciones": []}
    
    def save_history(self):
        """Guardar historial en archivo JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def add_to_history(self, tipo, archivo, datos_exportados, resumen=None):
        """Añadir nueva entrada al historial"""
        entry = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "archivo": os.path.basename(archivo) if archivo else "No guardado",
            "datos": datos_exportados,
            "resumen": resumen
        }
        
        self.history["exportaciones"].insert(0, entry)  # Insertar al principio
        self.save_history()
    
    def open_history_window(self):
        """Abrir ventana de historial de exportaciones"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Historial de Exportaciones")
        history_window.geometry("900x600")
        
        # Frame principal
        main_frame = ttk.Frame(history_window, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Historial de Exportaciones INE",
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Frame para la tabla
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para mostrar historial
        columns = ('Fecha', 'Tipo', 'Archivo', 'Resumen')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                           yscrollcommand=scroll_y.set, height=15)
        
        # Configurar columnas
        tree.heading('Fecha', text='Fecha y Hora')
        tree.column('Fecha', width=150)
        tree.heading('Tipo', text='Tipo')
        tree.column('Tipo', width=100)
        tree.heading('Archivo', text='Archivo Exportado')
        tree.column('Archivo', width=250)
        tree.heading('Resumen', text='Resumen de Datos')
        tree.column('Resumen', width=350)
        
        tree.pack(side=tk.LEFT, fill='both', expand=True)
        scroll_y.config(command=tree.yview)
        
        # Cargar datos del historial
        def refresh_history():
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            
            # Cargar historial actualizado
            self.load_history()
            
            # Insertar datos
            for entry in self.history.get("exportaciones", []):
                fecha = entry.get("fecha", "")
                tipo = entry.get("tipo", "")
                archivo = entry.get("archivo", "")
                
                # Crear resumen según el tipo
                resumen = ""
                if tipo == "Semanal":
                    datos = entry.get("datos", {})
                    pestanas = datos.get("pestanas", [])
                    resumen = f"Pestañas: {', '.join(pestanas)}"
                elif tipo == "Mensual":
                    datos = entry.get("datos", {})
                    resumen = f"V:{datos.get('viajeros', 0)} P:{datos.get('pernoctaciones', 0)} Pa:{datos.get('parcelas', 0)}"
                
                if entry.get("resumen"):
                    resumen = entry.get("resumen")
                
                entry_id = entry.get("id", "")
                print(f"DEBUG: Insertando en tree con ID: {entry_id}")
                tree.insert('', 'end', values=(fecha, tipo, archivo, resumen),
                           tags=(entry_id,))
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        def delete_selected():
            """Eliminar entrada seleccionada"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione una entrada para eliminar")
                return
            
            if messagebox.askyesno("Confirmar", "¿Eliminar la entrada seleccionada?"):
                item = tree.item(selected[0])
                entry_id = item['tags'][0] if item['tags'] else None
                if entry_id:
                    # Reconstruir el ID con underscores
                    entry_id = str(entry_id)
                    if len(entry_id) >= 15 and '_' not in entry_id:
                        entry_id = f"{entry_id[:8]}_{entry_id[8:14]}_{entry_id[14:]}"
                
                # Buscar y eliminar del historial
                self.history["exportaciones"] = [
                    e for e in self.history["exportaciones"] 
                    if e.get("id") != entry_id
                ]
                self.save_history()
                refresh_history()
                messagebox.showinfo("Éxito", "Entrada eliminada del historial")
        
        def view_details():
            """Cargar datos de la entrada seleccionada en las pestañas"""
            try:
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Advertencia", "Seleccione una entrada para cargar datos")
                    return
                
                print(f"DEBUG view_details: Entrada seleccionada")
                item = tree.item(selected[0])
                # Los tags en Tkinter eliminan underscores, necesitamos reconstruir el ID
                entry_id = item['tags'][0] if item['tags'] else None
                if entry_id:
                    # Reconstruir el ID con underscores
                    entry_id = str(entry_id)
                    if len(entry_id) >= 15 and '_' not in entry_id:
                        # Formato esperado: YYYYMMDD_HHMMSS_microseconds
                        entry_id = f"{entry_id[:8]}_{entry_id[8:14]}_{entry_id[14:]}"
                print(f"DEBUG view_details: ID de entrada reconstruido: {entry_id}")
                
                # Buscar entrada en el historial
                entry = None
                print(f"DEBUG: IDs disponibles en historial:")
                for e in self.history["exportaciones"]:
                    print(f"  - {e.get('id')}")
                    if e.get("id") == entry_id:
                        entry = e
                        break
                
                if entry:
                    tipo = entry.get("tipo", "")
                    datos = entry.get("datos", {})
                    print(f"DEBUG view_details: Tipo={tipo}, Datos keys={datos.keys() if datos else 'None'}")
                    
                    # Cerrar ventana de historial
                    history_window.destroy()
                    
                    if tipo == "Semanal":
                        print(f"DEBUG view_details: Cargando datos semanales")
                        # Cargar datos semanales en las pestañas
                        self.load_weekly_data_from_history(datos)
                        messagebox.showinfo("Datos Cargados", 
                            f"Datos semanales cargados desde el historial\nFecha: {entry.get('fecha', '')}")
                        
                    elif tipo == "Mensual":
                        print(f"DEBUG view_details: Cargando datos mensuales")
                        # Abrir ventana mensual y cargar datos
                        self.open_monthly_questionnaire_with_data(datos)
                        messagebox.showinfo("Datos Cargados", 
                            f"Datos mensuales cargados desde el historial\nFecha: {entry.get('fecha', '')}")
                else:
                    print(f"DEBUG view_details: No se encontró la entrada con ID {entry_id}")
            except Exception as e:
                print(f"DEBUG ERROR en view_details: {str(e)}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
        
        # Botones
        ttk.Button(button_frame, text="Cargar Datos", command=view_details,
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=delete_selected,
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=refresh_history,
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=history_window.destroy,
                  width=15).pack(side=tk.RIGHT, padx=5)
        
        # Cargar historial inicial
        refresh_history()

def main():
    root = tk.Tk()
    app = INEApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()