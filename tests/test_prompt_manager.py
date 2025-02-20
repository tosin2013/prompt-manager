"""Tests for the PromptManager class."""

import pytest
from datetime import datetime
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
import yaml


@pytest.fixture(autouse=True)  # Auto-use this fixture to clean up between tests
def clean_tasks(tmp_path):
    """Clean up tasks between tests."""
    # Create a tasks.yaml file in the tmp_path
    tasks_file = tmp_path / "tasks.yaml"
    tasks_file.write_text("{}")  # Empty tasks file
    
    # Create a PromptManager instance with the tmp_path
    manager = PromptManager("test_project", memory_path=tmp_path)
    
    # Patch the save_tasks and load_tasks methods to use tmp_path
    def save_tasks():
        with open(tasks_file, "w") as f:
            yaml.dump(
                {title: task.to_dict() for title, task in manager.tasks.items()},
                f,
                default_flow_style=False,
            )
    
    def load_tasks():
        if tasks_file.exists():
            with open(tasks_file) as f:
                data = yaml.safe_load(f)
                if data and isinstance(data, dict):
                    manager.tasks = {
                        title: Task.from_dict(task_data)
                        for title, task_data in data.items()
                    }
    
    # Patch the methods
    manager.save_tasks = save_tasks
    manager.load_tasks = load_tasks
    
    # Initialize the manager
    manager.initialize()
    
    # Clear any existing tasks
    manager.tasks.clear()
    manager.save_tasks()
    
    yield manager
    
    # Clean up tasks after each test
    manager.tasks.clear()
    manager.save_tasks()
    if tasks_file.exists():
        tasks_file.unlink()


@pytest.fixture
def populated_prompt_manager(request, clean_tasks):
    """Create a populated PromptManager instance."""
    task = Task(
        title=f"{TASK_TITLE}_{request.node.name}",  # Use test name to ensure uniqueness
        description=TASK_DESCRIPTION,
        template=TASK_TEMPLATE,
    )
    clean_tasks.add_task(task)
    return clean_tasks


@pytest.fixture
def mock_task_data(request):
    """Create mock task data."""
    return {
        "title": f"{TASK_TITLE}_{request.node.name}",  # Use test name to ensure uniqueness
        "description": TASK_DESCRIPTION,
        "template": TASK_TEMPLATE,
        "status": TaskStatus.PENDING.value,
        "priority": "medium",
        "dependencies": [],
        "assignee": None,
        "due_date": None,
        "status_notes": []
    }


def test_task_validation():
    """Test task validation."""
    # Test empty title
    with pytest.raises(ValueError, match="Title must be a non-empty string"):
        Task(title="", description="desc")

    # Test invalid priority
    with pytest.raises(ValueError, match="Priority must be one of: low, medium, high"):
        Task(title="test", description="desc", priority="invalid")

    # Test invalid due date
    with pytest.raises(ValueError, match="Due date must be in ISO format"):
        Task(title="test", description="desc", due_date="invalid-date")

    # Test valid due date
    valid_date = datetime.now().date().isoformat()
    task = Task(title="test", description="desc", due_date=valid_date)
    assert task.due_date == valid_date

    # Test dependencies type validation
    with pytest.raises(ValueError, match="Dependencies must be a list"):
        Task(title="test", description="desc", dependencies="not-a-list")


def test_task_status_transitions():
    """Test task status transitions."""
    task = Task(title="test", description="desc")
    
    # Test valid transition
    task.update_status(TaskStatus.IN_PROGRESS, "Starting work")
    assert task.status == TaskStatus.IN_PROGRESS
    assert len(task.status_notes) == 1
    assert "Starting work" in task.status_notes[0]

    # Test invalid status type
    with pytest.raises(ValueError, match="new_status must be a TaskStatus enum"):
        task.update_status("invalid")


def test_task_serialization():
    """Test task serialization and deserialization."""
    original_task = Task(
        title="test",
        description="desc",
        template="template",
        priority="high",
        dependencies=["dep1", "dep2"],
        assignee="user1",
        due_date=datetime.now().date().isoformat()
    )

    # Test serialization
    task_dict = original_task.to_dict()
    assert task_dict["title"] == "test"
    assert task_dict["priority"] == "high"
    assert len(task_dict["dependencies"]) == 2

    # Test deserialization
    new_task = Task.from_dict(task_dict)
    assert new_task.title == original_task.title
    assert new_task.priority == original_task.priority
    assert new_task.dependencies == original_task.dependencies

    # Test invalid input
    with pytest.raises(ValueError, match="Input must be a dictionary"):
        Task.from_dict("not-a-dict")

    # Test missing required field
    with pytest.raises(ValueError, match="Missing required field: title"):
        Task.from_dict({})


def test_bolt_task_validation():
    """Test BoltTask validation."""
    # Test required fields
    with pytest.raises(ValueError, match="bolt_id must be a non-empty string"):
        BoltTask(bolt_id="", bolt_type="type", bolt_status="status", bolt_priority=1, title="title")

    with pytest.raises(ValueError, match="bolt_priority must be an integer"):
        BoltTask(bolt_id="id", bolt_type="type", bolt_status="status", bolt_priority="not-int", title="title")

    # Test valid creation
    bolt_task = BoltTask(
        bolt_id="id",
        bolt_type="type",
        bolt_status="status",
        bolt_priority=1,
        title="title",
        priority="high",
        dependencies=["dep1"],
        metadata={"key": "value"}
    )
    assert bolt_task.bolt_id == "id"
    assert bolt_task.priority == "high"
    assert len(bolt_task.dependencies) == 1


