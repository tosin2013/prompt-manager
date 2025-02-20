"""
Memory management system for the prompt manager.

This module provides functionality for managing persistent memory and context
across development sessions. It handles file-based storage with token limits
and section management.
"""

from pathlib import Path
import json
import os
import shutil
import datetime
from typing import Dict, Any, Optional

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
        self.progress_file = self.memory_dir / "progress.md"
        self.backup_dir = self.memory_dir / "backups"
        
        # Initialize memory files if they don't exist
        self._init_memory_files()

    def _init_memory_files(self):
        """Initialize memory files if they don't exist."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize each file with empty JSON object if it doesn't exist
        for file_path in [self.tasks_file, self.prompts_file, self.context_file, self.progress_file]:
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

    def update_context_memory(self, update: Dict[str, Any]) -> None:
        """Update context memory with new data."""
        context = self.load_context_memory()
        context.update(update)
        self.save_context_memory(context)

    def update_progress(self, message: str) -> None:
        """Update progress tracking file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n## {timestamp}\n{message}\n"
        
        with open(self.progress_file, "a") as f:
            f.write(entry)

    def create_backup(self) -> str:
        """Create a backup of all memory files.
        
        Returns:
            str: Path to backup directory
        """
        # Create backup directory with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Copy memory files to backup
        for src in [self.context_file, self.tasks_file, self.progress_file]:
            if src.exists():
                shutil.copy2(src, backup_path)
        
        return str(backup_path)

    def restore_backup(self, backup_name: str = "latest") -> None:
        """Restore memory files from backup.
        
        Args:
            backup_name: Name of backup to restore from, or "latest"
        """
        # Get backup directory
        if backup_name == "latest":
            backups = sorted(self.backup_dir.glob("backup_*"))
            if not backups:
                raise ValueError("No backups found")
            backup_path = backups[-1]
        else:
            backup_path = self.backup_dir / backup_name
            if not backup_path.exists():
                raise ValueError(f"Backup not found: {backup_name}")
        
        # Restore files
        for src in backup_path.glob("*"):
            if src.name == "context.json":
                shutil.copy2(src, self.context_file)
            elif src.name == "tasks.json":
                shutil.copy2(src, self.tasks_file)
            elif src.name == "progress.md":
                shutil.copy2(src, self.progress_file)

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
