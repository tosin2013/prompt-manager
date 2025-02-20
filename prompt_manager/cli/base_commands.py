"""Base CLI commands."""

import click
from pathlib import Path
from prompt_manager import PromptManager, TaskStatus, MemoryBank
from prompt_manager.cli.utils import get_manager, with_prompt_option
from prompt_manager.prompts import get_prompt_for_command
from typing import Optional
import sys
import json

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
@click.argument('title', required=False)
@click.argument('description', required=False, default="")
@click.option('--title', 'title_opt', help='Task title')
@click.option('--description', 'desc_opt', help='Task description')
@click.option('--template', help='Template to use')
@click.option('--priority', type=int, default=0, help='Task priority')
@with_prompt_option('add-task')
def add_task(title: str = None, description: str = "", title_opt: str = None, desc_opt: str = None, template: str = None, priority: int = 0):
    """Add a new task.
    
    Args:
        title: Task title (positional)
        description: Task description (positional)
        title_opt: Task title (named)
        desc_opt: Task description (named)
        template: Optional task template
        priority: Task priority
    """
    # Use named arguments if provided, otherwise use positional
    final_title = title_opt if title_opt else title
    final_desc = desc_opt if desc_opt else description
    
    if not final_title:
        click.echo("Error: Task title is required", err=True)
        sys.exit(1)
    
    manager = get_manager()
    
    # Get existing tasks for context
    existing_tasks = manager.list_tasks()
    
    # Get and format prompt
    prompt = get_prompt_for_command("add-task")
    if prompt:
        context = {
            "title": final_title,
            "description": final_desc,
            "template": template or "none",
            "priority": priority,
            "existing_tasks": "\n".join(f"{t.status.value}: {t.title}" for t in existing_tasks)
        }
        prompt = prompt.format(**context)
        print_prompt_info("add-task", prompt)
    
    # Add the task
    task = manager.add_task(final_title, final_desc, template, priority)
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
        prompt = get_prompt_for_command("export-tasks")
        if prompt:
            context = {
                "tasks": "\n".join(str(task) for task in tasks),
                "export_format": output.split('.')[-1],
                "export_path": output,
                "project_metadata": project_metadata,
                "historical_exports": historical_exports
            }
            prompt = prompt.format(**context)
            print_prompt_info("export-tasks", prompt)
        
        # Export tasks
        manager.export_tasks(output)
        click.echo(f"Exported tasks to: {output}")
    except Exception as e:
        click.echo(f"Error exporting tasks: {str(e)}", err=True)
        sys.exit(1)

@base.command()
@click.option('--path', type=click.Path(), default='.', help='Path to initialize project at')
@with_prompt_option('init')
def init(path: str):
    """Initialize a new project.
    
    Args:
        path: Path to initialize project at (defaults to current directory)
    """
    try:
        path = str(Path(path).resolve())
        manager = get_manager()  # Use the utility function
        manager.init_project(path)  # Use init_project instead of initialize
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
    """Generate tasks for a bolt.new project."""
    try:
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
        result = manager.generate_bolt_tasks(description, framework)
        
        # Print tasks to console
        click.echo("Generated tasks:")
        for task in result:
            click.echo(f"- {task}")
        
        # Export tasks to file if output is specified
        if output:
            task_data = {
                'description': description,
                'framework': framework,
                'tasks': result
            }
            with open(output, 'w') as f:
                json.dump(task_data, f, indent=2)
            click.echo(f"Tasks exported to {output}")
            return True
        
        return True
    except Exception as e:
        click.echo(f"Error generating bolt tasks: {str(e)}", err=True)
        return False

@base.command()
@click.argument('task_title')
@click.argument('dependency_title')
@with_prompt_option('add-dependency')
def add_dependency(task_title: str, dependency_title: str):
    """Add a dependency between tasks."""
    try:
        manager = get_manager()
        
        # Get tasks
        task = manager.get_task(task_title)
        dependency = manager.get_task(dependency_title)
        
        if not task or not dependency:
            raise ValueError("Task not found")
        
        # Check for circular dependencies
        if dependency_title in task.dependencies or task_title in dependency.dependencies:
            raise ValueError("Circular dependency detected")
        
        # Add dependency
        task.dependencies.append(dependency_title)
        manager._save_tasks()
        
        click.echo(f"Added dependency: {task_title} -> {dependency_title}")
    except Exception as e:
        click.echo(f"Error adding dependency: {str(e)}", err=True)
        sys.exit(1)

@base.command()
@click.argument('task_title')
@with_prompt_option('list-dependencies')
def list_dependencies(task_title: str):
    """List task dependencies."""
    try:
        manager = get_manager()
        task = manager.get_task(task_title)
        
        if not task:
            raise ValueError("Task not found")
        
        if not task.dependencies:
            click.echo("No dependencies")
            return
        
        for dep in task.dependencies:
            click.echo(dep)
    except Exception as e:
        click.echo(f"Error listing dependencies: {str(e)}", err=True)
        sys.exit(1)

@base.command()
@click.option('--status', type=click.Choice([s.value for s in TaskStatus]), help='Filter by status')
@click.option('--sort-by', type=click.Choice(['priority', 'status']), help='Sort tasks by field')
@with_prompt_option('list-tasks')
def list_tasks(status: Optional[str] = None, sort_by: Optional[str] = None):
    """List tasks with filtering and sorting."""
    manager = get_manager()
    tasks = manager.list_tasks()
    
    # Apply status filter
    if status:
        tasks = [t for t in tasks if t.status.value == status]
    
    # Apply sorting
    if sort_by:
        if sort_by == 'priority':
            tasks.sort(key=lambda t: t.priority)
        elif sort_by == 'status':
            tasks.sort(key=lambda t: t.status.value)
    
    # Format tasks for display
    task_list = []
    for task in tasks:
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
            "filter_status": status or "all",
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
@click.argument('message')
@with_prompt_option('update-context')
def update_context(message: str):
    """Update project context with a message."""
    try:
        manager = get_manager()
        manager.memory.update_context_memory({"message": message})
        click.echo("Context updated")
    except Exception as e:
        click.echo(f"Error updating context: {str(e)}", err=True)
        sys.exit(1)

@base.command()
@with_prompt_option('backup-memory')
def backup_memory():
    """Create a backup of memory files."""
    try:
        manager = get_manager()
        backup_path = manager.memory.create_backup()
        click.echo(f"Memory backup created at {backup_path}")
    except Exception as e:
        click.echo(f"Error creating backup: {str(e)}", err=True)
        sys.exit(1)

@base.command()
@click.option('--backup', default='latest', help='Backup to restore from')
@with_prompt_option('restore-memory')
def restore_memory(backup: str):
    """Restore memory from a backup."""
    try:
        manager = get_manager()
        manager.memory.restore_backup(backup)
        click.echo(f"Memory restored from backup: {backup}")
    except Exception as e:
        click.echo(f"Error restoring backup: {str(e)}", err=True)
        sys.exit(1)

__all__ = ['base']
