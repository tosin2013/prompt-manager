"""Base CLI commands."""

import click
from pathlib import Path
from prompt_manager import PromptManager, TaskStatus, MemoryBank
from prompt_manager.cli.utils import get_manager, with_prompt_option
from prompt_manager.prompts import get_prompt_for_command
from typing import Optional
import sys

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
@with_prompt_option('add-task')
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
@with_prompt_option('update-progress')
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
@with_prompt_option('list-tasks')
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
@click.option('--output', '-o', required=True, type=click.Path(), help='Output file path')
@with_prompt_option('export-tasks')
def export_tasks(output: str):
    """Export tasks to a file."""
    try:
        manager = get_manager()
        
        # Get tasks and metadata
        tasks = manager.list_tasks()
        project_metadata = manager.get_project_metadata()
        historical_exports = manager.get_historical_exports()
        
        # Format context for prompt if needed
        if get_prompt_for_command("export-tasks"):
            context = {
                "tasks": "\n".join(str(task) for task in tasks),
                "export_format": output.split('.')[-1],
                "export_path": output,
                "project_metadata": project_metadata,
                "historical_exports": historical_exports
            }
            prompt = get_prompt_for_command("export-tasks")
            if prompt:
                prompt = prompt.format(**context)
                print_prompt_info("export-tasks", prompt)
        
        # Export tasks
        manager.export_tasks(output)
        click.echo(f"Exported tasks to: {output}")
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}", err=True)
        sys.exit(1)

@base.command()
@click.argument('path', type=click.Path(), default='.')
@with_prompt_option('init')
def init(path: str):
    """Initialize a new project.
    
    Args:
        path: Path to initialize project at (defaults to current directory)
    """
    try:
        manager = PromptManager(path)
        if manager.init_project(path):
            click.echo(f"Initialized project at {path}")
    except Exception as e:
        click.echo(f"Error initializing project: {e}", err=True)
        sys.exit(1)

@base.command()
@click.argument('description')
@click.option('--framework', '-f', help='Target framework')
@click.option('--output', help='Output file path')
@with_prompt_option('generate-bolt-tasks')
def generate_bolt_tasks(description: str, framework: Optional[str] = None, output: Optional[str] = None):
    """Generate bolt.new tasks."""
    manager = get_manager()
    
    # Get and format prompt
    prompt_template = get_prompt_for_command("generate-bolt-tasks")
    if prompt_template:
        context = {
            "description": description,
            "framework": framework or "any",
            "existing_tasks": "\n".join(str(task) for task in manager.list_tasks())
        }
        prompt = prompt_template.format(**context)
        print_prompt_info("generate-bolt-tasks", prompt)
    
    # Generate tasks
    tasks = manager.generate_bolt_tasks(description, framework)
    if tasks:
        click.echo("Generated tasks:")
        for task in tasks:
            click.echo(f"- {task}")
    else:
        click.echo("No tasks generated")

    if output:
        path = manager.export_tasks(output)
        click.echo(f"Tasks exported to {path}")

__all__ = ['base']
