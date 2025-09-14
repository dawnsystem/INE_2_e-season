@echo off
echo ================================================
echo    INE_4_e-season - Compilador de Ejecutable
echo    Para Campings Capfun con E-Season
echo ================================================
echo.

echo [1/5] Limpiando compilaciones anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
echo     [OK] Limpieza completada

echo.
echo [2/5] Verificando icono...
if not exist logo_ine.ico (
    echo     [ERROR] No se encontro logo_ine.ico
    echo     Ejecutando conversion de PNG a ICO...
    python convert_to_ico.py
)
echo     [OK] Icono disponible

echo.
echo [3/5] Instalando dependencias...
pip install -q pandas openpyxl pyinstaller
echo     [OK] Dependencias instaladas

echo.
echo [4/5] Compilando ejecutable...
echo     Esto puede tomar varios minutos...
pyinstaller --onefile --windowed --icon=logo_ine.ico --name="INE_4_e-season" ine_app_v3.py
echo     [OK] Compilacion completada

echo.
echo [5/5] Verificando resultado...
if exist "dist\INE_4_e-season.exe" (
    echo     [OK] Ejecutable creado exitosamente
    echo.
    echo ================================================
    echo    COMPILACION EXITOSA
    echo ================================================
    echo.
    echo El ejecutable se encuentra en: dist\INE_4_e-season.exe
    echo Tamano del archivo: 
    for %%A in ("dist\INE_4_e-season.exe") do echo     %%~zA bytes
    echo.
    echo Puede enviar este archivo a sus companeros de Capfun
) else (
    echo     [ERROR] No se pudo crear el ejecutable
    echo     Revise los mensajes de error anteriores
)

echo.
pause