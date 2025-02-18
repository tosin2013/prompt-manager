import pytest
from prompt_manager import PromptManager


@pytest.fixture
def test_project_path(tmp_path):
    """Create a temporary project directory"""
    return tmp_path


@pytest.fixture
def prompt_manager(test_project_path):
    """Create a PromptManager instance with test configuration"""
    return PromptManager("test_project")


@pytest.fixture
def sample_task(prompt_manager):
    """Create a sample task"""
    task_name = "test_task"
    prompt_manager.add_task(
        name=task_name,
        description="Test task description",
        prompt_template="Test prompt template",
    )
    return prompt_manager.get_task(task_name)
