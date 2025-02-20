"""Tests for the PromptManager class."""

import pytest
from prompt_manager import PromptManager, Task, TaskStatus, BoltTask
from tests.constants import (
    TASK_TITLE,
    TASK_DESCRIPTION,
    TASK_TEMPLATE,
    TASK_PRIORITY,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_DONE,
    TASK_NOT_FOUND_ERROR,
    INVALID_STATUS_ERROR,
    VALIDATION_ERROR,
)


@pytest.fixture
def prompt_manager(tmp_path):
    """Create a PromptManager instance."""
    return PromptManager("test_project", memory_path=tmp_path)


@pytest.fixture
def populated_prompt_manager(tmp_path):
    """Create a populated PromptManager instance."""
    manager = PromptManager("test_project", memory_path=tmp_path)
    task = Task(
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        prompt_template=TASK_TEMPLATE,
    )
    manager.add_task(task)
    return manager


@pytest.fixture
def mock_task_data():
    """Create mock task data."""
    return {
        "title": TASK_TITLE,
        "description": TASK_DESCRIPTION,
        "prompt_template": TASK_TEMPLATE,
    }


def test_prompt_manager_initialization(prompt_manager):
    """Test PromptManager initialization."""
    assert prompt_manager.project_name == "test_project"
    assert prompt_manager.is_initialized
    assert prompt_manager.memory_bank.is_active


def test_task_creation(prompt_manager, mock_task_data):
    """Test task creation and retrieval."""
    # Create task
    task = prompt_manager.add_task(
        title=mock_task_data["title"],
        description=mock_task_data["description"],
        template=mock_task_data["prompt_template"],
    )
    assert task.title == mock_task_data["title"]
    assert task.description == mock_task_data["description"]
    assert task.prompt_template == mock_task_data["prompt_template"]

    # Test retrieval
    retrieved_task = prompt_manager.get_task(mock_task_data["title"])
    assert retrieved_task.title == task.title
    assert retrieved_task.description == task.description
    assert retrieved_task.prompt_template == task.prompt_template


def test_task_update(populated_prompt_manager, mock_task_data):
    """Test task update functionality."""
    task_title = mock_task_data["title"]

    # Update task description
    new_description = "Updated description"
    populated_prompt_manager.update_task(
        task_title, description=new_description
    )
    task = populated_prompt_manager.get_task(task_title)
    assert task.description == new_description

    # Update task status
    populated_prompt_manager.update_task_status(
        task_title, status=TASK_STATUS_IN_PROGRESS, notes="Making progress"
    )
    task = populated_prompt_manager.get_task(task_title)
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.status_notes[-1] == "Making progress"


def test_task_deletion(populated_prompt_manager, mock_task_data):
    """Test task deletion."""
    task_title = mock_task_data["title"]

    # Delete task
    populated_prompt_manager.delete_task(task_title)

    # Verify task is deleted
    with pytest.raises(KeyError):
        populated_prompt_manager.get_task(task_title)

    # Test deleting non-existent task
    with pytest.raises(KeyError):
        populated_prompt_manager.delete_task("nonexistent-task")


def test_task_listing(populated_prompt_manager, mock_task_data):
    """Test task listing functionality."""
    # Add additional tasks
    task2_data = mock_task_data.copy()
    task2_data["title"] = "Task 2"
    task2_data["priority"] = 2
    task2 = Task(**task2_data)
    populated_prompt_manager.add_task(task2)

    # List all tasks
    tasks = populated_prompt_manager.list_tasks()
    assert len(tasks) == 2
    assert all(isinstance(task, Task) for task in tasks)

    # Test sorting by priority
    tasks = populated_prompt_manager.list_tasks(sort_by="priority")
    assert tasks[0].priority < tasks[1].priority


def test_task_filtering(populated_prompt_manager, mock_task_data):
    """Test task filtering functionality."""
    # Add tasks with different statuses
    task2_data = mock_task_data.copy()
    task2_data["title"] = "Task 2"
    task2 = Task(**task2_data)
    populated_prompt_manager.add_task(task2)

    # Update status of first task
    populated_prompt_manager.update_task_status(
        mock_task_data["title"], status=TASK_STATUS_IN_PROGRESS
    )

    # Filter by status
    in_progress = populated_prompt_manager.list_tasks(
        status=TASK_STATUS_IN_PROGRESS
    )
    assert len(in_progress) == 1
    assert in_progress[0].title == mock_task_data["title"]


def test_task_export_import(populated_prompt_manager, tmp_path):
    """Test task export and import functionality."""
    export_path = tmp_path / "tasks_export.json"

    # Export tasks
    populated_prompt_manager.export_tasks(export_path)
    assert export_path.exists()

    # Create new manager and import tasks
    new_manager = PromptManager("test_project_2", memory_path=tmp_path)
    new_manager.initialize()
    new_manager.import_tasks(export_path)

    # Verify imported tasks match original
    original_tasks = populated_prompt_manager.list_tasks()
    imported_tasks = new_manager.list_tasks()
    assert len(original_tasks) == len(imported_tasks)
    for t1, t2 in zip(original_tasks, imported_tasks):
        assert t1.title == t2.title


def test_error_handling(prompt_manager):
    """Test error handling in PromptManager."""
    # Test invalid task title
    with pytest.raises(KeyError):
        prompt_manager.get_task("nonexistent-task")

    # Add a task for status update test
    task = Task(
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        prompt_template=TASK_TEMPLATE,
        priority=TASK_PRIORITY,
    )
    prompt_manager.add_task(task)

    # Test invalid task status
    with pytest.raises(ValueError):
        prompt_manager.update_task_status(TASK_TITLE, "invalid_status")

    # Test invalid priority
    with pytest.raises(ValueError):
        prompt_manager.add_task(
            title=TASK_TITLE,
            description=TASK_DESCRIPTION,
            template=TASK_TEMPLATE,
            priority=-1
        )


