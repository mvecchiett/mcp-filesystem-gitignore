"""
MCP Server for filesystem operations.

This is a thin layer that translates MCP protocol to FileSystemService calls.
Business logic is in filesystem_service.py, not here.
"""

import asyncio
import json
import logging
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .config import Config
from .filesystem_service import FileSystemService


logger = logging.getLogger(__name__)

# MCP Server instance
app = Server("filesystem-gitignore")

# Service instance (initialized in main)
fs_service: FileSystemService | None = None


def model_to_dict(obj: Any) -> dict:
    """
    Convert a dataclass to a dict, handling nested structures.
    
    Args:
        obj: Object to convert (typically a dataclass).
        
    Returns:
        Dictionary representation.
    """
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field_name, field_value in obj.__dict__.items():
            if isinstance(field_value, list):
                result[field_name] = [model_to_dict(item) for item in field_value]
            else:
                result[field_name] = model_to_dict(field_value)
        return result
    else:
        return obj


@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available MCP tools."""
    return [
        types.Tool(
            name="read_file",
            description="Lee el contenido de un archivo de texto",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta absoluta del archivo a leer"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="write_file",
            description="Escribe contenido a un archivo",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta absoluta del archivo"
                    },
                    "content": {
                        "type": "string",
                        "description": "Contenido a escribir"
                    }
                },
                "required": ["path", "content"]
            }
        ),
        types.Tool(
            name="list_directory",
            description="Lista el contenido de un directorio (no recursivo). Respeta .gitignore por defecto.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta absoluta del directorio"
                    },
                    "respect_gitignore": {
                        "type": "boolean",
                        "description": "Si debe respetar .gitignore (default: true)",
                        "default": True
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="directory_tree",
            description="Genera un árbol recursivo del directorio. Respeta .gitignore por defecto (excluye venv, node_modules, etc).",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta absoluta del directorio"
                    },
                    "max_depth": {
                        "type": "integer",
                        "description": "Profundidad máxima del árbol (default: 5)",
                        "default": 5
                    },
                    "respect_gitignore": {
                        "type": "boolean",
                        "description": "Si debe respetar .gitignore (default: true)",
                        "default": True
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="search_files",
            description="Busca archivos por nombre. Respeta .gitignore por defecto.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directorio donde buscar"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Patrón a buscar (case-insensitive)"
                    },
                    "respect_gitignore": {
                        "type": "boolean",
                        "description": "Si debe respetar .gitignore (default: true)",
                        "default": True
                    }
                },
                "required": ["path", "pattern"]
            }
        ),
        types.Tool(
            name="get_file_info",
            description="Obtiene información detallada de un archivo o directorio",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta del archivo o directorio"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="create_directory",
            description="Crea un directorio (y sus padres si no existen)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta del directorio a crear"
                    }
                },
                "required": ["path"]
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle MCP tool calls.
    
    Translates MCP requests to FileSystemService calls.
    """
    if fs_service is None:
        raise RuntimeError("Filesystem service not initialized")
    
    try:
        result = None
        
        if name == "read_file":
            result = fs_service.read_file(arguments["path"])
        
        elif name == "write_file":
            result = fs_service.write_file(arguments["path"], arguments["content"])
        
        elif name == "list_directory":
            respect_gitignore = arguments.get("respect_gitignore", True)
            result = fs_service.list_directory(arguments["path"], respect_gitignore)
        
        elif name == "directory_tree":
            max_depth = arguments.get("max_depth", 5)
            respect_gitignore = arguments.get("respect_gitignore", True)
            result = fs_service.directory_tree(
                arguments["path"],
                max_depth,
                respect_gitignore
            )
        
        elif name == "search_files":
            respect_gitignore = arguments.get("respect_gitignore", True)
            result = fs_service.search_files(
                arguments["path"],
                arguments["pattern"],
                respect_gitignore
            )
        
        elif name == "get_file_info":
            result = fs_service.get_file_info(arguments["path"])
        
        elif name == "create_directory":
            result = fs_service.create_directory(arguments["path"])
        
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        # Convert dataclass to dict for JSON serialization
        result_dict = model_to_dict(result)
        
        return [types.TextContent(
            type="text",
            text=json.dumps(result_dict, indent=2, ensure_ascii=False)
        )]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
        )]


async def main():
    """Main entry point for the MCP server."""
    global fs_service
    
    try:
        # Load configuration
        config = Config()
        
        # Initialize service
        fs_service = FileSystemService(config)
        
        # Run MCP server
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=config.SERVER_NAME,
                    server_version=config.SERVER_VERSION,
                    capabilities=app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
    
    except Exception as e:
        logger.critical(f"Failed to start server: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
