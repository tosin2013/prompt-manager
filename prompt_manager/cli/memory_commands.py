"""Memory CLI commands."""

import click
from pathlib import Path
from prompt_manager import PromptManager
from prompt_manager.cli.utils import get_manager, with_prompt_option
from prompt_manager.prompts import get_prompt_for_command
from typing import Optional


@click.group()
def memory():
    """Memory commands."""
    pass


@memory.command()
@click.argument('key')
@click.argument('value')
@click.option('--output', help='Output file path')
@with_prompt_option('store-memory')
def store(key: str, value: str, output: Optional[str] = None):
    """Store value in memory."""
    manager = get_manager()
    result = manager.store_memory(key, value)
    
    if output:
        Path(output).write_text(result)
        click.echo(f"Memory store result written to {output}")
    else:
        click.echo(result)


@memory.command()
@click.argument('key')
@click.option('--output', help='Output file path')
@with_prompt_option('retrieve-memory')
def retrieve(key: str, output: Optional[str] = None):
    """Retrieve value from memory."""
    manager = get_manager()
    value = manager.retrieve_memory(key)
    
    if output:
        Path(output).write_text(value)
        click.echo(f"Memory value written to {output}")
    else:
        click.echo(value)


@memory.command()
@click.option('--output', help='Output file path')
@with_prompt_option('list-memories')
def list_all(output: Optional[str] = None):
    """List all stored memories."""
    manager = get_manager()
    memories = manager.list_memories()
    
    if output:
        Path(output).write_text(memories)
        click.echo(f"Memory list written to {output}")
    else:
        click.echo(memories)


__all__ = ['memory']
