from typing import Optional
import json
import click

@command
def generate_bolt_tasks(task_description: str, framework: Optional[str] = None, output: Optional[str] = None):
    """Generate tasks for a bolt.new project."""
    try:
        # Get existing tasks for context
        existing_tasks = task_manager.list_tasks()
        
        # Generate tasks using LLM
        result = task_manager.llm.generate_tasks(
            description=task_description,
            framework=framework,
            existing_tasks=existing_tasks
        )
        
        tasks = result.get('tasks', [])
        
        # Print tasks to console
        click.echo("Generated tasks:")
        for task in tasks:
            click.echo(f"- {task}")
            
        # Export tasks to file if output is specified
        if output:
            task_data = {
                'description': task_description,
                'framework': framework,
                'tasks': tasks
            }
            with open(output, 'w') as f:
                json.dump(task_data, f, indent=2)
            click.echo(f"Tasks exported to {output}")
            
        return True
    except Exception as e:
        click.echo(f"Error generating bolt tasks: {str(e)}", err=True)
        return False

@command
def add_dependency(task_title: str, dependency_title: str):
    """Add a dependency between two tasks."""
    try:
        task_manager.add_dependency(task_title, dependency_title)
        click.echo(f"Added dependency: {task_title} -> {dependency_title}")
        return True
    except CircularDependencyError:
        click.echo("Error: Cannot add dependency - would create a circular dependency", err=True)
        return False
    except Exception as e:
        click.echo(f"Error adding dependency: {str(e)}", err=True)
        return False 