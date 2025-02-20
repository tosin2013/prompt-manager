import click
from pathlib import Path
from typing import Optional
from . import PromptManager, Task, TaskStatus

@click.group()
@click.option('--project-dir', type=click.Path(exists=True), default='.')
@click.pass_context
def cli(ctx, project_dir):
    """Prompt Manager CLI"""
    ctx.obj = {
        'pm': PromptManager(Path(project_dir)),
        'project_dir': Path(project_dir)
    }

@cli.command()
@click.argument('path', type=click.Path())
@click.pass_context
def init(ctx, path):
    """Initialize new project"""
    try:
        ctx.obj['pm'].init_project(Path(path))
        click.echo(f"Initialized project at {path}")
    except Exception as e:
        click.secho(f"Error initializing project: {str(e)}", fg='red')

@cli.command()
@click.argument('name')
@click.argument('description')
@click.argument('template')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high']), default='medium', help='Task priority (low/medium/high)')
@click.pass_context
def add_task(ctx, name, description, template, priority):
    """Add new task"""
    pm = ctx.obj['pm']
    try:
        task = pm.add_task(
            title=name,
            description=description,
            template=template,
            priority=priority
        )
        click.echo(f"Task {name} added successfully")
    except ValueError as e:
        click.secho(f"Validation error: {str(e)}", fg='yellow')
        ctx.exit(1)

@cli.command()
@click.option('--title', required=True, help='Task title')
@click.option('--status', required=True, type=click.Choice(['PENDING', 'IN_PROGRESS', 'DONE', 'FAILED']), help='New task status')
@click.option('--note', help='Optional note about the status update')
@click.pass_context
def update_progress(ctx, title, status, note=None):
    """Update task progress"""
    pm = ctx.obj['pm']
    try:
        task = pm.update_task_status(title, status, notes=note)
        click.echo(f"Task {title} status updated to {status}")
    except (KeyError, ValueError) as e:
        click.secho(f"Error: {str(e)}", fg='red')
        ctx.exit(1)

@cli.command()
@click.option('--status', type=click.Choice(['PENDING', 'IN_PROGRESS', 'DONE', 'FAILED']), help='Filter by status')
@click.pass_context
def list_tasks(ctx, status=None):
    """List all tasks"""
    pm = ctx.obj['pm']
    try:
        tasks = pm.list_tasks(status=TaskStatus(status.lower()) if status else None)
        if not tasks:
            click.echo("No tasks found")
            return
        
        for task in tasks:
            click.echo(f"{task.title} - {task.status.value} - {task.priority}")
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')
        ctx.exit(1)

@cli.command()
@click.option('--output', type=click.Path(), required=True, help='Output file path')
@click.pass_context
def export_tasks(ctx, output):
    """Export tasks to JSON file"""
    pm = ctx.obj['pm']
    try:
        pm.export_tasks(Path(output))
        click.echo(f"Tasks exported successfully to {output}")
    except Exception as e:
        click.secho(f"Error exporting tasks: {str(e)}", fg='red')
        ctx.exit(1)

if __name__ == '__main__':
    cli()
