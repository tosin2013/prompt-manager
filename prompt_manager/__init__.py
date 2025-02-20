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
from dataclasses import dataclass
import json
from prompt_manager.memory import MemoryBank
import uuid

class TaskStatus(Enum):
    """Task status enum."""
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"
    cancelled = "cancelled"

@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    dependencies: List[str] = None
    tags: List[str] = None
    priority: int = 0
    notes: List[str] = None

class PromptManager:
    """Manages prompts and tasks for a project."""
    
    def __init__(self, project_path: str = None):
        """Initialize PromptManager."""
        self.tasks: Dict[str, Task] = {}
        self.config = {
            "version": "0.3.18",
            "memory_path": "memory",
            "templates_path": "templates",
            "default_template": "default",
        }
        
        if project_path:
            self.project_path = Path(project_path).resolve()
            # Try to load existing config
            config_file = self.project_path / ".prompt-manager/config.yaml"
            if config_file.exists():
                with open(config_file, "r") as f:
                    self.config.update(yaml.safe_load(f))
            self._load_tasks()
        else:
            # Try to load config from current directory
            self.project_path = Path.cwd()
            config_file = self.project_path / ".prompt-manager/config.yaml"
            if config_file.exists():
                with open(config_file, "r") as f:
                    self.config.update(yaml.safe_load(f))
                self._load_tasks()
        self.memory_bank = None

    def _load_or_create_config(self):
        config_path = self.project_path / "prompt_manager_config.yaml"
        if config_path.exists():
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        else:
            return {
                "memory_path": str(self.project_path / "memory"),
                "created_at": datetime.datetime.now().isoformat()
            }

    def _load_tasks(self) -> Dict[str, Task]:
        """Load tasks from memory directory."""
        try:
            memory_bank = MemoryBank(str(self.project_path))
            tasks_data = memory_bank.load_task_memory()
            
            tasks = {}
            for title, data in tasks_data.items():
                tasks[title] = Task(
                    id=data.get("id", title),
                    title=title,
                    description=data.get("description", ""),
                    status=TaskStatus(data.get("status", "not_started")),
                    created_at=datetime.datetime.fromisoformat(data.get("created_at")),
                    updated_at=datetime.datetime.fromisoformat(data.get("updated_at")),
                    completed_at=datetime.datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
                    dependencies=data.get("dependencies", []),
                    tags=data.get("tags", []),
                    priority=data.get("priority", 0),
                    notes=data.get("notes", [])
                )
            return tasks
        except Exception as e:
            print(f"Warning: Failed to load tasks: {e}")
            return {}

    def _save_tasks(self):
        """Save tasks to disk."""
        tasks_file = self.project_path / self.config["memory_path"] / "tasks.json"
        tasks_data = {}
        for title, task in self.tasks.items():
            tasks_data[title] = {
                "id": task.id,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "dependencies": task.dependencies,
                "tags": task.tags,
                "priority": task.priority,
                "notes": task.notes
            }
        
        with open(tasks_file, "w") as f:
            json.dump(tasks_data, f, indent=2)

    def init_project(self, path: str):
        """Initialize a new project.
        
        Args:
            path: Path to initialize project at
        """
        self.project_path = Path(path).resolve()
        
        # Create project directory if it doesn't exist
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        # Create config directory
        config_dir = self.project_path / ".prompt-manager"
        config_dir.mkdir(exist_ok=True)
        
        # Create memory directory
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir(exist_ok=True)
        
        # Create initial memory files
        memory_bank = MemoryBank(str(self.project_path))
        memory_bank._init_memory_files()
        
        # Create config file if it doesn't exist
        config_file = config_dir / "config.yaml"
        if not config_file.exists():
            with open(config_file, "w") as f:
                yaml.dump(self.config, f)
        
        # Create templates directory
        templates_dir = self.project_path / self.config["templates_path"]
        templates_dir.mkdir(exist_ok=True)
        
        # Create default template directory
        default_template_dir = templates_dir / self.config["default_template"]
        default_template_dir.mkdir(exist_ok=True)
        
        print(f"Initialized project at {self.project_path}")
        return True

    def add_task(self, title: str, description: str = "", template: str = None, priority: int = 0) -> Task:
        """Add a new task.
        
        Args:
            title: Task title
            description: Task description
            template: Optional task template
            priority: Task priority
            
        Returns:
            Task: The created task
        """
        now = datetime.datetime.now()
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            status=TaskStatus.not_started,
            created_at=now,
            updated_at=now,
            completed_at=None,
            dependencies=[],
            tags=[],
            priority=priority,
            notes=[]
        )
        
        self.tasks[title] = task
        self._save_tasks()
        return task

    def update_task_progress(self, title: str, status: str, note: str = "") -> Task:
        """Update task progress.
        
        Args:
            title: Task title
            status: New task status
            note: Optional note about the update
            
        Returns:
            Task: Updated task
        """
        # Load latest tasks from memory
        self.tasks = self._load_tasks()
        
        if title not in self.tasks:
            raise ValueError(f"Task '{title}' not found")
            
        task = self.tasks[title]
        task.status = TaskStatus(status)
        task.updated_at = datetime.datetime.now()
        
        if status == TaskStatus.completed.value:
            task.completed_at = datetime.datetime.now()
            
        if note:
            task.notes.append(note)
            
        # Save updated task
        self._save_tasks()
        return task

    def list_tasks(self) -> List[Task]:
        """List all tasks.
        
        Returns:
            List[Task]: List of tasks
        """
        # Load tasks from memory
        self.tasks = self._load_tasks()
        return list(self.tasks.values())
    
    def get_task(self, title: str) -> Optional[Task]:
        """Get a task by title.
        
        Args:
            title: Task title
            
        Returns:
            Optional[Task]: Task if found, None otherwise
        """
        # Load latest tasks from memory
        self.tasks = self._load_tasks()
        return self.tasks.get(title)
    
    def get_related_tasks(self, title: str) -> List[Task]:
        """Get tasks related to the given task.
        
        Args:
            title: Task title
            
        Returns:
            List of related tasks
        """
        task = self.get_task(title)
        if not task:
            return []
        
        # For now, just return tasks with same priority
        return [t for t in self.tasks.values() 
                if t.priority == task.priority and t.title != title]
    
    def get_project_timeline(self) -> Dict[str, Any]:
        """Get project timeline information.
        
        Returns:
            Dictionary with timeline information
        """
        if not self.tasks:
            return {"start": None, "end": None, "duration": 0}
        
        dates = [task.created_at for task in self.tasks.values()]
        start = min(dates)
        end = max(task.updated_at for task in self.tasks.values())
        
        return {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "duration": (end - start).days
        }
    
    def get_completion_stats(self) -> Dict[str, Any]:
        """Get task completion statistics.
        
        Returns:
            Dictionary with completion statistics
        """
        total = len(self.tasks)
        if not total:
            return {"total": 0, "completed": 0, "completion_rate": 0}
        
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.completed])
        return {
            "total": total,
            "completed": completed,
            "completion_rate": completed / total
        }
    
    def get_project_metadata(self) -> Dict[str, Any]:
        """Get project metadata.
        
        Returns:
            Dictionary with project metadata
        """
        return {
            "tasks": len(self.tasks),
            "timeline": self.get_project_timeline(),
            "completion": self.get_completion_stats()
        }
    
    def get_historical_exports(self) -> List[Dict[str, Any]]:
        """Get history of task exports.
        
        Returns:
            List of export records
        """
        if not self.memory_bank:
            return []
        
        exports = []
        content = self.memory_bank.read_context("productContext.md")
        if content:
            for line in content.split("\n"):
                if line.startswith("TaskExport_"):
                    exports.append({
                        "timestamp": line.split("_")[1],
                        "description": line
                    })
        return exports
    
    def export_tasks(self, filename: str):
        """Export tasks to a file.
        
        Args:
            filename: Output filename
        """
        tasks_data = []
        for task in self.tasks.values():
            task_data = {
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "priority": task.priority,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "notes": task.notes
            }
            tasks_data.append(task_data)
        
        with open(filename, "w") as f:
            yaml.dump(tasks_data, f)
        
        if self.memory_bank:
            self.memory_bank.update_context(
                "productContext.md",
                f"TaskExport_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                f"Tasks exported to {filename}",
                mode="append"
            )

    def delete_task(self, title: str) -> bool:
        """Delete a task.
        
        Args:
            title: Task title
            
        Returns:
            bool: True if task was deleted, False otherwise
        """
        # Load latest tasks from memory
        self.tasks = self._load_tasks()
        
        if title not in self.tasks:
            return False
            
        del self.tasks[title]
        self._save_tasks()
        return True
