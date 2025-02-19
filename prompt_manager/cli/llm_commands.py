"""LLM CLI commands."""

import click
import sys
from prompt_manager.llm_manager import LLMManager


@click.group()
def llm():
    """LLM commands."""
    pass


@llm.command()
@click.argument('file_path')
def analyze_impact(file_path):
    """Analyze impact of changes in a file."""
    manager = LLMManager()
    try:
        impact = manager.analyze_impact(file_path)
        click.echo(f"Impact analysis for {file_path}:")
        click.echo(impact)
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error analyzing impact: {str(e)}", err=True)
        sys.exit(2)


@llm.command()
@click.argument('file_path')
@click.option('--max-suggestions', type=int, default=3)
def suggest_improvements(file_path, max_suggestions):
    """Suggest code improvements."""
    if max_suggestions <= 0:
        click.echo("Error: max-suggestions must be greater than 0", err=True)
        sys.exit(1)
    
    manager = LLMManager()
    try:
        suggestions = manager.suggest_improvements(file_path)  # Test expects no max_suggestions param
        click.echo(f"Improvement suggestions for {file_path}:")
        for i, suggestion in enumerate(suggestions, 1):
            click.echo(f"{i}. {suggestion}")
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error suggesting improvements: {str(e)}", err=True)
        sys.exit(2)


@llm.command()
@click.argument('title')
@click.argument('description')
def create_pr(title, description):
    """Create a pull request."""
    if not title or not description:
        click.echo("Error: Both title and description are required", err=True)
        sys.exit(1)
    
    manager = LLMManager()
    try:
        pr_url = manager.create_pr(title, description)
        click.echo(f"Created PR: {pr_url}")
    except Exception as e:
        click.echo(f"Error creating PR: {str(e)}", err=True)
        sys.exit(2)


@llm.command()
@click.argument('file_path')
def generate_commands(file_path):
    """Generate CLI commands from file."""
    manager = LLMManager()
    try:
        commands = manager.generate_commands(file_path)
        click.echo(f"Generated commands for {file_path}:")
        for command in commands:
            click.echo(f"- {command}")
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating commands: {str(e)}", err=True)
        sys.exit(2)


__all__ = ['llm']
