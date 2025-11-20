"""
MCP Filesystem Server - Public API

A Model Context Protocol server that provides filesystem operations
while respecting .gitignore patterns automatically.
"""

__version__ = "2.0.0"

from .config import Config
from .errors import (
    FileSystemError,
    PathNotAllowedError,
    PathNotFoundError,
    NotAFileError,
    NotADirectoryError,
    FileReadError,
    FileWriteError,
)
from .filesystem_service import FileSystemService
from .ignore_manager import IgnoreManager
from .models import (
    DirectoryItem,
    DirectoryListing,
    FileContent,
    FileInfo,
    OperationResult,
    SearchResult,
    SearchResults,
    TreeNode,
)
from .path_validator import PathValidator

__all__ = [
    # Core
    "Config",
    "FileSystemService",
    "IgnoreManager",
    "PathValidator",
    # Errors
    "FileSystemError",
    "PathNotAllowedError",
    "PathNotFoundError",
    "NotAFileError",
    "NotADirectoryError",
    "FileReadError",
    "FileWriteError",
    # Models
    "DirectoryItem",
    "DirectoryListing",
    "FileContent",
    "FileInfo",
    "OperationResult",
    "SearchResult",
    "SearchResults",
    "TreeNode",
]
