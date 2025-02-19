"""Test LLM enhancement CLI commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
from prompt_manager.cli import cli
from pathlib import Path
import tempfile
import os


pytestmark = [pytest.mark.cli, pytest.mark.cli_llm]


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
def mock_llm_manager():
    """Create a mock LLMManager."""
    with patch('prompt_manager.cli.llm_commands.LLMManager') as mock:
        manager = Mock()
        mock.return_value = manager
        yield manager


def test_generate_bolt_tasks_command(runner, mock_llm_manager, temp_project_dir):
    """Test generate-bolt-tasks command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_llm_manager.generate_bolt_tasks.return_value = ['Task 1', 'Task 2']
    result = runner.invoke(cli, ['llm', 'generate-bolt-tasks', str(test_file)])
    assert result.exit_code == 0
    mock_llm_manager.generate_bolt_tasks.assert_called_once_with(str(test_file))


def test_analyze_impact_command(runner, mock_llm_manager, temp_project_dir):
    """Test analyze-impact command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_llm_manager.analyze_impact.return_value = {'impact': 'medium', 'details': 'Test impact'}
    result = runner.invoke(cli, ['llm', 'analyze-impact', str(test_file)])
    assert result.exit_code == 0
    mock_llm_manager.analyze_impact.assert_called_once_with(str(test_file))


def test_suggest_improvements_command(runner, mock_llm_manager, temp_project_dir):
    """Test suggest-improvements command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_llm_manager.suggest_improvements.return_value = ['Suggestion 1', 'Suggestion 2']
    result = runner.invoke(cli, ['llm', 'suggest-improvements', str(test_file)])
    assert result.exit_code == 0
    mock_llm_manager.suggest_improvements.assert_called_once_with(str(test_file))


def test_create_pr_command(runner, mock_llm_manager, temp_project_dir):
    """Test create-pr command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_llm_manager.create_pr.return_value = {'url': 'https://github.com/test/pr/1'}
    result = runner.invoke(cli, ['llm', 'create-pr', str(test_file), '--title', 'Test PR'])
    assert result.exit_code == 0
    mock_llm_manager.create_pr.assert_called_once_with(str(test_file), 'Test PR')


def test_generate_commands_command(runner, mock_llm_manager, temp_project_dir):
    """Test generate-commands command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_llm_manager.generate_commands.return_value = ['Command 1', 'Command 2']
    result = runner.invoke(cli, ['llm', 'generate-commands', str(test_file)])
    assert result.exit_code == 0
    mock_llm_manager.generate_commands.assert_called_once_with(str(test_file))


def test_analyze_impact_nonexistent_file(runner, mock_llm_manager, temp_project_dir):
    """Test analyze-impact command with nonexistent file."""
    result = runner.invoke(cli, ['llm', 'analyze-impact', 'nonexistent.py'])
    assert result.exit_code == 1
    assert 'file not found' in result.output.lower()


def test_suggest_improvements_invalid_max(runner, mock_llm_manager, temp_project_dir):
    """Test suggest-improvements command with invalid max suggestions."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    result = runner.invoke(cli, ['llm', 'suggest-improvements', str(test_file), '--max-suggestions', '-1'])
    assert result.exit_code == 1
    assert 'invalid value' in result.output.lower()


def test_create_pr_missing_args(runner, mock_llm_manager, temp_project_dir):
    """Test create-pr command with missing arguments."""
    result = runner.invoke(cli, ['llm', 'create-pr'])
    assert result.exit_code == 2
    assert 'missing argument' in result.output.lower()
