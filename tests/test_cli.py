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
    TASK_ADDED_MSG,
    TASK_STATUS_UPDATED_MSG,
    DEFAULT_EXPORT_PATH,
)


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


def test_analyze_repo(cli_runner, test_data_dir):
    """Test repository analysis command."""
    result = cli_runner.invoke(cli, ["analyze-repo", str(test_data_dir)])
    assert result.exit_code == 0
    assert "Repository analysis complete" in result.output


def test_add_task(cli_runner, test_data_dir):
    """Test task addition command."""
    result = cli_runner.invoke(cli, ['--project-dir', test_data_dir, 'add-task',
                                   '--title', TASK_TITLE,
                                   '--description', TASK_DESCRIPTION,
                                   '--template', TASK_TEMPLATE,
                                   '--priority', TASK_PRIORITY])
    assert result.exit_code == 0
    assert TASK_ADDED_MSG in result.output


def test_update_progress(cli_runner, test_data_dir):
    """Test task progress update command."""
    # First add a task
    cli_runner.invoke(cli, ['--project-dir', test_data_dir, 'add-task',
                          '--title', TASK_TITLE,
                          '--description', TASK_DESCRIPTION,
                          '--template', TASK_TEMPLATE,
                          '--priority', TASK_PRIORITY])
    
    # Then update its status
    result = cli_runner.invoke(cli, ['--project-dir', test_data_dir, 'update-progress',
                                   '--title', TASK_TITLE,
                                   '--status', TASK_STATUS_IN_PROGRESS])
    assert result.exit_code == 0
    assert TASK_STATUS_UPDATED_MSG in result.output


def test_list_tasks(cli_runner, test_data_dir):
    """Test task listing command."""
    # First add a task
    cli_runner.invoke(cli, ['--project-dir', test_data_dir, 'add-task',
                          '--title', TASK_TITLE,
                          '--description', TASK_DESCRIPTION,
                          '--template', TASK_TEMPLATE,
                          '--priority', TASK_PRIORITY])
    
    # Then list all tasks
    result = cli_runner.invoke(cli, ['--project-dir', test_data_dir, 'list-tasks'])
    assert result.exit_code == 0
    assert TASK_TITLE in result.output


def test_export_tasks(cli_runner, test_data_dir):
    """Test task export command."""
    result = cli_runner.invoke(cli, ['--project-dir', test_data_dir, 'export-tasks',
                                   '--output', DEFAULT_EXPORT_PATH])
    assert result.exit_code == 0
    assert f"Tasks exported successfully to {DEFAULT_EXPORT_PATH}" in result.output


def test_invalid_commands(cli_runner):
    """Test handling of invalid commands and options."""
    # Test invalid command
    result = cli_runner.invoke(cli, ["invalid-command"])
    assert result.exit_code != 0
    assert "No such command" in result.output

    # Test missing required argument
    result = cli_runner.invoke(cli, ["add-task"])
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


def test_generate_bolt_tasks(cli_runner, test_data_dir):
    """Test bolt.new task generation command."""
    # First initialize a project
    result = cli_runner.invoke(cli, ["init", "--path", str(test_data_dir)])
    assert result.exit_code == 0

    # Generate bolt tasks
    result = cli_runner.invoke(
        cli,
        [
            "generate-bolt-tasks",
            "Create a blog application",
            "--framework",
            "Next.js",
        ],
    )
    assert result.exit_code == 0

    # Verify output contains all tasks
    assert "Initial Project Setup" in result.output
    assert "UI Component Development" in result.output
    assert "API Integration" in result.output
    assert "Testing Implementation" in result.output
    assert "Deployment Setup" in result.output

    # Verify framework is set correctly
    assert "Framework: Next.js" in result.output

    # Verify prompt formatting
    assert "Project Requirements" in result.output
    assert "Technical Stack" in result.output
    assert "Development Instructions" in result.output
