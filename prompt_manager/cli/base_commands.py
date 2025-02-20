"""Base CLI commands."""

import click
import sys
from datetime import datetime
from prompt_manager import PromptManager
from prompt_manager.models import TaskStatus
from prompt_manager.cli.utils import get_manager
from pathlib import Path
import yaml
from prompt_manager.memory import MemoryBank


@click.group()
def base():
    """Base commands."""
    pass


@base.command()
@click.argument('title')
@click.argument('description')
@click.option('--template', help='Task template')
@click.option('--priority', type=click.Choice(['high', 'medium', 'low']), default='medium', help='Task priority')
def add_task(title: str, description: str = "", template: str = None, priority: str = "medium"):
    """Add a new task."""
    try:
        # Get current project directory
        project_dir = Path.cwd()
        
        # Find config file
        config_path = project_dir / "prompt_manager_config.yaml"
        if not config_path.exists():
            raise click.UsageError("No project configuration found. Please run 'prompt-manager init' first.")
        
        # Load config
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Initialize memory bank
        memory_dir = Path(config["memory_path"])
        memory_bank = MemoryBank(memory_dir)
        memory_bank.initialize()  # Initialize memory bank
        
        # Add task
        memory_bank.add_task(title, description, template, priority)
        click.echo(f"Added task: {title}")
        
        # Update active context with task creation
        if memory_bank:
            memory_bank.update_context(
                "activeContext.md",
                f"TaskCreation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                f"Created task '{title}' with priority {priority}\nDescription: {description}",
                mode="append"
            )
        return 0
    except Exception as e:
        click.echo(f"Error adding task: {str(e)}", err=True)
        return 2


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
        
        # Build task summary
        summary = []
        for task in tasks:
            task_line = f"- {task.title} ({task.priority}) - {task.status.value}"
            click.echo(task_line)
            summary.append(task_line)
        
        # Update system patterns with task overview
        if manager.memory_bank:
            manager.memory_bank.update_context(
                "systemPatterns.md",
                "TaskOverview",
                "Current Task Status:\n" + "\n".join(summary),
                mode="replace"
            )
        return 0
    except Exception as e:
        click.echo(f"Error listing tasks: {str(e)}", err=True)
        return 1


@base.command()
@click.argument('title')
@click.argument('status', type=click.Choice(['todo', 'in_progress', 'done', 'blocked']))
@click.option('--note', help='Optional note about the status update')
def update_progress(title, status, note=None):
    """Update task progress."""
    try:
        manager = get_manager()
        task = manager.update_task_status(title, TaskStatus(status), notes=note)
        click.echo(f"Updated task '{title}' to {status}")
        
        # Update progress tracking
        if manager.memory_bank:
            update_msg = f"Task '{title}' status changed to {status}"
            if note:
                update_msg += f"\nNote: {note}"
            
            manager.memory_bank.update_context(
                "progress.md",
                f"StatusUpdate_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                update_msg,
                mode="append"
            )
        return 0
    except Exception as e:
        click.echo(f"Error updating task: {str(e)}", err=True)
        return 1


@base.command()
@click.option('--path', required=True, help='Project directory path')
def init(path):
    """Initialize a new project."""
    try:
        manager = get_manager()
        manager.init_project(path)
        click.echo(f"Initialized project at {path}")
        return 0
    except Exception as e:
        click.echo(f"Error initializing project: {str(e)}", err=True)
        return 1


@base.command()
@click.argument('filename')
def export_tasks(filename):
    """Export tasks to a file."""
    try:
        manager = get_manager()
        manager.export_tasks(filename)
        click.echo(f"Tasks exported to {filename}")
        
        # Record export in product context
        if manager.memory_bank:
            manager.memory_bank.update_context(
                "productContext.md",
                f"TaskExport_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                f"Tasks exported to {filename}",
                mode="append"
            )
        return 0
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}", err=True)
        return 1


__all__ = ['base']
