# 🗂️ MCP Filesystem Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un servidor MCP (Model Context Protocol) profesional que proporciona operaciones de sistema de archivos mientras **respeta automáticamente los patrones de `.gitignore`**.

## 🎯 ¿Qué problema resuelve?

Cuando Claude trabaja con proyectos que tienen `venv/`, `node_modules/`, o `.git/`, intentar leer todo el directorio puede:
- ⚠️ **Agotar el límite de tokens** leyendo 50k+ archivos innecesarios
- ⏱️ **Ser extremadamente lento** al procesar directorios gigantes
- 🤯 **Ser confuso** mezclando código fuente con dependencias

**Este servidor resuelve eso** respetando `.gitignore` automáticamente, igual que Git. Claude solo ve lo que realmente importa: tu código.

## ✨ Características

- ✅ **Respeta `.gitignore` automáticamente**: Excluye `venv/`, `node_modules/`, `__pycache__/`, etc.
- ✅ **Optimizado para tokens**: Solo lee archivos relevantes de tu proyecto
- ✅ **Operaciones completas**: Leer, escribir, listar, buscar, y crear archivos/directorios
- ✅ **Seguridad por diseño**: Solo accede a directorios explícitamente permitidos
- ✅ **Caracteres especiales**: Maneja espacios, `#`, `@`, y otros caracteres en nombres
- ✅ **Cache inteligente**: Cachea patrones `.gitignore` con invalidación automática
- ✅ **Type-safe**: Completamente tipado con dataclasses y type hints
- ✅ **Production-ready**: Tests, logging, manejo de errores robusto

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Protocol Layer                       │
│  (server.py - Adaptador que traduce MCP ↔ FileSystemService)│
└────────────────────┬────────────────────────────────────────┘
                     │
┌───────────────────▼────────────────────────────────────────┐
│             Business Logic Layer                           │
│(filesystem_service.py - Orquesta validación + operaciones) │
└──────┬──────────────────────────────┬──────────────────────┘
       │                              │
       ▼                              ▼
┌──────────────────┐         ┌──────────────────────┐
│ Path Validation  │         │  .gitignore Manager  │
│ (path_validator) │         │  (ignore_manager)    │
│                  │         │                      │
│ - URL decoding   │         │ - Pattern matching   │
│ - Security check │         │ - Intelligent cache  │
└──────────────────┘         └──────────────────────┘
       │                              │
       └──────────────┬───────────────┘
                      │
       ┌──────────────▼──────────────────┐
       │    Data Access Layer            │
       │  (filesystem_operations.py)     │
       │                                 │
       │  - Pure I/O operations          │
       │  - No business logic            │
       └─────────────────────────────────┘
```

**Responsabilidades por capa:**

1. **MCP Protocol Layer** (`server.py`): 
   - Traduce requests MCP a llamadas del service
   - Serializa responses a JSON
   - Maneja el protocolo stdio

2. **Business Logic Layer** (`filesystem_service.py`):
   - Orquesta validación + filtering + operaciones
   - Punto de entrada público del sistema
   - Combina múltiples componentes para cada operación

3. **Support Components**:
   - `path_validator`: Normaliza y valida paths (seguridad)
   - `ignore_manager`: Cache y matching de `.gitignore`
   - `filesystem_operations`: I/O puro, sin lógica de negocio

4. **Foundation**:
   - `config.py`: Configuración centralizada
   - `errors.py`: Excepciones tipadas
   - `models.py`: Dataclasses para type safety

**Beneficios de esta arquitectura:**
- ✅ Cada capa es testeable independientemente
- ✅ Fácil cambiar implementación de una capa sin afectar otras
- ✅ Separación clara de responsabilidades
- ✅ Código reutilizable (el service puede usarse fuera de MCP)

## 📋 Requisitos

- Python 3.10+
- Claude Desktop o cualquier cliente MCP

## 🚀 Instalación Rápida

```bash
# 1. Clonar y navegar al proyecto
cd "C:\DesarrolloPython\MCP FileSystem"

# 2. Instalar dependencias de desarrollo
make.bat install-dev

# 3. Ejecutar tests para verificar
make.bat test
```

### Configurar Claude Desktop

Edita el archivo de configuración:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem-gitignore": {
      "command": "python",
      "args": [
        "-m",
        "mcp_filesystem"
      ],
      "env": {
        "ALLOWED_DIRECTORIES": "C:\\DesarrolloPython;C:\\MisProyectos"
      }
    }
  }
}
```

**Notas:**
- Usa paths absolutos
- Windows: separa directorios con `;`
- Unix/Mac: separa directorios con `:`

Reinicia Claude Desktop para aplicar cambios.

## 🔧 Uso

### Herramientas Disponibles

#### 1. `read_file` - Leer archivo de texto

```python
read_file(path="C:\\DesarrolloPython\\proyecto\\src\\main.py")
```

