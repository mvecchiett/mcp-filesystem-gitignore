"""
Integration tests for special character handling.

Comprehensive tests for spaces, hashtags, @ signs, parentheses, etc.
"""

import pytest


class TestSpecialCharacterHandling:
    """Test handling of special characters in file and directory names."""
    
    @pytest.mark.parametrize("filename,expected_content", [
        ("archivo con espacios.txt", "spaces"),
        ("archivo#con#hashtag.py", "hashtag"),
        ("archivo@especial.json", "at sign"),
        ("archivo (con paréntesis).md", "parentheses"),
        ("archivo [con corchetes].csv", "brackets"),
    ])
    def test_read_files_with_special_chars(self, fs_service, special_char_files, filename, expected_content):
        """Test reading files with various special characters."""
        file_path = str(special_char_files / filename)
        
        result = fs_service.read_file(file_path)
        
        assert result.content == expected_content
        assert result.error is None
    
    @pytest.mark.parametrize("dirname", [
        "Dir con espacios",
        "Dir#con#hashtag",
        "Dir@especial",
    ])
    def test_list_directories_with_special_chars(self, fs_service, special_char_files, dirname):
        """Test listing directories with special characters."""
        dir_path = str(special_char_files / dirname)
        
        listing = fs_service.list_directory(dir_path)
        
        assert listing.total > 0
        assert any(item.name == "readme.txt" for item in listing.items)
    
    def test_search_in_paths_with_special_chars(self, fs_service, special_char_files):
        """Test searching for files in paths with special characters."""
        results = fs_service.search_files(
            str(special_char_files),
            "archivo",
            respect_gitignore=False
        )
        
        assert results.total >= 5  # At least the 5 test files
    
    def test_write_file_with_special_chars_in_name(self, fs_service, temp_dir):
        """Test writing a file with special characters in its name."""
        file_path = str(temp_dir / "new file #with @special [chars].txt")
        content = "test content"
        
        result = fs_service.write_file(file_path, content)
        
        assert result.success
        
        # Verify by reading back
        read_result = fs_service.read_file(file_path)
        assert read_result.content == content
    
    def test_create_directory_with_special_chars(self, fs_service, temp_dir):
        """Test creating a directory with special characters."""
        dir_path = str(temp_dir / "New Dir #with @Special [Chars]")
        
        result = fs_service.create_directory(dir_path)
        
        assert result.success
        
        # Verify by listing
        listing = fs_service.list_directory(dir_path)
        assert listing.total == 0  # Empty directory
    
    def test_url_encoded_paths(self, fs_service, special_char_files):
        """Test that URL-encoded paths are properly decoded."""
        # Path with %20 for spaces
        file_path_encoded = str(special_char_files / "archivo%20con%20espacios.txt")
        
        result = fs_service.read_file(file_path_encoded)
        
        assert result.content == "spaces"
