"""Common test fixtures for CLI tests."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import tempfile
import os


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
