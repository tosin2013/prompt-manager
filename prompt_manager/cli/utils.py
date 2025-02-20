"""Utility functions for the CLI."""

import click
from pathlib import Path
import sys
from functools import wraps
from prompt_manager import PromptManager
from prompt_manager.memory import MemoryBank
from prompt_manager.prompts import get_prompt_for_command

def print_prompt_info(prompt_name: str, prompt: str):
    """Print prompt information in a formatted way."""
    click.echo("\n" + "="*80)
    click.echo(f"Using prompt template: {prompt_name}")
    click.echo("="*80)
    click.echo(prompt)
    click.echo("="*80 + "\n")

def with_prompt_option(command_name):
    """Decorator to add --show-prompt option to commands.
    
    Args:
        command_name: Name of the command's prompt template
    """
    def decorator(f):
        # Add the show-prompt option to the command
        f = click.option('--show-prompt', is_flag=True, 
                        help='Show the prompt template being used')(f)
        
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Extract and remove show_prompt from kwargs
            show_prompt = kwargs.pop('show_prompt', False)
            
            # If show_prompt is True, display the prompt template first
            if show_prompt:
                prompt_template = get_prompt_for_command(command_name)
                if prompt_template:
                    print_prompt_info(command_name, prompt_template)
            
            # Call the original function
            return f(*args, **kwargs)
        return wrapper
    return decorator

def get_manager() -> PromptManager:
    """Get a PromptManager instance for the current directory."""
    ctx = click.get_current_context()
    project_dir = ctx.obj.get('project_dir', str(Path.cwd()))
    
    # Create memory directory if it doesn't exist
    memory_path = Path(project_dir) / "prompt_manager_data"
    memory_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize manager without auto-initialization
    manager = PromptManager(project_dir, memory_path=memory_path)
    return manager
