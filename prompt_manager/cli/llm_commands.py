"""CLI commands for LLM Enhancement functionality."""
import click
from pathlib import Path
from typing import List, Optional
from prompt_manager.llm_enhancement import LLMEnhancement


@click.group()
def llm():
    """LLM Enhancement commands."""
    pass


@llm.command()
@click.option('--duration', type=int, help='Duration in minutes (default: continuous)')
def learn_session(duration: Optional[int]):
    """Start an autonomous learning session."""
    try:
        from prompt_manager import PromptManager
        pm = PromptManager.get_current()
        llm = pm.llm_enhancement
        
        llm.start_learning_session()
        click.echo("Started learning session")
        
        if duration:
            import time
            time.sleep(duration * 60)
            click.echo(f"Learning session completed after {duration} minutes")
            
    except Exception as e:
        click.echo(f"Error starting learning session: {str(e)}", err=True)
        raise click.Abort()


@llm.command()
@click.option('--path', type=click.Path(exists=True), help='Path to analyze')
@click.option('--max-suggestions', type=int, default=10, help='Maximum number of suggestions')
def suggest_improvements(path: Optional[str], max_suggestions: int):
    """Generate code improvement suggestions."""
    try:
        from prompt_manager import PromptManager
        pm = PromptManager.get_current()
        llm = pm.llm_enhancement
        
        target_path = Path(path) if path else Path.cwd()
        suggestions = llm.generate_suggestions()
        
        if not suggestions:
            click.echo("No improvements suggested")
            return
            
        for i, suggestion in enumerate(suggestions[:max_suggestions], 1):
            click.echo(f"\nSuggestion {i}:")
            click.echo(f"Title: {suggestion}")
            
    except Exception as e:
        click.echo(f"Error generating suggestions: {str(e)}", err=True)
        raise click.Abort()


@llm.command()
@click.option('--title', required=True, help='Pull request title')
@click.option('--description', required=True, help='Pull request description')
@click.option('--changes', required=True, multiple=True, type=click.Path(exists=True),
              help='Files to include in the pull request')
def create_pr(title: str, description: str, changes: List[str]):
    """Create a pull request from suggestions."""
    try:
        from prompt_manager import PromptManager
        pm = PromptManager.get_current()
        llm = pm.llm_enhancement
        
        # Prepare changes
        change_dict = {}
        for file_path in changes:
            path = Path(file_path)
            with open(path, 'r') as f:
                change_dict[str(path)] = f.read()
                
        # Create suggestion
        suggestion = llm.suggest_pull_request(
            changes=[change_dict],
            title=title,
            description=description
        )
        
        if not suggestion:
            click.echo("Failed to create pull request suggestion")
            raise click.Abort()
            
        # Create PR
        success, message = llm.create_pull_request(suggestion)
        if success:
            click.echo(f"Successfully created pull request: {message}")
        else:
            click.echo(f"Failed to create pull request: {message}", err=True)
            raise click.Abort()
            
    except Exception as e:
        click.echo(f"Error creating pull request: {str(e)}", err=True)
        raise click.Abort()


@llm.command()
@click.option('--files', required=True, multiple=True, type=click.Path(exists=True),
              help='Files to analyze')
def analyze_impact(files: List[str]):
    """Analyze the potential impact of changes."""
    try:
        from prompt_manager import PromptManager
        pm = PromptManager.get_current()
        llm = pm.llm_enhancement
        
        # Prepare changes for analysis
        changes = []
        for file_path in files:
            path = Path(file_path)
            with open(path, 'r') as f:
                changes.append({str(path): f.read()})
                
        # Analyze impact
        impact = llm._analyze_change_impact(changes)
        
        click.echo("\nImpact Analysis:")
        for file_path, impact_level in impact.items():
            click.echo(f"{file_path}: {impact_level}")
            
    except Exception as e:
        click.echo(f"Error analyzing impact: {str(e)}", err=True)
        raise click.Abort()


@llm.command()
@click.option('--output', type=click.Path(), help='Path to save generated commands')
def generate_commands(output: Optional[str]):
    """Generate custom CLI commands based on usage patterns."""
    try:
        from prompt_manager import PromptManager
        pm = PromptManager.get_current()
        llm = pm.llm_enhancement
        
        commands = llm.create_custom_commands()
        
        if not commands:
            click.echo("No commands generated")
            return
            
        if output:
            output_path = Path(output)
            output_path.write_text('\n\n'.join(commands))
            click.echo(f"Commands saved to {output}")
        else:
            click.echo("\nGenerated Commands:")
            for command in commands:
                click.echo(f"\n{command}")
                
    except Exception as e:
        click.echo(f"Error generating commands: {str(e)}", err=True)
        raise click.Abort()
