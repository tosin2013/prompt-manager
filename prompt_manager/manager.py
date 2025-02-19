"""
Core prompt manager functionality.

This module provides the main PromptManager class which handles task management,
configuration, and memory persistence. It serves as the central coordinator
for the prompt management system.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import yaml

from .models import Task, TaskStatus, BoltTask
from .memory import MemoryBank
from .debug import DebugManager


class PromptManager:
    """Main class for managing prompts and tasks.
    
    Handles task creation, storage, and retrieval along with configuration
    management and memory persistence.

    Attributes:
        project_name (str): Name of the current project
        memory_bank (MemoryBank): Memory management system
        config (Dict[str, Any]): Configuration settings
        tasks (Dict[str, Task]): Dictionary of tasks indexed by ID
        debug_mode (bool): Whether debug mode is enabled
        is_initialized (bool): Whether manager has been initialized
    """

    def __init__(
        self,
        project_name: str = "",
        memory_path: Optional[Union[str, Path]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize PromptManager with project configuration.
        
        Args:
            project_name: Name of the project
            memory_path: Path to store memory files, defaults to cwd/cline_docs
            config: Optional configuration dictionary
        """
        self.project_name = project_name
        self.memory_bank = MemoryBank(memory_path or Path.cwd() / "cline_docs")
        self.config = config or {}
        self.tasks: Dict[str, Task] = {}
        self.debug_mode = False
        self.is_initialized = False
        self.initialize()

    def initialize(self) -> None:
        """Initialize the prompt manager and memory bank.
        
        Loads configuration, initializes memory bank, and loads existing tasks.
        Only runs once, subsequent calls will be ignored if already initialized.
        """
        if not self.is_initialized:
            self._load_config()
            self.memory_bank.initialize()
            self.load_tasks()
            self.is_initialized = True

    def _load_config(self) -> None:
        """Load configuration from prompt_config.yaml if it exists.
        
        Updates the current config dictionary with values from the file.
        """
        config_path = Path("prompt_config.yaml")
        if config_path.exists():
            with open(config_path) as f:
                self.config.update(yaml.safe_load(f))

    def load_tasks(self) -> None:
        """Load tasks from tasks.yaml storage file.
        
        Creates an empty tasks.yaml file if it doesn't exist.
        """
        tasks_file = Path("tasks.yaml")
        if tasks_file.exists():
            with open(tasks_file) as f:
                tasks_data = yaml.safe_load(f)
                if tasks_data:
                    for task_data in tasks_data:
                        if task_data.get("framework"):  # BoltTask
                            task = BoltTask.from_dict(task_data)
                        else:  # Regular Task
                            task = Task.from_dict(task_data)
                        self.tasks[task.title] = task

    def save_tasks(self) -> None:
        """Save tasks to tasks.yaml storage file."""
        tasks_data = [task.to_dict() for task in self.tasks.values()]
        with open("tasks.yaml", "w") as f:
            yaml.safe_dump(tasks_data, f)

    def add_task(
        self,
        title: str,
        description: str,
        template: Optional[str] = None,
        priority: str = "medium",
    ) -> Task:
        """Add a new task to the workflow.
        
        Args:
            title: Task title
            description: Task description
            template: Optional prompt template
            priority: Task priority (low, medium, high)
        
        Returns:
            Task: Newly created task
        """
        if title in self.tasks:
            raise ValueError(f"Task with title '{title}' already exists")
        
        if priority not in ["low", "medium", "high"]:
            raise ValueError(f"Invalid priority '{priority}'. Must be one of: low, medium, high")
        
        task = Task(
            title=title,
            description=description,
            prompt_template=template or "",
            priority=priority,
        )
        self.tasks[title] = task
        self.save_tasks()
        return task

    def get_task(self, task_id: Union[str, int]) -> Task:
        """Get a task by its ID.
        
        Args:
            task_id: Task ID (title or index)
        
        Returns:
            Task: Task object
        """
        if isinstance(task_id, int):
            try:
                return list(self.tasks.values())[task_id]
            except IndexError:
                raise KeyError(f"No task found at index {task_id}")
        return self.tasks[task_id]

    def update_task(
        self,
        task_id: Union[str, int],
        description: Optional[str] = None,
        template: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Task:
        """Update task details.
        
        Args:
            task_id: Task ID (title or index)
            description: Optional new description
            template: Optional new prompt template
            priority: Optional new priority
        
        Returns:
            Task: Updated task
        """
        task = self.get_task(task_id)
        
        if description is not None:
            task.description = description
        if template is not None:
            task.prompt_template = template
        if priority is not None:
            if priority not in ["low", "medium", "high"]:
                raise ValueError(f"Invalid priority '{priority}'. Must be one of: low, medium, high")
            task.priority = priority
            
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
            task_id: Task ID (title or index)
            status: New task status
            notes: Optional notes
        
        Returns:
            Task: Updated task
        """
        task = self.get_task(task_id)
        
        if isinstance(status, str):
            try:
                status = TaskStatus(status.lower())
            except ValueError:
                raise ValueError(f"Invalid status '{status}'. Must be one of: {[s.value for s in TaskStatus]}")
                
        task.update_status(status, notes)
        self.save_tasks()
        return task

    def delete_task(self, task_id: Union[str, int]) -> None:
        """Delete a task.
        
        Args:
            task_id: Task ID (title or index)
        """
        task = self.get_task(task_id)
        del self.tasks[task.title]
        self.save_tasks()

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        sort_by: Optional[str] = None,
    ) -> List[Task]:
        """List tasks with optional filtering and sorting.
        
        Args:
            status: Optional task status filter
            sort_by: Optional sorting key (priority, created, updated)
        
        Returns:
            List[Task]: List of tasks
        """
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
            
        if sort_by:
            if sort_by == "priority":
                priority_order = {"high": 0, "medium": 1, "low": 2}
                tasks.sort(key=lambda x: priority_order[x.priority])
            elif sort_by == "created":
                tasks.sort(key=lambda x: x.created_at)
            elif sort_by == "updated":
                tasks.sort(key=lambda x: x.updated_at)
                
        return tasks

    def export_tasks(self, path: Union[str, Path]) -> None:
        """Export tasks to a JSON file.
        
        Args:
            path: Path to export file
        """
        path = Path(path)
        tasks_data = [task.to_dict() for task in self.tasks.values()]
        with open(path, "w") as f:
            yaml.safe_dump(tasks_data, f)

    def import_tasks(self, path: Union[str, Path]) -> None:
        """Import tasks from a JSON file.
        
        Args:
            path: Path to import file
        """
        path = Path(path)
        with open(path) as f:
            tasks_data = yaml.safe_load(f)
            for task_data in tasks_data:
                if task_data.get("framework"):  # BoltTask
                    task = BoltTask.from_dict(task_data)
                else:  # Regular Task
                    task = Task.from_dict(task_data)
                self.tasks[task.title] = task
        self.save_tasks()

    def enable_debug(self) -> None:
        """Enable debug mode."""
        self.debug_mode = True

    def disable_debug(self) -> None:
        """Disable debug mode."""
        self.debug_mode = False

    def debug_log(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log debug information if debug mode is enabled.
        
        Args:
            message: Debug message
            context: Optional context dictionary
        """
        if self.debug_mode:
            log_entry = f"[DEBUG] {message}"
            if context:
                log_entry += f"\nContext: {context}"
            print(log_entry)

    def get_prompt(self, task_title: str, **kwargs: Any) -> str:
        """Get formatted prompt for a task.
        
        Args:
            task_title: Task title
            **kwargs: Optional keyword arguments for prompt formatting
        
        Returns:
            str: Formatted prompt
        """
        task = self.get_task(task_title)
        if isinstance(task, BoltTask):
            return task.generate_prompt()
        return task.prompt_template.format(**kwargs)

    def load_project(self) -> None:
        """Load existing project data if available."""
        self.initialize()

    def save_project(self) -> None:
        """Save project data to YAML."""
        self.save_tasks()

    def add_task_to_project(self, title: str, description: str, prompt_template: str) -> Task:
        """Add a new task to the project.
        
        Args:
            title: Task title
            description: Task description
            prompt_template: Prompt template
        
        Returns:
            Task: Newly created task
        """
        return self.add_task(title, description, prompt_template)

    def get_task_from_project(self, title: str) -> Task:
        """Get a task by title.
        
        Args:
            title: Task title
        
        Returns:
            Task: Task object
        """
        return self.get_task(title)

    def update_progress(self, task_title: str, status: TaskStatus, note: str) -> None:
        """Update task progress.
        
        Args:
            task_title: Task title
            status: New task status
            note: Optional note
        """
        self.update_task_status(task_title, status, note)

    def update_markdown_files(self) -> None:
        """Update all markdown files with current project state."""
        self._update_project_plan()
        self._update_task_breakdown()
        self._update_progress_tracking()
        self._update_mermaid_diagrams()

    def _update_project_plan(self) -> None:
        """Update project_plan.md."""
        content = f"# {self.project_name} Project Plan\n\n"
        for task in self.list_tasks(sort_by="priority"):
            content += f"## {task.title}\n"
            content += f"Status: {task.status.value}\n"
            content += f"Priority: {task.priority}\n"
            content += f"\n{task.description}\n\n"
            
        with open("project_plan.md", "w") as f:
            f.write(content)

    def _update_task_breakdown(self) -> None:
        """Update task_breakdown.md."""
        content = "# Task Breakdown\n\n"
        for task in self.list_tasks():
            content += f"## {task.title}\n"
            content += f"- Status: {task.status.value}\n"
            content += f"- Priority: {task.priority}\n"
            content += f"- Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"- Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
        with open("task_breakdown.md", "w") as f:
            f.write(content)

    def _update_progress_tracking(self) -> None:
        """Update progress_tracking.md."""
        content = "# Progress Tracking\n\n"
        for task in self.list_tasks(sort_by="updated"):
            content += f"## {task.title}\n"
            content += f"Current Status: {task.status.value}\n\n"
            if task.notes:
                content += "### Notes:\n"
                for note in task.notes:
                    content += f"- {note}\n"
            content += "\n"
            
        with open("progress_tracking.md", "w") as f:
            f.write(content)

    def _update_mermaid_diagrams(self) -> None:
        """Update mermaid_diagrams.md with current project state."""
        content = "# Project Diagrams\n\n"
        
        # Task Status Flow
        content += "## Task Status Flow\n"
        content += "```mermaid\n"
        content += "graph TD\n"
        for task in self.tasks.values():
            content += f"    {task.title}[{task.title}] --> {task.status.value}\n"
        content += "```\n\n"
        
        # Task Priority Distribution
        content += "## Task Priority Distribution\n"
        content += "```mermaid\n"
        content += "pie\n"
        priorities = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks.values():
            priorities[task.priority] += 1
        for priority, count in priorities.items():
            content += f'    "{priority}" : {count}\n'
        content += "```\n"
        
        with open("mermaid_diagrams.md", "w") as f:
            f.write(content)

    def handle_task_failure(self, task: Task, error_message: str) -> None:
        """Handle task failure.
        
        Args:
            task: Task object
            error_message: Error message
        """
        debug_manager = DebugManager()
        debug_results = debug_manager.trace_error(error_message, task)
        
        # Update task status and add debug information
        self.update_task_status(
            task.title,
            TaskStatus.FAILED,
            f"Error: {error_message}\nDebug Results: {debug_results}"
        )
