"""Test base CLI commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
from prompt_manager import TaskStatus
from prompt_manager.cli import cli
from prompt_manager.manager import PromptManager
from pathlib import Path
import tempfile
import os


pytestmark = [pytest.mark.cli, pytest.mark.cli_base]


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for project testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        yield Path(tmpdir)
        os.chdir(original_dir)


@pytest.fixture(autouse=True)
def setup_project_dir(temp_project_dir):
    """Automatically set up project directory for all tests."""
    os.makedirs(temp_project_dir / "prompt_manager_data", exist_ok=True)
    yield


@pytest.fixture
def mock_prompt_manager():
    """Create a mock PromptManager."""
    with patch('prompt_manager.cli.base_commands.PromptManager') as mock:
        manager = Mock()
        mock.return_value = manager
        yield manager


def test_version(runner):
    """Test --version flag."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.3.18" in result.output


def test_help(runner):
    """Test --help flag."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_init_command(runner, temp_project_dir):
    """Test init command."""
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert "initialized successfully" in result.output.lower()


def test_init_command_error(runner, temp_project_dir):
    """Test init command with invalid path."""
    result = runner.invoke(cli, ["init", "--path", "/nonexistent/path"])
    assert result.exit_code == 1
    assert "does not exist" in result.output.lower()


def test_add_task_command(runner, mock_prompt_manager, temp_project_dir):
    """Test add-task command."""
    result = runner.invoke(cli, ['add-task', 'test task', '--priority', 'high'])
    assert result.exit_code == 0
    mock_prompt_manager.add_task.assert_called_once_with('test task', priority='high')


def test_list_tasks_command(runner, mock_prompt_manager, temp_project_dir):
    """Test list-tasks command."""
    mock_prompt_manager.list_tasks.return_value = [
        {'title': 'test task', 'priority': 'high', 'status': TaskStatus.TODO}
    ]
    result = runner.invoke(cli, ['list-tasks'])
    assert result.exit_code == 0
    assert 'test task' in result.output.lower()


def test_list_tasks_with_tasks(runner, mock_prompt_manager, temp_project_dir):
    """Test list-tasks command with existing tasks."""
    mock_prompt_manager.list_tasks.return_value = [
        {'title': 'test task', 'priority': 'high', 'status': TaskStatus.TODO}
    ]
    result = runner.invoke(cli, ['list-tasks'])
    assert result.exit_code == 0
    assert 'test task' in result.output.lower()


def test_update_progress_command(runner, mock_prompt_manager, temp_project_dir):
    """Test update-progress command."""
    result = runner.invoke(
        cli,
        [
            "update-progress",
            "Test Task",
            "in_progress",
            "--note",
            "Working on it",
        ],
    )

    assert result.exit_code == 0
    assert "status updated" in result.output.lower()


def test_export_tasks_command(runner, mock_prompt_manager, temp_project_dir):
    """Test export-tasks command."""
    result = runner.invoke(cli, ["export-tasks", "--output", str(temp_project_dir / "tasks.json")])

    assert result.exit_code == 0
    assert "exported" in result.output.lower()


def test_list_tasks_empty(mock_prompt_manager, runner, temp_project_dir):
    """Test listing tasks when no tasks exist."""
    result = runner.invoke(cli, ["list-tasks"])
    assert result.exit_code == 0
    assert "no tasks found" in result.output.lower()


def test_list_tasks_with_tasks(mock_prompt_manager, runner, temp_project_dir):
    """Test listing tasks when tasks exist."""
    mock_prompt_manager.list_tasks.return_value = [
        {'title': 'test task', 'priority': 'high', 'status': TaskStatus.TODO}
    ]

    result = runner.invoke(cli, ["list-tasks"])
    assert result.exit_code == 0
    assert "test task" in result.output.lower()
    assert "medium" in result.output.lower()
