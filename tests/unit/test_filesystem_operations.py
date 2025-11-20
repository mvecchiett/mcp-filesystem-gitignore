"""
Unit tests for filesystem_operations module.

Tests low-level I/O operations in isolation.
"""

import pytest
from pathlib import Path

from mcp_filesystem.config import Config
from mcp_filesystem.errors import (
    PathNotFoundError,
    NotAFileError,
    NotADirectoryError,
    FileReadError,
    FileWriteError,
)
from mcp_filesystem.filesystem_operations import FileSystemOperations
from mcp_filesystem.models import DirectoryItem, FileContent, FileInfo


class TestFileSystemOperations:
    """Test FileSystemOperations class."""
    
    def test_read_existing_file(self, test_config, sample_files):
        """Test reading an existing text file."""
        fs_ops = FileSystemOperations(test_config)
        file_path = sample_files / "README.md"
        
        result = fs_ops.read_file(file_path)
        
        assert isinstance(result, FileContent)
        assert result.content == "# Test Project"
        assert result.error is None
    
    def test_read_nonexistent_file(self, test_config, temp_dir):
        """Test reading a file that doesn't exist."""
        fs_ops = FileSystemOperations(test_config)
        file_path = temp_dir / "nonexistent.txt"
        
        with pytest.raises(PathNotFoundError):
            fs_ops.read_file(file_path)
    
    def test_read_directory_as_file(self, test_config, sample_files):
        """Test attempting to read a directory as a file."""
        fs_ops = FileSystemOperations(test_config)
        dir_path = sample_files / "src"
        
        with pytest.raises(NotAFileError):
            fs_ops.read_file(dir_path)
    
    def test_write_new_file(self, test_config, temp_dir):
        """Test writing content to a new file."""
        fs_ops = FileSystemOperations(test_config)
        file_path = temp_dir / "new_file.txt"
        content = "Hello, World!"
        
        fs_ops.write_file(file_path, content)
        
        assert file_path.exists()
        assert file_path.read_text() == content
    
    def test_write_file_creates_parent_dirs(self, test_config, temp_dir):
        """Test that writing creates parent directories."""
        fs_ops = FileSystemOperations(test_config)
        file_path = temp_dir / "nested" / "deep" / "file.txt"
        
        fs_ops.write_file(file_path, "content")
        
        assert file_path.exists()
        assert file_path.parent.parent.exists()
    
    def test_list_directory(self, test_config, sample_files):
        """Test listing directory contents."""
        fs_ops = FileSystemOperations(test_config)
        
        items = fs_ops.list_directory(sample_files)
        
        assert len(items) > 0
        assert all(isinstance(item, DirectoryItem) for item in items)
        
        # Check that we have expected items
        names = [item.name for item in items]
        assert "README.md" in names
        assert "src" in names
    
    def test_list_directory_with_filter(self, test_config, sample_files):
        """Test listing directory with a filter function."""
        fs_ops = FileSystemOperations(test_config)
        
        # Filter to only show .md files
        filter_fn = lambda p: p.suffix == ".md"
        items = fs_ops.list_directory(sample_files, filter_fn)
        
        assert len(items) == 1
        assert items[0].name == "README.md"
    
    def test_list_nonexistent_directory(self, test_config, temp_dir):
        """Test listing a directory that doesn't exist."""
        fs_ops = FileSystemOperations(test_config)
        dir_path = temp_dir / "nonexistent"
        
        with pytest.raises(PathNotFoundError):
            fs_ops.list_directory(dir_path)
    
    def test_list_file_as_directory(self, test_config, sample_files):
        """Test attempting to list a file as a directory."""
        fs_ops = FileSystemOperations(test_config)
        file_path = sample_files / "README.md"
        
        with pytest.raises(NotADirectoryError):
            fs_ops.list_directory(file_path)
    
    def test_get_file_info(self, test_config, sample_files):
        """Test getting file information."""
        fs_ops = FileSystemOperations(test_config)
        file_path = sample_files / "README.md"
        
        info = fs_ops.get_file_info(file_path)
        
        assert isinstance(info, FileInfo)
        assert info.name == "README.md"
        assert info.type == "file"
        assert info.size > 0
        assert info.created > 0
        assert info.modified > 0
    
    def test_get_directory_info(self, test_config, sample_files):
        """Test getting directory information."""
        fs_ops = FileSystemOperations(test_config)
        dir_path = sample_files / "src"
        
        info = fs_ops.get_file_info(dir_path)
        
        assert info.type == "directory"
        assert info.name == "src"
    
    def test_create_directory(self, test_config, temp_dir):
        """Test creating a new directory."""
        fs_ops = FileSystemOperations(test_config)
        new_dir = temp_dir / "new_directory"
        
        fs_ops.create_directory(new_dir)
        
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_create_nested_directories(self, test_config, temp_dir):
        """Test creating nested directories."""
        fs_ops = FileSystemOperations(test_config)
        nested_dir = temp_dir / "level1" / "level2" / "level3"
        
        fs_ops.create_directory(nested_dir)
        
        assert nested_dir.exists()
        assert nested_dir.is_dir()
    
    def test_search_files_basic(self, test_config, sample_files):
        """Test basic file search."""
        fs_ops = FileSystemOperations(test_config)
        
        results = fs_ops.search_files(sample_files, "main")
        
        assert len(results) >= 1
        assert any("main" in r.name.lower() for r in results)
    
    def test_search_files_case_insensitive(self, test_config, sample_files):
        """Test that file search is case-insensitive."""
        fs_ops = FileSystemOperations(test_config)
        
        results = fs_ops.search_files(sample_files, "MAIN")
        
        assert len(results) >= 1
    
    def test_search_files_with_filter(self, test_config, sample_files):
        """Test file search with filter function."""
        fs_ops = FileSystemOperations(test_config)
        
        # Filter out venv directory
        filter_fn = lambda p: "venv" not in p.parts
        results = fs_ops.search_files(sample_files, ".py", filter_fn)
        
        # Should find .py files but not in venv
        assert all("venv" not in r.path for r in results)
