"""Debug CLI commands."""

import click
import sys
from pathlib import Path
from prompt_manager import PromptManager
from prompt_manager.cli.utils import get_manager, with_prompt_option
from prompt_manager.prompts import get_prompt_for_command
from typing import Optional

def print_prompt_info(prompt_name: str, prompt: str):
    """Print prompt information in a formatted way."""
    click.echo("\n" + "="*80)
    click.echo(f"Using prompt template: {prompt_name}")
    click.echo("="*80)
    click.echo(prompt)
    click.echo("="*80 + "\n")

@click.group()
def debug():
    """Debug commands."""
    pass

@debug.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', help='Output file path')
@with_prompt_option('analyze-file')
def analyze_file(file_path: str, output: Optional[str] = None):
    """Analyze a file for potential issues."""
    manager = get_manager()
    try:
        # Read file content
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # Get project context
        project_context = "Python CLI Application"  # This should be determined dynamically
        tech_stack = "Python, Click, YAML"  # This should be determined dynamically
        previous_analyses = "No previous analyses found"  # This should be loaded from history
        
        # Get and format prompt
        prompt_template = get_prompt_for_command("analyze-file")
        if prompt_template:
            context = {
                "file_path": file_path,
                "context_lines": 5,
                "file_content": file_content,
                "project_context": project_context,
                "tech_stack": tech_stack,
                "previous_analyses": previous_analyses
            }
            prompt = prompt_template.format(**context)
            print_prompt_info("analyze-file", prompt)
        
        # Run analysis
        analysis = manager.analyze_file(file_path)
        
        if output:
            Path(output).write_text(analysis)
            click.echo(f"Analysis written to {output}")
        else:
            click.echo(analysis)
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error analyzing file: {str(e)}", err=True)
        sys.exit(2)

@debug.command()
@click.argument('error_log', type=click.Path(exists=True))
@click.option('--output', help='Output file path')
@with_prompt_option('find-root-cause')
def find_root_cause(error_log: str, output: Optional[str] = None):
    """Find root cause from error log."""
    manager = get_manager()
    try:
        # Get and format prompt
        prompt_template = get_prompt_for_command("find-root-cause")
        if prompt_template:
            context = {
                "error_message": error_log,
                "file_path": ""
            }
            prompt = prompt_template.format(**context)
            print_prompt_info("find-root-cause", prompt)
        
        # Find root cause
        analysis = manager.analyze_error_log(error_log)
        
        if output:
            Path(output).write_text(analysis)
            click.echo(f"Analysis written to {output}")
        else:
            click.echo(analysis)
    except Exception as e:
        click.echo(f"Error finding root cause: {str(e)}", err=True)
        sys.exit(1)

@debug.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', help='Output file path')
@with_prompt_option('test-roadmap')
def test_roadmap(file_path: str, output: Optional[str] = None):
    """Generate test roadmap for a file."""
    manager = get_manager()
    try:
        # Read file content
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # Get test context
        test_framework = "pytest"  # This should be determined from project config
        existing_tests = "No existing tests found"  # This should be loaded from test directory
        coverage_report = "No coverage report available"  # This should be generated from pytest-cov
        project_requirements = "Standard unit test coverage required"  # This should be loaded from project config
        
        # Get and format prompt
        prompt_template = get_prompt_for_command("test-roadmap")
        if prompt_template:
            context = {
                "file_path": file_path,
                "file_content": file_content,
                "test_framework": test_framework,
                "existing_tests": existing_tests,
                "coverage_report": coverage_report,
                "project_requirements": project_requirements
            }
            prompt = prompt_template.format(**context)
            print_prompt_info("test-roadmap", prompt)
        
        # Generate roadmap
        roadmap = manager.generate_test_roadmap(file_path)
        
        if output:
            Path(output).write_text(roadmap)
            click.echo(f"Test roadmap written to {output}")
        else:
            click.echo(roadmap)
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating test roadmap: {str(e)}", err=True)
        sys.exit(2)

@debug.command()
@click.argument('file_path')
def analyze_dependencies(file_path):
    """Analyze dependencies of a file."""
    manager = get_manager()
    try:
        # Get dependency context
        direct_deps = manager.get_direct_dependencies(file_path)
        indirect_deps = manager.get_indirect_dependencies(file_path)
        dep_graph = manager.get_dependency_graph(file_path)
        
        # Get and format prompt
        prompt_template = get_prompt_for_command("analyze-dependencies")
        if prompt_template:
            context = {
                "file_path": file_path,
                "direct_dependencies": direct_deps,
                "indirect_dependencies": indirect_deps,
                "dependency_graph": dep_graph,
                "system_packages": manager.get_system_packages()
            }
            prompt = prompt_template.format(**context)
            print_prompt_info("analyze-dependencies", prompt)
        
        # Run analysis
        analysis = manager.analyze_dependencies(file_path)
        click.echo(f"Dependency analysis for {file_path}:")
        click.echo(analysis)
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error analyzing dependencies: {str(e)}", err=True)
        sys.exit(2)

@debug.command()
@click.argument('error_message')
@click.option('--file-path', help='Path to file with error')
@click.option('--max-depth', type=int, default=5, help='Maximum trace depth')
def trace_error(error_message, file_path=None, max_depth=5):
    """Trace error through the codebase."""
    manager = get_manager()
    try:
        # Get trace context
        error_context = manager.get_error_context(error_message, file_path)
        call_stack = manager.get_call_stack()
        error_history = manager.get_error_history()
        
        # Get and format prompt
        prompt_template = get_prompt_for_command("trace-error")
        if prompt_template:
            context = {
                "error_message": error_message,
                "file_path": file_path or "unknown",
                "max_depth": max_depth,
                "error_context": error_context,
                "call_stack": call_stack,
                "error_history": error_history
            }
            prompt = prompt_template.format(**context)
            print_prompt_info("trace-error", prompt)
        
        # Trace error
        trace = manager.trace_error(error_message, file_path, max_depth)
        click.echo("Error trace:")
        click.echo(trace)
    except Exception as e:
        click.echo(f"Error tracing error: {str(e)}", err=True)
        sys.exit(1)

__all__ = ['debug']
