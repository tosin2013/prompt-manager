"""Utility functions for the CLI."""

import click
from pathlib import Path
import sys
from prompt_manager import PromptManager


def get_manager():
    """Get a PromptManager instance with the current project."""
    try:
        ctx = click.get_current_context()
        project_dir = ctx.obj.get('project_dir') if ctx.obj else None
        project_path = Path(project_dir) if project_dir else Path.cwd()
        
        manager = PromptManager(str(project_path), memory_path=project_path / "prompt_manager_data")
        return manager
    except Exception as e:
        click.echo(f"Error initializing project manager: {str(e)}", err=True)
        sys.exit(1)
