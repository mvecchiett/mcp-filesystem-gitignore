"""
Custom exceptions for the filesystem server.

All exceptions inherit from FileSystemError for easy catching.
"""


class FileSystemError(Exception):
    """Base exception for all filesystem operations."""
    
    def __init__(self, message: str, path: str | None = None):
        self.path = path
        super().__init__(message)


class PathNotAllowedError(FileSystemError):
    """Raised when trying to access a path outside allowed directories."""
    
    def __init__(self, path: str, allowed_dirs: list[str]):
        self.allowed_dirs = allowed_dirs
        message = (
            f"Access denied: '{path}' is not within allowed directories. "
            f"Allowed: {', '.join(allowed_dirs)}"
        )
        super().__init__(message, path)


class PathNotFoundError(FileSystemError):
    """Raised when a path does not exist."""
    
    def __init__(self, path: str):
        super().__init__(f"Path not found: '{path}'", path)


class NotAFileError(FileSystemError):
    """Raised when a path is expected to be a file but isn't."""
    
    def __init__(self, path: str):
        super().__init__(f"Not a file: '{path}'", path)


class NotADirectoryError(FileSystemError):
    """Raised when a path is expected to be a directory but isn't."""
    
    def __init__(self, path: str):
        super().__init__(f"Not a directory: '{path}'", path)


class FileReadError(FileSystemError):
    """Raised when a file cannot be read."""
    
    def __init__(self, path: str, reason: str):
        super().__init__(f"Cannot read file '{path}': {reason}", path)


class FileWriteError(FileSystemError):
    """Raised when a file cannot be written."""
    
    def __init__(self, path: str, reason: str):
        super().__init__(f"Cannot write file '{path}': {reason}", path)
