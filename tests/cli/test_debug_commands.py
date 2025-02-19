"""Test debug CLI commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
from prompt_manager.cli import cli
from pathlib import Path
import tempfile
import os


pytestmark = [pytest.mark.cli, pytest.mark.cli_debug]


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
def mock_debug_manager():
    """Create a mock DebugManager."""
    with patch('prompt_manager.cli.debug_commands.DebugManager') as mock:
        manager = Mock()
        mock.return_value = manager
        yield manager


def test_debug_analyze_file(runner, mock_debug_manager, temp_project_dir):
    """Test debug analyze-file command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    result = runner.invoke(cli, ['debug', 'analyze-file', str(test_file)])
    assert result.exit_code == 0
    mock_debug_manager.analyze_file.assert_called_once_with(str(test_file))


def test_debug_find_root_cause(runner, mock_debug_manager, temp_project_dir):
    """Test debug find-root-cause command."""
    test_file = temp_project_dir / "error.log"
    test_file.write_text("Error: test error")
    
    result = runner.invoke(cli, ['debug', 'find-root-cause', str(test_file)])
    assert result.exit_code == 0
    mock_debug_manager.find_root_cause.assert_called_once_with(str(test_file))


def test_debug_iterative_fix(runner, mock_debug_manager, temp_project_dir):
    """Test debug iterative-fix command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    mock_debug_manager.iterative_fix.return_value = ['Fix 1', 'Fix 2']
    result = runner.invoke(cli, ['debug', 'iterative-fix', str(test_file)])
    assert result.exit_code == 0
    mock_debug_manager.iterative_fix.assert_called_once_with(str(test_file))


def test_debug_test_roadmap(runner, mock_debug_manager, temp_project_dir):
    """Test debug test-roadmap command."""
    test_file = temp_project_dir / "test.py"
    test_file.write_text("def test(): pass")
    
    result = runner.invoke(cli, ['debug', 'test-roadmap', str(test_file)])
    assert result.exit_code == 0
    mock_debug_manager.generate_test_roadmap.assert_called_once_with(str(test_file))


def test_debug_analyze_dependencies(runner, mock_debug_manager, temp_project_dir):
    """Test debug analyze-dependencies command."""
    test_file = temp_project_dir / "requirements.txt"
    test_file.write_text("pytest==7.0.0")
    
    result = runner.invoke(cli, ['debug', 'analyze-dependencies', str(test_file)])
    assert result.exit_code == 0
    mock_debug_manager.analyze_dependencies.assert_called_once_with(str(test_file))


def test_debug_trace_error(runner, mock_debug_manager, temp_project_dir):
    """Test debug trace-error command."""
    test_file = temp_project_dir / "errors.md"
    test_file.write_text("Error: test error")
    
    result = runner.invoke(cli, ['debug', 'trace-error', str(test_file)])
    assert result.exit_code == 0
    mock_debug_manager.trace_error.assert_called_once_with(str(test_file))
