"""Tests for path_validator module."""
from pathlib import Path
import pytest
from mcp_filesystem.errors import PathNotAllowedError
from mcp_filesystem.path_validator import PathValidator

def test_normalize_simple_path(temp_dir):
    validator = PathValidator([temp_dir])
    result = validator.normalize(str(temp_dir / "test.txt"))
    assert isinstance(result, Path)
    assert result.is_absolute()

def test_validate_allowed_path(temp_dir):
    validator = PathValidator([temp_dir])
    path_to_validate = temp_dir / "subdir" / "file.txt"
    validator.validate(path_to_validate)

def test_validate_disallowed_path(temp_dir):
    validator = PathValidator([temp_dir])
    disallowed_path = Path("/some/other/path/file.txt")
    with pytest.raises(PathNotAllowedError):
        validator.validate(disallowed_path)
