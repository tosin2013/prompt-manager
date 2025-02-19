"""
Validation utilities for the prompt manager.
"""

from pathlib import Path
from typing import Union


def validate_file_path(file_path: Union[str, Path]) -> Path:
    """Validate and convert a file path to a Path object."""
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")
    return path


def validate_priority(priority: str) -> None:
    """Validate task priority."""
    if priority not in ["low", "medium", "high"]:
        raise ValueError("Priority must be one of: low, medium, high")


def validate_task_title(title: str) -> None:
    """Validate task title."""
    if not title or len(title.strip()) == 0:
        raise ValueError("Task title cannot be empty")
