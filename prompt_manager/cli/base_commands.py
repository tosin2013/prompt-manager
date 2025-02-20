"""Base CLI commands."""

import click
import sys
from prompt_manager import PromptManager
from prompt_manager.models import TaskStatus
from prompt_manager.cli.utils import get_manager


@click.group()
def base():
    """Base commands."""
    pass


@base.command()
@click.argument('name')
@click.argument('description')
@click.option('--template', help='Task template')
@click.option('--priority', type=int, default=2, help='Task priority (1=high, 2=medium, 3=low)')
def add_task(name, description, template=None, priority=2):
    """Add a new task."""
    try:
        manager = get_manager()
        priority_map = {1: 'high', 2: 'medium', 3: 'low'}
        task = manager.add_task(name, description=description, template=template, priority=priority_map[priority])
        click.echo(f"Added task: {task.title}")
        return 0
    except Exception as e:
        click.echo(f"Error adding task: {str(e)}", err=True)
        return 1


@base.command()
@click.option('--status', type=click.Choice(['todo', 'in_progress', 'done', 'blocked']), help='Filter by status')
def list_tasks(status=None):
    """List tasks."""
    try:
        manager = get_manager()
        if status:
            status_enum = TaskStatus(status)
            tasks = manager.list_tasks(status=status_enum)
            click.echo(f"Tasks with status {status}:")
        else:
            tasks = manager.list_tasks()
            click.echo("All tasks:")
        
        if not tasks:
            click.echo("No tasks found")
            return 0
        
        for task in tasks:
            click.echo(f"- {task.title} ({task.priority}) - {task.status.value}")
        return 0
    except Exception as e:
        click.echo(f"Error listing tasks: {str(e)}", err=True)
        return 1


@base.command()
@click.argument('task_id')
@click.argument('status', type=click.Choice(['todo', 'in_progress', 'done', 'blocked']))
def update_progress(task_id, status):
    """Update task progress."""
    try:
        manager = get_manager()
        manager.update_task_status(task_id, TaskStatus(status))
        click.echo(f"Updated task {task_id} to {status}")
        return 0
    except Exception as e:
        click.echo(f"Error updating task: {str(e)}", err=True)
        return 1


@base.command()
@click.argument('filename')
def export_tasks(filename):
    """Export tasks to a file."""
    try:
        manager = get_manager()
        manager.export_tasks(filename)
        click.echo(f"Tasks exported to {filename}")
        return 0
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}", err=True)
        return 1


__all__ = ['base']
