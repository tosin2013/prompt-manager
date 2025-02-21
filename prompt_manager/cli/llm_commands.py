"""LLM-related CLI commands."""

import click
from pathlib import Path
import git
from typing import List, Dict, Optional
import os

from prompt_manager.cli.utils import get_manager, with_prompt_option
from prompt_manager.prompts import get_prompt_for_command, save_prompt_history, list_available_templates

def get_repo_info(repo_path: str) -> Dict[str, str]:
    """Get repository information for context."""
    repo = git.Repo(repo_path)
    
    # Count files
    file_count = sum(1 for _ in Path(repo_path).rglob('*') if _.is_file())
    
    # Get main languages
    extensions = {}
    for file in Path(repo_path).rglob('*'):
        if file.is_file():
            ext = file.suffix
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
    main_languages = sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "repo_path": repo_path,
        "current_branch": repo.active_branch.name,
        "last_commit": str(repo.head.commit.message),
        "file_count": str(file_count),
        "main_languages": ", ".join(f"{ext} ({count})" for ext, count in main_languages)
    }

@click.group()
def llm():
    """LLM commands."""
    pass

@llm.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', help='Output file path')
@with_prompt_option('analyze-impact')
def analyze_impact(file_path: str, output: Optional[str] = None):
    """Analyze impact of changes in a file."""
    manager = get_manager()
    prompt_template = get_prompt_for_command("analyze-impact")
    
    # Get file changes
    repo = git.Repo(manager.project_path, search_parent_directories=True)
    file_path = str(Path(file_path).resolve())
    rel_path = str(Path(file_path).relative_to(repo.working_dir))
    
    # Get changes using git diff
    changes = repo.git.diff(file_path)
    
    # Get dependencies (files that import or are imported by this file)
    dependencies = "TODO: Implement dependency analysis"
    
    # Get previous analysis from memory
    previous_analysis = manager.memory.load_context_memory().get("commandHistory", "No previous analysis found.")
    
    context = {
        "file_path": rel_path,
        "changes": changes,
        "dependencies": dependencies,
        "previous_analysis": previous_analysis
    }
    
    prompt = prompt_template.format(**context)
    
    # TODO: Send to LLM and get response
    response = "TODO: Implement LLM call"
    
    # Save to memory bank
    save_prompt_history(manager.memory, "analyze-impact", prompt, response)
    
    if output:
        Path(output).write_text(response)
        click.echo(f"Impact analysis written to {output}")
    else:
        click.echo(response)

@llm.command()
def analyze_repo():
    """Analyze repository changes."""
    manager = get_manager()
    prompt_template = get_prompt_for_command("analyze-repo")
    
    # Get repo info
    repo_info = get_repo_info(manager.project_path)
    
    # Get previous analysis from memory
    previous_analysis = manager.memory.load_context_memory().get("commandHistory", "No previous analysis found.")
    
    context = {
        **repo_info,
        "previous_analysis": previous_analysis
    }
    
    prompt = prompt_template.format(**context)
    
    # TODO: Send to LLM and get response
    response = "TODO: Implement LLM call"
    
    # Save to memory bank
    save_prompt_history(manager.memory, "analyze-repo", prompt, response)
    
    click.echo(response)

@llm.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', help='Output file path')
@with_prompt_option('generate-commands')
def generate_commands(file_path: str, output: Optional[str] = None):
    """Generate CLI commands from file."""
    manager = get_manager()
    prompt_template = get_prompt_for_command("generate-commands")
    
    file_path = Path(file_path).resolve()
    with open(file_path) as f:
        file_content = f.read()
    
    # Get command history from memory
    command_history = manager.memory.load_context_memory().get("commandHistory", "No previous commands found.")
    
    context = {
        "file_path": str(file_path),
        "file_content": file_content,
        "command_history": command_history
    }
    
    prompt = prompt_template.format(**context)
    
    # TODO: Send to LLM and get response
    response = "TODO: Implement LLM call"
    
    # Save to memory bank
    save_prompt_history(manager.memory, "generate-commands", prompt, response)
    
    if output:
        Path(output).write_text(response)
        click.echo(f"Commands written to {output}")
    else:
        click.echo(response)

@llm.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--max-suggestions', type=int, default=3, help='Maximum number of suggestions')
@click.option('--output', help='Output file path')
@with_prompt_option('suggest-improvements')
def suggest_improvements(file_path: str, max_suggestions: int = 3, output: Optional[str] = None):
    """Suggest code improvements."""
    manager = get_manager()
    prompt_template = get_prompt_for_command("suggest-improvements")
    
    file_path = Path(file_path).resolve()
    with open(file_path) as f:
        file_content = f.read()
    
    # Get previous suggestions from memory
    previous_suggestions = manager.memory.load_context_memory().get("commandHistory", "No previous suggestions found.")
    
    context = {
        "file_path": str(file_path),
        "file_content": file_content,
        "previous_suggestions": previous_suggestions,
        "max_suggestions": max_suggestions
    }
    
    prompt = prompt_template.format(**context)
    
    # TODO: Send to LLM and get response
    response = "TODO: Implement LLM call"
    
    # Save to memory bank
    save_prompt_history(manager.memory, "suggest-improvements", prompt, response)
    
    if output:
        Path(output).write_text(response)
        click.echo(f"Suggestions written to {output}")
    else:
        click.echo(response)

@llm.command()
@click.argument('title')
@click.argument('description')
@click.option('--branch', help='Branch name')
@click.option('--output', help='Output file path')
@with_prompt_option('create-pr')
def create_pr(title: str, description: str, branch: Optional[str] = None, output: Optional[str] = None):
    """Create a pull request."""
    manager = get_manager()
    prompt_template = get_prompt_for_command("create-pr")
    
    repo = git.Repo(manager.project_path, search_parent_directories=True)
    
    # Get changed files
    changed_files = repo.git.diff('--name-status')
    
    # Get recent commits
    commit_history = repo.git.log('--oneline', '-n', '5')
    
    # Get previous PRs from memory
    previous_prs = manager.memory.load_context_memory().get("commandHistory", "No previous PRs found.")
    
    context = {
        "title": title,
        "description": description,
        "changed_files": changed_files,
        "commit_history": commit_history,
        "previous_prs": previous_prs
    }
    
    prompt = prompt_template.format(**context)
    
    # TODO: Send to LLM and get response
    response = "TODO: Implement LLM call"
    
    # Save to memory bank
    save_prompt_history(manager.memory, "create-pr", prompt, response)
    
    if output:
        Path(output).write_text(response)
        click.echo(f"PR details written to {output}")
    else:
        click.echo(response)

@llm.command()
def list_templates():
    """List all available prompt templates."""
    from prompt_manager.prompts import list_available_templates
    
    templates = list_available_templates()
    if not templates:
        click.echo("No templates found.")
        return
        
    click.echo("\nAvailable prompt templates:")
    for template in templates:
        click.echo(f"\n{template['name']}:")
        click.echo(f"  Description: {template['description']}")
        click.echo(f"  Required context: {', '.join(template['required_context'])}")

__all__ = ['llm']
