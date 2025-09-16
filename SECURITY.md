# 🛡️ Información de Seguridad - INE Transformer

## ⚠️ Falsos Positivos del Antivirus

Este ejecutable puede ser detectado como amenaza por algunos antivirus. **Esto es un FALSO POSITIVO** común con aplicaciones creadas con PyInstaller.

### Por qué ocurre esto:
1. PyInstaller es usado frecuentemente por malware, lo que causa detecciones genéricas
2. El ejecutable contiene un intérprete de Python completo
3. El código está empaquetado y comprimido
4. No está firmado digitalmente (aún)

## ✅ Verificación de Seguridad

### Opción 1: Verificar el Hash SHA256
Cada release incluye el hash SHA256 del ejecutable. Para verificarlo:

```powershell
# En PowerShell
Get-FileHash .\INE_4_e-season.exe -Algorithm SHA256
```

Compara el resultado con el hash publicado en la página de releases.

### Opción 2: Análisis en VirusTotal
1. Visita https://www.virustotal.com
2. Sube el archivo o busca el hash
3. Revisa los resultados (algunos falsos positivos son normales)

### Opción 3: Revisar el Código Fuente
Todo el código está disponible públicamente:
- https://github.com/dawnsystem/INE_2_e-season

## 🔧 Soluciones para Ejecutar la Aplicación

### Método 1: Añadir Excepción al Antivirus

#### Windows Defender:
1. Abre **Seguridad de Windows**
2. Ve a **Protección antivirus y contra amenazas**
3. En **Configuración de protección antivirus y contra amenazas**, haz clic en **Administrar configuración**
4. Baja hasta **Exclusiones** y haz clic en **Agregar o quitar exclusiones**
5. Haz clic en **Agregar una exclusión** > **Archivo**
6. Selecciona `INE_4_e-season.exe`

#### Otros Antivirus:
- **Avast**: Configuración > General > Exclusiones
- **AVG**: Configuración > Componentes > Excepciones
- **Kaspersky**: Configuración > Adicional > Amenazas y exclusiones
- **Norton**: Configuración > Antivirus > Exclusiones

### Método 2: Ejecutar desde Código Fuente (Más Seguro)
Si no confías en el ejecutable, puedes ejecutar desde el código:

```bash
# Clonar el repositorio
git clone https://github.com/dawnsystem/INE_2_e-season.git
cd INE_2_e-season

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python ine_app_v3.py
```

### Método 3: Usar el Instalador MSI (Próximamente)
Estamos trabajando en un instalador MSI que tiene menos problemas con antivirus.

## 🔐 Medidas de Seguridad Implementadas

1. **Código Abierto**: Todo el código es público y auditable
2. **Sin Conexión a Internet**: La aplicación funciona completamente offline
3. **Sin Recopilación de Datos**: No se envía ninguna información a servidores externos
4. **Procesamiento Local**: Todos los datos se procesan en tu ordenador
5. **Sin Permisos Especiales**: No requiere permisos de administrador

## 📝 Reportar Falsos Positivos

Ayúdanos reportando falsos positivos a los proveedores:

### Microsoft Defender:
1. Visita: https://www.microsoft.com/wdsi/submission
2. Selecciona "Software" como tipo de envío
3. Sube el archivo y marca como "Falso Positivo"

### VirusTotal:
1. Después de analizar en VirusTotal
2. Haz clic en "Community"
3. Comenta que es un falso positivo con enlace al repositorio

## 🚀 Mejoras Futuras

Estamos trabajando en:
- [ ] Certificado de firma digital (Code Signing)
- [ ] Instalador MSI certificado
- [ ] Versión Microsoft Store
- [ ] Builds reproducibles

## 💬 Soporte

Si tienes problemas:
1. Abre un issue en GitHub: https://github.com/dawnsystem/INE_2_e-season/issues
2. Contacta: darenas@capfun.com
3. Revisa el [Manual de Usuario](docs/MANUAL_USUARIO_COMPLETO.md)

## 📊 Estado de Detecciones

Última actualización: Diciembre 2024

| Antivirus | Estado | Notas |
|-----------|--------|-------|
| Windows Defender | ⚠️ Posible FP | Añadir excepción |
| Avast | ✅ OK | Sin problemas |
| AVG | ⚠️ Posible FP | Heurística genérica |
| Kaspersky | ✅ OK | Sin problemas |
| Norton | ⚠️ Posible FP | Reputación baja |

FP = Falso Positivo

---

**Recuerda**: Si el antivirus detecta el archivo, es un **FALSO POSITIVO**. El código es completamente seguro y está disponible para revisión pública.