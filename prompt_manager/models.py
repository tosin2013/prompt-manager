"""
Data models for the prompt manager system.
"""

import datetime
from enum import Enum
from typing import Dict, Any, List, Optional


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"


class Task:
    """Represents a task with its properties and metadata."""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        status: TaskStatus = TaskStatus.PENDING,
        prompt_template: str = "",
        notes: List[str] = None,
    ):
        """Initialize a new task.

        Args:
            title: Title of the task
            description: Detailed description
            priority: Task priority (low/medium/high)
            status: Current status
            prompt_template: Template for task prompts
            notes: List of notes about the task
        """
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.prompt_template = prompt_template
        self.notes = notes or []
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at

    def update_status(self, status: TaskStatus, note: Optional[str] = None) -> None:
        """Update task status and optionally add a note."""
        self.status = status
        self.updated_at = datetime.datetime.now()
        if note:
            timestamp = self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            self.notes.append(f"{timestamp} - {note}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization."""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status.value,
            "prompt_template": self.prompt_template,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            status=TaskStatus(data.get("status", "pending")),
            prompt_template=data.get("prompt_template", ""),
            notes=data.get("notes", []),
        )
        task.created_at = datetime.datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.datetime.fromisoformat(data["updated_at"])
        return task


class BoltTask(Task):
    """Represents a task specifically for bolt.new development."""

    def __init__(
        self,
        title: str,
        description: str = "",
        prompt_template: str = "",
        framework: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        ui_components: Optional[List[str]] = None,
        api_endpoints: Optional[List[Dict[str, str]]] = None,
        priority: str = "medium",
        status: TaskStatus = TaskStatus.PENDING,
        notes: List[str] = None,
    ):
        """Initialize a new bolt.new task."""
        super().__init__(
            title=title,
            description=description,
            prompt_template=prompt_template,
            priority=priority,
            status=status,
            notes=notes,
        )
        self.framework = framework
        self.dependencies = dependencies or []
        self.ui_components = ui_components or []
        self.api_endpoints = api_endpoints or []

    def generate_prompt(self) -> str:
        """Generate a prompt using the template and task details."""
        prompt = self.prompt_template.format(
            framework=self.framework, description=self.description
        )

        # Add dependencies if present
        if self.dependencies:
            prompt += "\n\nDependencies:\n" + "\n".join(
                [f"- {dep}" for dep in self.dependencies]
            )

        # Add UI components if present
        if self.ui_components:
            prompt += "\n\nUI Components:\n" + "\n".join(
                [f"- {comp}" for comp in self.ui_components]
            )

        # Add API endpoints if present
        if self.api_endpoints:
            prompt += "\n\nAPI Endpoints:"
            for endpoint in self.api_endpoints:
                path = endpoint['path']
                method = endpoint['method']
                desc = endpoint.get('description', '')
                prompt += f"\n- {method} {path}"
                if desc:
                    prompt += f": {desc}"

        return prompt

    def to_bolt_prompt(self) -> str:
        """Generate a bolt.new-compatible prompt."""
        prompt = [
            f"# {self.title}",
            f"Description: {self.description}",
            f"Framework: {self.framework}",
        ]

        if self.dependencies:
            prompt.append("\nDependencies:")
            prompt.extend([f"- {dep}" for dep in self.dependencies])

        if self.ui_components:
            prompt.append("\nUI Components:")
            prompt.extend([f"- {comp}" for comp in self.ui_components])

        if self.api_endpoints:
            prompt.append("\nAPI Endpoints:")
            for endpoint in self.api_endpoints:
                prompt.append(
                    f"- {endpoint['method']} {endpoint['path']}: {endpoint.get('description', '')}"
                )

        prompt.append(f"\nPrompt Template:\n{self.prompt_template}")
        return "\n".join(prompt)

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization."""
        data = super().to_dict()
        data.update(
            {
                "framework": self.framework,
                "dependencies": self.dependencies,
                "ui_components": self.ui_components,
                "api_endpoints": self.api_endpoints,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BoltTask":
        """Create task from dictionary."""
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            prompt_template=data.get("prompt_template", ""),
            framework=data.get("framework"),
            dependencies=data.get("dependencies", []),
            ui_components=data.get("ui_components", []),
            api_endpoints=data.get("api_endpoints", []),
            priority=data.get("priority", "medium"),
            status=TaskStatus(data.get("status", "pending")),
            notes=data.get("notes", []),
        )
        task.created_at = datetime.datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.datetime.fromisoformat(data["updated_at"])
        return task
