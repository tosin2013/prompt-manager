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


@cli.command()
@click.option("--interactive", "-i", is_flag=True, help="Start in interactive mode")
def startup(interactive: bool):
    """Start the prompt manager with optional interactive mode."""
    try:
        if interactive:
            click.echo("Welcome to Prompt Manager! Let's get started.")
            click.echo("\nAvailable commands:")
            click.echo("1. Initialize new project")
            click.echo("2. Generate bolt.new tasks")
            click.echo("3. List existing tasks")
            click.echo("4. Add new task")
            click.echo("5. Import tasks from file")
            click.echo("6. Reset Memory Bank")
            click.echo("0. Exit")

            while True:
                choice = click.prompt("\nEnter command number", type=int)
                
                if choice == 0:
                    click.echo("Goodbye!")
                    break
                elif choice == 1:
                    path = click.prompt("Enter project path (or '.' for current directory)", default=".")
                    name = click.prompt("Enter project name")
                    init(path)
                    click.echo(f"Project {name} initialized at {path}")
                elif choice == 2:
                    desc = click.prompt("Enter project description")
                    framework = click.prompt("Enter framework (default: Next.js)", default="Next.js")
                    generate_bolt_tasks(desc, framework)
                elif choice == 3:
                    status = click.prompt("Filter by status (optional)", default="")
                    sort_by = click.prompt("Sort by (optional)", default="")
                    list_tasks(status or None, sort_by or None)
                elif choice == 4:
                    name = click.prompt("Task name")
                    desc = click.prompt("Task description")
                    prompt = click.prompt("Prompt template")
                    priority = click.prompt("Priority (default: 1)", type=int, default=1)
                    add_task(name, desc, prompt, priority)
                elif choice == 5:
                    path = click.prompt("Enter file path")
                    import_tasks(path)
                elif choice == 6:
                    if click.confirm("Are you sure you want to reset the Memory Bank?"):
                        manager = _get_manager()
                        manager.memory_bank.reset()
                        click.echo("Memory Bank reset successfully")
                else:
                    click.echo("Invalid choice. Please try again.")
        else:
            manager = _get_manager()
            manager.initialize()
            click.echo("Prompt Manager started successfully")
    except Exception as e:
        click.echo(f"Error during startup: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def reflect():
    """Analyze LLM's interaction patterns and effectiveness."""
    manager = _get_manager()
    click.echo("Analyzing LLM interaction patterns...")
    
    patterns = manager.analyze_patterns()
    click.echo("\nMost effective prompt patterns:")
    for pattern in patterns:
        click.echo(f"- {pattern}")
    
    suggestions = manager.generate_suggestions()
    click.echo("\nOptimization suggestions:")
    for suggestion in suggestions:
        click.echo(f"- {suggestion}")


@cli.command()
def learn_mode():
    """Enable autonomous learning mode for the LLM."""
    manager = _get_manager()
    click.echo("Enabling autonomous learning mode...")
    manager.start_learning_session()
    click.echo("Learning mode enabled")


@cli.command()
def meta_program():
    """Allow LLM to modify its own tooling."""
    manager = _get_manager()
    click.echo("Entering meta-programming mode...")
    
    utilities = manager.generate_custom_utilities()
    click.echo("\nGenerated custom utilities:")
    for util in utilities:
        click.echo(f"- {util}")
    
    commands = manager.create_custom_commands()
    click.echo("\nCreated custom commands:")
    for cmd in commands:
        click.echo(f"- {cmd}")


if __name__ == "__main__":
    cli()
