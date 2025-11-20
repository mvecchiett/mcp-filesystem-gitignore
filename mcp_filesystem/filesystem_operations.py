"""
Low-level filesystem operations.

Pure I/O functions without business logic - easily testable and reusable.
"""

import logging
import os
from pathlib import Path
from typing import Callable

from .config import Config
from .errors import (
    FileReadError,
    FileWriteError,
    NotADirectoryError,
    NotAFileError,
    PathNotFoundError,
)
from .models import DirectoryItem, FileContent, FileInfo, SearchResult


logger = logging.getLogger(__name__)


class FileSystemOperations:
    """
    Low-level filesystem operations.
    
    All methods assume paths are already validated.
    No .gitignore logic here - that's handled by FileSystemService.
    """
    
    def __init__(self, config: Config):
        """
        Initialize filesystem operations.
        
        Args:
            config: Configuration object for encoding settings.
        """
        self.config = config
    
    def read_file(self, path: Path) -> FileContent:
        """
        Read the contents of a text file.
        
        Args:
            path: Validated path to read.
            
        Returns:
            FileContent with content or error.
            
        Raises:
            PathNotFoundError: If file doesn't exist.
            NotAFileError: If path is not a file.
            FileReadError: If file cannot be read.
        """
        if not path.exists():
            raise PathNotFoundError(str(path))
        
        if not path.is_file():
            raise NotAFileError(str(path))
        
        try:
            with open(
                path,
                'r',
                encoding=self.config.FILE_ENCODING,
                errors=self.config.FILE_ENCODING_ERRORS
            ) as f:
                content = f.read()
            
            logger.info(f"Read file: {path}")
            return FileContent(content=content)
            
        except Exception as e:
            logger.error(f"Error reading file {path}: {e}")
            raise FileReadError(str(path), str(e))
    
    def write_file(self, path: Path, content: str) -> None:
        """
        Write content to a file, creating parent directories if needed.
        
        Args:
            path: Validated path to write.
            content: Content to write.
            
        Raises:
            FileWriteError: If file cannot be written.
        """
        try:
            # Create parent directories
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding=self.config.FILE_ENCODING) as f:
                f.write(content)
            
            logger.info(f"Wrote file: {path} ({len(content)} chars)")
            
        except Exception as e:
            logger.error(f"Error writing file {path}: {e}")
            raise FileWriteError(str(path), str(e))
    
    def list_directory(
        self,
        path: Path,
        filter_fn: Callable[[Path], bool] | None = None
    ) -> list[DirectoryItem]:
        """
        List items in a directory (non-recursive).
        
        Args:
            path: Validated directory path.
            filter_fn: Optional function to filter items (return True to include).
            
        Returns:
            List of DirectoryItem objects.
            
        Raises:
            PathNotFoundError: If directory doesn't exist.
            NotADirectoryError: If path is not a directory.
        """
        if not path.exists():
            raise PathNotFoundError(str(path))
        
        if not path.is_dir():
            raise NotADirectoryError(str(path))
        
        items = []
        
        try:
            for item in sorted(path.iterdir()):
                # Apply filter if provided
                if filter_fn and not filter_fn(item):
                    continue
                
                item_type = "directory" if item.is_dir() else "file"
                items.append(DirectoryItem(
                    name=item.name,
                    type=item_type,
                    path=str(item)
                ))
            
            logger.debug(f"Listed directory: {path} ({len(items)} items)")
            return items
            
        except PermissionError as e:
            logger.error(f"Permission denied accessing {path}: {e}")
            return []
    
    def get_file_info(self, path: Path) -> FileInfo:
        """
        Get detailed information about a file or directory.
        
        Args:
            path: Validated path to inspect.
            
        Returns:
            FileInfo object with metadata.
            
        Raises:
            PathNotFoundError: If path doesn't exist.
        """
        if not path.exists():
            raise PathNotFoundError(str(path))
        
        stat = path.stat()
        
        info = FileInfo(
            name=path.name,
            path=str(path),
            type="directory" if path.is_dir() else "file",
            size=stat.st_size,
            created=stat.st_ctime,
            modified=stat.st_mtime,
            is_symlink=path.is_symlink()
        )
        
        logger.debug(f"Got info for: {path}")
        return info
    
    def create_directory(self, path: Path) -> None:
        """
        Create a directory and its parents if they don't exist.
        
        Args:
            path: Validated path to create.
            
        Raises:
            FileWriteError: If directory cannot be created.
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            raise FileWriteError(str(path), str(e))
    
    def search_files(
        self,
        base_path: Path,
        pattern: str,
        filter_fn: Callable[[Path], bool] | None = None
    ) -> list[SearchResult]:
        """
        Search for files matching a pattern (case-insensitive).
        
        Args:
            base_path: Directory to search in.
            pattern: Pattern to search for in filenames.
            filter_fn: Optional function to filter paths (return True to include).
            
        Returns:
            List of SearchResult objects.
            
        Raises:
            PathNotFoundError: If base_path doesn't exist.
        """
        if not base_path.exists():
            raise PathNotFoundError(str(base_path))
        
        pattern_lower = pattern.lower()
        results = []
        
        try:
            for root, dirs, files in os.walk(base_path):
                root_path = Path(root)
                
                # Filter directories if filter_fn provided
                if filter_fn:
                    dirs[:] = [
                        d for d in dirs
                        if filter_fn(root_path / d)
                    ]
                
                # Search in files
                for file in files:
                    file_path = root_path / file
                    
                    # Apply filter
                    if filter_fn and not filter_fn(file_path):
                        continue
                    
                    if pattern_lower in file.lower():
                        results.append(SearchResult(
                            name=file,
                            path=str(file_path),
                            directory=str(root_path)
                        ))
            
            logger.info(f"Search in {base_path} for '{pattern}': {len(results)} results")
            return results
            
        except PermissionError as e:
            logger.error(f"Permission error during search in {base_path}: {e}")
            return results
