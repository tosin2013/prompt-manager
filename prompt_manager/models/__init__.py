"""
Models for the prompt manager.
"""

from dataclasses import dataclass, field, fields
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"

    @classmethod
    def from_str(cls, status: str) -> 'TaskStatus':
        """Create TaskStatus from string, with validation."""
        try:
            return cls(status.lower())
        except ValueError:
            raise ValueError(f"Invalid status: {status}. Must be one of: {[s.value for s in cls]}")


@dataclass
class Task:
    """Task model."""
    title: str
    description: str
    template: str = ""  # Template for task prompts
    status: TaskStatus = TaskStatus.PENDING
    priority: str = "medium"
    dependencies: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    status_notes: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Title must be a non-empty string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.template, str):
            raise ValueError("Template must be a string")
        if not isinstance(self.priority, str):
            raise ValueError("Priority must be a string")
        if self.priority.lower() not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of: low, medium, high")
        if self.due_date:
            try:
                datetime.fromisoformat(self.due_date)
            except ValueError:
                raise ValueError("Due date must be in ISO format (YYYY-MM-DD)")
        if not isinstance(self.dependencies, list):
            raise ValueError("Dependencies must be a list")
        if not isinstance(self.status_notes, list):
            raise ValueError("Status notes must be a list")

    def to_dict(self) -> dict:
        """Convert Task to a dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "template": self.template,
            "status": self.status.value,
            "priority": self.priority.lower(),
            "dependencies": self.dependencies,
            "assignee": self.assignee,
            "due_date": self.due_date,
            "status_notes": self.status_notes
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")
        
        if "title" not in data:
            raise ValueError("Missing required field: title")

        status = data.get('status', TaskStatus.PENDING.value)
        if isinstance(status, str):
            status = TaskStatus.from_str(status)
        elif not isinstance(status, TaskStatus):
            raise ValueError("Status must be a string or TaskStatus enum")

        return cls(
            title=data['title'],
            description=data.get('description', ''),
            template=data.get('template', ''),
            status=status,
            priority=data.get('priority', 'medium').lower(),
            dependencies=data.get('dependencies', []),
            assignee=data.get('assignee'),
            due_date=data.get('due_date'),
            status_notes=data.get('status_notes', [])
        )

    def update_status(self, new_status: TaskStatus, note: Optional[str] = None) -> None:
        """Update task status with optional note."""
        if not isinstance(new_status, TaskStatus):
            raise ValueError("new_status must be a TaskStatus enum")
        
        old_status = self.status
        self.status = new_status
        
        if note:
            timestamp = datetime.now().isoformat()
            self.status_notes.append(f"[{timestamp}] Status changed from {old_status.value} to {new_status.value}: {note}")


@dataclass
class BoltTask:
    """Bolt task model."""
    title: str
    bolt_id: str
    bolt_type: str
    bolt_status: str
    bolt_priority: int
    description: Optional[str] = None
    priority: str = "medium"
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    subtasks: List['BoltTask'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    bolt_assignee: Optional[str] = None
    bolt_due_date: Optional[str] = None

    def __post_init__(self):
        """Validate bolt task data after initialization."""
        if not self.title or not isinstance(self.title, str):
            raise ValueError("title must be a non-empty string")
        if not self.bolt_id or not isinstance(self.bolt_id, str):
            raise ValueError("bolt_id must be a non-empty string")
        if not self.bolt_type or not isinstance(self.bolt_type, str):
            raise ValueError("bolt_type must be a non-empty string")
        if not isinstance(self.bolt_priority, int):
            raise ValueError("bolt_priority must be an integer")
        if self.priority.lower() not in ["low", "medium", "high"]:
            raise ValueError("priority must be one of: low, medium, high")
        if self.bolt_due_date:
            try:
                datetime.fromisoformat(self.bolt_due_date)
            except ValueError:
                raise ValueError("bolt_due_date must be in ISO format (YYYY-MM-DD)")
        if not isinstance(self.dependencies, list):
            raise ValueError("dependencies must be a list")
        if not isinstance(self.subtasks, list):
            raise ValueError("subtasks must be a list")
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dictionary")

    def to_dict(self) -> dict:
        """Convert BoltTask to a dictionary."""
        return {
            "title": self.title,
            "bolt_id": self.bolt_id,
            "bolt_type": self.bolt_type,
            "bolt_status": self.bolt_status,
            "bolt_priority": self.bolt_priority,
            "description": self.description,
            "priority": self.priority.lower(),
            "status": self.status.value,
            "dependencies": self.dependencies,
            "subtasks": [t.to_dict() for t in self.subtasks],
            "metadata": self.metadata,
            "bolt_assignee": self.bolt_assignee,
            "bolt_due_date": self.bolt_due_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BoltTask':
        """Create a BoltTask from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        required_fields = ["title", "bolt_id", "bolt_type", "bolt_status", "bolt_priority"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        status = data.get('status', TaskStatus.PENDING.value)
        if isinstance(status, str):
            status = TaskStatus.from_str(status)
        elif not isinstance(status, TaskStatus):
            raise ValueError("Status must be a string or TaskStatus enum")

        return cls(
            title=data["title"],
            bolt_id=data["bolt_id"],
            bolt_type=data["bolt_type"],
            bolt_status=data["bolt_status"],
            bolt_priority=int(data["bolt_priority"]),
            description=data.get("description"),
            priority=data.get("priority", "medium").lower(),
            status=status,
            dependencies=data.get("dependencies", []),
            subtasks=[cls.from_dict(t) for t in data.get("subtasks", [])],
            metadata=data.get("metadata", {}),
            bolt_assignee=data.get("bolt_assignee"),
            bolt_due_date=data.get("bolt_due_date")
        )


__all__ = ['Task', 'BoltTask', 'TaskStatus']
