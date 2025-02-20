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
from prompt_manager.llm_enhancement import LLMEnhancement
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
    created_at: datetime.datetime
    updated_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    dependencies: List[str] = None
    tags: List[str] = None
    priority: int = 0
    notes: List[str] = None

    def __post_init__(self):
        """Initialize default values for lists."""
        self.dependencies = self.dependencies or []
        self.tags = self.tags or []
        self.notes = self.notes or []

class PromptManager:
    """Manages prompts and tasks for a project."""
    
    def __init__(self, project_path: str = None):
        """Initialize PromptManager."""
        self.project_path = project_path or os.getcwd()
        self.config_file = os.path.join(self.project_path, ".prompt-manager", "config.yaml")
        self.tasks_file = os.path.join(self.project_path, ".prompt-manager", "tasks.json")
        self.memory = MemoryBank(self.project_path)
        self.llm = LLMEnhancement(self.memory)
        self._load_or_create_config()
        self._load_tasks()

    def _load_or_create_config(self):
        """Load or create configuration."""
        if not os.path.exists(self.config_file):
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            self.config = {
                "version": __version__,
                "memory_path": "memory",
                "templates_path": "templates",
                "default_template": "default",
            }
            with open(self.config_file, "w") as f:
                yaml.dump(self.config, f)
        else:
            with open(self.config_file, "r") as f:
                self.config = yaml.safe_load(f)

    def _load_tasks(self) -> Dict[str, Task]:
        """Load tasks from file."""
        if not os.path.exists(self.tasks_file):
            os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
            self.tasks = {}
            self._save_tasks()
        else:
            with open(self.tasks_file, "r") as f:
                tasks_data = json.load(f)
                self.tasks = {}
                for task_id, task_data in tasks_data.items():
                    self.tasks[task_id] = Task(
                        id=task_id,
                        title=task_data["title"],
                        description=task_data["description"],
                        status=TaskStatus(task_data["status"]),
                        created_at=datetime.datetime.fromisoformat(task_data["created_at"]),
                        updated_at=datetime.datetime.fromisoformat(task_data["updated_at"]),
                        completed_at=datetime.datetime.fromisoformat(task_data["completed_at"]) if task_data.get("completed_at") else None,
                        dependencies=task_data.get("dependencies", []),
                        tags=task_data.get("tags", []),
                        priority=task_data.get("priority", 0),
                        notes=task_data.get("notes", [])
                    )
        return self.tasks

    def _save_tasks(self):
        """Save tasks to file."""
        tasks_data = {}
        for task_id, task in self.tasks.items():
            tasks_data[task_id] = {
                "title": task.title,
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
        with open(self.tasks_file, "w") as f:
            json.dump(tasks_data, f, indent=2)

    def init_project(self, path: str):
        """Initialize a new project."""
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Create .prompt-manager directory
        prompt_manager_dir = os.path.join(path, ".prompt-manager")
        os.makedirs(prompt_manager_dir, exist_ok=True)
        
        # Create config file
        config_file = os.path.join(prompt_manager_dir, "config.yaml")
        config = {
            "version": __version__,
            "memory_path": "memory",
            "templates_path": "templates",
            "default_template": "default",
        }
        with open(config_file, "w") as f:
            yaml.dump(config, f)
        
        # Create tasks file
        tasks_file = os.path.join(prompt_manager_dir, "tasks.json")
        with open(tasks_file, "w") as f:
            json.dump({}, f)
        
        # Create memory directory
        memory_dir = os.path.join(path, "memory")
        os.makedirs(memory_dir, exist_ok=True)
        
        # Create templates directory
        templates_dir = os.path.join(path, "templates")
        os.makedirs(templates_dir, exist_ok=True)
        
        # Create default template directory
        default_template_dir = os.path.join(templates_dir, "default")
        os.makedirs(default_template_dir, exist_ok=True)
        
        print(f"Initialized project at {path}")
        return True

    def add_task(self, title: str, description: str = "", template: str = None, priority: int = 0) -> Task:
        """Add a new task."""
        task_id = str(uuid.uuid4())
        now = datetime.datetime.now()
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.not_started,
            created_at=now,
            updated_at=now,
            priority=priority
        )
        self.tasks[task_id] = task
        self._save_tasks()
        return task

    def update_task_progress(self, title: str, status: str, note: str = "") -> Task:
        """Update task progress."""
        task = None
        for t in self.tasks.values():
            if t.title == title:
                task = t
                break
        
        if not task:
            raise ValueError(f"Task '{title}' not found")
        
        task.status = TaskStatus(status)
        task.updated_at = datetime.datetime.now()
        
        if note:
            task.notes.append(note)
        
        if status == TaskStatus.completed.value:
            task.completed_at = datetime.datetime.now()
        
        self._save_tasks()
        return task

    def list_tasks(self) -> List[Task]:
        """List all tasks."""
        return list(self.tasks.values())

    def get_task(self, title: str) -> Optional[Task]:
        """Get a task by title."""
        for task in self.tasks.values():
            if task.title == title:
                return task
        return None

    def get_related_tasks(self, title: str) -> List[Task]:
        """Get tasks related to the given task."""
        task = self.get_task(title)
        if not task:
            return []
        
        related = []
        for t in self.tasks.values():
            if t.id != task.id:
                if (set(t.tags) & set(task.tags)) or \
                   (t.id in task.dependencies) or \
                   (task.id in t.dependencies):
                    related.append(t)
        return related

    def get_project_timeline(self) -> Dict[str, Any]:
        """Get project timeline information."""
        timeline = {
            "start_date": None,
            "end_date": None,
            "total_tasks": len(self.tasks),
            "completed_tasks": 0,
            "in_progress_tasks": 0,
            "blocked_tasks": 0
        }
        
        for task in self.tasks.values():
            if task.status == TaskStatus.completed:
                timeline["completed_tasks"] += 1
            elif task.status == TaskStatus.in_progress:
                timeline["in_progress_tasks"] += 1
            elif task.status == TaskStatus.blocked:
                timeline["blocked_tasks"] += 1
                
            if not timeline["start_date"] or task.created_at < timeline["start_date"]:
                timeline["start_date"] = task.created_at
            if task.completed_at and (not timeline["end_date"] or task.completed_at > timeline["end_date"]):
                timeline["end_date"] = task.completed_at
        
        return timeline

    def get_completion_stats(self) -> Dict[str, Any]:
        """Get task completion statistics."""
        total = len(self.tasks)
        if total == 0:
            return {
                "completion_rate": 0,
                "average_completion_time": 0,
                "blocked_rate": 0
            }
        
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.completed)
        blocked = sum(1 for t in self.tasks.values() if t.status == TaskStatus.blocked)
        
        completion_times = []
        for task in self.tasks.values():
            if task.completed_at:
                completion_time = (task.completed_at - task.created_at).total_seconds() / 3600  # hours
                completion_times.append(completion_time)
        
        return {
            "completion_rate": completed / total,
            "average_completion_time": sum(completion_times) / len(completion_times) if completion_times else 0,
            "blocked_rate": blocked / total
        }

    def get_project_metadata(self) -> Dict[str, Any]:
        """Get project metadata."""
        return {
            "version": self.config["version"],
            "memory_path": self.config["memory_path"],
            "templates_path": self.config["templates_path"],
            "default_template": self.config["default_template"],
            "task_count": len(self.tasks),
            "last_updated": datetime.datetime.now().isoformat()
        }

    def get_historical_exports(self) -> List[Dict[str, Any]]:
        """Get list of historical exports.
        
        Returns:
            List of export records
        """
        if not self.memory:
            return []
        
        exports = []
        content = self.memory.load_context_memory()
        if content:
            for line in content.get("exports", []):
                try:
                    timestamp = datetime.datetime.strptime(
                        line.split("_")[1].strip(),
                        "%Y%m%d_%H%M%S"
                    )
                    exports.append({
                        "id": line.strip(),
                        "timestamp": timestamp.isoformat(),
                        "task_count": len(self.tasks)
                    })
                except (ValueError, IndexError):
                    continue
        return exports

    def export_tasks(self, filename: str):
        """Export tasks to a file."""
        tasks_data = {}
        for task_id, task in self.tasks.items():
            tasks_data[task_id] = {
                "title": task.title,
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
        
        with open(filename, "w") as f:
            if filename.endswith(".json"):
                json.dump(tasks_data, f, indent=2)
            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                yaml.dump(tasks_data, f)
        
        if self.memory:
            # Load existing context
            context = self.memory.load_context_memory()
            
            # Add new export record
            export_id = f"TaskExport_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if "exports" not in context:
                context["exports"] = []
            context["exports"].append({
                "id": export_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "filename": filename,
                "task_count": len(tasks_data)
            })
            
            # Save updated context
            self.memory.save_context_memory(context)

    def delete_task(self, title: str) -> bool:
        """Delete a task."""
        task_id = None
        for tid, task in self.tasks.items():
            if task.title == title:
                task_id = tid
                break
        
        if not task_id:
            return False
        
        del self.tasks[task_id]
        self._save_tasks()
        return True

    def generate_bolt_tasks(self, description: str, framework: Optional[str] = None) -> List[str]:
        """Generate tasks for a bolt.new project.
        
        Args:
            description: Project description
            framework: Optional target framework
            
        Returns:
            List of task descriptions
        """
        # Get existing tasks for context
        existing_tasks = self.list_tasks()
        
        # Generate tasks using LLM
        result = self.llm.generate_tasks(
            description=description,
            framework=framework,
            existing_tasks=existing_tasks
        )
        
        # Extract and return task list
        return result.get('tasks', [])
