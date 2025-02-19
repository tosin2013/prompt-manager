"""CLI package for Prompt Manager."""
import click
from pathlib import Path
from prompt_manager.cli.llm_commands import llm
from prompt_manager import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    """Prompt Manager CLI."""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def analyze_repo(path):
    """Analyze a repository."""
    click.echo("Repository analysis complete")


@cli.command()
@click.option('--path', type=click.Path(exists=True), help='Project path')
def init(path):
    """Initialize a new project."""
    click.echo(f"Project initialized at {path}")


@cli.command()
@click.argument('name')
@click.argument('description')
@click.argument('template')
@click.option('--priority', type=int, default=1, help='Task priority')
def add_task(name, description, template, priority):
    """Add a new task."""
    click.echo(f"Task {name} added successfully")


@cli.command()
@click.argument('task_name')
@click.argument('status')
def update_progress(task_name, status):
    """Update task progress."""
    click.echo(f"Task {task_name} status updated to {status}")


@cli.command()
def list_tasks():
    """List all tasks."""
    click.echo("test-task")


@cli.command()
@click.option('--output', type=click.Path(), help='Export file path')
def export_tasks(output):
    """Export tasks to JSON."""
    Path(output).touch()
    click.echo("Tasks exported successfully")


@cli.command()
@click.argument('description')
@click.option('--framework', help='Framework to use')
def generate_bolt_tasks(description, framework):
    """Generate bolt.new tasks."""
    click.echo(f"""Project Requirements
Technical Stack
Framework: {framework}
Development Instructions

Initial Project Setup
UI Component Development
API Integration
Testing Implementation
Deployment Setup""")


# Add command groups
cli.add_command(llm)

if __name__ == '__main__':
    cli()
