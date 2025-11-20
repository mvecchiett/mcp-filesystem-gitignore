"""
.gitignore pattern matching and caching.

Handles loading, caching, and matching of .gitignore patterns.
"""

import logging
from pathlib import Path
from typing import Optional

import pathspec


logger = logging.getLogger(__name__)


class IgnoreManager:
    """
    Manages .gitignore patterns with intelligent caching.
    
    Features:
    - Loads .gitignore files from directories
    - Caches PathSpec objects per directory
    - Invalidates cache when .gitignore is modified
    - Handles relative path matching
    """
    
    def __init__(self):
        """Initialize the ignore manager with an empty cache."""
        # Cache structure: {directory_path: (PathSpec, mtime)}
        self._cache: dict[str, tuple[pathspec.PathSpec, float]] = {}
    
    def should_ignore(self, path: Path, base_dir: Path) -> bool:
        """
        Check if a path should be ignored according to .gitignore.
        
        Args:
            path: Path to check (absolute).
            base_dir: Base directory containing .gitignore.
            
        Returns:
            True if the path should be ignored, False otherwise.
        """
        spec = self._get_gitignore_spec(base_dir)
        
        if spec is None:
            return False
        
        # Get relative path from base_dir
        try:
            relative_path = path.relative_to(base_dir)
        except ValueError:
            # Path is not relative to base_dir, don't ignore
            return False
        
        # Convert to POSIX format (forward slashes) - pathspec requirement
        relative_str = relative_path.as_posix()
        
        # Add trailing slash for directories (gitignore convention)
        if path.is_dir():
            relative_str += '/'
        
        return spec.match_file(relative_str)
    
    def _get_gitignore_spec(self, directory: Path) -> Optional[pathspec.PathSpec]:
        """
        Get or load the PathSpec for a directory's .gitignore.
        
        Uses cache if available and up-to-date.
        
        Args:
            directory: Directory containing .gitignore.
            
        Returns:
            PathSpec object or None if no .gitignore exists.
        """
        gitignore_path = directory / ".gitignore"
        cache_key = str(directory)
        
        # Check if .gitignore exists
        if not gitignore_path.exists():
            return None
        
        # Check cache
        current_mtime = gitignore_path.stat().st_mtime
        
        if cache_key in self._cache:
            cached_spec, cached_mtime = self._cache[cache_key]
            if current_mtime == cached_mtime:
                logger.debug(f"Using cached .gitignore for {directory}")
                return cached_spec
        
        # Load and cache
        try:
            spec = self._load_gitignore(gitignore_path)
            self._cache[cache_key] = (spec, current_mtime)
            logger.debug(f"Loaded .gitignore from {gitignore_path}")
            return spec
        except Exception as e:
            logger.error(f"Error loading .gitignore from {gitignore_path}: {e}")
            return None
    
    def _load_gitignore(self, gitignore_path: Path) -> pathspec.PathSpec:
        """
        Load a .gitignore file and create a PathSpec.
        
        Args:
            gitignore_path: Path to .gitignore file.
            
        Returns:
            PathSpec object for pattern matching.
            
        Raises:
            IOError: If file cannot be read.
        """
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            patterns = f.read().splitlines()
        
        return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
    
    def clear_cache(self) -> None:
        """Clear the entire .gitignore cache."""
        self._cache.clear()
        logger.info("Cleared .gitignore cache")
    
    def invalidate(self, directory: Path) -> None:
        """
        Invalidate cache for a specific directory.
        
        Args:
            directory: Directory whose cache should be invalidated.
        """
        cache_key = str(directory)
        if cache_key in self._cache:
            del self._cache[cache_key]
            logger.debug(f"Invalidated cache for {directory}")
