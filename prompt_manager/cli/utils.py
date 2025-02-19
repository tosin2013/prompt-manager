"""Utility functions for the CLI."""

import click
from pathlib import Path
import sys
from prompt_manager import PromptManager


def get_manager():
    """Get a PromptManager instance with the current project."""
    try:
        cwd = Path.cwd()
        manager = PromptManager(str(cwd), memory_path=cwd / "prompt_manager_data")
        return manager
    except Exception as e:
        click.echo(f"Error initializing project manager: {str(e)}", err=True)
        sys.exit(1)
