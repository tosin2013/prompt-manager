"""Self-improvement CLI commands for Prompt Manager."""

import click
from pathlib import Path
import subprocess
from typing import Optional
from prompt_manager.cli.utils import get_manager
from prompt_manager.prompts import get_prompt_for_command

@click.group()
def improve():
    """Self-improvement commands."""
    pass

@improve.command()
@click.argument('target', type=click.Path(exists=True))
@click.option('--type', 'improvement_type', type=click.Choice(['tests', 'commands', 'plugins']), default='tests')
@click.option('--create-pr/--no-pr', default=True, help='Create a pull request with improvements')
def enhance(target: str, improvement_type: str, create_pr: bool):
    """Enhance the system by analyzing and improving specified components.
    
    TARGET: Path to the component to enhance (file or directory)
    """
    manager = get_manager()
    
    try:
        # Get enhancement prompt template
        prompt_template = get_prompt_for_command("enhance-system")
        if not prompt_template:
            raise click.ClickException("Enhancement prompt template not found")
            
        # Get current state
        if improvement_type == 'tests':
            current_state = _get_test_coverage(target)
        elif improvement_type == 'commands':
            current_state = _get_command_coverage(target)
        else:  # plugins
            current_state = _get_plugin_info(target)
            
        # Format prompt with context
        context = {
            'target_path': target,
            'improvement_type': improvement_type,
            'current_state': current_state,
            'system_capabilities': _get_system_capabilities()
        }
        
        prompt = prompt_template.format(**context)
        
        # Get enhancement suggestions
        enhancements = manager.llm.suggest_improvements(prompt)
        
        if create_pr:
            # Create branch for improvements
            branch_name = f"enhancement/{improvement_type}-{Path(target).stem}"
            _create_branch(branch_name)
            
            # Apply enhancements
            for enhancement in enhancements:
                if enhancement.get('type') == 'new_file':
                    _create_file(enhancement['path'], enhancement['content'])
                elif enhancement.get('type') == 'modify_file':
                    _modify_file(enhancement['path'], enhancement['changes'])
                    
            # Create pull request
            _create_pull_request(
                branch_name,
                f"Enhancement: {improvement_type} improvements for {Path(target).name}",
                f"Automated enhancement of {improvement_type} for {target}\n\n" + \
                "Changes made:\n" + \
                "\n".join(f"- {e['description']}" for e in enhancements)
            )
            
            click.echo(f"Created pull request for {improvement_type} improvements")
        else:
            # Just show suggestions
            click.echo("\nSuggested Improvements:")
            for enhancement in enhancements:
                click.echo(f"\n- {enhancement['description']}")
                if 'code' in enhancement:
                    click.echo("\nProposed changes:")
                    click.echo(enhancement['code'])
                    
    except Exception as e:
        raise click.ClickException(f"Error enhancing system: {str(e)}")

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