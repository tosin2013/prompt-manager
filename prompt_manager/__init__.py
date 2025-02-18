"""
Prompt Manager: Development workflow management system with memory tracking.
"""

from typing import Dict, Optional, Any, Union
from pathlib import Path
import yaml
import datetime
import uuid


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

        file_path = self.docs_path / file_name
        if mode == "append":
            with file_path.open("a") as f:
                f.write(f"\n## {section}\n{content}\n")
        else:
            with file_path.open("w") as f:
                f.write(f"## {section}\n{content}\n")

    def validate_context(self) -> bool:
        """Validate that all required context files exist and have content."""
        if not self.is_active:
            return False

        for file in self.required_files:
            file_path = self.docs_path / file
            if not file_path.exists():
                return False
            if file_path.stat().st_size == 0:
                return False
        return True

    def reset_context(self) -> None:
        """Reset all context files while preserving essential information."""
        if not self.is_active:
            return

        # Backup product context before reset
        product_context = ""
        product_file = self.docs_path / "productContext.md"
        if product_file.exists():
            with product_file.open() as f:
                product_context = f.read()

        # Reset all files
        self.initialize()

        # Restore product context
        if product_context:
            with product_file.open('w') as f:
                f.write(product_context)

    def check_token_limit(self) -> bool:
        """Check if token limit has been exceeded."""
        return self.current_tokens >= self.max_tokens

    def increment_tokens(self, count: int) -> None:
        """Increment token count."""
        self.current_tokens += count


