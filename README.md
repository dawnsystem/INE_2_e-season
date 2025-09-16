# INE Transformer 4 E-Season 📊

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)
[![GitHub release](https://img.shields.io/github/release/dawnsystem/INE_2_e-season.svg)](https://GitHub.com/dawnsystem/INE_2_e-season/releases/)
[![GitHub issues](https://img.shields.io/github/issues/dawnsystem/INE_2_e-season.svg)](https://GitHub.com/dawnsystem/INE_2_e-season/issues/)
[![Build Status](https://github.com/dawnsystem/INE_2_e-season/workflows/Build%20and%20Release/badge.svg)](https://github.com/dawnsystem/INE_2_e-season/actions)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Sistema automatizado para procesar y transformar datos de E-Season PMS al formato requerido por el Instituto Nacional de Estadística (INE) de España.

## 🎯 Descripción

**INE Transformer 4 E-Season** es una aplicación desarrollada específicamente para campings que utilizan E-Season PMS y necesitan enviar encuestas periódicas al INE español. La aplicación automatiza completamente el proceso de transformación de datos, ahorrando tiempo y reduciendo errores.

### Características principales:

- ✅ Procesamiento automático de archivos Excel exportados desde E-Season
- ✅ Generación de cuestionarios semanales y mensuales
- ✅ Sistema de historial integrado
- ✅ Interfaz gráfica intuitiva
- ✅ Sin necesidad de instalación (versión ejecutable)

## 📸 Capturas de pantalla

#### Pantalla principal

![1758038381466](image/README/1758038381466.png)

#### Pantalla INE Mensual

![1758038623191](image/README/1758038623191.png)

#### Pantalla Historial

![1758038652143](image/README/1758038652143.png)

### Pantalla principal

La aplicación cuenta con una interfaz limpia dividida en pestañas para cada tipo de dato.

### Procesamiento de datos

Los datos se procesan automáticamente y se muestran organizados por categorías.


## 🚀 Inicio rápido

### Opción 1: Usar el ejecutable (Recomendado)

1. Descargar `INE_4_e-season.exe` desde [Releases](https://github.com/dawnsystem/INE_2_e-season/releases)
2. Ejecutar directamente (no requiere instalación)

### Opción 2: Ejecutar desde código fuente

```bash
# Clonar el repositorio
git clone https://github.com/dawnsystem/INE_2_e-season.git

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python ine_app_v3.py
```

## 📋 Requisitos

### Para el ejecutable:

- Windows 10 o superior
- 100 MB de espacio libre

### Para ejecutar desde código:

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.0.0

## 📖 Uso básico

### Cuestionario Semanal

1. Crear una carpeta para la semana
2. Exportar los 6 archivos desde E-Season (ver manual)
3. Copiar `Export_Alojamientos.xlsx` a la carpeta
4. Abrir INE Transformer y seleccionar la carpeta
5. Exportar los resultados

### Cuestionario Mensual

1. Exportar archivo de estadísticas mensuales desde E-Season
2. Cargar en INE Transformer
3. Exportar resultados

📚 **[Manual de Usuario Completo](docs/MANUAL_USUARIO_COMPLETO.md)** - Guía detallada paso a paso

## 🏗️ Compilar el ejecutable

Si deseas compilar tu propia versión del ejecutable:

```bash
# Windows
build_exe.bat
```

El ejecutable se generará en la carpeta `dist/`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Disclaimer

Este es un proyecto personal y no oficial. No está afiliado, asociado, autorizado, respaldado por, o de cualquier manera conectado oficialmente con el Instituto Nacional de Estadística (INE) de España, E-Season PMS, o Capfun.

Ver [DISCLAIMER.md](DISCLAIMER.md) para más información.

## 👨‍💻 Autor

**Dawnsystem - David Arenas**

- Email: darenas@capfun.com
- Desarrollado para: Campings Capfun España

## 🙏 Agradecimientos

- A todos los campings de la cadena Capfun que utilizan esta herramienta
- A la comunidad de Python por las excelentes librerías
- Al equipo de E-Season por su sistema PMS

---

*Si esta herramienta te ha sido útil, considera darle una ⭐ al repositorio*
