"""Tests for base CLI commands."""

import pytest
import tempfile
import os
from pathlib import Path
from click.testing import CliRunner
from prompt_manager.cli import cli
from prompt_manager.cli.base_commands import add_task, update_progress, list_tasks, export_tasks
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

pytestmark = [pytest.mark.cli, pytest.mark.cli_base]


@pytest.fixture
def cli_runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def test_data_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        os.makedirs(path / "prompt_manager_data", exist_ok=True)
        yield path


def test_add_task(cli_runner, test_data_dir):
    """Test adding a new task."""
    # First initialize the project
    cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'init'])
    
    # Then add a task
    result = cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'add-task',
                                   '--title', TASK_TITLE,
                                   '--description', TASK_DESCRIPTION,
                                   '--template', TASK_TEMPLATE,
                                   '--priority', TASK_PRIORITY])
    assert result.exit_code == 0
    assert TASK_ADDED_MSG in result.output


def test_update_progress(cli_runner, test_data_dir):
    """Test updating task progress."""
    # First initialize the project
    cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'init'])
    
    # Add a task
    cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'add-task',
                          '--title', TASK_TITLE,
                          '--description', TASK_DESCRIPTION,
                          '--template', TASK_TEMPLATE,
                          '--priority', TASK_PRIORITY])
    
    # Then update its status
    result = cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'update-progress',
                                   '--title', TASK_TITLE,
                                   '--status', TASK_STATUS_IN_PROGRESS])
    assert result.exit_code == 0
    assert TASK_STATUS_UPDATED_MSG in result.output


def test_list_tasks(cli_runner, test_data_dir):
    """Test listing tasks."""
    # First initialize the project
    cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'init'])
    
    # Add a task
    cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'add-task',
                          '--title', TASK_TITLE,
                          '--description', TASK_DESCRIPTION,
                          '--template', TASK_TEMPLATE,
                          '--priority', TASK_PRIORITY])
    
    # Then list all tasks
    result = cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'list-tasks'])
    assert result.exit_code == 0
    assert TASK_TITLE in result.output


def test_export_tasks(cli_runner, test_data_dir):
    """Test exporting tasks."""
    # First initialize the project
    cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'init'])
    
    # Add a task
    cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'add-task',
                          '--title', TASK_TITLE,
                          '--description', TASK_DESCRIPTION,
                          '--template', TASK_TEMPLATE,
                          '--priority', TASK_PRIORITY])
    
    # Then export tasks
    export_path = test_data_dir / DEFAULT_EXPORT_PATH
    result = cli_runner.invoke(cli, ['--project-dir', str(test_data_dir), 'export-tasks',
                                   '--output', str(export_path)])
    assert result.exit_code == 0
    assert f"Tasks exported successfully to {export_path}" in result.output