def test_bolt_task_serialization():
    """Test BoltTask serialization and deserialization."""
    original_task = BoltTask(
        bolt_id="id",
        bolt_type="type",
        bolt_status="status",
        bolt_priority=1,
        title="title",
        description="desc",
        priority="high",
        dependencies=["dep1"],
        metadata={"key": "value"},
        bolt_assignee="user1",
        bolt_due_date=datetime.now().date().isoformat()
    )

    # Test serialization
    task_dict = original_task.to_dict()
    assert task_dict["bolt_id"] == "id"
    assert task_dict["priority"] == "high"
    assert task_dict["metadata"]["key"] == "value"

    # Test deserialization
    new_task = BoltTask.from_dict(task_dict)
    assert new_task.bolt_id == original_task.bolt_id
    assert new_task.priority == original_task.priority
    assert new_task.metadata == original_task.metadata

    # Test invalid input
    with pytest.raises(ValueError, match="Input must be a dictionary"):
        BoltTask.from_dict("not-a-dict")

    # Test missing required fields
    with pytest.raises(ValueError, match="Missing required field"):
        BoltTask.from_dict({"title": "title"})


def test_task_creation(clean_tasks, mock_task_data):
    """Test task creation and retrieval."""
    # Create task
    task = Task(
        title=mock_task_data["title"],
        description=mock_task_data["description"],
        template=mock_task_data["template"],
    )
    added_task = clean_tasks.add_task(task)
    assert added_task.title == mock_task_data["title"]
    assert added_task.description == mock_task_data["description"]
    assert added_task.template == mock_task_data["template"]

    # Test retrieval
    retrieved_task = clean_tasks.get_task(mock_task_data["title"])
    assert retrieved_task.title == task.title
    assert retrieved_task.description == task.description
    assert retrieved_task.template == task.template


def test_task_update(populated_prompt_manager, mock_task_data):
    """Test task update functionality."""
    task_title = f"{TASK_TITLE}_{test_task_update.__name__}"

    # Update task description
    new_description = "Updated description"
    populated_prompt_manager.update_task(task_title, description=new_description)
    updated_task = populated_prompt_manager.get_task(task_title)
    assert updated_task.description == new_description

    # Update task status
    populated_prompt_manager.update_task_status(task_title, TaskStatus.IN_PROGRESS, "Making progress")
    updated_task = populated_prompt_manager.get_task(task_title)
    assert updated_task.status == TaskStatus.IN_PROGRESS
    assert "Making progress" in updated_task.status_notes[-1]  # Check if note contains the message

    # Update task priority
    populated_prompt_manager.update_task(task_title, priority="high")
    updated_task = populated_prompt_manager.get_task(task_title)
    assert updated_task.priority == "high"


def test_task_deletion(populated_prompt_manager, mock_task_data):
    """Test task deletion."""
    task_title = f"{TASK_TITLE}_{test_task_deletion.__name__}"
    populated_prompt_manager.delete_task(task_title)
    with pytest.raises(KeyError):
        populated_prompt_manager.get_task(task_title)


def test_task_listing(populated_prompt_manager, mock_task_data):
    """Test task listing functionality."""
    tasks = populated_prompt_manager.list_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert task.title == f"{TASK_TITLE}_{test_task_listing.__name__}"
    assert task.description == TASK_DESCRIPTION
    assert task.template == TASK_TEMPLATE


def test_task_filtering(populated_prompt_manager, mock_task_data):
    """Test task filtering functionality."""
    # Add another task with different status
    another_task = Task(
        title="Another Task",
        description="Another description",
        template="Another template",
    )
    populated_prompt_manager.add_task(another_task)
    populated_prompt_manager.update_task_status(another_task.title, TaskStatus.IN_PROGRESS, "Started")

    # Test filtering by status
    pending_tasks = populated_prompt_manager.list_tasks(status=TaskStatus.PENDING)
    in_progress_tasks = populated_prompt_manager.list_tasks(status=TaskStatus.IN_PROGRESS)

    assert len(pending_tasks) == 1
    assert len(in_progress_tasks) == 1
    assert pending_tasks[0].title == f"{TASK_TITLE}_{test_task_filtering.__name__}"
    assert in_progress_tasks[0].title == "Another Task"


def test_task_export_import(populated_prompt_manager, tmp_path):
    """Test task export and import functionality."""
    export_path = tmp_path / "tasks.json"
    populated_prompt_manager.export_tasks(export_path)

    # Create new manager and import tasks
    new_manager = PromptManager("test_project", memory_path=tmp_path)
    new_manager.import_tasks(export_path)

    # Verify tasks were imported correctly
    tasks = new_manager.list_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert isinstance(task, Task)
    assert task.title == f"{TASK_TITLE}_{test_task_export_import.__name__}"
    assert task.description == TASK_DESCRIPTION
    assert task.template == TASK_TEMPLATE


def test_error_handling(clean_tasks):
    """Test error handling in PromptManager."""
    task_title = f"{TASK_TITLE}_{test_error_handling.__name__}"
    
    # Test task not found
    with pytest.raises(KeyError) as exc_info:
        clean_tasks.get_task(task_title)
    assert f"Task '{task_title}' not found" in str(exc_info.value)

    # Test invalid status update
    task = Task(title=task_title, description="test")
    clean_tasks.add_task(task)
    with pytest.raises(ValueError) as exc_info:
        clean_tasks.update_task_status(task_title, "invalid_status", "note")
    assert INVALID_STATUS_ERROR in str(exc_info.value)

    # Test validation error
    with pytest.raises(ValueError) as exc_info:
        clean_tasks.add_task(Task(title="", description=""))  # Empty title
    assert "Title must be a non-empty string" in str(exc_info.value)
