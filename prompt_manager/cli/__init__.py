"""CLI package for Prompt Manager."""
import click
from prompt_manager.cli.llm_commands import llm


@click.group()
def cli():
    """Prompt Manager CLI."""
    pass


# Add command groups
cli.add_command(llm)

if __name__ == '__main__':
    cli()
