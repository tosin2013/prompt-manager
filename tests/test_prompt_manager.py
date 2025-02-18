"""
Tests for the PromptManager component.
"""
import pytest
from pathlib import Path
from prompt_manager import PromptManager, Task, TaskStatus, BoltTask

@pytest.fixture
def prompt_manager(tmp_path):
    return PromptManager("test_project", memory_path=tmp_path)

@pytest.fixture
def populated_prompt_manager(tmp_path):
    manager = PromptManager("test_project", memory_path=tmp_path)
    task = Task(
        name="test-task",
        description="Test description",
        prompt_template="Test template"
    )
    manager.add_task(task)
    return manager

@pytest.fixture
def mock_task_data():
    return {
        "name": "test-task",
        "description": "Test description",
        "prompt_template": "Test template"
    }

@pytest.fixture
def test_data_dir(tmp_path):
    return tmp_path

def test_prompt_manager_initialization(prompt_manager):
    """Test PromptManager initialization."""
    assert prompt_manager.project_name == "test_project"
    assert prompt_manager.is_initialized
    assert prompt_manager.memory_bank.is_active

def test_task_creation(prompt_manager, mock_task_data):
    """Test task creation and retrieval."""
    # Create task
    task = prompt_manager.add_task(
        mock_task_data["name"],
        mock_task_data["description"],
        mock_task_data["prompt_template"]
    )
    assert task.name == mock_task_data["name"]
    assert task.description == mock_task_data["description"]
    assert task.prompt_template == mock_task_data["prompt_template"]

    # Test retrieval
    retrieved_task = prompt_manager.get_task(mock_task_data["name"])
    assert retrieved_task.name == task.name
    assert retrieved_task.description == task.description
    assert retrieved_task.prompt_template == task.prompt_template

def test_task_update(populated_prompt_manager, mock_task_data):
    """Test task update functionality."""
    task_name = mock_task_data["name"]
    
    # Update task description
    new_description = "Updated description"
    populated_prompt_manager.update_task(
        task_name,
        description=new_description
    )
    task = populated_prompt_manager.get_task(task_name)
    assert task.description == new_description
    
    # Update task status
    populated_prompt_manager.update_task_status(
        task_name,
        status=TaskStatus.IN_PROGRESS,
        notes="Making progress"
    )
    task = populated_prompt_manager.get_task(task_name)
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.status_notes[-1] == "Making progress"

def test_task_deletion(populated_prompt_manager, mock_task_data):
    """Test task deletion."""
    task_name = mock_task_data["name"]
    
    # Delete task
    populated_prompt_manager.delete_task(task_name)
    
    # Verify task is deleted
    with pytest.raises(KeyError):
        populated_prompt_manager.get_task(task_name)
    
    # Test deleting non-existent task
    with pytest.raises(KeyError):
        populated_prompt_manager.delete_task("nonexistent-task")

def test_task_listing(populated_prompt_manager, mock_task_data):
    """Test task listing functionality."""
    # Add additional tasks
    task2_data = mock_task_data.copy()
    task2_data["name"] = "test-task-2"
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
    task2_data["name"] = "test-task-2"
    task2 = Task(**task2_data)
    populated_prompt_manager.add_task(task2)
    
    # Update status of first task
    populated_prompt_manager.update_task_status(
        mock_task_data["name"],
        status=TaskStatus.IN_PROGRESS
    )
    
    # Filter by status
    in_progress_tasks = populated_prompt_manager.list_tasks(
        status=TaskStatus.IN_PROGRESS
    )
    assert len(in_progress_tasks) == 1
    assert in_progress_tasks[0].name == mock_task_data["name"]

def test_task_export_import(populated_prompt_manager, test_data_dir):
    """Test task export and import functionality."""
    export_path = test_data_dir / "tasks_export.json"
    
    # Export tasks
    populated_prompt_manager.export_tasks(export_path)
    assert export_path.exists()
    
    # Create new manager and import tasks
    new_manager = PromptManager("test_project_2", memory_path=test_data_dir)
    new_manager.initialize()
    new_manager.import_tasks(export_path)
    
    # Verify imported tasks match original
    original_tasks = populated_prompt_manager.list_tasks()
    imported_tasks = new_manager.list_tasks()
    assert len(original_tasks) == len(imported_tasks)
    assert all(t1.name == t2.name for t1, t2 in zip(original_tasks, imported_tasks))

