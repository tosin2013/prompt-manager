"""
Models for the prompt manager.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict


class TaskStatus(Enum):
    """Task status."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


@dataclass
class Task:
    """Task model."""
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: str = "medium"
    dependencies: Optional[List[str]] = None
    assignee: Optional[str] = None
    due_date: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert Task to a dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "assignee": self.assignee,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task from a dictionary."""
        return cls(
            title=data["title"],
            description=data.get("description"),
            priority=data.get("priority", "medium"),
            status=TaskStatus(data.get("status", "todo")),
            dependencies=data.get("dependencies"),
            assignee=data.get("assignee"),
            due_date=data.get("due_date")
        )


@dataclass
class BoltTask:
    """Bolt task model."""
    # Required fields first
    bolt_id: str
    bolt_type: str
    bolt_status: str
    bolt_priority: int
    title: str
    
    # Optional fields with defaults
    description: Optional[str] = None
    priority: str = "medium"
    status: TaskStatus = TaskStatus.TODO
    dependencies: Optional[List[str]] = None
    subtasks: Optional[List['BoltTask']] = field(default_factory=list)
    metadata: Optional[Dict[str, str]] = field(default_factory=dict)
    bolt_assignee: Optional[str] = None
    bolt_due_date: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert BoltTask to a dictionary."""
        return {
            "bolt_id": self.bolt_id,
            "bolt_type": self.bolt_type,
            "bolt_status": self.bolt_status,
            "bolt_priority": self.bolt_priority,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "subtasks": [t.to_dict() for t in self.subtasks] if self.subtasks else None,
            "metadata": self.metadata,
            "bolt_assignee": self.bolt_assignee,
            "bolt_due_date": self.bolt_due_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BoltTask':
        """Create a BoltTask from a dictionary."""
        return cls(
            bolt_id=data["bolt_id"],
            bolt_type=data["bolt_type"],
            bolt_status=data["bolt_status"],
            bolt_priority=data["bolt_priority"],
            title=data["title"],
            description=data.get("description"),
            priority=data.get("priority", "medium"),
            status=TaskStatus(data.get("status", "todo")),
            dependencies=data.get("dependencies"),
            subtasks=[cls.from_dict(t) for t in data["subtasks"]] if data.get("subtasks") else [],
            metadata=data.get("metadata", {}),
            bolt_assignee=data.get("bolt_assignee"),
            bolt_due_date=data.get("bolt_due_date")
        )


__all__ = ['Task', 'BoltTask', 'TaskStatus']
