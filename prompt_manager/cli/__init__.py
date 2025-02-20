"""CLI package for Prompt Manager."""

import click
from pathlib import Path
from prompt_manager import PromptManager, TaskStatus, Task
from typing import Optional
import sys
from prompt_manager.cli.base_commands import base
from prompt_manager.cli.debug_commands import debug
from prompt_manager.cli.memory_commands import memory
from prompt_manager.cli.llm_commands import llm
from prompt_manager.cli.repo_commands import repo
from prompt_manager.cli.utils import get_manager


@click.group()
@click.version_option(version="0.3.18")
@click.option('--project-dir', type=click.Path(exists=True), help='Project directory')
@click.pass_context
def cli(ctx, project_dir=None):
    """Prompt Manager CLI - Development workflow management system."""
    if not hasattr(ctx, 'obj') or not ctx.obj:
        ctx.obj = {}
    if project_dir:
        ctx.obj['project_dir'] = project_dir
    elif 'project_dir' not in ctx.obj:
        ctx.obj['project_dir'] = str(Path.cwd())
    # Store command info in context for tracking
    ctx.ensure_object(dict)
    ctx.obj['command'] = ctx.command.name
    ctx.obj['args'] = ctx.args


@cli.result_callback()
@click.pass_context
def process_result(ctx, result, **kwargs):
    """Track command execution in memory bank."""
    try:
        manager = get_manager()
        if manager.memory_bank:
            command = ctx.obj.get('command', '')
            args = ' '.join(ctx.obj.get('args', []))
            result_str = str(result) if result is not None else 'Success'
            manager.memory_bank.track_command(command, args, result_str)
    except Exception:
        pass  # Don't fail if tracking fails
    return result


# Import and register commands
cli.add_command(base)
cli.add_command(debug)
cli.add_command(memory)
cli.add_command(llm)
cli.add_command(repo)


@cli.command()
@click.option("--path", type=click.Path(), default=".")
@click.pass_context
def init(ctx, path: str):
    """Initialize a new project."""
    try:
        project_path = Path(path).absolute()
        if not project_path.exists():
            click.echo(f"Error: Path '{path}' does not exist", err=True)
            sys.exit(1)
            
        # Set project directory in context
        if not hasattr(ctx, 'obj') or not ctx.obj:
            ctx.obj = {}
        ctx.obj['project_dir'] = str(project_path)
            
        # Initialize project
        manager = PromptManager(str(project_path))
        manager.init_project(str(project_path))
        
        click.echo(f"Initialized project at {project_path}")
        return 0
    except Exception as e:
        click.echo(f"Error initializing project: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("title")
@click.argument("description", required=False)
@click.option("--template", "-t", help="Task template")
@click.option("--priority", "-p", type=click.Choice(['low', 'medium', 'high']), default='medium', help="Task priority")
@click.pass_context
def add_task(ctx, title: str, description: Optional[str] = None, template: Optional[str] = None, priority: str = 'medium'):
    """Add a new task."""
    try:
        click.echo(f"Debug: Getting manager with project_dir={ctx.obj.get('project_dir')}")
        manager = get_manager()
        click.echo(f"Debug: Creating task with title={title}, description={description}, template={template}, priority={priority}")
        # Create a Task object first to validate the data
        task = Task(
            title=title,
            description=description or "",
            template=template or "",
            priority=priority.lower()
        )
        click.echo(f"Debug: Task object created successfully")
        # Add the task using the manager
        task = manager.add_task(task)
        click.echo(f"Task '{title}' added successfully")
        return 0
    except Exception as e:
        click.echo(f"Error adding task: {str(e)}", err=True)
        click.echo(f"Debug: Exception type: {type(e)}")
        sys.exit(2)


@cli.command()
@click.argument("title")
@click.argument("status", type=click.Choice([s.value for s in TaskStatus]))
@click.option("--note", "-n", help="Progress note")
@click.pass_context
def update_progress(ctx, title: str, status: str, note: Optional[str] = None):
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
@click.pass_context
def export_tasks(ctx, output: str):
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
@click.pass_context
def list_tasks(ctx):
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
@click.pass_context
def generate_bolt_tasks(ctx, description: str, framework: Optional[str] = None):
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
    cli(obj={})
