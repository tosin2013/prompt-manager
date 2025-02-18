"""Command-line interface for Prompt Manager."""

import click
from pathlib import Path
from . import PromptManager


@click.group()
def cli():
    """Prompt Manager CLI - Development workflow management system."""
    pass


@cli.command()
@click.argument('project_name')
@click.option('--memory-path', '-m', type=click.Path(), 
              help='Path to store memory files')
def init(project_name: str, memory_path: str = None):
    """Initialize a new project with Prompt Manager."""
    click.echo(f"Current working directory: {Path.cwd()}")
    if memory_path:
        memory_path = Path(memory_path)
    manager = PromptManager(project_name, config={"memory_path": memory_path} if memory_path else None)
    click.echo(f"Initialized project '{project_name}'")
    if memory_path:
        click.echo(f"Memory files will be stored in: {memory_path}")
    click.echo(f"Memory path: {manager.memory.docs_path}")


@cli.command()
@click.argument('task_name')
@click.argument('description')
@click.argument('prompt_template')
@click.option('--priority', '-p', type=int, default=1,
              help='Task priority (lower is higher priority)')
def add_task(task_name: str, description: str, prompt_template: str, 
             priority: int):
    """Add a new task to the workflow."""
    manager = PromptManager("default")
    manager.add_task(task_name, description, prompt_template)
    click.echo(f"Added task '{task_name}'")


@cli.command()
@click.argument('task_name')
def get_task(task_name: str):
    """Get details about a task."""
    manager = PromptManager("default")
    task = manager.get_task(task_name)
    if task:
        click.echo(f"Task: {task_name}")
        click.echo(f"Description: {task.description}")
        click.echo(f"Status: {task.status}")
    else:
        click.echo(f"Task '{task_name}' not found", err=True)


@cli.command()
@click.argument('task_name')
@click.argument('status')
@click.argument('note')
def update_progress(task_name: str, status: str, note: str):
    """Update task progress."""
    manager = PromptManager("default")
    manager.update_progress(task_name, status, note)
    click.echo(f"Updated progress for task '{task_name}'")


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True))
def analyze_repo(repo_path: str):
    """Analyze an existing GitHub repository."""
    click.echo(f"Analyzing repository at: {repo_path}")
    
    # Convert to absolute path
    repo_path = Path(repo_path).resolve()
    
    # Check if it's a git repository
    if not (repo_path / ".git").exists():
        click.echo("Error: Not a git repository", err=True)
        return
    
    # Initialize PromptManager with repo name
    repo_name = repo_path.name
    manager = PromptManager(repo_name)
    
    # Add .gitignore entry if needed
    gitignore_path = repo_path / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            if "cline_docs/" not in f.read():
                with open(gitignore_path, "a") as f:
                    f.write("\n# Cline documentation\ncline_docs/\n")
    else:
        with open(gitignore_path, "w") as f:
            f.write("# Cline documentation\ncline_docs/\n")
    
    click.echo(f"Initialized Cline for repository: {repo_name}")
    click.echo(f"Memory files will be stored in: {manager.memory.docs_path}")
    click.echo("Added cline_docs/ to .gitignore")


if __name__ == '__main__':
    cli()