class PromptManager:
    """Manages development workflow, tasks, and debugging."""

    def __init__(
        self,
        project_name: str,
        memory_path: Optional[Union[str, Path]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize PromptManager with project configuration."""
        self.project_name = project_name
        default_path = Path.cwd() / "cline_docs"
        self.memory = MemoryBank(memory_path or default_path)
        self.config = config or {}
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.debug_mode = False
        self.initialize()

    def initialize(self) -> None:
        """Initialize the prompt manager and memory bank."""
        # Create base directory first
        print(f"Creating directory at: {self.memory.docs_path}")
        self.memory.docs_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize memory bank
        self.memory.initialize()
        
        # Create project data file
        project_file = self.memory.docs_path / "project_data.yaml"
        project_data = {
            "project_name": self.project_name,
            "tasks": []
        }
        
        print(f"Creating project file at: {project_file}")
        with project_file.open('w') as f:
            yaml.dump(project_data, f)
            
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        config_file = self.memory.docs_path / "config.yaml"
        if config_file.exists():
            with config_file.open() as f:
                self.config.update(yaml.safe_load(f) or {})

    def add_task(
        self,
        name: str,
        description: str,
        prompt_template: str,
        priority: int = 1,
    ) -> None:
        """Add a new task to the workflow."""
        task = {
            "name": name,
            "description": description,
            "prompt_template": prompt_template,
            "priority": priority,
            "status": "Not Started",
            "created_at": datetime.datetime.now().isoformat(),
            "id": str(uuid.uuid4()),
        }
        self.tasks[name] = task

    def get_task(self, name: str) -> Optional[Dict[str, Any]]:
        """Get task details by name."""
        return self.tasks.get(name)

    def update_task_status(self, name: str, status: str) -> None:
        """Update task status."""
        if name in self.tasks:
            self.tasks[name]["status"] = status

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
                return task["prompt_template"].format(**kwargs)
            except KeyError as e:
                self.debug_log(f"Missing prompt variable: {e}")
                return None
        return None

    def load_project(self):
        """Load existing project data if available"""
        project_data = self.memory.docs_path / "project_data.yaml"
        if project_data.exists():
            with open(project_data, "r") as f:
                data = yaml.safe_load(f)
                for task_data in data.get("tasks", []):
                    task = {
                        "name": task_data["name"],
                        "description": task_data["description"],
                        "prompt_template": task_data["prompt_template"],
                        "priority": task_data["priority"],
                        "status": task_data["status"],
                        "created_at": task_data["created_at"],
                        "id": task_data["id"],
                    }
                    self.tasks[task["name"]] = task

    def save_project(self):
        """Save project data to YAML"""
        project_data = {
            "project_name": self.project_name,
            "tasks": list(self.tasks.values()),
        }
        with open(self.memory.docs_path / "project_data.yaml", "w") as f:
            yaml.dump(project_data, f)

    def add_task_to_project(self, name: str, description: str, prompt_template: str) -> Dict[str, Any]:
        """Add a new task to the project"""
        task = {
            "name": name,
            "description": description,
            "prompt_template": prompt_template,
            "priority": 1,
            "status": "Not Started",
            "created_at": datetime.datetime.now().isoformat(),
            "id": str(uuid.uuid4()),
        }
        self.tasks[name] = task
        self.update_markdown_files()
        self.save_project()
        return task

    def get_task_from_project(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a task by name"""
        return self.tasks.get(name)

    def update_progress(self, task_name: str, status: str, note: str):
        """Update task progress"""
        task = self.get_task(task_name)
        if task:
            task["status"] = status
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
            content += f"### {task['name']}\n"
            content += f"- Status: {task['status']}\n"
            content += f"- Description: {task['description']}\n\n"

        with open(self.memory.docs_path / "project_plan.md", "w") as f:
            f.write(content)

    def _update_task_breakdown(self):
        """Update task_breakdown.md"""
        content = "# Task Breakdown\n\n"
        for task in self.tasks.values():
            content += f"## {task['name']}\n"
            content += f"Description: {task['description']}\n\n"
            content += "### Prompt Template\n```\n"
            content += task["prompt_template"]
            content += "\n```\n\n"

        with open(self.memory.docs_path / "task_breakdown.md", "w") as f:
            f.write(content)

    def _update_progress_tracking(self):
        """Update progress_tracking.md"""
        content = f"# Progress Tracking - {self.project_name}\n\n"
        for task in self.tasks.values():
            content += f"## {task['name']}\n"
            content += f"Status: {task['status']}\n\n"
            content += "### Progress Notes\n"
            content += "\n"

        with open(self.memory.docs_path / "progress_tracking.md", "w") as f:
            f.write(content)

    def _update_mermaid_diagrams(self):
        """Update mermaid_diagrams.md with current project state"""
        content = "# Project Workflow Diagrams\n\n"

        # Task Status Diagram
        content += "## Task Status\n```mermaid\ngraph TD\n"
        for task in self.tasks.values():
            style = {
                "Not Started": "fill:#fff",
                "In Progress": "fill:#yellow",
                "Complete": "fill:#green",
            }.get(task["status"], "fill:#fff")

            content += f"    {task['name']}[{task['name']}]:::status{task['status']}\n"
        content += "```\n\n"

        with open(self.memory.docs_path / "mermaid_diagrams.md", "w") as f:
            f.write(content)

    def execute_task(self, task_name: str, execution_result: str) -> bool:
        """Execute a task and handle any failures"""
        if self.memory.check_token_limit():
            self._handle_memory_reset()
            return

        task = self.get_task(task_name)
        if not task:
            return

        try:
            # Update active context with current task
            self.memory.update_context(
                "activeContext.md",
                "Current Tasks",
                f"- {task_name}: {task['description']}",
            )

            # Execute task
            if "error" in execution_result.lower():
                self._handle_task_failure(task, execution_result)
            else:
                task["status"] = "Completed"
                self.update_progress(task_name, "Completed", execution_result)

                # Update progress in memory bank
                self.memory.update_context(
                    "progress.md", "Completed", f"- {task_name}: {execution_result}"
                )

            self.save_project()
            self.update_markdown_files()

        except Exception as e:
            self._handle_task_failure(task, str(e))

    def _handle_memory_reset(self):
        """Handle memory bank reset"""
        # Document current state
        active_tasks = [t for t in self.tasks.values() if t["status"] == "In Progress"]
        next_steps = "\n".join(
            [f"- Continue {t['name']}: {t['description']}" for t in active_tasks]
        )

        self.memory.update_context("activeContext.md", "Next Steps", next_steps)

        # Update progress
        self.memory.update_context(
            "progress.md",
            "In Progress",
            "\n".join([f"- {t['name']}: {t['status']}" for t in self.tasks.values()]),
        )

        # Reset token count
        self.memory.current_tokens = 0

    def _handle_task_failure(self, task: Dict[str, Any], error_message: str):
        """Handle task failure with progressive debugging"""
        # Update active context with failure
        self.memory.update_context(
            "activeContext.md",
            "Recent Changes",
            f"- Failed: {task['name']}\n  Error: {error_message}",
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

    def _attempt_debugging(self, task: Dict[str, Any], error_message: str) -> Dict[str, Any]:
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

    def _debug_environment_layer(self, task: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """Debug environment-related issues"""
        prompt = self._get_debug_prompt("Layered Debug Analysis")
        # Here you would integrate with your LLM to analyze environment issues
        return {"success": False, "message": "Environment layer checked", "fix_attempt": "No issues found"}

    def _debug_code_logic_layer(self, task: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """Debug code logic issues"""
        prompt = self._get_debug_prompt("Root Cause Analysis")
        # Here you would integrate with your LLM to analyze code logic
        return {"success": False, "message": "Code logic layer checked", "fix_attempt": "No issues found"}

    def _attempt_firecrawl_research(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to research solutions using Firecrawl"""
        research_prompt = self._get_debug_prompt("Firecrawl Research")
        # Here you would integrate with Firecrawl to search for solutions
        return {"success": False, "message": "Firecrawl research attempted", "fix_attempt": "Research logged"}

    def _perform_rca(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform Root Cause Analysis"""
        rca_prompt = self._get_debug_prompt("Root Cause Analysis")
        # Here you would integrate with your LLM to perform RCA
        return {"success": False, "message": "RCA performed", "fix_attempt": "Analysis logged"}

    def _escalate_to_human(self, task: Dict[str, Any]):
        """Escalate the issue to human intervention"""
        escalation_note = {
            "timestamp": datetime.datetime.now().isoformat(),
            "message": "Task requires human intervention after multiple failed attempts",
            "debug_history": [],
        }
        self.update_markdown_files()

    def _get_debug_prompt(self, prompt_type: str) -> str:
        """Get a specific type of debugging prompt"""
        with open(self.memory.docs_path / "debugging_prompts.md", "r") as f:
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
        pm.update_progress(args.name, args.status, args.note)
    elif args.command == "execute-task":
        pm = PromptManager("")  # Load existing project
        pm.execute_task(args.name, args.execution_result)
