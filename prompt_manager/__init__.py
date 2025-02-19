"""
Prompt Manager: Development workflow management system with memory tracking.
"""

__version__ = "0.3.18"

from typing import Dict, Optional, Any, Union, List
from pathlib import Path
from enum import Enum
import yaml
import datetime
import uuid
import os
import logging
import json
from .llm_enhancement import LLMEnhancement


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class PromptManager:
    def __init__(
        self,
        project_name: str = "",
        memory_path: Optional[Union[str, Path]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize PromptManager.

        Args:
            project_name: Name of the project.
            memory_path: Optional path to memory storage.
            config: Optional configuration dictionary.
        """
        self.project_name = project_name
        self.memory_path = memory_path
        self.config = config or {}
        self.memory_bank = MemoryBank(memory_path or Path.cwd() / "cline_docs")
        self.llm_enhancement = LLMEnhancement(self.memory_bank)

    def start_learning_session(self) -> None:
        """Start an autonomous learning session."""
        self.llm_enhancement.start_learning_session()

    def analyze_patterns(self) -> List[str]:
        """Analyze successful interaction patterns."""
        return self.llm_enhancement.analyze_patterns()

    def generate_suggestions(self) -> List[str]:
        """Generate optimization suggestions."""
        return self.llm_enhancement.generate_suggestions()

    def generate_custom_utilities(self) -> List[str]:
        """Generate custom utilities based on project needs."""
        return self.llm_enhancement.generate_custom_utilities()

    def create_custom_commands(self) -> List[str]:
        """Create custom CLI commands based on usage patterns."""
        return self.llm_enhancement.create_custom_commands()

    def process_prompt(self, prompt: str) -> Optional[str]:
        """Process a single prompt and return the response.

        Args:
            prompt: Input prompt to process.

        Returns:
            Processed response or None if processing fails.
        """
        try:
            response = self._generate_response(prompt)
            self._save_response(prompt, response)
            return response
        except Exception as e:
            logging.error(f"Error processing prompt: {str(e)}")
            return None

    def _generate_response(self, prompt: str) -> str:
        """Generate a response for the given prompt.

        Args:
            prompt: Input prompt.

        Returns:
            Generated response.
        """
        return f"Response to: {prompt}"

    def _save_response(self, prompt: str, response: str) -> None:
        """Save prompt-response pair to output directory.

        Args:
            prompt: Original prompt.
            response: Generated response.
        """
        timestamp = datetime.datetime.now().isoformat()
        output_path = os.path.join(
            self.config.get("output_dir", "outputs"),
            f"response_{timestamp}.txt",
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(f"Prompt: {prompt}\nResponse: {response}")

    def process_batch(self, prompts: List[str]) -> List[Optional[str]]:
        """Process a batch of prompts.

        Args:
            prompts: List of prompts to process.

        Returns:
            List of responses (None for failed prompts).
        """
        return [self.process_prompt(prompt) for prompt in prompts]

    def get_prompt_history(self) -> List[Dict[str, str]]:
        """Get history of processed prompts and responses.

        Returns:
            List of prompt-response pairs with timestamps.
        """
        history = []
        output_dir = self.config.get("output_dir", "outputs")

        if not os.path.exists(output_dir):
            return history

        for filename in os.listdir(output_dir):
            if filename.startswith("response_") and filename.endswith(".txt"):
                file_path = os.path.join(output_dir, filename)
                with open(file_path, "r") as f:
                    content = f.read()
                    history.append({
                        "timestamp": filename[9:-4],
                        "content": content,
                    })

        return sorted(history, key=lambda x: x["timestamp"], reverse=True)

    def clear_history(self) -> None:
        """Clear prompt-response history."""
        output_dir = self.config.get("output_dir", "outputs")
        if not os.path.exists(output_dir):
            return

        for filename in os.listdir(output_dir):
            if filename.startswith("response_") and filename.endswith(".txt"):
                os.remove(os.path.join(output_dir, filename))

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update configuration with new settings.

        Args:
            new_config: New configuration settings to apply.
        """
        self.config.update(new_config)


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
            "progress.md"
        ]

    def initialize(self) -> None:
        """Initialize the memory bank by creating required files."""
        self.docs_path.mkdir(parents=True, exist_ok=True)
        for file in self.required_files:
            file_path = self.docs_path / file
            if not file_path.exists():
                file_path.touch()
                # Initialize with basic structure
                with file_path.open('w') as f:
                    f.write(f"# {file[:-3]}\n\n")
        self.is_active = True

    def update_context(
        self, file_name: str, section: str, content: str, mode: str = "append"
    ) -> None:
        """Update a specific context file with new content."""
        if not self.is_active:
            return

        if file_name not in [f.name for f in self.docs_path.glob("*.md")]:
            raise ValueError(f"Invalid file name: {file_name}")

        if mode not in ["append", "replace"]:
            raise ValueError(f"Invalid mode: {mode}")

        file_path = self.docs_path / file_name
        current_content = file_path.read_text() if file_path.exists() else ""

        # Find section in current content
        section_header = f"## {section}"
        section_start = current_content.find(section_header)

        if section_start == -1:
            # Section doesn't exist, append it
            new_content = current_content.rstrip() + f"\n\n{section_header}\n{content}\n"
        else:
            # Find end of section (next ## or end of file)
            next_section = current_content.find("\n##", section_start + 1)
            if next_section == -1:
                next_section = len(current_content)

            if mode == "append":
                # Append to existing section
                section_content = current_content[section_start:next_section].rstrip()
                new_section = f"{section_content}\n{content}"
            else:  # replace
                new_section = f"{section_header}\n{content}"

            new_content = (
                current_content[:section_start] +
                new_section +
                current_content[next_section:]
            )

        # Update token count
        self.increment_tokens(len(new_content) - len(current_content))

        # Write updated content
        with file_path.open('w') as f:
            f.write(new_content)

    def check_token_limit(self) -> bool:
        """Check if current token count exceeds limit."""
        return self.current_tokens >= self.max_tokens

    def increment_tokens(self, count: int) -> None:
        """Increment token count."""
        self.current_tokens += count

    def decrement_tokens(self, count: int) -> None:
        """Decrement token count."""
        self.current_tokens = max(0, self.current_tokens - count)

    def reset(self) -> None:
        """Reset memory bank state."""
        self.is_active = False
        self.current_tokens = 0
        for file in self.required_files:
            file_path = self.docs_path / file
            if file_path.exists():
                file_path.unlink()


class Task:
    """Represents a task in the workflow."""
    
    def __init__(
        self,
        name: str,
        description: str,
        prompt_template: str,
        priority: int = 1,
        status: TaskStatus = TaskStatus.PENDING
    ) -> None:
        """Initialize a new task."""
        self.name = name
        self.description = description
        self.prompt_template = prompt_template
        self.priority = priority
        self.status = status
        self.status_notes: List[str] = []
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at
        self.id = str(uuid.uuid4())

    def update_status(self, status: TaskStatus, note: Optional[str] = None) -> None:
        """Update task status with optional note."""
        self.status = status
        if note:
            self.status_notes.append(note)
        self.updated_at = datetime.datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "prompt_template": self.prompt_template,
            "priority": self.priority,
            "status": self.status.value,
            "status_notes": self.status_notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        task = cls(
            name=data["name"],
            description=data["description"],
            prompt_template=data["prompt_template"],
            priority=data["priority"],
            status=TaskStatus(data["status"])
        )
        task.id = data["id"]
        task.status_notes = data["status_notes"]
        task.created_at = datetime.datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.datetime.fromisoformat(data["updated_at"])
        return task


class BoltTask(Task):
    """Represents a task specifically for bolt.new development."""

    def __init__(
        self,
        name: str,
        description: str,
        prompt_template: str,
        framework: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        ui_components: Optional[List[str]] = None,
        api_endpoints: Optional[List[Dict[str, str]]] = None,
        priority: int = 1,
        status: TaskStatus = TaskStatus.PENDING
    ) -> None:
        """Initialize a new bolt.new task."""
        super().__init__(name, description, prompt_template, priority, status)
        self.framework = framework
        self.dependencies = dependencies or []
        self.ui_components = ui_components or []
        self.api_endpoints = api_endpoints or []

    def generate_prompt(self) -> str:
        """Generate a prompt using the template and task details."""
        prompt = self.prompt_template.format(
            framework=self.framework,
            description=self.description
        )
        
        # Add dependencies if present
        if self.dependencies:
            prompt += f"\n\nDependencies:\n" + "\n".join([f"- {dep}" for dep in self.dependencies])
        
        # Add UI components if present
        if self.ui_components:
            prompt += f"\n\nUI Components:\n" + "\n".join([f"- {comp}" for comp in self.ui_components])
        
        # Add API endpoints if present
        if self.api_endpoints:
            prompt += "\n\nAPI Endpoints:"
            for endpoint in self.api_endpoints:
                prompt += f"\n- {endpoint['method']} {endpoint['path']}"
                if endpoint.get('description'):
                    prompt += f": {endpoint['description']}"
        
        return prompt

    def to_bolt_prompt(self) -> str:
        """Generate a bolt.new-compatible prompt."""
        prompt = [
            f"# {self.name}",
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
        data.update({
            "framework": self.framework,
            "dependencies": self.dependencies,
            "ui_components": self.ui_components,
            "api_endpoints": self.api_endpoints,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BoltTask":
        """Create task from dictionary."""
        task = cls(
            name=data["name"],
            description=data["description"],
            prompt_template=data["prompt_template"],
            framework=data.get("framework"),
            dependencies=data.get("dependencies", []),
            ui_components=data.get("ui_components", []),
            api_endpoints=data.get("api_endpoints", []),
            priority=data.get("priority", 1),
            status=TaskStatus(data.get("status", TaskStatus.PENDING.value))
        )
        task.status_notes = data.get("status_notes", [])
        task.created_at = datetime.datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.datetime.fromisoformat(data["updated_at"])
        task.id = data["id"]
        return task

    @classmethod
    def generate_task_sequence(
        cls,
        project_description: str,
        framework: str,
        dependencies: List[str],
        ui_components: List[str],
        api_endpoints: List[Dict[str, str]]
    ) -> List["BoltTask"]:
        """Generate a sequence of tasks for a bolt.new project.

        Args:
            project_description: Description of the project
            framework: Target framework (e.g., Next.js, React)
            dependencies: List of project dependencies
            ui_components: List of UI components to create
            api_endpoints: List of API endpoints to implement

        Returns:
            List of BoltTask objects representing the development sequence
        """
        tasks = []

        # Project setup task
        tasks.append(cls(
            name="Project Setup",
            description=f"Initialize {framework} project with required dependencies",
            prompt_template="Create a new {framework} project and set up the following dependencies: {dependencies}",
            framework=framework,
            dependencies=dependencies,
            priority=1
        ))

        # UI component tasks
        for component in ui_components:
            tasks.append(cls(
                name=f"{component} Component",
                description=f"Create the {component} component",
                prompt_template="Create a {framework} component for {description}",
                framework=framework,
                dependencies=dependencies,
                ui_components=[component],
                priority=2
            ))

        # API endpoint tasks
        for endpoint in api_endpoints:
            tasks.append(cls(
                name=f"{endpoint['method']} {endpoint['path']} Endpoint",
                description=endpoint.get('description', ''),
                prompt_template="Implement {method} endpoint at {path} for {description}",
                framework=framework,
                dependencies=dependencies,
                api_endpoints=[endpoint],
                priority=3
            ))

        return tasks


class PromptManager:
    """Manages development workflow, tasks, and debugging."""

    def __init__(
        self,
        project_name: str = "",
        memory_path: Optional[Union[str, Path]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize PromptManager with project configuration."""
        self.project_name = project_name
        self.memory_bank = MemoryBank(memory_path or Path.cwd() / "cline_docs")
        self.config = config or {}
        self.tasks: Dict[str, Task] = {}
        self.debug_mode = False
        self.is_initialized = False
        self.llm_enhancement = LLMEnhancement(self.memory_bank)
        self.initialize()

    def initialize(self) -> None:
        """Initialize the prompt manager and memory bank."""
        self.memory_bank.initialize()
        self._load_config()
        self.load_tasks()  # Load existing tasks
        self.is_initialized = True

    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        config_path = self.memory_bank.docs_path / "config.yaml"
        if config_path.exists():
            with config_path.open() as f:
                self.config.update(yaml.safe_load(f) or {})

    def load_tasks(self) -> None:
        """Load tasks from storage."""
        tasks_path = self.memory_bank.docs_path / "tasks.yaml"
        if tasks_path.exists():
            with tasks_path.open() as f:
                data = yaml.safe_load(f) or {}
                self.tasks = {
                    name: Task.from_dict(task_data)
                    for name, task_data in data.items()
                }

    def save_tasks(self) -> None:
        """Save tasks to storage."""
        tasks_path = self.memory_bank.docs_path / "tasks.yaml"
        with tasks_path.open('w') as f:
            data = {name: task.to_dict() for name, task in self.tasks.items()}
            yaml.dump(data, f)

    def add_task(
        self,
        name_or_task: Union[str, Task],
        description: Optional[str] = None,
        prompt_template: Optional[str] = None,
        priority: int = 1,
    ) -> Task:
        """Add a new task to the workflow.
        
        Args:
            name_or_task: Either a Task object or a task name string
            description: Task description (only used if name_or_task is a string)
            prompt_template: Prompt template (only used if name_or_task is a string)
            priority: Task priority (only used if name_or_task is a string)
            
        Returns:
            Task: The added task
            
        Raises:
            ValueError: If task name already exists, required parameters are missing,
                      or priority is invalid
        """
        if isinstance(name_or_task, Task):
            task = name_or_task
            name = task.name
            if task.priority < 1:
                raise ValueError("Priority must be a positive integer")
        else:
            if not description or not prompt_template:
                raise ValueError("Description and prompt_template are required when adding a task by name")
            if priority < 1:
                raise ValueError("Priority must be a positive integer")
            name = name_or_task
            task = Task(
                name=name,
                description=description,
                prompt_template=prompt_template,
                priority=priority,
            )
            
        if name in self.tasks:
            raise ValueError(f"Task {name} already exists")
            
        self.tasks[name] = task
        self.save_tasks()
        return task

    def get_task(self, name: str) -> Task:
        """Get task details by name."""
        if name not in self.tasks:
            raise KeyError(f"Task {name} not found")
        return self.tasks[name]

    def update_task(
        self,
        name: str,
        description: Optional[str] = None,
        prompt_template: Optional[str] = None,
        priority: Optional[int] = None,
    ) -> Task:
        """Update task details."""
        task = self.get_task(name)
        if description is not None:
            task.description = description
        if prompt_template is not None:
            task.prompt_template = prompt_template
        if priority is not None:
            task.priority = priority
        self.save_tasks()
        return task

    def update_task_status(
        self,
        name: str,
        status: Union[str, TaskStatus],
        notes: Optional[str] = None
    ) -> Task:
        """Update task status.
        
        Args:
            name: Name of the task to update
            status: New status (either TaskStatus enum or string)
            notes: Optional notes about the status update
            
        Returns:
            Task: The updated task
            
        Raises:
            KeyError: If task does not exist
            ValueError: If status string is invalid
        """
        task = self.get_task(name)
        if isinstance(status, str):
            try:
                status = TaskStatus(status.upper())
            except ValueError:
                raise ValueError(f"Invalid status: {status}")
        task.update_status(status, notes)
        self.save_tasks()
        return task

    def delete_task(self, name: str) -> None:
        """Delete a task."""
        if name not in self.tasks:
            raise KeyError(f"Task {name} not found")
        del self.tasks[name]
        self.save_tasks()

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        sort_by: Optional[str] = None
    ) -> List[Task]:
        """List tasks with optional filtering and sorting."""
        tasks = list(self.tasks.values())

        if status:
            tasks = [t for t in tasks if t.status == status]

        if sort_by:
            if sort_by == "priority":
                tasks.sort(key=lambda t: t.priority)
            elif sort_by == "created":
                tasks.sort(key=lambda t: t.created_at)
            elif sort_by == "updated":
                tasks.sort(key=lambda t: t.updated_at)

        return tasks

    def export_tasks(self, path: Union[str, Path]) -> None:
        """Export tasks to a JSON file."""
        path = Path(path)
        data = {
            "project_name": self.project_name,
            "tasks": [task.to_dict() for task in self.tasks.values()]
        }
        with path.open('w') as f:
            yaml.dump(data, f)

    def import_tasks(self, path: Union[str, Path]) -> None:
        """Import tasks from a JSON file."""
        path = Path(path)
        with path.open() as f:
            data = yaml.safe_load(f)
            for task_data in data.get("tasks", []):
                task = Task.from_dict(task_data)
                self.tasks[task.name] = task
        self.save_tasks()

    def enable_debug(self) -> None:
        """Enable debug mode."""
        self.debug_mode = True

    def disable_debug(self) -> None:
        """Disable debug mode."""
        self.debug_mode = False

    def debug_log(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log debug information if debug mode is enabled."""
        if self.debug_mode:
            log_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "message": message,
                "context": context or {},
            }
            print(f"DEBUG: {log_entry}")

    def get_prompt(self, task_name: str, **kwargs: Any) -> Optional[str]:
        """Get formatted prompt for a task."""
        task = self.get_task(task_name)
        if task:
            try:
                return task.prompt_template.format(**kwargs)
            except KeyError as e:
                self.debug_log(f"Missing prompt variable: {e}")
                return None
        return None

    def load_project(self):
        """Load existing project data if available"""
        project_data = self.memory_bank.docs_path / "project_data.yaml"
        if project_data.exists():
            with open(project_data, "r") as f:
                data = yaml.safe_load(f)
                for task_data in data.get("tasks", []):
                    task = Task.from_dict(task_data)
                    self.tasks[task.name] = task

    def save_project(self):
        """Save project data to YAML"""
        project_data = {
            "project_name": self.project_name,
            "tasks": [task.to_dict() for task in self.tasks.values()],
        }
        with open(self.memory_bank.docs_path / "project_data.yaml", "w") as f:
            yaml.dump(project_data, f)

    def add_task_to_project(self, name: str, description: str, prompt_template: str) -> Task:
        """Add a new task to the project"""
        task = Task(
            name=name,
            description=description,
            prompt_template=prompt_template,
        )
        self.tasks[name] = task
        self.update_markdown_files()
        self.save_project()
        return task

    def get_task_from_project(self, name: str) -> Optional[Task]:
        """Get a task by name"""
        return self.tasks.get(name)

    def update_progress(self, task_name: str, status: TaskStatus, note: str):
        """Update task progress"""
        task = self.get_task(task_name)
        if task:
            task.update_status(status, note)
            self.update_markdown_files()
            self.save_project()

    def update_markdown_files(self):
        """Update all markdown files with current project state"""
        self._update_project_plan()
        self._update_task_breakdown()
        self._update_progress_tracking()
        self._update_mermaid_diagrams()

    def _update_project_plan(self):
        """Update project_plan.md"""
        content = f"# {self.project_name}\n\n## Tasks\n"
        for task in self.tasks.values():
            content += f"### {task.name}\n"
            content += f"- Status: {task.status.value}\n"
            content += f"- Description: {task.description}\n\n"

        with open(self.memory_bank.docs_path / "project_plan.md", "w") as f:
            f.write(content)

    def _update_task_breakdown(self):
        """Update task_breakdown.md"""
        content = "# Task Breakdown\n\n"
        for task in self.tasks.values():
            content += f"## {task.name}\n"
            content += f"Description: {task.description}\n\n"
            content += "### Prompt Template\n```\n"
            content += task.prompt_template
            content += "\n```\n\n"

        with open(self.memory_bank.docs_path / "task_breakdown.md", "w") as f:
            f.write(content)

    def _update_progress_tracking(self):
        """Update progress_tracking.md"""
        content = f"# Progress Tracking - {self.project_name}\n\n"
        for task in self.tasks.values():
            content += f"## {task.name}\n"
            content += f"Status: {task.status.value}\n\n"
            content += "### Progress Notes\n"
            content += "\n".join(task.status_notes)
            content += "\n"

        with open(self.memory_bank.docs_path / "progress_tracking.md", "w") as f:
            f.write(content)

    def _update_mermaid_diagrams(self):
        """Update mermaid_diagrams.md with current project state"""
        content = "# Project Workflow Diagrams\n\n"

        # Task Status Diagram
        content += "## Task Status\n```mermaid\ngraph TD\n"
        for task in self.tasks.values():
            style = {
                TaskStatus.PENDING: "fill:#fff",
                TaskStatus.IN_PROGRESS: "fill:#yellow",
                TaskStatus.COMPLETED: "fill:#green",
                TaskStatus.FAILED: "fill:#red",
            }.get(task.status, "fill:#fff")

            content += f"    {task.name}[{task.name}]:::status{task.status.value}\n"
        content += "```\n\n"

        with open(self.memory_bank.docs_path / "mermaid_diagrams.md", "w") as f:
            f.write(content)

    def execute_task(self, task_name: str, execution_result: str) -> bool:
        """Execute a task and handle any failures"""
        if self.memory_bank.check_token_limit():
            self._handle_memory_reset()
            return

        task = self.get_task(task_name)
        if not task:
            return

        try:
            # Update active context with current task
            self.memory_bank.update_context(
                "activeContext.md",
                "Current Tasks",
                f"- {task_name}: {task.description}",
            )

            # Execute task
            if "error" in execution_result.lower():
                self._handle_task_failure(task, execution_result)
            else:
                task.update_status(TaskStatus.COMPLETED, execution_result)

                # Update progress in memory bank
                self.memory_bank.update_context(
                    "progress.md", "Completed", f"- {task_name}: {execution_result}"
                )

            self.save_project()
            self.update_markdown_files()

        except Exception as e:
            self._handle_task_failure(task, str(e))

    def _handle_memory_reset(self):
        """Handle memory bank reset"""
        # Document current state
        active_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]
        next_steps = "\n".join(
            [f"- Continue {t.name}: {t.description}" for t in active_tasks]
        )

        self.memory_bank.update_context("activeContext.md", "Next Steps", next_steps)

        # Update progress
        self.memory_bank.update_context(
            "progress.md",
            "In Progress",
            "\n".join([f"- {t.name}: {t.status.value}" for t in self.tasks.values()]),
        )

        # Reset token count
        self.memory_bank.current_tokens = 0

    def _handle_task_failure(self, task: Task, error_message: str):
        """Handle task failure with progressive debugging"""
        # Update active context with failure
        self.memory_bank.update_context(
            "activeContext.md",
            "Recent Changes",
            f"- Failed: {task.name}\n  Error: {error_message}",
        )

        # Try debugging first
        debug_result = self._attempt_debugging(task, error_message)
        if debug_result.success:
            return

        # If debugging fails, try Firecrawl research
        research_result = self._attempt_firecrawl_research(task)
        if research_result.success:
            return

        # If all else fails, perform RCA
        rca_result = self._perform_rca(task)
        if rca_result.success:
            return
        else:
            self._escalate_to_human(task)
            return False

        return False

    def _attempt_debugging(self, task: Task, error_message: str) -> Dict[str, Any]:
        """Attempt to debug a task failure using layered debugging approach"""
        # First try single-file debugging
        debug_result = self._debug_environment_layer(task, error_message)
        if debug_result.success:
            return debug_result

        # If single-file debug fails, try multi-file debugging
        debug_result = self._debug_code_logic_layer(task, error_message)
        if debug_result.success:
            return debug_result

        return {"success": False, "message": "All debugging attempts failed", "fix_attempt": "No successful fix found"}

    def _debug_environment_layer(self, task: Task, error_message: str) -> Dict[str, Any]:
        """Debug environment-related issues"""
        prompt = self._get_debug_prompt("Layered Debug Analysis")
        # Here you would integrate with your LLM to analyze environment issues
        return {"success": False, "message": "Environment layer checked", "fix_attempt": "No issues found"}

    def _debug_code_logic_layer(self, task: Task, error_message: str) -> Dict[str, Any]:
        """Debug code logic issues"""
        prompt = self._get_debug_prompt("Root Cause Analysis")
        # Here you would integrate with your LLM to analyze code logic
        return {"success": False, "message": "Code logic layer checked", "fix_attempt": "No issues found"}

    def _attempt_firecrawl_research(self, task: Task) -> Dict[str, Any]:
        """Attempt to research solutions using Firecrawl"""
        research_prompt = self._get_debug_prompt("Firecrawl Research")
        # Here you would integrate with Firecrawl to search for solutions
        return {"success": False, "message": "Firecrawl research attempted", "fix_attempt": "Research logged"}

    def _perform_rca(self, task: Task) -> Dict[str, Any]:
        """Perform Root Cause Analysis"""
        rca_prompt = self._get_debug_prompt("Root Cause Analysis")
        # Here you would integrate with your LLM to perform RCA
        return {"success": False, "message": "RCA performed", "fix_attempt": "Analysis logged"}

    def _escalate_to_human(self, task: Task):
        """Escalate the issue to human intervention"""
        escalation_note = {
            "timestamp": datetime.datetime.now().isoformat(),
            "message": "Task requires human intervention after multiple failed attempts",
            "debug_history": [],
        }
        self.update_markdown_files()

    def _get_debug_prompt(self, prompt_type: str) -> str:
        """Get a specific type of debugging prompt"""
        with open(self.memory_bank.docs_path / "debugging_prompts.md", "r") as f:
            content = f.read()
            # Parse the content to find the specific prompt type
            # This is a simplified version - you'd want to implement proper YAML parsing
            if prompt_type in content:
                return f"Using {prompt_type} prompt"
            return "Default debugging prompt"

    def debug_file(self, file_path: str, error_message: Optional[str] = None, file_purpose: Optional[str] = None) -> Dict[str, Any]:
        """Perform layered analysis of a single file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        purpose = file_purpose or self._infer_file_purpose(file_path)
        env_issues = self._check_environment(file_path)
        code_issues = self._analyze_code_logic(file_path, error_message)
        integration_issues = self._analyze_integration(file_path)
        
        return {
            "file_purpose": purpose,
            "environment_issues": env_issues,
            "code_issues": code_issues,
            "integration_issues": integration_issues
        }

    def find_root_cause(self, file_path: str, error_message: Optional[str] = None, file_purpose: Optional[str] = None) -> Dict[str, Any]:
        """Find the root cause of an error in a specific file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        issues = self._identify_issues(file_path, error_message)
        purpose = file_purpose or self._infer_file_purpose(file_path)
        fixes = self._suggest_fixes(issues, purpose)
        verification = self._generate_verification_plan(file_path, fixes)
        
        return {
            "issues": issues,
            "suggested_fixes": fixes,
            "verification_plan": verification
        }

    def iterative_fix(self, file_path: str, error_message: Optional[str] = None, file_purpose: Optional[str] = None) -> Dict[str, Any]:
        """Apply iterative fixes to resolve an error."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        key_functions = self._identify_key_functions(file_path, error_message)
        fixes = []
        for func in key_functions:
            fix = self._apply_fix(file_path, func)
            if fix:
                fixes.append(fix)
                if error_message and self._validate_fix(file_path, error_message):
                    break
        
        return {
            "key_functions": key_functions,
            "applied_fixes": fixes
        }

    def generate_test_roadmap(self, file_path: str, error_message: Optional[str] = None, file_purpose: Optional[str] = None) -> Dict[str, Any]:
        """Generate a testing roadmap for a specific file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        existing_tests = self._find_existing_tests(file_path)
        new_tests = self._suggest_new_tests(file_path, error_message, existing_tests)
        test_plan = self._generate_test_plan(file_path, new_tests)
        
        return {
            "existing_tests": existing_tests,
            "suggested_tests": new_tests,
            "test_plan": test_plan
        }

    def analyze_dependencies(self, file_paths: List[str], error_message: Optional[str] = None) -> Dict[str, Any]:
        """Analyze dependencies between files."""
        for path in file_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
        
        dependencies = self._map_dependencies(file_paths)
        error_sources = self._identify_error_sources(dependencies, error_message) if error_message else []
        purposes = {path: self._infer_file_purpose(path) for path in file_paths}
        fixes = self._suggest_cross_file_fixes(error_sources, purposes)
        
        return {
            "dependencies": dependencies,
            "error_sources": error_sources,
            "suggested_fixes": fixes
        }

    def trace_error(self, file_paths: List[str], error_message: Optional[str] = None) -> Dict[str, Any]:
        """Trace error path across multiple files."""
        for path in file_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
        
        error_path = self._map_error_path(file_paths, error_message)
        primary_fixes = self._suggest_primary_fixes(error_path)
        secondary_fixes = self._suggest_secondary_fixes(error_path)
        verification = self._generate_verification_steps(primary_fixes + secondary_fixes)
        
        return {
            "error_path": error_path,
            "primary_fixes": primary_fixes,
            "secondary_fixes": secondary_fixes,
            "verification_steps": verification
        }

    def _infer_file_purpose(self, file_path: str) -> str:
        """Infer the purpose of a file based on its name, location, and contents."""
        # Implementation details
        pass

    def _check_environment(self, file_path: str) -> Dict[str, Any]:
        """Check environment and dependency issues affecting a file."""
        # Implementation details
        pass

    def _analyze_code_logic(self, file_path: str, error_message: Optional[str]) -> Dict[str, Any]:
        """Analyze code logic issues in a file."""
        # Implementation details
        pass

    def _analyze_integration(self, file_path: str) -> Dict[str, Any]:
        """Analyze how a file interacts with other files."""
        # Implementation details
        pass

    def _validate_fix(self, file_path: str, error_message: str) -> bool:
        """Validate that a fix resolves the error."""
        # Implementation details
        pass

    def _identify_issues(self, file_path: str, error_message: Optional[str]) -> List[Dict]:
        """Identify issues in a file."""
        # Implementation details
        pass

    def _suggest_fixes(self, issues: List[Dict], file_purpose: str) -> List[Dict]:
        """Suggest fixes for identified issues."""
        # Implementation details
        pass

    def _generate_verification_plan(self, file_path: str, fixes: List[Dict]) -> Dict[str, Any]:
        """Generate a plan to verify fixes."""
        # Implementation details
        pass

    def _identify_key_functions(self, file_path: str, error_message: Optional[str]) -> List[str]:
        """Identify key functions related to an error."""
        # Implementation details
        pass

    def _apply_fix(self, file_path: str, function: str) -> Dict[str, Any]:
        """Apply a fix to a specific function."""
        # Implementation details
        pass

    def _find_existing_tests(self, file_path: str) -> List[str]:
        """Find existing tests for a file."""
        # Implementation details
        pass

    def _suggest_new_tests(self, file_path: str, error_message: Optional[str], existing_tests: List[str]) -> List[Dict]:
        """Suggest new tests for a file."""
        # Implementation details
        pass

    def _generate_test_plan(self, file_path: str, new_tests: List[Dict]) -> Dict[str, Any]:
        """Generate a test plan."""
        # Implementation details
        pass

    def _map_dependencies(self, file_paths: List[str]) -> Dict[str, List[str]]:
        """Map dependencies between files."""
        # Implementation details
        pass

    def _identify_error_sources(self, dependencies: Dict[str, List[str]], error_message: str) -> List[str]:
        """Identify potential error sources in dependencies."""
        # Implementation details
        pass

    def _suggest_cross_file_fixes(self, error_sources: List[str], purposes: Dict[str, str]) -> List[Dict]:
        """Suggest fixes across multiple files."""
        # Implementation details
        pass

    def _map_error_path(self, file_paths: List[str], error_message: Optional[str]) -> List[Dict]:
        """Map the path of an error through files."""
        # Implementation details
        pass

    def _suggest_primary_fixes(self, error_path: List[Dict]) -> List[Dict]:
        """Suggest primary fixes for error path."""
        # Implementation details
        pass

    def _suggest_secondary_fixes(self, error_path: List[Dict]) -> List[Dict]:
        """Suggest secondary fixes for error path."""
        # Implementation details
        pass

    def _generate_verification_steps(self, fixes: List[Dict]) -> Dict[str, Any]:
        """Generate steps to verify fixes."""
        # Implementation details
        pass

    def generate_bolt_tasks(self, project_description: str) -> List[BoltTask]:
        """Generate a sequence of bolt.new development tasks."""
        tasks = []
        
        # 1. Project Setup Task
        setup_task = BoltTask(
            name="Initial Project Setup",
            description=f"Set up the development environment for: {project_description}",
            prompt_template="""
Please create a new project with the following setup:
1. Initialize the project with the specified framework
2. Install all required dependencies
3. Set up the basic project structure
4. Configure development tools (ESLint, Prettier, etc.)
5. Create a development server
            """.strip(),
            framework="Next.js",  # Default, can be overridden
            dependencies=[
                "typescript",
                "tailwindcss",
                "eslint",
                "prettier"
            ],
            priority=1
        )
        tasks.append(setup_task)
        
        # 2. UI Components Task
        ui_task = BoltTask(
            name="UI Component Development",
            description="Create the core UI components for the application",
            prompt_template="""
Please implement the following UI components:
1. Create reusable base components
2. Implement the layout structure
3. Add responsive styling
4. Ensure accessibility compliance
5. Add interactive elements
            """.strip(),
            ui_components=[
                "Layout",
                "Navigation",
                "Forms",
                "Cards",
                "Modals"
            ],
            priority=2
        )
        tasks.append(ui_task)
        
        # 3. API Integration Task
        api_task = BoltTask(
            name="API Integration",
            description="Implement backend API endpoints and data management",
            prompt_template="""
Please implement the following API features:
1. Set up API routes
2. Implement data models
3. Add authentication
4. Create CRUD operations
5. Add error handling
            """.strip(),
            api_endpoints=[
                {"method": "GET", "path": "/api/items", "description": "List all items"},
                {"method": "POST", "path": "/api/items", "description": "Create new item"},
                {"method": "PUT", "path": "/api/items/:id", "description": "Update item"},
                {"method": "DELETE", "path": "/api/items/:id", "description": "Delete item"}
            ],
            priority=3
        )
        tasks.append(api_task)
        
        # 4. Testing Task
        test_task = BoltTask(
            name="Testing Implementation",
            description="Add comprehensive testing suite",
            prompt_template="""
Please implement tests for:
1. Unit tests for components
2. Integration tests for API
3. End-to-end testing
4. Performance testing
5. Accessibility testing
            """.strip(),
            dependencies=[
                "jest",
                "cypress",
                "@testing-library/react"
            ],
            priority=4
        )
        tasks.append(test_task)
        
        # 5. Deployment Task
        deploy_task = BoltTask(
            name="Deployment Setup",
            description="Configure deployment and CI/CD",
            prompt_template="""
Please set up deployment:
1. Configure build process
2. Set up environment variables
3. Add deployment scripts
4. Configure CI/CD
5. Add monitoring
            """.strip(),
            priority=5
        )
        tasks.append(deploy_task)
        
        return tasks


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prompt Engineering Project Manager")
    parser.add_argument(
        "command", choices=["init", "add-task", "update-progress", "execute-task"]
    )
    parser.add_argument("name", help="Project name or task name")
    parser.add_argument("--description", help="Task description")
    parser.add_argument("--prompt", help="Prompt template")
    parser.add_argument("--status", help="Task status")
    parser.add_argument("--note", help="Progress note")
    parser.add_argument("--execution-result", help="Execution result")

    args = parser.parse_args()

    if args.command == "init":
        pm = PromptManager(args.name)
        pm.save_project()
    elif args.command == "add-task":
        pm = PromptManager("")  # Load existing project
        pm.add_task_to_project(args.name, args.description, args.prompt)
    elif args.command == "update-progress":
        pm = PromptManager("")  # Load existing project
        pm.update_progress(args.name, TaskStatus(args.status), args.note)
    elif args.command == "execute-task":
        pm = PromptManager("")  # Load existing project
        pm.execute_task(args.name, args.execution_result)
