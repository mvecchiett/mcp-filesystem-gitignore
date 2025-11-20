# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [2.0.0] - 2024-11-19

### 🎉 Refactor Arquitectónico Mayor - Portfolio Profesional

**BREAKING CHANGES:**
- Reorganización completa del proyecto para portfolio profesional
- Ahora ejecutable como paquete Python: `python -m mcp_filesystem`
- Configuración moderna con `pyproject.toml`

### ✨ Agregado

**Arquitectura:**
- ✅ Arquitectura por capas claramente definida (Protocol → Service → Operations)
- ✅ `mcp_filesystem/__init__.py` con API pública exportada
- ✅ `mcp_filesystem/__main__.py` para ejecución como módulo
- ✅ Suite de tests organizada (`tests/unit/` + `tests/integration/`)

**Tooling:**
- ✅ `make.bat` con comandos comunes (install, test, lint, format)
- ✅ `pyproject.toml` para configuración moderna
- ✅ `requirements-dev.txt` con dependencias de desarrollo
- ✅ Soporte para black, ruff, mypy
- ✅ Coverage reports con pytest-cov

**Testing:**
- ✅ Tests unitarios exhaustivos para cada componente
- ✅ Tests de integración para flujos completos
- ✅ Tests específicos para caracteres especiales mejorados
- ✅ Fixtures compartidas en conftest.py
- ✅ Parametrized tests para casos múltiples

**Documentación:**
- ✅ README.md mejorado con arquitectura visual
- ✅ Sección "Decisiones de Diseño" explicando .gitignore y optimización de tokens
- ✅ Ejemplos de uso para cada herramienta
- ✅ Troubleshooting extendido
- ✅ Guías de contribución

### 🔄 Cambiado

- Consolidación de múltiples versiones del servidor en una sola
- Mejora en la organización de módulos (separación clara de responsabilidades)
- Logging más estructurado y útil para debugging
- Type hints completos en todos los módulos
- Documentación inline mejorada

### 🐛 Corregido

- Manejo más robusto de errores de permisos
- Mejor detección de cambios en .gitignore (invalidación de cache)
- Edge cases en path normalization

### 📊 Métricas del Refactor

- **Archivos de código eliminados**: 3 (server_backup.py, server_improved.py, server_refactored.py)
- **Tests agregados**: 40+ nuevos tests
- **Cobertura de código**: >85%
- **Documentación**: +200% más extensa
- **Tiempo de instalación**: <2 minutos con `make.bat install-dev`

---

## [1.0.0] - 2024-01-17

### ✨ Agregado

- ✨ Servidor MCP inicial con soporte completo para .gitignore
- 📁 Herramientas de filesystem básicas:
  - `read_file`: Leer archivos de texto
  - `write_file`: Escribir archivos
  - `list_directory`: Listar contenido de directorios
  - `directory_tree`: Generar árbol recursivo de directorios
  - `search_files`: Buscar archivos por nombre
  - `get_file_info`: Obtener información detallada de archivos
  - `create_directory`: Crear directorios
- 🚫 Respeto automático de patrones .gitignore usando pathspec
- 💾 Sistema de caché para .gitignore (mejora rendimiento)
- 🔒 Seguridad basada en directorios permitidos
- 📝 Documentación completa en README.md
- 🧪 Suite de tests (test_server.py)
- 🛠️ Scripts de instalación y configuración

### Características destacadas

- Evita agotamiento de tokens ignorando venv/, node_modules/, etc.
- Compatible con cualquier proyecto que use .gitignore
- Parámetro opcional `respect_gitignore` en todas las herramientas relevantes
- Caché inteligente de .gitignore por directorio

### Notas de implementación

- Usa pathspec library para matching exacto de patrones Git
- Implementa stdio protocol para MCP
- Maneja errores de permisos y archivos binarios
- Logging configurable

---

## [Unreleased] - Ideas para futuras versiones

### Considerado para v2.1

- [ ] Soporte para múltiples archivos .gitignore en jerarquía
- [ ] Estadísticas de archivos ignorados
- [ ] Herramienta de diff entre archivos
- [ ] Modo "dry-run" para operaciones de escritura
- [ ] Watch mode para detectar cambios en .gitignore

### Considerado para v3.0

- [ ] Soporte para .git/info/exclude
- [ ] Integración con Git para ver archivos tracked/untracked
- [ ] Compresión/descompresión de archivos
- [ ] Soporte para archivos binarios (base64 encoding)
- [ ] Plugin system para extensiones customizadas
