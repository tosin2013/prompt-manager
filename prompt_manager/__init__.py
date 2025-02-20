"""
Prompt Manager: Development workflow management system with memory tracking.
"""

__version__ = "0.3.18"

import os
import yaml
import datetime
from enum import Enum
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from prompt_manager.models import Task, BoltTask, TaskStatus


class PromptManager:
    """Manages development workflow and task tracking."""

    def __init__(
        self,
        project_name: str = "",
        memory_path: Optional[Union[str, Path]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize PromptManager with project configuration."""
        self.project_name = project_name
        self.project_dir = Path.cwd()
        self.memory_bank = None
        self.config = config or {}
        self.tasks: Dict[str, Task] = {}
        self.debug_mode = False
        self.is_initialized = False
        self.initialize()

    def initialize(self) -> None:
        """Initialize the prompt manager and memory bank."""
        self._load_config()
        self.load_tasks()
        self.is_initialized = True

    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        config_path = Path("prompt_manager_config.yaml")
        if config_path.exists():
            with open(config_path) as f:
                self.config.update(yaml.safe_load(f))

    def load_tasks(self) -> None:
        """Load tasks from storage."""
        tasks_path = self.project_dir / "tasks.yaml"
        if not tasks_path.exists():
            return
            
        with open(tasks_path) as f:
            data = yaml.safe_load(f)
            if not data or "tasks" not in data:
                return
                
            for title, task_data in data["tasks"].items():
                self.tasks[title] = Task(
                    title=title,
                    description=task_data.get("description", ""),
                    status=TaskStatus(task_data.get("status", "todo")),
                    template=task_data.get("template"),
                    priority=task_data.get("priority", "medium")
                )

    def save_tasks(self) -> None:
        """Save tasks to storage."""
        tasks_path = self.project_dir / "tasks.yaml"
        tasks_path.parent.mkdir(parents=True, exist_ok=True)
        tasks_data = {
            "tasks": {
                title: {
                    "description": task.description,
                    "status": task.status.value,
                    "template": task.template,
                    "priority": task.priority
                }
                for title, task in self.tasks.items()
            }
        }
        with open(tasks_path, "w") as f:
            yaml.dump(tasks_data, f)

    def init_project(self, path: str) -> None:
        """Initialize a new project at the specified path.
        
        Args:
            path (str): Path to initialize project at
        """
        project_dir = Path(path)
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create memory directory
        memory_dir = project_dir / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Create config file
        config_path = project_dir / "prompt_manager_config.yaml"
        config = {
            "project_name": project_dir.name,
            "memory_path": str(memory_dir),
            "created_at": datetime.datetime.now().isoformat()
        }
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        
        # Initialize memory bank
        self.memory_bank = MemoryBank(memory_dir)
        self.memory_bank.initialize()
        
        # Update project context
        self.memory_bank.update_context(
            "activeContext.md",
            "Project Initialization",
            f"Project initialized on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Project Name: {project_dir.name}\n"
            f"Project Path: {project_dir}",
            mode="append"
        )

    def add_task(
        self,
        title_or_task: Union[str, Task],
        description: Optional[str] = None,
        template: Optional[str] = None,
        priority: str = "medium",
    ) -> Task:
        """Add a new task to the workflow.

        Args:
            title_or_task: Task title or Task object
            description: Task description (if title_or_task is str)
            template: Optional prompt template (if title_or_task is str)
            priority: Task priority (low/medium/high) (if title_or_task is str)

        Returns:
            Task: The added task

        Raises:
            ValueError: If task title already exists or priority is invalid
        """
        if isinstance(title_or_task, Task):
            task = title_or_task
        else:
            task = Task(
                title=title_or_task,
                description=description or "",
                template=template or "",
                priority=priority.lower()
            )

        if task.title in self.tasks:
            raise ValueError(f"Task with title '{task.title}' already exists")

        self.tasks[task.title] = task
        if self.memory_bank:
            self.memory_bank.add_task(task.title, task.description, task.priority)
        self.save_tasks()
        return task

    def get_task(self, task_id: Union[str, int]) -> Task:
        """Get a task by its ID."""
        if isinstance(task_id, int):
            task_id = str(task_id)
        if task_id not in self.tasks:
            raise KeyError(f"Task '{task_id}' not found")
        return self.tasks[task_id]

    def update_task(
        self,
        task_id: Union[str, int],
        description: Optional[str] = None,
        template: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Task:
        """Update task details."""
        task = self.get_task(task_id)

        if description is not None:
            task.description = description
        if template is not None:
            task.template = template
        if priority is not None:
            task.priority = priority.lower()

        if self.memory_bank:
            self.memory_bank.update_task(task.title, description, priority)
        self.save_tasks()
        return task

    def update_task_status(
        self,
        task_id: Union[str, int],
        status: Union[str, TaskStatus],
        notes: Optional[str] = None,
    ) -> Task:
        """Update task status.

        Args:
            task_id: ID of the task to update
            status: New status (either TaskStatus enum or string)
            notes: Optional notes about the status update

        Returns:
            Task: The updated task

        Raises:
            KeyError: If task does not exist
            ValueError: If status string is invalid
        """
        task = self.get_task(task_id)
        if isinstance(status, str):
            try:
                status = TaskStatus[status.upper()]
            except KeyError:
                raise ValueError(f"Invalid status: {status}")

        task.status = status
        if self.memory_bank:
            self.memory_bank.update_task_status(task.title, status.value, notes)
        self.save_tasks()
        return task

    def delete_task(self, task_id: Union[str, int]) -> None:
        """Delete a task."""
        if isinstance(task_id, int):
            task_id = str(task_id)
        if task_id not in self.tasks:
            raise KeyError(f"Task '{task_id}' not found")
        del self.tasks[task_id]
        self.save_tasks()

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        sort_by: Optional[str] = None,
    ) -> List[Task]:
        """List tasks with optional filtering and sorting."""
        tasks = list(self.tasks.values())

        if status:
            tasks = [task for task in tasks if task.status == status]

        if sort_by:
            tasks.sort(key=lambda x: getattr(x, sort_by))

        return tasks

    def export_tasks(self, path: Union[str, Path]) -> None:
        """Export tasks to a JSON file."""
        path = Path(path)
        with open(path, "w") as f:
            yaml.dump(
                {title: task.to_dict() for title, task in self.tasks.items()},
                f,
                default_flow_style=False,
            )

    def import_tasks(self, path: Union[str, Path]) -> None:
        """Import tasks from a JSON file."""
        path = Path(path)
        with open(path) as f:
            data = yaml.safe_load(f)
            if data and isinstance(data, dict):
                self.tasks = {
                    title: Task.from_dict(task_data)
                    for title, task_data in data.items()
                }
                self.save_tasks()


class MemoryBank:
    """Manages persistent memory and context for the development workflow."""

    def __init__(
        self, docs_path: Union[str, Path], max_tokens: int = 2_000_000
    ) -> None:
        """Initialize MemoryBank with path and token limit."""
        self.docs_path = Path(docs_path)
        self.max_tokens = max_tokens
        self.is_active = False
        self.current_tokens = 0
        self.required_files = [
            "productContext.md",
            "activeContext.md",
            "systemPatterns.md",
            "techContext.md",
            "progress.md",
            "commandHistory.md"
        ]

    def initialize(self) -> None:
        """Initialize the memory bank by creating required files."""
        self.docs_path.mkdir(parents=True, exist_ok=True)
        for file_name in self.required_files:
            file_path = self.docs_path / file_name
            if not file_path.exists():
                file_path.touch()
        self.is_active = True

    def update_context(
        self, file_name: str, section: str, content: str, mode: str = "append"
    ) -> None:
        """Update a specific context file with new content."""
        if not self.is_active:
            return

        file_path = self.docs_path / file_name
        if not file_path.exists():
            return

        if mode == "append":
            with open(file_path, "a") as f:
                f.write(f"\n\n## {section}\n{content}")
        else:
            with open(file_path, "w") as f:
                f.write(f"# {section}\n{content}")

    def check_token_limit(self) -> bool:
        """Check if current token count exceeds limit."""
        return self.current_tokens <= self.max_tokens

    def increment_tokens(self, count: int) -> None:
        """Increment token count."""
        self.current_tokens += count

    def decrement_tokens(self, count: int) -> None:
        """Decrement token count."""
        self.current_tokens = max(0, self.current_tokens - count)

    def reset(self) -> None:
        """Reset memory bank state."""
        self.current_tokens = 0
        for file_name in self.required_files:
            file_path = self.docs_path / file_name
            if file_path.exists():
                file_path.unlink()
        self.initialize()

    def add_task(self, title: str, description: str, priority: str) -> None:
        """Add a new task to the memory bank."""
        self.update_context("progress.md", title, f"Priority: {priority}\n{description}")

    def update_task(self, title: str, description: str, priority: str) -> None:
        """Update a task in the memory bank."""
        self.update_context("progress.md", title, f"Priority: {priority}\n{description}", mode="replace")

    def update_task_status(self, title: str, status: str, notes: str) -> None:
        """Update a task status in the memory bank."""
        self.update_context("progress.md", title, f"Status: {status}\n{notes}")
