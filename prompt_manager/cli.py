"""
Command-line interface for the Prompt Manager.
"""
import click
from pathlib import Path
from prompt_manager import PromptManager, Task, TaskStatus
from typing import Optional
import sys


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Prompt Manager CLI - Development workflow management system."""
    pass


# Global variable to store the current project path
_current_project_path = None

def _get_manager():
    """Get a PromptManager instance with the current project."""
    global _current_project_path
    if _current_project_path is None:
        _current_project_path = Path.cwd()
    manager = PromptManager("", memory_path=_current_project_path / "prompt_manager_data")
    return manager

@cli.command()
@click.argument("path", type=click.Path(exists=True))
def analyze_repo(path: str):
    """Analyze a repository for project context."""
    click.echo(f"Analyzing repository at: {path}")
    
    # Initialize PromptManager with repository path
    manager = PromptManager("", memory_path=Path(path))
    
    try:
        # Perform repository analysis
        manager.initialize()
        click.echo("Repository analysis complete")
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
@click.option("--path", type=click.Path(), default=".")
def init(path: str):
    """Initialize a new project."""
    try:
        global _current_project_path
        _current_project_path = Path(path)
        manager = _get_manager()
        manager.initialize()
        click.echo("Project initialized successfully")
    except Exception as e:
        click.echo(f"Error initializing project: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.argument("description")
@click.argument("prompt")
@click.option("--priority", type=int, default=1)
def add_task(name: str, description: str, prompt: str, priority: int = 1):
    """Add a new task."""
    try:
        if priority < 1:
            raise ValueError("Priority must be a positive integer")
            
        manager = _get_manager()
        task = manager.add_task(name, description, prompt, priority)
        click.echo(f"Task {task.name} added successfully")
    except Exception as e:
        click.echo(f"Error adding task: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.argument("status", type=click.Choice([s.value for s in TaskStatus], case_sensitive=False))
def update_progress(name: str, status: str):
    """Update task progress."""
    try:
        manager = _get_manager()
        task = manager.update_task_status(name, status.upper())
        click.echo(f"Task {task.name} status updated to {task.status.value}")
    except Exception as e:
        click.echo(f"Error updating task: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--status', type=click.Choice([s.value for s in TaskStatus], case_sensitive=False),
              help='Filter tasks by status')
@click.option('--sort-by', type=click.Choice(['priority', 'created', 'updated'], case_sensitive=False),
              help='Sort tasks by field')
def list_tasks(status: Optional[str] = None, sort_by: Optional[str] = None):
    """List tasks with optional filtering and sorting."""
    try:
        manager = _get_manager()
        task_status = TaskStatus(status.upper()) if status else None
        tasks = manager.list_tasks(status=task_status, sort_by=sort_by)
        
        if not tasks:
            click.echo("No tasks found")
            return
        
        # Print header
        click.echo("\nTasks:")
        click.echo("=" * 50)
        
        for task in tasks:
            click.echo(f"\nName: {task.name}")
            click.echo(f"Status: {task.status.value}")
            click.echo(f"Description: {task.description}")
            click.echo(f"Priority: {task.priority}")
            click.echo(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.status_notes:
                click.echo("Status Notes:")
                for note in task.status_notes:
                    click.echo(f"  - {note}")
            click.echo("-" * 50)
    except Exception as e:
        click.echo(f"Error listing tasks: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--output", type=click.Path(), required=True)
def export_tasks(output: str):
    """Export tasks to a file."""
    try:
        manager = _get_manager()
        manager.export_tasks(Path(output))
        click.echo("Tasks exported successfully")
        click.echo(f"Output file: {output}")
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}")


@cli.command()
@click.argument("project_description")
@click.option("--framework", default="Next.js", help="Framework to use (e.g., Next.js, React, Vue)")
def generate_bolt_tasks(project_description: str, framework: str):
    """Generate a sequence of bolt.new development tasks."""
    try:
        manager = _get_manager()
        tasks = manager.generate_bolt_tasks(project_description)
        
        # Update framework for setup task
        tasks[0].framework = framework
        
        # Add tasks to manager
        for task in tasks:
            manager.add_task(task)
        
        click.echo("\nGenerated Bolt.new Development Tasks:")
        click.echo("=" * 60)
        
        for task in tasks:
            click.echo(f"\n{task.name} (Priority: {task.priority})")
            click.echo("-" * len(task.name))
            click.echo(f"Status: {task.status.value}")
            
            # Show bolt.new prompt
            click.echo("\nBolt.new Prompt:")
            click.echo(task.to_bolt_prompt())
            click.echo("\n" + "=" * 60)
            
    except Exception as e:
        click.echo(f"Error generating bolt tasks: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
