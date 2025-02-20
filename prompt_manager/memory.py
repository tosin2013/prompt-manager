"""
Memory management system for the prompt manager.

This module provides functionality for managing persistent memory and context
across development sessions. It handles file-based storage with token limits
and section management.
"""

from pathlib import Path
import json

class MemoryBank:
    """Manages persistent memory and context for the development workflow.
    
    Attributes:
        project_path (Path): Path to the project directory
        memory_dir (Path): Path to the memory directory
        tasks_file (Path): Path to the tasks file
        prompts_file (Path): Path to the prompts file
        context_file (Path): Path to the context file
    """

    def __init__(self, project_path: str):
        """Initialize MemoryBank with project path.
        
        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self.memory_dir = self.project_path / "memory"
        self.tasks_file = self.memory_dir / "tasks.json"
        self.prompts_file = self.memory_dir / "prompts.json"
        self.context_file = self.memory_dir / "context.json"
        
        # Initialize memory files if they don't exist
        self._init_memory_files()

    def _init_memory_files(self):
        """Initialize memory files if they don't exist."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize each file with empty JSON object if it doesn't exist
        for file_path in [self.tasks_file, self.prompts_file, self.context_file]:
            if not file_path.exists():
                with open(file_path, "w") as f:
                    json.dump({}, f, indent=2)

    def save_task_memory(self, task_data: dict):
        """Save task-related memory."""
        self._save_to_file(self.tasks_file, task_data)

    def save_prompt_memory(self, prompt_data: dict):
        """Save prompt-related memory."""
        self._save_to_file(self.prompts_file, prompt_data)

    def save_context_memory(self, context_data: dict):
        """Save context-related memory."""
        self._save_to_file(self.context_file, context_data)

    def load_task_memory(self) -> dict:
        """Load task-related memory."""
        return self._load_from_file(self.tasks_file)

    def load_prompt_memory(self) -> dict:
        """Load prompt-related memory."""
        return self._load_from_file(self.prompts_file)

    def load_context_memory(self) -> dict:
        """Load context-related memory."""
        return self._load_from_file(self.context_file)

    def _save_to_file(self, file_path: Path, data: dict):
        """Save data to a JSON file."""
        try:
            # Read existing data
            current_data = self._load_from_file(file_path)
            
            # Update with new data
            current_data.update(data)
            
            # Write back to file
            with open(file_path, "w") as f:
                json.dump(current_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save to {file_path.name}: {e}")

    def _load_from_file(self, file_path: Path) -> dict:
        """Load data from a JSON file."""
        try:
            if not file_path.exists():
                return {}
            with open(file_path, "r") as f:
                return json.load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load from {file_path.name}: {e}")
            return {}
