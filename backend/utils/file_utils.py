"""
File Utilities for Interview Coach
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure a directory exists, create if it doesn't"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_file(data: bytes, path: Union[str, Path], overwrite: bool = True) -> Path:
    """Save data to a file"""
    path = Path(path)
    
    # Ensure parent directory exists
    ensure_directory(path.parent)
    
    # Check if file exists and overwrite is False
    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")
    
    # Save the file
    with open(path, 'wb') as f:
        f.write(data)
    
    logger.info(f"File saved: {path}")
    return path


def delete_file(path: Union[str, Path]) -> bool:
    """Delete a file if it exists"""
    path = Path(path)
    
    if path.exists() and path.is_file():
        path.unlink()
        logger.info(f"File deleted: {path}")
        return True
    
    return False


def get_file_size(path: Union[str, Path]) -> int:
    """Get file size in bytes"""
    path = Path(path)
    
    if path.exists() and path.is_file():
        return path.stat().st_size
    
    return 0


def get_file_extension(path: Union[str, Path]) -> str:
    """Get file extension"""
    path = Path(path)
    return path.suffix.lower()


def is_valid_file_type(path: Union[str, Path], allowed_extensions: list) -> bool:
    """Check if file has allowed extension"""
    extension = get_file_extension(path)
    return extension in allowed_extensions


def read_file_text(path: Union[str, Path]) -> Optional[str]:
    """Read file as text"""
    path = Path(path)
    
    if path.exists() and path.is_file():
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    return None


def read_file_bytes(path: Union[str, Path]) -> Optional[bytes]:
    """Read file as bytes"""
    path = Path(path)
    
    if path.exists() and path.is_file():
        with open(path, 'rb') as f:
            return f.read()
    
    return None


def copy_file(source: Union[str, Path], destination: Union[str, Path], overwrite: bool = True) -> Path:
    """Copy a file"""
    source = Path(source)
    destination = Path(destination)
    
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    
    # Ensure parent directory exists
    ensure_directory(destination.parent)
    
    # Copy the file
    shutil.copy2(source, destination)
    
    logger.info(f"File copied: {source} -> {destination}")
    return destination


def move_file(source: Union[str, Path], destination: Union[str, Path], overwrite: bool = True) -> Path:
    """Move a file"""
    source = Path(source)
    destination = Path(destination)
    
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    
    # Ensure parent directory exists
    ensure_directory(destination.parent)
    
    # Move the file
    shutil.move(str(source), str(destination))
    
    logger.info(f"File moved: {source} -> {destination}")
    return destination
