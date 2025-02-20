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
        if not project_dir:
            project_dir = str(Path.cwd())
            
        project_path = Path(project_dir)
        if not project_path.exists():
            click.echo(f"Error: Project directory '{project_dir}' does not exist", err=True)
            sys.exit(2)
            
        manager = PromptManager(str(project_path), memory_path=project_path / "prompt_manager_data")
        return manager
    except Exception as e:
        click.echo(f"Error initializing project manager: {str(e)}", err=True)
        sys.exit(2)