#### 2. `write_file` - Escribir archivo

```python
write_file(
    path="C:\\DesarrolloPython\\nuevo_archivo.py",
    content="print('Hello, World!')"
)
```

#### 3. `list_directory` - Listar contenido (no recursivo)

```python
# Por defecto respeta .gitignore
list_directory(path="C:\\DesarrolloPython\\proyecto")

# Forzar mostrar TODO (incluso venv)
list_directory(path="C:\\DesarrolloPython\\proyecto", respect_gitignore=False)
```

#### 4. `directory_tree` - Árbol recursivo

```python
directory_tree(
    path="C:\\DesarrolloPython\\proyecto",
    max_depth=5,
    respect_gitignore=True  # Default
)
```

#### 5. `search_files` - Buscar archivos

```python
search_files(
    path="C:\\DesarrolloPython",
    pattern="config",  # Case-insensitive
    respect_gitignore=True
)
```

#### 6. `get_file_info` - Información detallada

```python
get_file_info(path="C:\\DesarrolloPython\\proyecto\\README.md")
```

#### 7. `create_directory` - Crear directorio

```python
create_directory(path="C:\\DesarrolloPython\\nuevo_proyecto\\src")
```

## 📝 Decisiones de Diseño

### ¿Cómo se maneja `.gitignore`?

1. **Parseo con pathspec**: Usamos la librería `pathspec` que implementa el mismo algoritmo que Git
2. **Cache inteligente**: 
   - Cada `.gitignore` se parsea una sola vez y se cachea
   - El cache se invalida automáticamente cuando el `.gitignore` cambia (detecta por `mtime`)
   - Cache por directorio (cada dir tiene su propio `.gitignore`)
3. **Matching preciso**: 
   - Convierte paths a formato POSIX (forward slashes)
   - Agrega `/` al final de directorios (convención de Git)
   - Usa `gitwildmatch` para matching exacto

### ¿Cómo se optimiza el consumo de tokens?

1. **Filtrado temprano**: Los archivos ignorados ni siquiera se listan
2. **Control de profundidad**: `directory_tree` limita profundidad máxima (default: 5)
3. **Sin lectura de contenido**: Solo lista nombres, no lee contenidos
4. **Respeto opcional**: Todas las herramientas tienen `respect_gitignore` flag (default: `True`)

**Comparación:**

```python
# ❌ Sin .gitignore (50k+ archivos en venv):
directory_tree("C:\\proyecto")  # 🔥 Consume 100k+ tokens

# ✅ Con .gitignore (solo archivos de proyecto):
directory_tree("C:\\proyecto")  # ✅ ~2k tokens
```

### Seguridad: ¿Por qué directorios permitidos?

- Previene acceso a archivos sensibles del sistema
- Claude solo puede trabajar en tus proyectos
- Validación en cada operación (no se puede "escapar" con `../../../`)

## 🧪 Testing

```bash
# Ejecutar todos los tests
make.bat test

# Solo tests unitarios
make.bat test-unit

# Solo tests de integración
make.bat test-integration

# Con reporte de coverage
make.bat test-cov
```

## 🛠️ Desarrollo

```bash
# Formatear código
make.bat format

# Linters
make.bat lint

# Limpiar archivos generados
make.bat clean
```

## 🐛 Troubleshooting

### "ALLOWED_DIRECTORIES environment variable must be set"

**Solución:** Configura la variable de entorno en Claude Desktop config.

### "Access denied"

**Causa:** El path no está en `ALLOWED_DIRECTORIES`

**Solución:** Agrega el directorio a la lista.

### No respeta `.gitignore`

**Verifica:**
1. ¿Existe `.gitignore` en el directorio?
2. ¿Los patrones están bien escritos?
3. ¿Estás usando `respect_gitignore=True`? (es el default)

### Consume muchos tokens

**Solución:**
1. Crea/mejora tu `.gitignore`
2. Reduce `max_depth` en `directory_tree`

```gitignore
# .gitignore recomendado para Python:
venv/
env/
__pycache__/
*.pyc
.git/
.pytest_cache/
.mypy_cache/
htmlcov/
```

## 📚 Referencias

- [MCP Protocol Specification](https://github.com/modelcontextprotocol/specification)
- [pathspec library](https://pypi.org/project/pathspec/)
- [gitignore patterns](https://git-scm.com/docs/gitignore)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

**Antes de hacer PR:**
- ✅ Ejecuta `make.bat test` (todos los tests deben pasar)
- ✅ Ejecuta `make.bat lint` (sin warnings)
- ✅ Ejecuta `make.bat format` (código formateado)
- ✅ Agrega tests para nueva funcionalidad

## 📄 Licencia

MIT License - Úsalo libremente.

---

**Desarrollado con ❤️ para optimizar la interacción de Claude con proyectos reales**
