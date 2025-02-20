"""
Tests for the CLI interface.
"""

import pytest
from click.testing import CliRunner
from prompt_manager.cli import cli
from tests.constants import (
    TASK_TITLE,
    TASK_DESCRIPTION,
    TASK_TEMPLATE,
    TASK_PRIORITY,
    TASK_STATUS_IN_PROGRESS,
    DEFAULT_EXPORT_PATH,
)


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def invoke_cli(cli_runner, test_data_dir):
    """Helper to invoke CLI with project directory."""
    def _invoke(command_args):
        args = ['--project-dir', str(test_data_dir)] + command_args
        return cli_runner.invoke(cli, args, obj={})
    return _invoke


def test_add_task(invoke_cli):
    """Test task addition command."""
    result = invoke_cli(['base', 'add-task',
                        TASK_TITLE,
                        TASK_DESCRIPTION,
                        '--template', TASK_TEMPLATE,
                        '--priority', 2])
    assert result.exit_code == 0
    assert f"Added task: {TASK_TITLE}" in result.output


def test_update_progress(invoke_cli):
    """Test task progress update command."""
    # First add a task
    invoke_cli(['base', 'add-task',
               TASK_TITLE,
               TASK_DESCRIPTION,
               '--template', TASK_TEMPLATE,
               '--priority', 2])
    
    # Then update its status
    result = invoke_cli(['base', 'update-progress',
                        TASK_TITLE,
                        TASK_STATUS_IN_PROGRESS.lower()])
    assert result.exit_code == 0
    assert f"Updated task {TASK_TITLE} to {TASK_STATUS_IN_PROGRESS.lower()}" in result.output


def test_list_tasks(invoke_cli):
    """Test task listing command."""
    # First add a task
    invoke_cli(['base', 'add-task',
               TASK_TITLE,
               TASK_DESCRIPTION,
               '--template', TASK_TEMPLATE,
               '--priority', 2])
    
    # Then list all tasks
    result = invoke_cli(['base', 'list-tasks'])
    assert result.exit_code == 0
    assert TASK_TITLE in result.output


def test_export_tasks(invoke_cli):
    """Test task export command."""
    result = invoke_cli(['base', 'export-tasks', DEFAULT_EXPORT_PATH])
    assert result.exit_code == 0
    assert f"Tasks exported to {DEFAULT_EXPORT_PATH}" in result.output


def test_invalid_commands(cli_runner):
    """Test handling of invalid commands and options."""
    # Test invalid command
    result = cli_runner.invoke(cli, ["invalid-command"])
    assert result.exit_code != 0
    assert "No such command" in result.output

    # Test missing required argument
    result = cli_runner.invoke(cli, ["base", "add-task"])
    assert result.exit_code != 0
    assert "Missing argument" in result.output


def test_help_command(cli_runner):
    """Test help command output."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output


def test_version_command(cli_runner):
    """Test version command output."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()
