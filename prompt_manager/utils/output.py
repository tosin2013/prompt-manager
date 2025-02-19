"""
Output utility functions for prompt_manager.
"""
from typing import Any, Dict, Optional
import click


def print_analysis(analysis: Dict[str, Any]) -> None:
    """Print analysis results in a formatted way."""
    click.echo("\nAnalysis Results:")
    for key, value in analysis.items():
        if isinstance(value, (list, tuple)):
            click.echo(f"\n{key}:")
            for item in value:
                click.echo(f"  - {item}")
        else:
            click.echo(f"\n{key}: {value}")


def print_error(message: str, details: Optional[str] = None) -> None:
    """Print error message in red."""
    click.secho(f"Error: {message}", fg="red", err=True)
    if details:
        click.secho(f"Details: {details}", fg="red", err=True)


def print_success(message: str) -> None:
    """Print success message in green."""
    click.secho(message, fg="green")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    click.secho(f"Warning: {message}", fg="yellow")


def print_info(message: str) -> None:
    """Print info message in blue."""
    click.secho(message, fg="blue")
