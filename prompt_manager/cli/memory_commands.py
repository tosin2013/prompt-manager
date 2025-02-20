"""Memory management CLI commands."""

import click
from datetime import datetime
from prompt_manager.cli.utils import get_manager


@click.group()
def memory():
    """Memory management commands."""
    pass


@memory.command()
@click.argument('memory_id')
def delete(memory_id):
    """Delete a memory entry by its ID."""
    try:
        manager = get_manager()
        if not manager.memory_bank:
            click.echo("Error: No memory bank initialized for this project", err=True)
            return 1
            
        manager.memory_bank.delete_entry(memory_id)
        click.echo(f"Memory entry '{memory_id}' deleted successfully")
        return 0
    except Exception as e:
        click.echo(f"Error deleting memory entry: {str(e)}", err=True)
        return 1


@memory.command()
@click.option('--file', help='Filter by memory file (e.g., progress.md)')
def list(file=None):
    """List memory entries."""
    try:
        manager = get_manager()
        if not manager.memory_bank:
            click.echo("Error: No memory bank initialized for this project", err=True)
            return 1
            
        entries = manager.memory_bank.list_entries(file)
        if not entries:
            click.echo("No memory entries found")
            return 0
            
        for entry in entries:
            click.echo(f"- {entry['file']}: {entry['section']} ({entry['timestamp']})")
        return 0
    except Exception as e:
        click.echo(f"Error listing memory entries: {str(e)}", err=True)
        return 1


__all__ = ['memory']
