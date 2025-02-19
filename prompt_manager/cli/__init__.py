"""CLI package for Prompt Manager."""

import click
from pathlib import Path
from prompt_manager import PromptManager, TaskStatus
from typing import Optional
import sys
from prompt_manager.cli.base_commands import base
from prompt_manager.cli.debug_commands import debug
from prompt_manager.cli.llm_commands import llm
from prompt_manager.cli.repo_commands import repo
from prompt_manager.cli.utils import get_manager


@click.group()
@click.version_option(version="0.3.18")
def cli():
    """Prompt Manager CLI - Development workflow management system."""
    pass


# Import and register commands
cli.add_command(base)
cli.add_command(debug)
cli.add_command(llm)
cli.add_command(repo)


@cli.command()
@click.option("--path", type=click.Path(), default=".")
def init(path: str):
    """Initialize a new project."""
    try:
        project_path = Path(path).absolute()
        if not project_path.exists():
            click.echo(f"Error: Path '{path}' does not exist", err=True)
            sys.exit(1)
            
        manager = PromptManager(
            "", memory_path=project_path / "prompt_manager_data"
        )
        manager.initialize()
        click.echo("Project initialized successfully")
        return 0
    except Exception as e:
        click.echo(f"Error initializing project: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("title")
@click.argument("description", required=False)
@click.option("--template", "-t", help="Task template")
@click.option("--priority", "-p", type=click.Choice(['low', 'medium', 'high']), default='medium', help="Task priority")
def add_task(title: str, description: Optional[str] = None, template: Optional[str] = None, priority: str = 'medium'):
    """Add a new task."""
    try:
        manager = get_manager()
        priority_map = {'low': 1, 'medium': 2, 'high': 3}
        task = manager.add_task(title, description, template, priority_map[priority])
        click.echo(f"Task '{title}' added successfully")
        return 0
    except Exception as e:
        click.echo(f"Error adding task: {str(e)}", err=True)
        sys.exit(2)


@cli.command()
@click.argument("title")
@click.argument("status", type=click.Choice([s.value for s in TaskStatus]))
@click.option("--note", "-n", help="Progress note")
def update_progress(title: str, status: str, note: Optional[str] = None):
    """Update task progress status."""
    try:
        manager = get_manager()
        manager.update_task_status(title, TaskStatus(status), note)
        click.echo(f"Task '{title}' status updated to {status}")
        return 0
    except Exception as e:
        click.echo(f"Error updating task status: {str(e)}", err=True)
        sys.exit(2)


@cli.command()
@click.option("--output", "-o", required=True, type=click.Path(), help="Output file path")
def export_tasks(output: str):
    """Export tasks to JSON."""
    try:
        manager = get_manager()
        manager.export_tasks(output)
        click.echo(f"Tasks exported to {output}")
        return 0
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}", err=True)
        sys.exit(1)


@cli.command(name="list-tasks")
def list_tasks():
    """List all tasks."""
    try:
        manager = get_manager()
        tasks = manager.list_tasks()
        
        if not tasks:
            click.echo("No tasks found")
            return 0
            
        for task in tasks:
            status = task.status.value if hasattr(task.status, 'value') else task.status
            priority = {1: 'low', 2: 'medium', 3: 'high'}.get(task.priority, 'medium')
            
            click.echo(f"\nTask: {task.title}")
            if task.description:
                click.echo(f"Description: {task.description}")
            click.echo(f"Status: {status}")
            click.echo(f"Priority: {priority}")
            
            if hasattr(task, 'status_notes') and task.status_notes:
                click.echo("Notes:")
                for note in task.status_notes:
                    click.echo(f"  - {note}")
        return 0
    except Exception as e:
        click.echo(f"Error listing tasks: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("description")
@click.option("--framework", "-f", help="Target framework")
def generate_bolt_tasks(description: str, framework: Optional[str] = None):
    """Generate bolt.new tasks."""
    try:
        manager = get_manager()
        tasks = manager.generate_bolt_tasks(description, framework)
        click.echo("Generated tasks:")
        for task in tasks:
            click.echo(f"- {task}")
        return 0
    except Exception as e:
        click.echo(f"Error generating tasks: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
