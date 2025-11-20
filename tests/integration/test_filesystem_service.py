"""
Integration tests for FileSystemService.

Tests the service layer orchestrating all components together.
"""

import pytest

from mcp_filesystem.errors import PathNotAllowedError, PathNotFoundError
from mcp_filesystem.models import DirectoryListing, OperationResult, TreeNode


class TestFileSystemServiceIntegration:
    """Integration tests for FileSystemService."""
    
    def test_read_write_cycle(self, fs_service, temp_dir):
        """Test writing and then reading a file."""
        file_path = str(temp_dir / "test.txt")
        content = "Hello, World!"
        
        # Write
        write_result = fs_service.write_file(file_path, content)
        assert write_result.success
        
        # Read
        read_result = fs_service.read_file(file_path)
        assert read_result.content == content
    
    def test_list_directory_respects_gitignore(self, fs_service, sample_files):
        """Test that list_directory respects .gitignore patterns."""
        # With .gitignore respect (default)
        listing = fs_service.list_directory(str(sample_files), respect_gitignore=True)
        
        assert isinstance(listing, DirectoryListing)
        names = [item.name for item in listing.items]
        
        # Should NOT include venv and __pycache__ (they're in .gitignore)
        assert "venv" not in names
        assert "__pycache__" not in names
        
        # Should include non-ignored items
        assert "README.md" in names
        assert "src" in names
    
    def test_list_directory_ignores_gitignore_when_disabled(self, fs_service, sample_files):
        """Test listing with respect_gitignore=False shows all files."""
        listing = fs_service.list_directory(str(sample_files), respect_gitignore=False)
        
        names = [item.name for item in listing.items]
        
        # Should include everything, even ignored items
        assert "venv" in names
        assert "__pycache__" in names
    
    def test_directory_tree_respects_gitignore(self, fs_service, sample_files):
        """Test that directory_tree respects .gitignore."""
        tree = fs_service.directory_tree(str(sample_files), max_depth=2, respect_gitignore=True)
        
        assert isinstance(tree, TreeNode)
        assert tree.type == "directory"
        
        # Get all child names
        child_names = [child.name for child in tree.children] if tree.children else []
        
        # Should NOT include venv and __pycache__
        assert "venv" not in child_names
        assert "__pycache__" not in child_names
    
    def test_search_files_respects_gitignore(self, fs_service, sample_files):
        """Test that search respects .gitignore."""
        results = fs_service.search_files(
            str(sample_files),
            ".py",
            respect_gitignore=True
        )
        
        # Should find .py files but not in venv
        assert results.total > 0
        assert all("venv" not in r.path for r in results.results)
    
    def test_create_directory_and_write_file(self, fs_service, temp_dir):
        """Test creating a directory and writing a file to it."""
        new_dir = str(temp_dir / "new_dir")
        
        # Create directory
        create_result = fs_service.create_directory(new_dir)
        assert create_result.success
        
        # Write file in new directory
        file_path = str(temp_dir / "new_dir" / "file.txt")
        write_result = fs_service.write_file(file_path, "content")
        assert write_result.success
        
        # Verify
        read_result = fs_service.read_file(file_path)
        assert read_result.content == "content"
    
    def test_access_denied_outside_allowed_dirs(self, fs_service):
        """Test that accessing paths outside allowed directories raises error."""
        disallowed_path = "C:\\Windows\\System32\\test.txt"
        
        with pytest.raises(PathNotAllowedError):
            fs_service.read_file(disallowed_path)
    
    def test_get_file_info_for_existing_file(self, fs_service, sample_files):
        """Test getting info for an existing file."""
        file_path = str(sample_files / "README.md")
        
        info = fs_service.get_file_info(file_path)
        
        assert info.name == "README.md"
        assert info.type == "file"
        assert info.size > 0
    
    def test_special_characters_in_paths(self, fs_service, special_char_files):
        """Test handling files with special characters."""
        # Test file with spaces
        file_with_spaces = str(special_char_files / "archivo con espacios.txt")
        result = fs_service.read_file(file_with_spaces)
        assert result.content == "spaces"
        
        # Test file with hashtag
        file_with_hash = str(special_char_files / "archivo#con#hashtag.py")
        result = fs_service.read_file(file_with_hash)
        assert result.content == "hashtag"
        
        # Test directory with spaces
        dir_with_spaces = str(special_char_files / "Dir con espacios")
        listing = fs_service.list_directory(dir_with_spaces)
        assert listing.total > 0
