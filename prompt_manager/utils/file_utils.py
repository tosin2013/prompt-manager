"""
File utilities for the prompt manager.
"""

from pathlib import Path
from typing import Union


def read_file(file_path: Union[str, Path]) -> str:
    """Read contents of a file."""
    path = Path(file_path)
    return path.read_text()


def write_file(file_path: Union[str, Path], content: str) -> None:
    """Write content to a file."""
    path = Path(file_path)
    path.write_text(content)
