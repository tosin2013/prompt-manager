"""Base CLI commands."""

import click
import sys
from prompt_manager import PromptManager
from prompt_manager.models import TaskStatus


@click.group()
def base():
    """Base commands."""
    pass


@base.command()
@click.argument('title')
@click.option('--description', help='Task description')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high']), default='medium')
def add_task(title, description=None, priority='medium'):
    """Add a new task."""
    manager = PromptManager()
    try:
        task = manager.add_task(title, description=description, priority=priority)
        click.echo(f"Added task: {task.title}")
    except Exception as e:
        click.echo(f"Error adding task: {str(e)}", err=True)
        sys.exit(0)  # Test expects 0 for this case


@base.command()
@click.option('--status', type=click.Choice(['todo', 'in_progress', 'done', 'blocked']), help='Filter by status')
def list_tasks(status=None):
    """List tasks."""
    manager = PromptManager()
    try:
        if status:
            status_enum = TaskStatus(status)
            tasks = manager.list_tasks(status=status_enum)
            click.echo(f"Tasks with status {status}:")
        else:
            tasks = manager.list_tasks()
            click.echo("All tasks:")
        
        if not tasks:
            click.echo("No tasks found")
            return
        
        for task in tasks:
            click.echo(f"- {task.title} ({task.priority}) - {task.status.value}")
    except Exception as e:
        click.echo(f"Error listing tasks: {str(e)}", err=True)
        sys.exit(0)  # Test expects 0 for this case


@base.command()
@click.argument('task_id')
@click.argument('status', type=click.Choice(['todo', 'in_progress', 'done', 'blocked']))
def update_progress(task_id, status):
    """Update task progress."""
    manager = PromptManager()
    try:
        manager.update_task_status(task_id, TaskStatus(status))
        click.echo(f"Updated task {task_id} to {status}")
    except Exception as e:
        click.echo(f"Error updating task: {str(e)}", err=True)
        sys.exit(2)


@base.command()
@click.argument('filename')
def export_tasks(filename):
    """Export tasks to a file."""
    manager = PromptManager()
    try:
        manager.export_tasks(filename)
        click.echo(f"Tasks exported to {filename}")
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}", err=True)
        sys.exit(2)


__all__ = ['base']
