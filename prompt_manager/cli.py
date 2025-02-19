"""
Command-line interface for the Prompt Manager.
"""
import click
from pathlib import Path
from prompt_manager import PromptManager, Task, TaskStatus
from prompt_manager.llm_guidance import LLMGuidance
from typing import Optional
import sys


@click.group()
@click.version_option(version="0.3.18")
def cli():
    """Prompt Manager CLI - Development workflow management system."""
    pass


def get_manager():
    """Get a PromptManager instance with the current project."""
    manager = PromptManager("", memory_path=Path.cwd() / "prompt_manager_data")
    return manager


def get_llm_guidance(command: str) -> str:
    """Get formatted guidance for an LLM about how to use a command."""
    guidance = LLMGuidance.get_command_guidance(command)
    return LLMGuidance.format_guidance(guidance)


@cli.command()
@click.option("--path", type=click.Path(), default=".")
def init(path: str):
    """Initialize a new project."""
    click.echo(get_llm_guidance("init"))
    try:
        manager = PromptManager("", memory_path=Path(path).absolute() / "prompt_manager_data")
        manager.initialize()
        click.echo("Project initialized successfully")
    except Exception as e:
        click.echo(f"Error initializing project: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def analyze_repo(path: str):
    """Analyze a repository for project context."""
    click.echo(get_llm_guidance("analyze_repo"))
    click.echo(f"Analyzing repository at: {path}")
    
    try:
        # Initialize PromptManager with repository path
        manager = PromptManager("", memory_path=Path(path))
        manager.initialize()
        click.echo("Repository analysis complete")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--title", required=True, help="Name/title of the task")
@click.option("--description", required=True, help="Description of the task")
@click.option("--template", required=True, help="Template/prompt for the task")
@click.option("--priority", type=click.Choice(['low', 'medium', 'high']), default='medium', 
              help="Task priority (low/medium/high)")
def add_task(title: str, description: str, template: str, priority: str = 'medium'):
    """Add a new task."""
    click.echo(get_llm_guidance("add_task"))
    try:
        # Convert priority string to integer
        priority_map = {'low': 1, 'medium': 2, 'high': 3}
        priority_int = priority_map[priority.lower()]
            
        manager = get_manager()
        task = manager.add_task(title, description, template, priority_int)
        click.echo(f"Task '{task.name}' added successfully with priority {priority}")
    except Exception as e:
        click.echo(f"Error adding task: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def list_tasks():
    """List all tasks."""
    click.echo(get_llm_guidance("list_tasks"))
    try:
        manager = get_manager()
        tasks = manager.list_tasks()
        for task in tasks:
            click.echo(f"{task.name} ({task.status.value})")
    except Exception as e:
        click.echo(f"Error listing tasks: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.argument("status", type=click.Choice([s.value for s in TaskStatus], case_sensitive=False))
def update_progress(name: str, status: str):
    """Update task progress."""
    click.echo(get_llm_guidance("update_progress"))
    try:
        manager = get_manager()
        task = manager.update_task_status(name, status.upper())
        click.echo(f"Task {task.name} status updated to {task.status.value}")
    except Exception as e:
        click.echo(f"Error updating task: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--output", required=True, type=click.Path(), help="Export file path")
def export_tasks(output: str):
    """Export tasks to JSON."""
    click.echo(get_llm_guidance("export_tasks"))
    try:
        manager = get_manager()
        manager.export_tasks(output)
        click.echo(f"Tasks exported to {output}")
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("description")
@click.option("--framework", default="Next.js", help="Framework to use")
def generate_bolt_tasks(description: str, framework: str):
    """Generate bolt.new tasks."""
    click.echo(get_llm_guidance("generate_bolt_tasks"))
    try:
        manager = get_manager()
        tasks = manager.generate_bolt_tasks(description, framework)
        click.echo(f"Generated {len(tasks)} tasks for {framework} project")
    except Exception as e:
        click.echo(f"Error generating tasks: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def llm():
    """LLM Enhancement commands."""
    pass


@llm.command()
def learn_session():
    """Start an autonomous learning session."""
    try:
        manager = get_manager()
        manager.llm.start_learning_session()
        click.echo("Learning session started successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)


@llm.command()
def analyze_impact():
    """Analyze the potential impact of changes."""
    try:
        manager = get_manager()
        manager.llm.analyze_impact()
        click.echo("Impact analysis complete")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)


@llm.command()
def suggest_improvements():
    """Generate code improvement suggestions."""
    try:
        manager = get_manager()
        manager.llm.suggest_improvements()
        click.echo("Generated improvement suggestions")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)


@llm.command()
def create_pr():
    """Create a pull request from suggestions."""
    try:
        manager = get_manager()
        manager.llm.create_pr()
        click.echo("Pull request created successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)


@llm.command()
def generate_commands():
    """Generate custom CLI commands."""
    try:
        manager = get_manager()
        manager.llm.generate_commands()
        click.echo("Commands generated successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
