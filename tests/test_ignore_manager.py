"""Tests for ignore_manager module."""
from pathlib import Path
import pytest
from mcp_filesystem.ignore_manager import IgnoreManager

def test_should_ignore_without_gitignore(temp_dir):
    manager = IgnoreManager()
    test_path = temp_dir / "test.txt"
    assert not manager.should_ignore(test_path, temp_dir)

def test_should_ignore_with_gitignore(temp_dir):
    manager = IgnoreManager()
    (temp_dir / ".gitignore").write_text("*.pyc\nvenv/\n")
    pyc_file = temp_dir / "test.pyc"
    assert manager.should_ignore(pyc_file, temp_dir)
    py_file = temp_dir / "test.py"
    assert not manager.should_ignore(py_file, temp_dir)

def test_should_ignore_directory(temp_dir):
    manager = IgnoreManager()
    (temp_dir / ".gitignore").write_text("venv/\n")
    venv_dir = temp_dir / "venv"
    venv_dir.mkdir()
    assert manager.should_ignore(venv_dir, temp_dir)

def test_cache_invalidation(temp_dir):
    manager = IgnoreManager()
    (temp_dir / ".gitignore").write_text("*.txt\n")
    manager.should_ignore(temp_dir / "test.txt", temp_dir)
    manager.invalidate(temp_dir)
    assert temp_dir not in [Path(k) for k in manager._cache.keys()]
