"""Base CLI commands."""

import click
from pathlib import Path
from prompt_manager import PromptManager, TaskStatus, MemoryBank
from prompt_manager.cli.utils import get_manager
from prompt_manager.prompts import get_prompt_for_command

def print_prompt_info(prompt_name: str, prompt: str):
    """Print prompt information in a formatted way."""
    click.echo("\n" + "="*80)
    click.echo(f"Using prompt template: {prompt_name}")
    click.echo("="*80)
    click.echo(prompt)
    click.echo("="*80 + "\n")

@click.group()
def base():
    """Base commands."""
    pass

@base.command()
@click.argument('title')
@click.argument('description', required=False, default="")
@click.option('--template', help='Template to use')
@click.option('--priority', type=int, default=0, help='Task priority')
def add_task(title: str, description: str = "", template: str = None, priority: int = 0):
    """Add a new task.
    
    Args:
        title: Task title
        description: Task description
        template: Optional task template
        priority: Task priority
    """
    manager = get_manager()
    
    # Get existing tasks for context
    existing_tasks = manager.list_tasks()
    
    # Get and format prompt
    prompt = get_prompt_for_command("add-task")
    if prompt:
        context = {
            "title": title,
            "description": description,
            "template": template or "none",
            "priority": priority,
            "existing_tasks": "\n".join(f"{t.status.value}: {t.title}" for t in existing_tasks)
        }
        prompt = prompt.format(**context)
        print_prompt_info("add-task", prompt)
    
    # Add the task
    task = manager.add_task(title, description, template, priority)
    if task:
        click.echo(f"Added task: {task.title}")
        click.echo(f"Status: {task.status.value}")
        
        # Save task to memory
        memory_bank = MemoryBank(str(manager.project_path))
        memory_bank.save_task_memory({
            task.title: {
                "id": task.id,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "dependencies": task.dependencies,
                "tags": task.tags,
                "priority": task.priority,
                "notes": task.notes
            }
        })

@base.command()
@click.argument('title')
@click.argument('status', type=click.Choice([s.value for s in TaskStatus]), required=True)
@click.option('-n', '--note', help='Progress note')
def update_progress(title, status, note=None):
    """Update task progress status."""
    manager = PromptManager(Path.cwd())
    
    # Get task history and related tasks
    task = manager.get_task(title)
    related_tasks = manager.get_related_tasks(title)
    
    # Get and format prompt
    prompt_template = get_prompt_for_command("update-progress")
    if prompt_template:
        context = {
            "task_title": title,
            "new_status": status,
            "current_status": task.status.value if task else "unknown",
            "progress_note": note or "",
            "task_history": "\n".join(task.notes) if task and task.notes else "",
            "related_tasks": "\n".join(str(t) for t in related_tasks)
        }
        prompt = prompt_template.format(**context)
        print_prompt_info("update-progress", prompt)
    
    # Update the task
    task = manager.update_task_progress(title, status, note)
    if task:
        click.echo(f"Updated task status: {title} -> {status}")
        
        # Save updated task to memory
        memory_bank = MemoryBank(str(manager.project_path))
        memory_bank.save_task_memory({
            task.title: {
                "id": task.id,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "dependencies": task.dependencies,
                "tags": task.tags,
                "priority": task.priority,
                "notes": task.notes
            }
        })

@base.command()
def list_tasks():
    """List all tasks."""
    manager = get_manager()
    tasks = manager.list_tasks()
    
    # Format tasks for display
    task_list = []
    for task in sorted(tasks, key=lambda t: (t.status.value, t.title)):
        task_info = [f"{task.status.value}: {task.title}"]
        if task.description:
            task_info.append(f"  Description: {task.description}")
        if task.priority:
            task_info.append(f"  Priority: {task.priority}")
        task_list.append("\n".join(task_info))
    
    tasks_text = "\n".join(task_list) if task_list else "No tasks found"
    
    # Get and format prompt
    prompt = get_prompt_for_command("list-tasks")
    if prompt:
        # Calculate completion stats
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == TaskStatus.completed)
        in_progress = sum(1 for t in tasks if t.status == TaskStatus.in_progress)
        blocked = sum(1 for t in tasks if t.status == TaskStatus.blocked)
        
        context = {
            "tasks": tasks_text,
            "filter_status": "all",
            "project_timeline": "Current project status overview",
            "completion_stats": f"Total: {total_tasks}, Completed: {completed_tasks}, In Progress: {in_progress}, Blocked: {blocked}"
        }
        prompt = prompt.format(**context)
        print_prompt_info("list-tasks", prompt)
    
    # Print tasks
    if not tasks:
        click.echo("No tasks found")
    else:
        click.echo(tasks_text)

@base.command()
@click.option('--status', type=click.Choice([s.value for s in TaskStatus]), help='Filter by status')
def export_tasks(output_file):
    """Export tasks to a file."""
    manager = PromptManager(Path.cwd())
    
    # Get export context
    tasks = manager.list_tasks()
    project_metadata = manager.get_project_metadata()
    historical_exports = manager.get_historical_exports()
    
    # Get and format prompt
    prompt_template = get_prompt_for_command("export-tasks")
    if prompt_template:
        context = {
            "tasks": "\n".join(str(task) for task in tasks),
            "export_format": output_file.split('.')[-1],
            "export_path": output_file,
            "project_metadata": project_metadata,
            "historical_exports": historical_exports
        }
        prompt = prompt_template.format(**context)
        print_prompt_info("export-tasks", prompt)
    
    # Export tasks
    manager.export_tasks(output_file)
    click.echo(f"Exported tasks to: {output_file}")

@base.command()
@click.option('--path', default='.', help='Path to initialize project at')
def init(path: str):
    """Initialize a new project."""
    try:
        manager = PromptManager(path)
        if manager.init_project(path):
            click.echo(f"Initialized project at {path}")
    except Exception as e:
        click.echo(f"Error initializing project: {e}", err=True)
        raise click.Abort()

__all__ = ['base']
