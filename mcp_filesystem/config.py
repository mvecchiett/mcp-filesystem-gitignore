"""
Configuration management for the filesystem server.

Centralizes all configuration and constants in one place.
"""

import logging
import os
from pathlib import Path
from typing import ClassVar


class Config:
    """
    Configuration for the filesystem server.
    
    Loads settings from environment variables with sensible defaults.
    """
    
    # Default values
    DEFAULT_MAX_DEPTH: ClassVar[int] = 5
    DEFAULT_LOG_LEVEL: ClassVar[str] = "INFO"
    SERVER_NAME: ClassVar[str] = "filesystem-gitignore"
    SERVER_VERSION: ClassVar[str] = "2.0.0"
    
    # File encoding
    FILE_ENCODING: ClassVar[str] = "utf-8"
    FILE_ENCODING_ERRORS: ClassVar[str] = "replace"
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.allowed_directories = self._load_allowed_directories()
        self.log_level = self._load_log_level()
        self._setup_logging()
    
    def _load_allowed_directories(self) -> list[Path]:
        """
        Load and normalize allowed directories from ALLOWED_DIRECTORIES env var.
        
        Returns:
            List of resolved Path objects.
            
        Raises:
            ValueError: If ALLOWED_DIRECTORIES is not set or empty.
        """
        dirs_str = os.environ.get("ALLOWED_DIRECTORIES", "")
        
        if not dirs_str:
            raise ValueError(
                "ALLOWED_DIRECTORIES environment variable must be set. "
                "Example: ALLOWED_DIRECTORIES=C:\\Projects;C:\\Documents"
            )
        
        # Split by ; on Windows, : on Unix
        separator = ";" if os.name == "nt" else ":"
        dirs = [d.strip() for d in dirs_str.split(separator) if d.strip()]
        
        if not dirs:
            raise ValueError("ALLOWED_DIRECTORIES contains no valid directories")
        
        # Convert to Path objects and resolve
        resolved_dirs = []
        for dir_str in dirs:
            path = Path(dir_str).resolve()
            if not path.exists():
                logging.warning(f"Allowed directory does not exist: {path}")
            resolved_dirs.append(path)
        
        return resolved_dirs
    
    def _load_log_level(self) -> str:
        """Load log level from LOG_LEVEL env var."""
        level = os.environ.get("LOG_LEVEL", self.DEFAULT_LOG_LEVEL).upper()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        if level not in valid_levels:
            logging.warning(f"Invalid LOG_LEVEL '{level}', using INFO")
            return "INFO"
        
        return level
    
    def _setup_logging(self) -> None:
        """Configure logging with the specified level."""
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            force=True  # Override any existing config
        )
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger with the configured level.
        
        Args:
            name: Logger name (typically __name__ of the module).
            
        Returns:
            Configured logger instance.
        """
        return logging.getLogger(name)
