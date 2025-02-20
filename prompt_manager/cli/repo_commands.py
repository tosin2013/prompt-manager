"""Repository CLI commands."""

import click
import sys
from prompt_manager.repo_manager import RepoManager
from prompt_manager.prompts import get_prompt_for_command

def print_prompt_info(prompt_name: str, prompt: str):
    """Print prompt information in a formatted way."""
    click.echo("\n" + "="*80)
    click.echo(f"Using prompt template: {prompt_name}")
    click.echo("="*80)
    click.echo(prompt)
    click.echo("="*80 + "\n")

@click.group()
def repo():
    """Repository commands."""
    pass

@repo.command()
@click.argument('file_path')
def analyze_repo(file_path):
    """Analyze repository changes."""
    manager = RepoManager()
    try:
        # Get repo context
        stats = manager.get_repo_stats(file_path)
        current_branch = manager.get_current_branch(file_path)
        last_commit = manager.get_commit_history(file_path, limit=1)[0] if manager.get_commit_history(file_path) else "No commits"
        
        # Get and format prompt
        prompt_template = get_prompt_for_command("analyze-repo")
        if prompt_template:
            context = {
                "repo_path": file_path,
                "current_branch": current_branch,
                "last_commit": last_commit,
                "file_count": stats['total_files'],
                "main_languages": stats['languages'],
                "previous_analysis": "No previous analysis available"  # This should be loaded from history
            }
            prompt = prompt_template.format(**context)
            print_prompt_info("analyze-repo", prompt)
        
        # Run analysis
        analysis = manager.analyze_repo(file_path)
        click.echo(f"Repository analysis for {file_path}:")
        click.echo(analysis)
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error analyzing repository: {str(e)}", err=True)
        sys.exit(2)

@repo.command()
@click.argument('file_path')
@click.option('--duration', type=int, default=30, help='Duration in minutes')
def learn_session(file_path, duration):
    """Start a learning session for repository understanding."""
    manager = RepoManager()
    try:
        # Start session
        session = manager.learn_session(file_path, duration=duration)
        if 'error' in session:
            click.echo(f"Error: {session['error']}", err=True)
            sys.exit(1)

        # Display session information
        click.echo("\nLearning Session Started:")
        click.echo(f"Duration: {session['session']['duration']} minutes")
        click.echo(f"Start Time: {session['session']['start_time']}")
        click.echo(f"End Time: {session['session']['end_time']}")
        click.echo(f"Status: {'Active' if session['session']['is_active'] else 'Inactive'}")
        if session['session']['time_remaining']:
            click.echo(f"Time Remaining: {session['session']['time_remaining']}")

        # Get and format prompt
        prompt_template = get_prompt_for_command("learn-session")
        if prompt_template:
            context = session['template_context']
            try:
                prompt = prompt_template.format(**context)
                print_prompt_info("learn-session", prompt)
            except ValueError as e:
                click.echo(f"Error formatting prompt: {str(e)}", err=True)
                sys.exit(1)
        
        # Print repository stats
        click.echo("\nRepository Stats:")
        click.echo(f"Total Files: {session['stats'].get('total_files', 0)}")
        click.echo(f"Languages: {', '.join(session['stats'].get('languages', []))}")
        
        click.echo(f"\nCurrent Branch: {session['current_branch']}")
        
        click.echo("\nRecent Changes:")
        for change in session['recent_changes']:
            if 'error' in change:
                click.echo(f"Error getting changes: {change['error']}")
            else:
                click.echo(f"- [{change['date']}] {change['message']} (by {change['author']})")
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error starting learning session: {str(e)}", err=True)
        sys.exit(2)

__all__ = ['repo']
