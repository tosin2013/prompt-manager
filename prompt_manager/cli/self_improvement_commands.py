"""Self-improvement CLI commands for Prompt Manager."""

import click
from pathlib import Path
import subprocess
from typing import Optional
from prompt_manager.cli.utils import get_manager, with_prompt_option
from prompt_manager.prompts import get_prompt_for_command

@click.group()
def improve():
    """Self-improvement commands."""
    pass

@improve.command()
@click.argument('target_path', type=click.Path(exists=True))
@click.option('--type', 'enhancement_type', type=click.Choice(['tests', 'commands', 'plugins']), required=True)
@click.option('--no-pr', is_flag=True, help='Skip creating PR')
@click.option('--output', help='Output file path')
@with_prompt_option('enhance-system')
def enhance(target_path: str, enhancement_type: str, no_pr: bool = False, output: Optional[str] = None):
    """Enhance system components."""
    manager = get_manager()
    enhancements = manager.enhance_system(target_path, enhancement_type, create_pr=not no_pr)
    
    if output:
        Path(output).write_text(enhancements)
        click.echo(f"Enhancements written to {output}")
    else:
        click.echo(enhancements)

def _get_test_coverage(path: str) -> dict:
    """Get current test coverage information."""
    try:
        # Run pytest with coverage
        result = subprocess.run(
            ['pytest', '--cov=' + path, '--cov-report=json', '-v'],
            capture_output=True,
            text=True
        )
        return {
            'coverage_report': result.stdout,
            'test_output': result.stderr
        }
    except Exception as e:
        return {'error': str(e)}

def _get_command_coverage(path: str) -> dict:
    """Get information about CLI commands and their coverage."""
    try:
        # Get all commands
        result = subprocess.run(
            ['prompt-manager', '--help'],
            capture_output=True,
            text=True
        )
        return {
            'available_commands': result.stdout,
            'command_path': path
        }
    except Exception as e:
        return {'error': str(e)}

def _get_plugin_info(path: str) -> dict:
    """Get information about existing plugins."""
    try:
        plugins_dir = Path(path)
        return {
            'plugins': [p.name for p in plugins_dir.glob('*.py')],
            'plugin_path': str(plugins_dir)
        }
    except Exception as e:
        return {'error': str(e)}

def _get_system_capabilities() -> dict:
    """Get current system capabilities."""
    return {
        'can_create_files': True,
        'can_modify_files': True,
        'can_create_pr': True,
        'can_run_tests': True,
        'can_analyze_code': True
    }

def _create_branch(branch_name: str) -> None:
    """Create and checkout a new git branch."""
    subprocess.run(['git', 'checkout', '-b', branch_name], check=True)

def _create_file(path: str, content: str) -> None:
    """Create a new file with given content."""
    Path(path).write_text(content)

def _modify_file(path: str, changes: list) -> None:
    """Apply changes to an existing file."""
    file_path = Path(path)
    if not file_path.exists():
        raise click.ClickException(f"File not found: {path}")
        
    content = file_path.read_text()
    for change in changes:
        if change['type'] == 'replace':
            content = content.replace(change['old'], change['new'])
        elif change['type'] == 'append':
            content += '\n' + change['content']
        elif change['type'] == 'prepend':
            content = change['content'] + '\n' + content
            
    file_path.write_text(content)

def _create_pull_request(branch_name: str, title: str, description: str) -> None:
    """Create a pull request with the changes."""
    # Add all changes
    subprocess.run(['git', 'add', '.'], check=True)
    
    # Commit changes
    subprocess.run(['git', 'commit', '-m', title], check=True)
    
    # Push branch
    subprocess.run(['git', 'push', '-u', 'origin', branch_name], check=True)
    
    # Create PR (using gh cli if available)
    try:
        subprocess.run(
            ['gh', 'pr', 'create', '--title', title, '--body', description],
            check=True
        )
    except Exception:
        click.echo(
            "Could not create PR automatically. Please create it manually:\n" +
            f"Branch: {branch_name}\n" +
            f"Title: {title}\n" +
            f"Description: {description}"
        )

__all__ = ['improve'] 