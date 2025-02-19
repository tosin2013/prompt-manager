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
@click.argument('description')
@click.option('--priority', type=int, default=3)
@click.pass_context
def add_task(ctx, description, priority):
    """Add new task"""
    pm = ctx.obj['pm']
    try:
        task = pm.create_task(description, priority=priority)
        click.echo(f"Created task #{task.id}: {task.description}")
    except ValueError as e:
        click.secho(f"Validation error: {str(e)}", fg='yellow')

if __name__ == '__main__':
    cli()
