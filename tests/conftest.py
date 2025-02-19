"""
Global pytest fixtures and configuration.
"""

import pytest
from pathlib import Path
from prompt_manager import PromptManager


@pytest.fixture(scope="function")
def test_data_dir(tmp_path) -> Path:
    """Create and return a temporary directory for test data."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(scope="function")
def prompt_manager(test_data_dir) -> PromptManager:
    """Create a PromptManager instance for testing."""
    manager = PromptManager("test_project", memory_path=test_data_dir)
    manager.initialize()
    return manager


@pytest.fixture(scope="function")
def mock_task_data() -> dict:
    """Return mock task data for testing."""
    return {
        "name": "test-task",
        "description": "Test task description",
        "prompt_template": "Test prompt template",
        "priority": 1,
    }


@pytest.fixture(scope="function")
def populated_prompt_manager(prompt_manager, mock_task_data) -> PromptManager:
    """Create a PromptManager instance with pre-populated test data."""
    prompt_manager.add_task(**mock_task_data)
    return prompt_manager
