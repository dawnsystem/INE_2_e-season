@echo off
echo ========================================
echo COMPILADOR MEJORADO INE_4_e-season v4.1
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    pause
    exit /b 1
)

:: Limpiar compilaciones anteriores
echo [1/7] Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist *.spec del *.spec

:: Instalar/actualizar dependencias
echo [2/7] Verificando dependencias...
pip install --upgrade pip >nul 2>&1
pip install --upgrade pyinstaller >nul 2>&1
pip install --upgrade -r requirements.txt >nul 2>&1

:: Crear información de versión
echo [3/7] Creando archivo de version...
(
echo VSVersionInfo^(
echo   ffi=FixedFileInfo^(
echo     filevers=^(4, 1, 0, 0^),
echo     prodvers=^(4, 1, 0, 0^),
echo     mask=0x3f,
echo     flags=0x0,
echo     OS=0x40004,
echo     fileType=0x1,
echo     subtype=0x0,
echo     date=^(0, 0^)
echo   ^),
echo   kids=[
echo     StringFileInfo^(
echo       [
echo         StringTable^(
echo           '040904B0',
echo           [
echo             StringStruct^('CompanyName', 'Capfun Spain'^),
echo             StringStruct^('FileDescription', 'INE Transformer para E-Season PMS'^),
echo             StringStruct^('FileVersion', '4.1.0.0'^),
echo             StringStruct^('InternalName', 'INE_4_e-season'^),
echo             StringStruct^('LegalCopyright', 'Copyright 2024 David Arenas - MIT License'^),
echo             StringStruct^('OriginalFilename', 'INE_4_e-season.exe'^),
echo             StringStruct^('ProductName', 'INE Transformer 4 E-Season'^),
echo             StringStruct^('ProductVersion', '4.1.0.0'^)
echo           ]
echo         ^)
echo       ]
echo     ^),
echo     VarFileInfo^([VarStruct^('Translation', [1033, 1200]^)]^)
echo   ]
echo ^)
) > version_info.txt

:: Compilar con PyInstaller
echo [4/7] Compilando ejecutable con PyInstaller...
pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name="INE_4_e-season" ^
    --icon="logo_ine.ico" ^
    --version-file="version_info.txt" ^
    --manifest="ine_app.manifest" ^
    --add-data="logo_ine.ico;." ^
    --add-data="logo_ine.png;." ^
    --hidden-import="tkinter" ^
    --hidden-import="pandas" ^
    --hidden-import="openpyxl" ^
    --hidden-import="PIL._tkinter_finder" ^
    --exclude-module="matplotlib" ^
    --exclude-module="numpy.random._examples" ^
    --exclude-module="scipy" ^
    --exclude-module="test" ^
    --exclude-module="unittest" ^
    --clean ^
    --log-level=WARN ^
    ine_app_v3.py

:: Verificar compilación
if not exist "dist\INE_4_e-season.exe" (
    echo.
    echo ERROR: La compilacion ha fallado
    pause
    exit /b 1
)

:: Calcular hash SHA256
echo [5/7] Calculando hash SHA256...
for /f "tokens=1" %%A in ('certutil -hashfile "dist\INE_4_e-season.exe" SHA256 ^| findstr /v ":"') do (
    set SHA256=%%A
    goto :gotSHA
)
:gotSHA
echo SHA256: %SHA256%
echo %SHA256% > dist\INE_4_e-season.exe.sha256

:: Crear archivo de información
echo [6/7] Creando archivo de informacion...
(
echo INE Transformer 4 E-Season
echo Version: 4.1
echo Compilado: %date% %time%
echo SHA256: %SHA256%
echo.
echo Si tu antivirus detecta este archivo como amenaza:
echo 1. Es un FALSO POSITIVO
echo 2. Agrega el archivo a las exclusiones
echo 3. O ejecuta desde el codigo fuente
echo.
echo Mas informacion: https://github.com/dawnsystem/INE_2_e-season
) > dist\README.txt

:: Limpiar archivos temporales
echo [7/7] Limpiando archivos temporales...
if exist version_info.txt del version_info.txt
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: Resultado final
echo.
echo ========================================
echo COMPILACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Archivo generado: dist\INE_4_e-season.exe
echo SHA256: %SHA256%
echo.
echo IMPORTANTE:
echo - El ejecutable puede ser detectado como falso positivo
echo - Lee SECURITY.md para mas informacion
echo - Considera firmar digitalmente el ejecutable
echo.
echo Presiona cualquier tecla para abrir la carpeta dist...
pause >nul
explorer dist