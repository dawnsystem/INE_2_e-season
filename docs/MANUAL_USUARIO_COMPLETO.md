# 📘 Manual de Usuario Completo - INE Transformer 4 E-Season

## Sistema de Procesamiento de Encuestas INE para Campings Capfun

### Versión 4.0 - Para E-Season PMS (CapFun - España)

---

## 🎯 DESCRIPCIÓN GENERAL

**INE Transformer 4 E-Season** es una aplicación diseñada específicamente para los campings de la cadena Capfun que necesitan procesar los datos extraidos de e-Season para responder a las encuestas del Instituto Nacional de Estadística (INE) de España.

La aplicación automatiza la transformación de los datos exportados desde E-Season PMS al formato exacto requerido por el INE, tanto para cuestionarios semanales como mensuales.

ATENCIÓN! NO NOS CONFUNDAMOS, LA APP NO ENVÍA LOS CUESTIONARIOS, SOLO TRANSFORMA LOS ARCHIVOS EXCEL PARA OBTENER LOS RESULTADOS QUE LUEGO INTRODUCIREMOS EN [www.iria.ine.es](https://iria.ine.es/iriaPortal/contents/index.jsf)

---

## 🔧 INSTALACIÓN

### Opción A: Ejecutable Windows (Recomendado)

1. Descargar el archivo `INE_4_e-season.exe`
2. No requiere instalación, solo ejecutar directamente
3. Si Windows muestra advertencia de seguridad, seleccionar "Ejecutar de todos modos"

### Opción B: Desde Python

1. Instalar Python 3.8 o superior
2. Instalar dependencias: `pip install pandas openpyxl pillow`
3. Ejecutar: `python ine_app_v3.py`

---

## 📁 PREPARACIÓN INICIAL (Una vez por temporada)

### Exportar el archivo de configuración de alojamientos

Este archivo solo necesita exportarse **UNA VEZ al inicio de temporada** o cuando se añadan nuevos tipos de alojamiento.

**Pasos en E-Season:**

1. Ir a: **Menu principal → Admin → Paramétrages → Emplacement**
2. Aparecerá una tabla con todos los alojamientos del camping
3. **Clic derecho** sobre la tabla
4. Seleccionar **"Exporter la table vers Excel..."**
5. Guardar con el nombre exacto: `Export_Alojamientos.xlsx`
6. Guardar este archivo y copiarlo en cada carpeta de cuestionario semanal

⚠️ **IMPORTANTE**: Este archivo es esencial para el procesamiento correcto del Apartado 4.

---

## 📊 CUESTIONARIO SEMANAL - Guía Completa

### PASO 1: Crear carpeta de trabajo

**IMPORTANTE**: Para cada cuestionario semanal, crear una **nueva carpeta** donde se guardarán TODOS los archivos necesarios.

Ejemplo de nombre de carpeta: `INE_Semana_01_07_2024`

### PASO 2: Exportar archivos desde E-Season

#### 2.1 - Archivos de Personas (Países y Regiones)

**Ruta en E-Season**:
📍 **Menu Principal → Statistiques → Séjours → Statistiques INE Personnes (Espagne)**

**Procedimiento:**

1. Introducir la **fecha de inicio** del cuestionario semanal
2. Pulsar el botón **"Calculer"**
3. Una vez calculados los datos, pulsar el **botón con símbolo de Excel** 📊
4. Se abrirán automáticamente **4 archivos Excel**:
   - `INE-DD_MM_AAAA-Pays Arrivées.xlsx` (Llegadas por país)
   - `INE-DD_MM_AAAA-Pays Occupation.xlsx` (Ocupación por país)
   - `INE-DD_MM_AAAA-Régions Arrivées.xlsx` (Llegadas por región)
   - `INE-DD_MM_AAAA-Régions Occupation.xlsx` (Ocupación por región)
5. **"Guardar Como" los 4 archivos** en la carpeta creada **SIN cambiar los nombres**

#### 2.2 - Archivo de Alojamientos Ocupados

**Ruta en E-Season**:
📍 **Menu Principal → Statistiques → Séjours → Statistiques INE Catégorie (Espagne)**

**Procedimiento:**

1. Introducir la **fecha de inicio** de la semana
2. Pulsar el botón **"Calculer"**
3. Pulsar el **botón con símbolo de Excel** 📊
4. Se abrirán 2 archivos Excel
5. **SOLO necesitamos** el archivo (el otro lo podemos cerrar sin guardar): `INE-DD_MM_AAAA-Emplacements nus et locatifs Occupés.xlsx`
6. **Guardar este archivo** en la misma carpeta

#### 2.3 - Archivo de Estadísticas (para precios)

**Ruta en E-Season**:
📍 **Menu Principal → Statistiques → Séjours → Statistiques INS**

**Procedimiento:**

1. Seleccionar **mes y año** correspondientes
2. Pulsar **"Rechercher"**
3. Una vez aparezcan los datos, pulsar el **botón Excel** 📊
4. Se abrirá el archivo: `Statistiques pour le mois de [Mes] AAAA.xlsx`
5. **Guardar** en la misma carpeta **SIN cambiar el nombre**

#### 2.4 - Copiar archivo de configuración

Copiar el archivo `Export_Alojamientos.xlsx` (exportado al inicio de temporada) en la carpeta del cuestionario.

### PASO 3: Procesar en INE Transformer

1. **Abrir** la aplicación `INE_4_e-season.exe`
2. En la pestaña **"Cargar Archivos"**, hacer clic en **"Seleccionar Archivos INE"**
3. **Navegar hasta la carpeta** creada con todos los archivos
4. **Seleccionar la carpeta** (no los archivos individuales)
5. La aplicación **detectará y cargará automáticamente** todos los archivos con los nombres correctos

### PASO 4: Verificar datos procesados

La aplicación mostrará los datos procesados en 3 pestañas:

#### 📑 Pestaña 1: "Apartados 2 y 3 - Llegadas y Pernoctaciones"

- Datos combinados de países y regiones
- Verificar totales de viajeros y pernoctaciones

#### 📑 Pestaña 2: "Apartado 4 - Alojamientos Ocupados"

- Muestra ocupación por tipo de alojamiento y día
- Categorías:
  - 4.1.1 Parcelas larga duración (Parcelas Residente)
  - 4.1.2 Resto parcelas
  - 4.2 Bungalows y similares
  - 4.3 Caravanas
  - 4.4 Zona sin parcelar

#### 📑 Pestaña 3: "Apartado 6 - Precios"

* Precios medios: deberéis hacer un "**devis"** de la semana en cuestion para obtener el precio diario de las tarifas que useis.
* Este programa solo arroja los porcentajes de las siguientes categorías (si existe movimiento):

1. Tarifa normal: Tarifa aplicada a clientes ocasionales o de paso (Camping)

### PASO 5: Exportar resultados

1. En cada pestaña activa, hacer clic en **"Exportar INE Completo"**
2. Los archivos se guardarán con formato: `INE_Completo_AAAAMMDD_HHMMSS.xlsx`
3. El archivo está **listo para enviar al INE**
4. Los datos se guardan en el historial **SOLO si se exportan**

⚠️ **IMPORTANTE**: Si no exportas los datos a Excel, NO se guardarán en el historial

---

## 📈 CUESTIONARIO MENSUAL - Guía Completa

El cuestionario mensual procesa automáticamente los datos del archivo de estadísticas mensuales.

### PASO 1: Preparar el archivo mensual

1. Exportar desde E-Season el archivo `Statistiques pour le mois de [Mes] AAAA.xlsx`
   - Ruta: **Menu Principal → Statistiques → Séjours → Statistiques INS**
   - Seleccionar mes y año, pulsar "Rechercher" y luego botón Excel

### PASO 2: Cargar archivo en INE Transformer

1. En el menú principal, hacer clic en **"Cuestionario Mensual"**
2. Hacer clic en **"Cargar archivo mensual"**
3. Seleccionar el archivo `Statistiques pour le mois de [Mes] AAAA.xlsx`
4. La aplicación **procesará automáticamente** los datos:
   - Total de viajeros del mes
   - Total de pernoctaciones del mes
   - Total de parcelas disponibles

### PASO 3: Verificar y Exportar

1. Verificar los datos mostrados en pantalla
2. Hacer clic en **"Exportar INE Mensual"**
3. El archivo se guardará como: `INE_Mensual_AAAAMMDD_HHMMSS.xlsx`
4. Los datos se guardan en el historial **SOLO si se exportan**
5. El archivo está listo para enviar al INE

---

## 📚 GESTIÓN DEL HISTORIAL

### Ver historial de exportaciones

1. Hacer clic en **"Ver Historial"**
2. Se mostrará lista con:
   - Fecha y hora de exportación
   - Tipo (Semanal/Mensual)
   - Nombre del archivo
   - Resumen de datos

### Recuperar datos anteriores

1. Seleccionar una entrada del historial
2. Hacer clic en **"Cargar Datos"**
3. Los datos se cargarán en las pestañas correspondientes
4. Útil para:
   - Revisar envíos anteriores
   - Reenviar información
   - Comparar períodos

### Eliminar entradas

1. Seleccionar entrada a eliminar
2. Hacer clic en **"Eliminar"**
3. Confirmar eliminación

---

## ⚙️ CONFIGURACIÓN IMPORTANTE EN E-SEASON

### Configuración de Tarifas

⚠️ **PREREQUISITO**: En cada apartado de estadísticas INE, verificar que estén configuradas las tarifas correctas en el botón **"Tarifs"**.

Esto es esencial para que los datos se calculen correctamente en:

- Statistiques INE Personnes
- Statistiques INE Catégorie
- Statistiques INS

---

## 🔍 SOLUCIÓN DE PROBLEMAS

### Problema: "No se encontró Export_Alojamientos.xlsx"

**Solución**:

1. Exportar el archivo siguiendo los pasos de "Preparación Inicial"
2. Copiarlo en la carpeta con los demás archivos

### Problema: La aplicación no carga todos los archivos

**Causa**: Los archivos no están en la misma carpeta o tienen nombres modificados
**Solución**:

1. Verificar que TODOS los archivos estén en la misma carpeta
2. No cambiar los nombres de los archivos al exportar desde E-Season

### Problema: Faltan las pestañas 2 y 3

**Causa**: Faltan archivos necesarios
**Solución**: Verificar que se han exportado:

- Archivo de alojamientos (para pestaña 2)
- Archivo de estadísticas del mes (para pestaña 3)

### Problema: Los totales no coinciden

**Solución**:

1. Verificar fechas seleccionadas en E-Season
2. Comprobar configuración de tarifas en E-Season
3. Asegurar que se calcularon los datos antes de exportar

---

## 📋 RESUMEN DE ARCHIVOS NECESARIOS

### Para Cuestionario SEMANAL (7 archivos):

1. ✅ `INE-DD_MM_AAAA-Pays Arrivées.xlsx`
2. ✅ `INE-DD_MM_AAAA-Pays Occupation.xlsx`
3. ✅ `INE-DD_MM_AAAA-Régions Arrivées.xlsx`
4. ✅ `INE-DD_MM_AAAA-Régions Occupation.xlsx`
5. ✅ `INE-DD_MM_AAAA-Emplacements nus et locatifs Occupés.xlsx`
6. ✅ `Statistiques pour le mois de [Mes] AAAA.xlsx`
7. ✅ `Export_Alojamientos.xlsx` (configuración)

### Para Cuestionario MENSUAL (1 archivo):

- ✅ `Statistiques pour le mois de [Mes] AAAA.xlsx` (datos agregados del mes)

---

## 💡 CONSEJOS Y MEJORES PRÁCTICAS

### Organización recomendada:

```
📁 INE_2024/
  📁 Configuracion/
    📄 Export_Alojamientos.xlsx (archivo maestro - guardar copia)
  📁 Semana_01_07_2024/
    📄 Export_Alojamientos.xlsx (copiado aquí)
    📄 INE-01_07_2024-Pays Arrivées.xlsx
    📄 INE-01_07_2024-Pays Occupation.xlsx
    📄 INE-01_07_2024-Régions Arrivées.xlsx
    📄 INE-01_07_2024-Régions Occupation.xlsx
    📄 INE-01_07_2024-Emplacements nus et locatifs Occupés.xlsx
    📄 Statistiques pour le mois de Juillet 2024.xlsx
  📁 Semana_08_07_2024/
    📄 Export_Alojamientos.xlsx (copiado aquí)
    📄 Todos los demás archivos de la semana...
  📁 Mensuales/
    📄 Statistiques pour le mois de Juillet 2024.xlsx
    📄 INE_Mensual_exportado.xlsx
```

⚠️ **RECUERDA**: El archivo `Export_Alojamientos.xlsx` DEBE estar en CADA carpeta semanal junto con los otros 6 archivos.

### Flujo de trabajo semanal:

1. **Crear** carpeta nueva para la semana
2. **Exportar** todos los archivos desde E-Season
3. **Copiar** Export_Alojamientos.xlsx
4. **Procesar** con INE Transformer
5. **Verificar** datos antes de enviar
6. **Guardar** copia del archivo enviado

### Verificaciones importantes:

- ✅ Fechas correctas en E-Season
- ✅ Todos los archivos en la misma carpeta
- ✅ No modificar nombres de archivos
- ✅ Revisar totales antes de exportar
- ✅ Guardar copia de lo enviado al INE

---

## 📁 ESTRUCTURA DE ARCHIVOS DEL PROGRAMA

### Archivos esenciales del sistema:

- `INE_4_e-season.exe` - Aplicación ejecutable
- `ine_app_v3.py` - Código fuente (si se ejecuta con Python)
- `historial_exportaciones.json` - Base de datos del historial
- `logo_ine.ico` - Icono de la aplicación

### Archivos generados:

- `INE_Completo_*.xlsx` - Cuestionarios semanales exportados
- `INE_Mensual_*.xlsx` - Cuestionarios mensuales exportados

---

## 📞 SOPORTE Y AYUDA

### En caso de problemas:

1. Verificar este manual
2. Comprobar que se siguen todos los pasos
3. Contactar a la direccion de correo darenas@capfun.com, y haré todo lo posible por ayudarte.

### Información técnica:

- Versión: 4.0
- Compatible con: E-Season PMS
- Requisitos: Windows 10 o superior
- Desarrollado para: Campings Capfun - España

---

*© 2024 - INE Transformer 4 E-Season*
*Desarrollado específicamente para el procesamiento de encuestas INE*
*en los campings de la cadena Capfun con E-Season PMS*
