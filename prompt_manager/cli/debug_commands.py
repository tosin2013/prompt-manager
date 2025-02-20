"""Debug CLI commands."""

import click
from prompt_manager.cli.utils import get_manager
from prompt_manager.debug_manager import DebugManager


@click.group()
def debug():
    """Debug commands for analyzing and fixing code."""
    pass


@debug.command()
@click.argument('file')
def analyze_file(file):
    """Analyze a file for potential issues."""
    manager = DebugManager()
    result = manager.analyze_file(file)
    click.echo(f"Analysis results: {result}")
    
    # Update memory bank
    prompt_manager = get_manager()
    prompt_manager.memory_bank.update_context(
        "techContext.md",
        f"Analysis_{file}",
        f"File Analysis Results:\n{result}",
        mode="replace"
    )


@debug.command()
@click.argument('file')
def find_root_cause(file):
    """Find root cause of an issue in a file."""
    manager = DebugManager()
    result = manager.find_root_cause(file)
    click.echo(f"Root cause: {result}")
    
    # Update memory bank
    prompt_manager = get_manager()
    prompt_manager.memory_bank.update_context(
        "techContext.md",
        f"RootCause_{file}",
        f"Root Cause Analysis:\n{result}",
        mode="replace"
    )


@debug.command()
@click.argument('file')
def iterative_fix(file):
    """Apply iterative fixes to resolve issues."""
    manager = DebugManager()
    result = manager.iterative_fix(file)
    click.echo(f"Applied fixes: {result}")
    
    # Update memory bank
    prompt_manager = get_manager()
    prompt_manager.memory_bank.update_context(
        "techContext.md",
        f"Fixes_{file}",
        f"Applied Fixes:\n{result}",
        mode="replace"
    )


@debug.command()
@click.argument('file')
def test_roadmap(file):
    """Generate a test roadmap for a file."""
    manager = DebugManager()
    result = manager.generate_test_roadmap(file)
    click.echo(f"Test roadmap: {result}")
    
    # Update memory bank
    prompt_manager = get_manager()
    prompt_manager.memory_bank.update_context(
        "techContext.md",
        f"TestRoadmap_{file}",
        f"Test Roadmap:\n{result}",
        mode="replace"
    )


@debug.command()
@click.argument('file')
def analyze_dependencies(file):
    """Analyze dependencies of a file."""
    manager = DebugManager()
    result = manager.analyze_dependencies(file)
    click.echo(f"Dependencies: {result}")
    
    # Update memory bank
    prompt_manager = get_manager()
    prompt_manager.memory_bank.update_context(
        "techContext.md",
        f"Dependencies_{file}",
        f"Dependencies:\n{result}",
        mode="replace"
    )


@debug.command()
@click.argument('file')
def trace_error(file):
    """Trace an error through the codebase."""
    manager = DebugManager()
    result = manager.trace_error(file)
    click.echo(f"Error trace: {result}")
    
    # Update memory bank
    prompt_manager = get_manager()
    prompt_manager.memory_bank.update_context(
        "techContext.md",
        f"ErrorTrace_{file}",
        f"Error Trace:\n{result}",
        mode="replace"
    )


__all__ = ['debug']