def test_error_handling(prompt_manager):
    """Test error handling in PromptManager."""
    # Test invalid task name
    with pytest.raises(KeyError):
        prompt_manager.get_task("nonexistent-task")

    # Add a task for status update test
    task = Task(
        name="test-task",
        description="Test task",
        prompt_template="Test prompt",
        priority=1
    )
    prompt_manager.add_task(task)

    # Test invalid task status
    with pytest.raises(ValueError):
        prompt_manager.update_task_status(
            "test-task",
            "invalid_status"
        )

    # Test invalid priority
    with pytest.raises(ValueError):
        prompt_manager.add_task(
            "test-task-2",
            "Test description",
            "Test prompt",
            priority=-1
        )

def test_bolt_task_creation():
    """Test BoltTask creation and properties."""
    task = BoltTask(
        name="Test Bolt Task",
        description="Test description",
        prompt_template="Test template",
        framework="Next.js",
        dependencies=["react", "typescript"],
        ui_components=["Button", "Card"],
        api_endpoints=[{"method": "GET", "path": "/api/test", "description": "Test endpoint"}]
    )
    
    assert task.name == "Test Bolt Task"
    assert task.description == "Test description"
    assert task.prompt_template == "Test template"
    assert task.framework == "Next.js"
    assert "react" in task.dependencies
    assert "Button" in task.ui_components
    assert task.api_endpoints[0]["method"] == "GET"
    assert task.status == TaskStatus.NOT_STARTED

def test_bolt_task_serialization():
    """Test BoltTask serialization and deserialization."""
    original_task = BoltTask(
        name="Test Bolt Task",
        description="Test description",
        prompt_template="Test template",
        framework="Next.js",
        dependencies=["react"],
        ui_components=["Button"],
        api_endpoints=[{"method": "GET", "path": "/api/test", "description": "Test endpoint"}]
    )
    
    # Test serialization
    task_dict = original_task.to_dict()
    assert task_dict["name"] == "Test Bolt Task"
    assert task_dict["framework"] == "Next.js"
    assert "react" in task_dict["dependencies"]
    
    # Test deserialization
    restored_task = BoltTask.from_dict(task_dict)
    assert restored_task.name == original_task.name
    assert restored_task.framework == original_task.framework
    assert restored_task.dependencies == original_task.dependencies
    assert restored_task.ui_components == original_task.ui_components
    assert restored_task.api_endpoints == original_task.api_endpoints

def test_bolt_prompt_generation():
    """Test bolt.new prompt generation."""
    task = BoltTask(
        name="Test Bolt Task",
        description="Test description",
        prompt_template="1. Step one\n2. Step two",
        framework="Next.js",
        dependencies=["react"],
        ui_components=["Button"],
        api_endpoints=[{"method": "GET", "path": "/api/test", "description": "Test endpoint"}]
    )
    
    prompt = task.to_bolt_prompt()
    assert "# Test Bolt Task" in prompt
    assert "Framework: Next.js" in prompt
    assert "- react" in prompt
    assert "- Button" in prompt
    assert "GET /api/test" in prompt
    assert "1. Step one" in prompt

def test_generate_bolt_tasks():
    """Test generation of bolt.new task sequence."""
    manager = PromptManager()
    tasks = manager.generate_bolt_tasks("Test Project")
    
    assert len(tasks) == 5  # Verify all task types are generated
    
    # Verify task order and priorities
    assert tasks[0].name == "Initial Project Setup"
    assert tasks[0].priority == 1
    assert tasks[1].name == "UI Component Development"
    assert tasks[1].priority == 2
    assert tasks[2].name == "API Integration"
    assert tasks[2].priority == 3
    
    # Verify task contents
    setup_task = tasks[0]
    assert setup_task.framework == "Next.js"
    assert "typescript" in setup_task.dependencies
    assert "tailwindcss" in setup_task.dependencies
    
    ui_task = tasks[1]
    assert "Layout" in ui_task.ui_components
    assert "Navigation" in ui_task.ui_components
    
    api_task = tasks[2]
    assert any(endpoint["method"] == "GET" for endpoint in api_task.api_endpoints)
    assert any(endpoint["method"] == "POST" for endpoint in api_task.api_endpoints)
