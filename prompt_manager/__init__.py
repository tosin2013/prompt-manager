"""
Prompt Manager: Development workflow management system with memory tracking.
"""

from typing import Dict, Optional, Any, Union, List
from pathlib import Path
from enum import Enum
import yaml
import datetime
import uuid


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class Task:
    """Represents a task in the workflow."""
    
    def __init__(
        self,
        name: str,
        description: str,
        prompt_template: str,
        priority: int = 1,
        status: TaskStatus = TaskStatus.NOT_STARTED
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
        default_path = Path.cwd() / "cline_docs"
        self.memory_bank = MemoryBank(memory_path or default_path)
        self.config = config or {}
        self.tasks: Dict[str, Task] = {}
        self.debug_mode = False
        self.is_initialized = False
        self.initialize()

    def initialize(self) -> None:
        """Initialize the prompt manager and memory bank."""
        self.memory_bank.initialize()
        self._load_config()
        self.is_initialized = True

    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        config_path = self.memory_bank.docs_path / "config.yaml"
        if config_path.exists():
            with config_path.open() as f:
                self.config.update(yaml.safe_load(f) or {})

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
        return task

    def delete_task(self, name: str) -> None:
        """Delete a task."""
        if name not in self.tasks:
            raise KeyError(f"Task {name} not found")
        del self.tasks[name]

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
                TaskStatus.NOT_STARTED: "fill:#fff",
                TaskStatus.IN_PROGRESS: "fill:#yellow",
                TaskStatus.COMPLETED: "fill:#green",
                TaskStatus.FAILED: "fill:#red",
                TaskStatus.BLOCKED: "fill:#gray",
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
