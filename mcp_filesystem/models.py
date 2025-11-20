"""
Data models for filesystem operations.

Uses dataclasses for type safety and better IDE support.
"""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class FileInfo:
    """Information about a file or directory."""
    
    name: str
    path: str
    type: Literal["file", "directory"]
    size: int
    created: float
    modified: float
    is_symlink: bool = False


@dataclass
class DirectoryItem:
    """An item in a directory listing."""
    
    name: str
    type: Literal["file", "directory"]
    path: str


@dataclass
class DirectoryListing:
    """Result of listing a directory."""
    
    items: list[DirectoryItem]
    total: int
    error: str | None = None


@dataclass
class SearchResult:
    """Result of searching for files."""
    
    name: str
    path: str
    directory: str


@dataclass
class SearchResults:
    """Collection of search results."""
    
    results: list[SearchResult]
    total: int


@dataclass
class FileContent:
    """Content of a file read operation."""
    
    content: str | None = None
    error: str | None = None
    size: int | None = None


@dataclass
class OperationResult:
    """Generic result for write/create operations."""
    
    success: bool
    path: str
    error: str | None = None


@dataclass
class TreeNode:
    """A node in a directory tree."""
    
    name: str
    type: Literal["file", "directory"]
    path: str
    children: list["TreeNode"] = field(default_factory=list)
    truncated: bool = False
    error: str | None = None
