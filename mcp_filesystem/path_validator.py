"""
Path validation and normalization.

Handles URL decoding, path resolution, and security checks.
"""

import urllib.parse
from pathlib import Path
from typing import Protocol

from .errors import PathNotAllowedError


class PathValidator:
    """
    Validates and normalizes file paths.
    
    Ensures paths are:
    1. Properly decoded (handles URL encoding like %20)
    2. Absolute and resolved
    3. Within allowed directories
    """
    
    def __init__(self, allowed_directories: list[Path]):
        """
        Initialize the path validator.
        
        Args:
            allowed_directories: List of allowed base directories.
        """
        self.allowed_directories = allowed_directories
    
    def normalize(self, path_str: str) -> Path:
        """
        Normalize a path string to an absolute Path object.
        
        Handles:
        - URL encoding (e.g., %20 -> space)
        - Relative paths
        - Special characters (#, @, spaces, etc.)
        
        Args:
            path_str: Path string to normalize.
            
        Returns:
            Absolute, resolved Path object.
        """
        # Decode URL encoding if present
        decoded = urllib.parse.unquote(path_str)
        
        # Convert to Path and resolve to absolute
        return Path(decoded).resolve()
    
    def validate(self, path: Path) -> None:
        """
        Validate that a path is within allowed directories.
        
        Args:
            path: Path to validate (should be normalized first).
            
        Raises:
            PathNotAllowedError: If path is not within allowed directories.
        """
        path_resolved = path.resolve()
        
        is_allowed = any(
            path_resolved == allowed_dir or allowed_dir in path_resolved.parents
            for allowed_dir in self.allowed_directories
        )
        
        if not is_allowed:
            raise PathNotAllowedError(
                str(path),
                [str(d) for d in self.allowed_directories]
            )
    
    def normalize_and_validate(self, path_str: str) -> Path:
        """
        Normalize and validate a path in one step.
        
        Args:
            path_str: Path string to process.
            
        Returns:
            Normalized and validated Path.
            
        Raises:
            PathNotAllowedError: If path is not within allowed directories.
        """
        normalized = self.normalize(path_str)
        self.validate(normalized)
        return normalized
