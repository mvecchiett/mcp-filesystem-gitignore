"""
High-level filesystem service.

Orchestrates path validation, .gitignore handling, and filesystem operations.
This is the main business logic layer.
"""

import logging
from pathlib import Path

from .config import Config
from .errors import NotADirectoryError, PathNotFoundError
from .filesystem_operations import FileSystemOperations
from .ignore_manager import IgnoreManager
from .models import (
    DirectoryItem,
    DirectoryListing,
    FileContent,
    FileInfo,
    OperationResult,
    SearchResults,
    TreeNode,
)
from .path_validator import PathValidator


logger = logging.getLogger(__name__)


class FileSystemService:
    """
    High-level filesystem service.
    
    This is the main public API that combines:
    - Path validation (security)
    - .gitignore handling (filtering)
    - Filesystem operations (I/O)
    
    All methods accept string paths and return typed models.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the filesystem service.
        
        Args:
            config: Configuration object with allowed directories.
        """
        self.config = config
        self.path_validator = PathValidator(config.allowed_directories)
        self.ignore_manager = IgnoreManager()
        self.fs_ops = FileSystemOperations(config)
        
        logger.info("=" * 60)
        logger.info("FileSystemService initialized")
        logger.info(f"Allowed directories: {len(config.allowed_directories)}")
        for directory in config.allowed_directories:
            logger.info(f"  - {directory}")
        logger.info("=" * 60)
    
    def read_file(self, path: str) -> FileContent:
        """
        Read a text file.
        
        Args:
            path: Path string to read.
            
        Returns:
            FileContent with content or error.
            
        Raises:
            PathNotAllowedError: If path is not allowed.
            PathNotFoundError: If file doesn't exist.
            NotAFileError: If path is not a file.
            FileReadError: If file cannot be read.
        """
        validated_path = self.path_validator.normalize_and_validate(path)
        return self.fs_ops.read_file(validated_path)
    
    def write_file(self, path: str, content: str) -> OperationResult:
        """
        Write content to a file.
        
        Args:
            path: Path string to write.
            content: Content to write.
            
        Returns:
            OperationResult with success status.
            
        Raises:
            PathNotAllowedError: If path is not allowed.
            FileWriteError: If file cannot be written.
        """
        validated_path = self.path_validator.normalize_and_validate(path)
        
        try:
            self.fs_ops.write_file(validated_path, content)
            return OperationResult(success=True, path=str(validated_path))
        except Exception as e:
            return OperationResult(success=False, path=str(validated_path), error=str(e))
    
    def list_directory(
        self,
        path: str,
        respect_gitignore: bool = True
    ) -> DirectoryListing:
        """
        List items in a directory (non-recursive).
        
        Args:
            path: Directory path string.
            respect_gitignore: Whether to filter by .gitignore patterns.
            
        Returns:
            DirectoryListing with items.
            
        Raises:
            PathNotAllowedError: If path is not allowed.
            PathNotFoundError: If directory doesn't exist.
            NotADirectoryError: If path is not a directory.
        """
        validated_path = self.path_validator.normalize_and_validate(path)
        
        # Create filter function if respecting .gitignore
        filter_fn = None
        if respect_gitignore:
            filter_fn = lambda p: not self.ignore_manager.should_ignore(p, validated_path)
        
        try:
            items = self.fs_ops.list_directory(validated_path, filter_fn)
            return DirectoryListing(items=items, total=len(items))
        except PermissionError as e:
            logger.error(f"Permission denied: {e}")
            return DirectoryListing(
                items=[],
                total=0,
                error=f"Permission denied: {str(e)}"
            )
    
    def directory_tree(
        self,
        path: str,
        max_depth: int | None = None,
        respect_gitignore: bool = True
    ) -> TreeNode:
        """
        Generate a recursive directory tree.
        
        Args:
            path: Directory path string.
            max_depth: Maximum depth to traverse (None for unlimited).
            respect_gitignore: Whether to filter by .gitignore patterns.
            
        Returns:
            TreeNode representing the tree structure.
            
        Raises:
            PathNotAllowedError: If path is not allowed.
            PathNotFoundError: If directory doesn't exist.
            NotADirectoryError: If path is not a directory.
        """
        validated_path = self.path_validator.normalize_and_validate(path)
        
        if not validated_path.exists():
            raise PathNotFoundError(str(validated_path))
        
        if not validated_path.is_dir():
            raise NotADirectoryError(str(validated_path))
        
        if max_depth is None:
            max_depth = self.config.DEFAULT_MAX_DEPTH
        
        def build_tree(current_path: Path, depth: int = 0) -> TreeNode:
            """Recursively build tree structure."""
            
            if depth > max_depth:
                return TreeNode(
                    name=current_path.name,
                    type="directory",
                    path=str(current_path),
                    truncated=True
                )
            
            node = TreeNode(
                name=current_path.name,
                type="directory" if current_path.is_dir() else "file",
                path=str(current_path)
            )
            
            if current_path.is_dir():
                try:
                    children = []
                    for item in sorted(current_path.iterdir()):
                        # Skip if should be ignored
                        if respect_gitignore and self.ignore_manager.should_ignore(
                            item, current_path
                        ):
                            continue
                        
                        children.append(build_tree(item, depth + 1))
                    
                    node.children = children
                    
                except PermissionError:
                    node.error = "Permission denied"
            
            return node
        
        tree = build_tree(validated_path)
        logger.info(f"Generated tree for: {validated_path}")
        return tree
    
    def search_files(
        self,
        path: str,
        pattern: str,
        respect_gitignore: bool = True
    ) -> SearchResults:
        """
        Search for files matching a pattern.
        
        Args:
            path: Base directory path string.
            pattern: Pattern to search for (case-insensitive).
            respect_gitignore: Whether to filter by .gitignore patterns.
            
        Returns:
            SearchResults with matching files.
            
        Raises:
            PathNotAllowedError: If path is not allowed.
            PathNotFoundError: If directory doesn't exist.
        """
        validated_path = self.path_validator.normalize_and_validate(path)
        
        # Create filter function if respecting .gitignore
        filter_fn = None
        if respect_gitignore:
            filter_fn = lambda p: not self.ignore_manager.should_ignore(p, validated_path)
        
        results = self.fs_ops.search_files(validated_path, pattern, filter_fn)
        return SearchResults(results=results, total=len(results))
    
    def get_file_info(self, path: str) -> FileInfo:
        """
        Get detailed information about a file or directory.
        
        Args:
            path: Path string to inspect.
            
        Returns:
            FileInfo with metadata.
            
        Raises:
            PathNotAllowedError: If path is not allowed.
            PathNotFoundError: If path doesn't exist.
        """
        validated_path = self.path_validator.normalize_and_validate(path)
        return self.fs_ops.get_file_info(validated_path)
    
    def create_directory(self, path: str) -> OperationResult:
        """
        Create a directory and its parents.
        
        Args:
            path: Directory path string to create.
            
        Returns:
            OperationResult with success status.
            
        Raises:
            PathNotAllowedError: If path is not allowed.
        """
        validated_path = self.path_validator.normalize_and_validate(path)
        
        try:
            self.fs_ops.create_directory(validated_path)
            return OperationResult(success=True, path=str(validated_path))
        except Exception as e:
            return OperationResult(success=False, path=str(validated_path), error=str(e))
