@echo off
echo.
echo ================================================
echo  QUICK START - MCP FILESYSTEM REFACTORED
echo ================================================
echo.

echo Este script instalara y probara el proyecto en 3 pasos.
echo.
echo Presiona cualquier tecla para continuar o Ctrl+C para salir...
pause > nul

echo.
echo [PASO 1/3] Instalando dependencias...
echo ================================================
echo.
call make.bat install-dev
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo OK - Dependencias instaladas correctamente
timeout /t 2 > nul

echo.
echo [PASO 2/3] Ejecutando tests...
echo ================================================
echo.
call make.bat test
if %errorlevel% neq 0 (
    echo.
    echo ADVERTENCIA: Algunos tests fallaron
    echo Esto puede ser normal si aun no has configurado todo
    timeout /t 3 > nul
) else (
    echo.
    echo OK - Todos los tests pasaron correctamente
    timeout /t 2 > nul
)

echo.
echo [PASO 3/3] Verificando configuracion...
echo ================================================
echo.

set CONFIG_PATH=%APPDATA%\Claude\claude_desktop_config.json

if exist "%CONFIG_PATH%" (
    echo OK - Archivo de configuracion de Claude encontrado
    echo.
    echo IMPORTANTE: Verifica que tu configuracion contenga:
    echo.
    echo {
    echo   "mcpServers": {
    echo     "filesystem-gitignore": {
    echo       "command": "python",
    echo       "args": ["-m", "mcp_filesystem"],
    echo       "env": {
    echo         "ALLOWED_DIRECTORIES": "C:\\DesarrolloPython;..."
    echo       }
    echo     }
    echo   }
    echo }
    echo.
) else (
    echo AVISO - Archivo de configuracion de Claude NO encontrado
    echo.
    echo Debes crear: %CONFIG_PATH%
    echo Con el contenido del ejemplo en README.md
    echo.
)

echo.
echo ================================================
echo  INSTALACION COMPLETADA
echo ================================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Si aun no lo hiciste, configura Claude Desktop:
echo    - Edita: %CONFIG_PATH%
echo    - Agrega la configuracion del servidor MCP
echo.
echo 2. Reinicia Claude Desktop completamente
echo.
echo 3. Prueba con Claude:
echo    "Lista los archivos en C:\DesarrolloPython"
echo.
echo 4. Lee la documentacion completa:
echo    - README.md
echo    - README_REFACTOR.md
echo    - RESUMEN_REFACTOR.md
echo.
echo ================================================
echo.
echo Comandos utiles disponibles:
echo.
echo   make.bat test            - Ejecutar tests
echo   make.bat test-cov        - Tests con coverage
echo   make.bat lint            - Verificar calidad
echo   make.bat format          - Formatear codigo
echo   make.bat clean           - Limpiar archivos
echo   make.bat help            - Ver todos los comandos
echo.
echo ================================================
echo.
echo OK - Tu proyecto esta listo para usarse
echo OK - Y listo para tu portfolio profesional
echo.
echo ================================================
pause
