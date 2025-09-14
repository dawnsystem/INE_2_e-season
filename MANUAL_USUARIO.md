# Manual de Usuario - INE Transformer
## Sistema de Procesamiento de Encuestas INE para Campings

### Índice
1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Interfaz Principal](#interfaz-principal)
5. [Cuestionario Semanal](#cuestionario-semanal)
6. [Cuestionario Mensual](#cuestionario-mensual)
7. [Sistema de Historial](#sistema-de-historial)
8. [Resolución de Problemas](#resolución-de-problemas)

---

## 1. Introducción

INE Transformer es una aplicación diseñada para procesar y gestionar las encuestas del Instituto Nacional de Estadística (INE) para establecimientos de camping en Cataluña, que utilicen el PMS E-Season. La aplicación permite:

- Procesar archivos Excel con datos de encuestas semanales y mensuales
- Transformar y organizar los datos según los requisitos del INE
- Mantener un historial de todas las exportaciones realizadas
- Recuperar datos de exportaciones anteriores

## 2. Requisitos del Sistema

### Software Necesario
- Python 3.8 o superior
- Windows 10/11 (recomendado)

### Bibliotecas Python Requeridas
```
pandas
openpyxl
tkinter (incluido con Python)
```

### Instalación de Dependencias
```bash
pip install pandas openpyxl
```

## 3. Instalación

1. Descargue el archivo `ine_app_v3.py` en su carpeta de trabajo
2. Asegúrese de tener Python instalado en su sistema
3. Instale las dependencias necesarias usando pip
4. Ejecute la aplicación:
```bash
python ine_app_v3.py
```

## 4. Interfaz Principal

### Elementos de la Ventana Principal

#### Pestañas de Datos
La aplicación tiene 3 pestañas principales para visualizar datos procesados:

1. **Llegadas y Pernoctaciones**: Muestra datos de visitantes por región/país
2. **Alojamientos Ocupados**: Información sobre ocupación de diferentes tipos de alojamiento
3. **Precios**: Porcentajes de aplicación de diferentes tarifas

#### Botones Principales
- **Cargar Archivo Semanal**: Abre selector para cargar archivo Excel semanal
- **Cuestionario Mensual**: Abre ventana para procesar datos mensuales
- **Exportar Todo a Excel**: Genera archivo Excel con todos los datos procesados
- **Ver Historial**: Acceso rápido al historial de exportaciones

## 5. Cuestionario Semanal

### Proceso de Carga y Exportación

#### Paso 1: Cargar Archivo
1. Haga clic en "Cargar Archivo Semanal"
2. Seleccione el archivo Excel descargado del INE
3. El sistema procesará automáticamente:
   - Datos de llegadas y pernoctaciones por región
   - Información de alojamientos ocupados
   - Estadísticas de precios

#### Paso 2: Revisar Datos
- Los datos se mostrarán en las pestañas correspondientes
- Verifique que la información esté completa y correcta

#### Paso 3: Exportar
1. Haga clic en "Exportar Todo a Excel"
2. Elija ubicación y nombre para el archivo
3. El sistema generará un Excel con formato INE
4. Los datos se guardarán automáticamente en el historial

### Estructura del Archivo Exportado
El archivo Excel generado contendrá:
- **Hoja 1**: Llegadas y Pernoctaciones (datos por día de la semana)
- **Hoja 2**: Alojamientos Ocupados (ocupación diaria)
- **Hoja 3**: Precios (porcentajes de tarifas aplicadas)

## 6. Cuestionario Mensual

### Acceso y Uso

#### Abrir Cuestionario Mensual
1. Haga clic en "Cuestionario Mensual" en la ventana principal
2. Se abrirá una nueva ventana con campos específicos

#### Campos del Formulario
- **Viajeros**: Número total de viajeros en el mes
- **Pernoctaciones**: Total de pernoctaciones del mes
- **Parcelas totales ocupadas**: Número de parcelas ocupadas

#### Proceso de Datos Mensuales

##### Opción A: Entrada Manual
1. Introduzca los valores en cada campo
2. Haga clic en "Exportar Resultados"
3. Elija ubicación para guardar el archivo

##### Opción B: Cargar desde Archivo
1. Haga clic en "Cargar Archivo Mensual"
2. Seleccione el archivo Excel del INE
3. Los datos se cargarán automáticamente
4. Exporte los resultados procesados

### Formato de Exportación Mensual
El archivo generado contendrá una hoja con:
- Resumen de viajeros
- Total de pernoctaciones
- Parcelas ocupadas
- Cálculos y totales requeridos por el INE

## 7. Sistema de Historial

### Funcionalidades del Historial

#### Acceder al Historial
- Botón: "Ver Historial" en ventana principal

#### Ventana de Historial
La ventana muestra una tabla con:
- **Fecha y Hora**: Momento de la exportación
- **Tipo**: Semanal o Mensual
- **Archivo**: Nombre del archivo exportado
- **Resumen**: Información resumida de los datos

### Operaciones con el Historial

#### Ver Detalles y Cargar Datos
1. Seleccione una entrada en la tabla
2. Haga clic en "Ver Detalles"
3. Los datos se cargarán en las pestañas correspondientes
4. Para datos mensuales, se abrirá automáticamente el cuestionario mensual

#### Eliminar Entradas
1. Seleccione la entrada a eliminar
2. Haga clic en "Eliminar"
3. Confirme la eliminación
4. La entrada se eliminará permanentemente

#### Actualizar Lista
- Haga clic en "Actualizar" para refrescar la lista
- Útil si se han realizado cambios externos

### Archivo de Historial
- Los datos se guardan en: `historial_exportaciones.json`
- Formato JSON legible y editable si es necesario
- Se actualiza automáticamente con cada exportación

## 8. Resolución de Problemas

### Problemas Comunes y Soluciones

#### Error al Cargar Archivo
**Problema**: "Error al procesar el archivo"
**Solución**: 
- Verifique que el archivo sea un Excel válido (.xlsx)
- Asegúrese de que tenga el formato esperado del INE
- Compruebe que el archivo no esté abierto en otro programa

#### Datos No Se Muestran
**Problema**: Las pestañas aparecen vacías después de cargar
**Solución**:
- Verifique que el archivo contenga datos
- Revise la consola para mensajes de error
- Intente recargar el archivo

#### Error al Exportar
**Problema**: "Error al exportar los resultados"
**Solución**:
- Asegúrese de tener permisos de escritura en la carpeta destino
- Verifique que el nombre de archivo sea válido
- Cierre el archivo si está abierto en Excel

#### Historial No Se Actualiza
**Problema**: Las exportaciones no aparecen en el historial
**Solución**:
- Verifique que existe el archivo `historial_exportaciones.json`
- Compruebe permisos de escritura en la carpeta
- Haga clic en "Actualizar" en la ventana de historial

### Mensajes de Error Específicos

#### "AttributeError: 'INEApp' object has no attribute..."
- Reinicie la aplicación
- Si persiste, verifique la versión del archivo `ine_app_v3.py`

#### "No se encontraron datos válidos"
- El archivo Excel no contiene las hojas esperadas
- Verifique que sea un archivo del INE correcto

### Consejos de Uso

1. **Backup Regular**: Mantenga copias del archivo `historial_exportaciones.json`
2. **Nombres Descriptivos**: Use nombres de archivo descriptivos al exportar
3. **Verificación**: Siempre verifique los datos antes de exportar
4. **Actualizaciones**: Mantenga las bibliotecas Python actualizadas

### Soporte Técnico

Para problemas no cubiertos en este manual:
1. Revise los mensajes de consola para información detallada
2. Verifique que todas las dependencias estén instaladas correctamente
3. Asegúrese de usar la versión más reciente de la aplicación

---

## Anexo: Estructura de Datos

### Formato de Datos Semanales
```
Llegadas y Pernoctaciones:
- Columna 1: Zona/País
- Columnas 2-15: Llegadas y Pernoctaciones por día (7 días)

Alojamientos:
- Columna 1: Tipo de alojamiento
- Columnas 2-8: Ocupación diaria

Precios:
- Columna 1: Tipo de tarifa
- Columna 2: Porcentaje de aplicación
```

### Formato de Datos Mensuales
```
- Viajeros: Número entero
- Pernoctaciones: Número entero
- Parcelas totales ocupadas: Número entero
```

---

*Versión del Manual: 1.0*  
*Fecha: Septiembre 2025*  
*Aplicación: INE Transformer v3*