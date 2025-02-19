"""Test repository CLI commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
from prompt_manager.cli import cli
from pathlib import Path
import tempfile
import os


pytestmark = [pytest.mark.cli, pytest.mark.cli_repo]


@pytest.fixture
def mock_repo_manager():
    """Create a mock RepoManager."""
    with patch('prompt_manager.cli.repo_commands.RepoManager') as mock:
        manager = Mock()
        mock.return_value = manager
        yield manager


def test_analyze_repo_command(runner, mock_repo_manager, temp_project_dir):
    """Test analyze-repo command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_repo_manager.analyze_repo.return_value = {
        'files': 1,
        'lines': 1,
        'complexity': 'low'
    }
    result = runner.invoke(cli, ['repo', 'analyze', str(test_file)])
    assert result.exit_code == 0
    mock_repo_manager.analyze_repo.assert_called_once_with(str(test_file))


def test_learn_session_command(runner, mock_repo_manager, temp_project_dir):
    """Test learn-session command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_repo_manager.learn_session.return_value = {
        'duration': '30m',
        'insights': ['Insight 1', 'Insight 2']
    }
    result = runner.invoke(cli, ['repo', 'learn-session', str(test_file), '--duration', '30'])
    assert result.exit_code == 0
    mock_repo_manager.learn_session.assert_called_once_with(str(test_file), duration=30)


def test_learn_session_invalid_duration(runner, mock_repo_manager, temp_project_dir):
    """Test learn-session command with invalid duration."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    result = runner.invoke(cli, ['repo', 'learn-session', str(test_file), '--duration', '-1'])
    assert result.exit_code == 1
    assert 'invalid duration' in result.output.lower()


def test_analyze_repo_nonexistent_file(runner, mock_repo_manager, temp_project_dir):
    """Test analyze-repo command with nonexistent file."""
    result = runner.invoke(cli, ['repo', 'analyze', 'nonexistent.py'])
    assert result.exit_code == 1
    assert 'file not found' in result.output.lower()
