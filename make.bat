@echo off
REM MCP Filesystem - Comandos de desarrollo

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="test-unit" goto test-unit
if "%1"=="test-integration" goto test-integration
if "%1"=="test-cov" goto test-cov
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="clean" goto clean

:help
echo MCP Filesystem - Comandos disponibles:
echo.
echo   make.bat install          Instalar dependencias de produccion
echo   make.bat install-dev      Instalar dependencias de desarrollo
echo   make.bat test             Ejecutar todos los tests
echo   make.bat test-unit        Ejecutar solo tests unitarios
echo   make.bat test-integration Ejecutar solo tests de integracion
echo   make.bat test-cov         Ejecutar tests con coverage
echo   make.bat lint             Ejecutar linters (ruff, mypy)
echo   make.bat format           Formatear codigo con black
echo   make.bat clean            Limpiar archivos generados
echo.
goto end

:install
echo Instalando dependencias de produccion...
pip install -r requirements.txt
goto end

:install-dev
echo Instalando dependencias de desarrollo...
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
echo.
echo OK - Entorno de desarrollo listo
goto end

:test
echo Ejecutando todos los tests...
pytest tests/
goto end

:test-unit
echo Ejecutando tests unitarios...
pytest tests/unit/
goto end

:test-integration
echo Ejecutando tests de integracion...
pytest tests/integration/
goto end

:test-cov
echo Ejecutando tests con coverage...
pytest tests/ --cov=mcp_filesystem --cov-report=html --cov-report=term-missing
echo.
echo Reporte de coverage generado en htmlcov\index.html
goto end

:lint
echo Ejecutando linters...
ruff check mcp_filesystem tests
mypy mcp_filesystem
goto end

:format
echo Formateando codigo...
black mcp_filesystem tests
ruff check --fix mcp_filesystem tests
goto end

:clean
echo Limpiando archivos generados...
if exist __pycache__ rmdir /s /q __pycache__
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist .mypy_cache rmdir /s /q .mypy_cache
if exist .ruff_cache rmdir /s /q .ruff_cache
if exist htmlcov rmdir /s /q htmlcov
if exist .coverage del .coverage
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
echo OK - Limpieza completada
goto end

:end
