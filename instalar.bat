@echo off
REM ============================================
REM  INICIO RAPIDO - MCP FILESYSTEM v2.0
REM ============================================

echo.
echo ============================================
echo  INICIO RAPIDO - MCP FILESYSTEM v2.0
echo ============================================
echo.
echo Este script te guiara en 3 pasos simples
echo.
pause

REM PASO 1: Instalar dependencias
echo.
echo ============================================
echo  PASO 1: Instalando dependencias
echo ============================================
echo.
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias
    echo Verifica que pip funcione correctamente
    pause
    exit /b 1
)

echo.
echo OK - Dependencias instaladas

REM PASO 2: Ejecutar tests
echo.
echo ============================================
echo  PASO 2: Ejecutando tests
echo ============================================
echo.
pytest tests/ -v

echo.
echo Presiona cualquier tecla para continuar...
pause > nul

REM PASO 3: Informacion de configuracion
echo.
echo ============================================
echo  PASO 3: Configurar Claude Desktop
echo ============================================
echo.
echo Para usar el servidor MCP con Claude Desktop:
echo.
echo 1. Edita este archivo:
echo    %APPDATA%\Claude\claude_desktop_config.json
echo.
echo 2. Agrega esta configuracion:
echo.
echo    {
echo      "mcpServers": {
echo        "filesystem-gitignore": {
echo          "command": "python",
echo          "args": ["-m", "mcp_filesystem"],
echo          "env": {
echo            "ALLOWED_DIRECTORIES": "C:\\DesarrolloPython;C:\\TusProyectos"
echo          }
echo        }
echo      }
echo    }
echo.
echo 3. Reinicia Claude Desktop completamente
echo.
echo 4. Prueba preguntando a Claude:
echo    "Lista los archivos en C:\DesarrolloPython"
echo.
echo ============================================
echo  INSTALACION COMPLETADA
echo ============================================
echo.
echo Tu proyecto esta listo para:
echo  - Usarse con Claude Desktop
echo  - Mostrarse en tu portfolio
echo  - Extenderse con nuevas features
echo.
echo Comandos utiles:
echo   python -m mcp_filesystem     Ejecutar servidor
echo   pytest tests/                Ejecutar tests
echo   pytest tests/ --cov          Tests con coverage
echo.
echo Lee README.md para mas detalles
echo.
pause
