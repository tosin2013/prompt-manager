"""Repository CLI commands."""

import click
import sys
from prompt_manager.repo_manager import RepoManager


@click.group()
def repo():
    """Repository commands."""
    pass


@repo.command()
@click.argument('file_path')
def analyze_repo(file_path):
    """Analyze repository changes."""
    manager = RepoManager()
    try:
        analysis = manager.analyze_repo(file_path)
        click.echo(f"Repository analysis for {file_path}:")
        click.echo(analysis)
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error analyzing repository: {str(e)}", err=True)
        sys.exit(2)


@repo.command()
@click.argument('file_path')
@click.option('--duration', type=int, default=7, help='Duration in days')
def learn_session(file_path, duration):
    """Start a learning session for repository understanding."""
    if duration <= 0:
        click.echo("invalid duration", err=True)  # Test expects this exact message
        sys.exit(1)

    manager = RepoManager()
    try:
        result = manager.learn_session(file_path, duration=duration)
        click.echo(f"Learning session results for {file_path}:")
        click.echo(result)
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error starting learning session: {str(e)}", err=True)
        sys.exit(2)


__all__ = ['repo']
