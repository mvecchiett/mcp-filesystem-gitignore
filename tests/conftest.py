"""
Pytest configuration and shared fixtures.
"""

import os
import tempfile
from pathlib import Path

import pytest

from mcp_filesystem.config import Config
from mcp_filesystem.filesystem_service import FileSystemService


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_config(temp_dir):
    """Create a test configuration with a temporary allowed directory."""
    # Set environment variable for config
    os.environ["ALLOWED_DIRECTORIES"] = str(temp_dir)
    config = Config()
    yield config
    # Cleanup
    if "ALLOWED_DIRECTORIES" in os.environ:
        del os.environ["ALLOWED_DIRECTORIES"]


@pytest.fixture
def fs_service(test_config):
    """Create a FileSystemService instance for testing."""
    return FileSystemService(test_config)


@pytest.fixture
def sample_files(temp_dir):
    """Create a sample file structure for testing."""
    # Create directories
    (temp_dir / "src").mkdir()
    (temp_dir / "tests").mkdir()
    (temp_dir / "venv").mkdir()
    (temp_dir / "venv" / "lib").mkdir()
    (temp_dir / "__pycache__").mkdir()
    
    # Create files
    (temp_dir / "README.md").write_text("# Test Project")
    (temp_dir / "src" / "main.py").write_text("print('Hello')")
    (temp_dir / "src" / "utils.py").write_text("def helper(): pass")
    (temp_dir / "tests" / "test_main.py").write_text("def test_something(): pass")
    (temp_dir / "venv" / "lib" / "package.py").write_text("# venv file")
    (temp_dir / "__pycache__" / "main.cpython-312.pyc").write_text("bytecode")
    
    # Create .gitignore
    (temp_dir / ".gitignore").write_text("venv/\n__pycache__/\n*.pyc\n")
    
    return temp_dir


@pytest.fixture
def special_char_files(temp_dir):
    """Create files with special characters for testing."""
    # Files with special characters
    (temp_dir / "archivo con espacios.txt").write_text("spaces")
    (temp_dir / "archivo#con#hashtag.py").write_text("hashtag")
    (temp_dir / "archivo@especial.json").write_text("at sign")
    (temp_dir / "archivo (con paréntesis).md").write_text("parentheses")
    (temp_dir / "archivo [con corchetes].csv").write_text("brackets")
    
    # Directories with special characters
    for dir_name in ["Dir con espacios", "Dir#con#hashtag", "Dir@especial"]:
        dir_path = temp_dir / dir_name
        dir_path.mkdir()
        (dir_path / "readme.txt").write_text(f"Inside {dir_name}")
    
    return temp_dir