def test_bolt_task_creation():
    """Test BoltTask creation and properties."""
    task = BoltTask(
        title="Test Bolt Task",
        description="Test description",
        prompt_template="Test template",
        framework="Next.js",
        dependencies=["react", "typescript"],
        ui_components=["Button", "Card"],
        api_endpoints=[
            {
                "method": "GET",
                "path": "/api/test",
                "description": "Test endpoint",
            }
        ],
    )

    assert task.title == "Test Bolt Task"
    assert task.description == "Test description"
    assert task.prompt_template == "Test template"
    assert task.framework == "Next.js"
    assert "react" in task.dependencies
    assert "typescript" in task.dependencies
    assert "Button" in task.ui_components
    assert len(task.api_endpoints) == 1
    assert task.api_endpoints[0]["method"] == "GET"


def test_bolt_task_serialization():
    """Test BoltTask serialization and deserialization."""
    task = BoltTask(
        title="Test Bolt Task",
        description="Test description",
        prompt_template="Test template",
        framework="Next.js",
        dependencies=["react", "typescript"],
        ui_components=["Button", "Card"],
        api_endpoints=[
            {
                "method": "GET",
                "path": "/api/test",
                "description": "Test endpoint",
            }
        ],
    )

    # Test serialization
    task_dict = task.to_dict()
    assert task_dict["title"] == task.title
    assert task_dict["framework"] == task.framework
    assert "dependencies" in task_dict
    assert "ui_components" in task_dict
    assert "api_endpoints" in task_dict

    # Test deserialization
    new_task = BoltTask.from_dict(task_dict)
    assert new_task.title == task.title
    assert new_task.framework == task.framework
    assert new_task.dependencies == task.dependencies
    assert new_task.ui_components == task.ui_components
    assert new_task.api_endpoints == task.api_endpoints


def test_bolt_prompt_generation():
    """Test bolt.new prompt generation."""
    task = BoltTask(
        title="Test Bolt Task",
        description="Create a simple button component",
        prompt_template="Create a {framework} component: {description}",
        framework="Next.js",
        dependencies=["react", "typescript"],
        ui_components=["Button"],
        api_endpoints=[],
    )

    prompt = task.generate_prompt()
    assert "Next.js" in prompt
    assert "button component" in prompt
    assert "react" in prompt.lower()
    assert "typescript" in prompt.lower()


def test_generate_bolt_tasks():
    """Test generation of bolt.new task sequence."""
    tasks = BoltTask.generate_task_sequence(
        "Create a user authentication system",
        framework="Next.js",
        dependencies=["react", "typescript", "next-auth"],
        ui_components=["LoginForm", "SignupForm", "UserProfile"],
        api_endpoints=[
            {"method": "POST", "path": "/api/auth/signup"},
            {"method": "POST", "path": "/api/auth/login"},
            {"method": "GET", "path": "/api/user/profile"},
        ],
    )

    assert len(tasks) >= 3  # Should generate multiple tasks
    assert all(isinstance(task, BoltTask) for task in tasks)
    assert any("login" in task.title.lower() for task in tasks)
    assert any("signup" in task.title.lower() for task in tasks)
    assert any("profile" in task.title.lower() for task in tasks)


def test_add_task(prompt_manager):
    """Test adding a new task."""
    task = prompt_manager.add_task(
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        template=TASK_TEMPLATE,
        priority=TASK_PRIORITY
    )
    assert task.title == TASK_TITLE
    assert task.description == TASK_DESCRIPTION
    assert task.template == TASK_TEMPLATE
    assert task.priority == TASK_PRIORITY
    assert task.status == TaskStatus.PENDING


def test_update_task_status(prompt_manager):
    """Test updating task status."""
    # First add a task
    task = prompt_manager.add_task(
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        template=TASK_TEMPLATE,
        priority=TASK_PRIORITY
    )
    
    # Update its status
    updated_task = prompt_manager.update_task_status(
        title=TASK_TITLE,
        status=TASK_STATUS_IN_PROGRESS
    )
    assert updated_task.status == TaskStatus.IN_PROGRESS


def test_list_tasks(prompt_manager):
    """Test listing tasks."""
    # First add a task
    prompt_manager.add_task(
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        template=TASK_TEMPLATE,
        priority=TASK_PRIORITY
    )
    
    # List all tasks
    tasks = prompt_manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == TASK_TITLE


def test_task_not_found(prompt_manager):
    """Test handling of non-existent task."""
    with pytest.raises(KeyError, match=TASK_NOT_FOUND_ERROR):
        prompt_manager.update_task_status(
            title="non-existent-task",
            status=TASK_STATUS_DONE
        )


def test_invalid_status(prompt_manager):
    """Test handling of invalid status."""
    with pytest.raises(ValueError, match=INVALID_STATUS_ERROR):
        prompt_manager.update_task_status(
            title=TASK_TITLE,
            status="invalid_status"
        )


def test_invalid_task_data(prompt_manager):
    """Test handling of invalid task data."""
    with pytest.raises(ValueError, match=VALIDATION_ERROR):
        prompt_manager.add_task(
            title="",  # Empty title
            description=TASK_DESCRIPTION,
            template=TASK_TEMPLATE,
            priority=TASK_PRIORITY
        )
