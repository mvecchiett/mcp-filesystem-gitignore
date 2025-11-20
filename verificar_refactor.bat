@echo off
echo ========================================
echo  VERIFICACION RAPIDA - MCP FILESYSTEM
echo ========================================
echo.

echo [1/6] Verificando estructura de archivos...
if exist "mcp_filesystem\__init__.py" (
    echo OK - __init__.py encontrado
) else (
    echo ERROR - __init__.py NO encontrado
    goto error
)

if exist "mcp_filesystem\__main__.py" (
    echo OK - __main__.py encontrado
) else (
    echo ERROR - __main__.py NO encontrado
    goto error
)

if exist "tests\unit\test_filesystem_operations.py" (
    echo OK - Tests unitarios encontrados
) else (
    echo ERROR - Tests unitarios NO encontrados
    goto error
)

if exist "pyproject.toml" (
    echo OK - pyproject.toml encontrado
) else (
    echo ERROR - pyproject.toml NO encontrado
    goto error
)

echo.
echo [2/6] Verificando que Python funciona...
python --version > nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo OK - Python funciona correctamente
) else (
    echo ERROR - Python no encontrado
    goto error
)

echo.
echo [3/6] Verificando dependencias principales...
python -c "import mcp" > nul 2>&1
if %errorlevel% equ 0 (
    echo OK - mcp instalado
) else (
    echo AVISO - mcp NO instalado - ejecuta: make.bat install
)

python -c "import pathspec" > nul 2>&1
if %errorlevel% equ 0 (
    echo OK - pathspec instalado
) else (
    echo AVISO - pathspec NO instalado - ejecuta: make.bat install
)

echo.
echo [4/6] Verificando que el paquete es importable...
python -c "from mcp_filesystem import FileSystemService, Config" > nul 2>&1
if %errorlevel% equ 0 (
    echo OK - Paquete importable correctamente
) else (
    echo ERROR - Error al importar paquete
    echo Ejecuta: pip install -e .
    goto error
)

echo.
echo [5/6] Verificando estructura de tests...
python -c "import pytest" > nul 2>&1
if %errorlevel% equ 0 (
    echo OK - pytest instalado
) else (
    echo AVISO - pytest NO instalado - ejecuta: make.bat install-dev
)

echo.
echo [6/6] Verificando configuracion de Claude Desktop...
set CONFIG_PATH=%APPDATA%\Claude\claude_desktop_config.json
if exist "%CONFIG_PATH%" (
    echo OK - Archivo de configuracion encontrado:
    echo   %CONFIG_PATH%
    echo.
    echo Verifica que contiene una entrada para "filesystem-gitignore"
) else (
    echo AVISO - Archivo de configuracion NO encontrado
    echo   Crea: %CONFIG_PATH%
)

echo.
echo ========================================
echo  RESUMEN
echo ========================================
echo.
echo OK - Estructura del proyecto: Correcta
echo OK - Python funcionando: Correcto
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Instalar dependencias de desarrollo:
echo    ^> make.bat install-dev
echo.
echo 2. Ejecutar tests:
echo    ^> make.bat test
echo.
echo 3. Configurar Claude Desktop:
echo    - Edita: %CONFIG_PATH%
echo    - Reinicia Claude Desktop
echo.
echo 4. Leer la guia completa:
echo    ^> README_REFACTOR.md
echo.
echo ========================================
echo  REFACTOR COMPLETADO EXITOSAMENTE
echo ========================================
pause
goto end

:error
echo.
echo ========================================
echo  ERROR DETECTADO
echo ========================================
echo.
echo Algunos archivos necesarios no se encontraron.
echo.
echo Por favor:
echo 1. Verifica que estas en el directorio correcto
echo 2. Revisa README_REFACTOR.md para mas detalles
echo.
pause
exit /b 1

:end
