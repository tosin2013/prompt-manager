"""Utility functions for the CLI."""

import click
from pathlib import Path
import sys
from prompt_manager import PromptManager
from prompt_manager.memory import MemoryBank


def get_manager() -> PromptManager:
    """Get a PromptManager instance for the current directory."""
    return PromptManager()
