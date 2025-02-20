"""
Memory management system for the prompt manager.

This module provides functionality for managing persistent memory and context
across development sessions. It handles file-based storage with token limits
and section management.
"""

from pathlib import Path
from typing import Union, List, Dict, Optional
from datetime import datetime

class MemoryBank:
    """Manages persistent memory and context for the development workflow.
    
    Attributes:
        docs_path (Path): Path to the documentation directory
        max_tokens (int): Maximum number of tokens allowed
        is_active (bool): Whether the memory bank is currently active
        current_tokens (int): Current token count
        required_files (List[str]): List of required context files
    """

    def __init__(self, docs_path: Union[str, Path], max_tokens: int = 2_000_000) -> None:
        """Initialize MemoryBank with path and token limit.
        
        Args:
            docs_path: Path to store documentation files
            max_tokens: Maximum number of tokens allowed in memory bank
        """
        self.docs_path = Path(docs_path)
        self.max_tokens = max_tokens
        self.is_active = False
        self.current_tokens = 0
        self.required_files: List[str] = [
            "productContext.md",
            "activeContext.md",
            "systemPatterns.md",
            "techContext.md",
            "progress.md",
            "commandHistory.md"  # Track all command executions
        ]

    def initialize(self) -> None:
        """Initialize the memory bank by creating required files.
        
        Creates the documentation directory and all required files if they don't exist.
        Sets the memory bank to active state and adds default content.
        """
        self.docs_path.mkdir(parents=True, exist_ok=True)
        
        # Define default headers and descriptions for each memory file
        default_content = {
            "productContext.md": {
                "header": "# Product Context",
                "description": "Track product requirements, business context, and high-level objectives."
            },
            "activeContext.md": {
                "header": "# Active Context",
                "description": "Track current development tasks, priorities, and immediate goals."
            },
            "systemPatterns.md": {
                "header": "# System Patterns",
                "description": "Document system architecture, design patterns, and key technical decisions."
            },
            "techContext.md": {
                "header": "# Tech Context",
                "description": "Track technical implementation details, dependencies, and constraints."
            },
            "progress.md": {
                "header": "# Progress",
                "description": "Track development milestones, achievements, and key updates."
            },
            "commandHistory.md": {
                "header": "# Command History",
                "description": "Track command executions, results, and system interactions."
            }
        }
        
        # Initialize each memory file with proper header and description
        for file_name in self.required_files:
            file_path = self.docs_path / file_name
            content = default_content[file_name]
            
            # Check if file exists and has content
            if file_path.exists():
                with open(file_path, "r") as f:
                    existing_content = f.read().strip()
                    if existing_content:
                        # If file has content but no header, prepend header
                        if not existing_content.startswith(content["header"]):
                            with open(file_path, "w") as f:
                                f.write(f"{content['header']}\n\n{existing_content}\n")
                        continue
            
            # Create new file with header and description
            with open(file_path, "w") as f:
                f.write(f"{content['header']}\n\n{content['description']}\n")
        
        self.is_active = True

    def update_context(self, file_name: str, section: str, content: str, mode: str = "append") -> None:
        """Update context in a memory file.
        
        Args:
            file_name (str): Name of the memory file to update
            section (str): Section name to update
            content (str): Content to add/update
            mode (str, optional): Update mode - 'append' or 'replace'. Defaults to "append".
        """
        file_path = self.docs_path / file_name
        if not file_path.exists():
            raise ValueError(f"Memory file {file_name} does not exist")
        
        # Get default header for this file
        default_content = {
            "productContext.md": {
                "header": "# Product Context",
                "description": "Track product requirements, business context, and high-level objectives."
            },
            "activeContext.md": {
                "header": "# Active Context",
                "description": "Track current development tasks, priorities, and immediate goals."
            },
            "systemPatterns.md": {
                "header": "# System Patterns",
                "description": "Document system architecture, design patterns, and key technical decisions."
            },
            "techContext.md": {
                "header": "# Tech Context",
                "description": "Track technical implementation details, dependencies, and constraints."
            },
            "progress.md": {
                "header": "# Progress",
                "description": "Track development milestones, achievements, and key updates."
            },
            "commandHistory.md": {
                "header": "# Command History",
                "description": "Track command executions, results, and system interactions."
            }
        }
        
        # Read existing content or use default header
        try:
            with open(file_path, "r") as f:
                existing_content = f.read().strip()
                if not existing_content:
                    existing_content = f"{default_content[file_name]['header']}\n\n{default_content[file_name]['description']}"
                elif not existing_content.startswith(default_content[file_name]['header']):
                    # If file exists but doesn't have header, add it
                    existing_content = f"{default_content[file_name]['header']}\n\n{default_content[file_name]['description']}\n\n{existing_content}"
        except FileNotFoundError:
            raise ValueError(f"Memory file {file_name} does not exist")
        
        # Update content based on mode
        if mode == "replace":
            # Find section if it exists
            section_start = existing_content.find(f"\n## {section}\n")
            if section_start == -1:
                # Section doesn't exist, append it
                new_content = f"{existing_content}\n\n## {section}\n{content}"
            else:
                # Replace existing section
                next_section_start = existing_content.find("\n## ", section_start + 1)
                if next_section_start == -1:
                    next_section_start = len(existing_content)
                new_content = (
                    existing_content[:section_start] +
                    f"\n## {section}\n{content}" +
                    existing_content[next_section_start:]
                )
        else:  # append
            new_content = f"{existing_content}\n\n## {section}\n{content}"
        
        # Write updated content
        with open(file_path, "w") as f:
            f.write(new_content)

    def add_task(self, title: str, description: str = "", template: str = None, priority: str = "medium") -> None:
        """Add a new task to the memory bank.
        
        Args:
            title: Task title
            description: Task description
            template: Optional task template
            priority: Task priority (high, medium, low)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add task to active context
        task_content = f"\n## Task: {title}\n"
        task_content += f"Created: {timestamp}\n"
        task_content += f"Priority: {priority}\n"
        if description:
            task_content += f"\nDescription:\n{description}\n"
        if template:
            task_content += f"\nTemplate: {template}\n"
        
        # Update active context with task
        self.update_context(
            "activeContext.md",
            f"Task_{title}_{timestamp}",
            task_content,
            mode="append"
        )

    def update_task_status(self, title: str, status: str, notes: Optional[str] = None) -> None:
        """Update task status in memory.
        
        Args:
            title: Task title
            status: New status
            notes: Optional notes about the status update
        """
        if not self.is_active:
            return
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_content = f"Task: {title}\nStatus: {status}\n"
        
        if notes:
            update_content += f"Notes: {notes}\n"
            
        self.update_context("progress.md", f"Status_{title}_{timestamp}", update_content, mode="append")

    def track_command(self, command: str, args: str, result: str) -> None:
        """Track command execution in memory.
        
        Args:
            command: Command name
            args: Command arguments
            result: Command execution result
        """
        if not self.is_active:
            return
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = f"Command: {command}\nArgs: {args}\nResult: {result}\nTimestamp: {timestamp}\n"
        
        self.update_context(
            "commandHistory.md",
            f"Command_{timestamp}",
            content,
            mode="append"
        )

    def delete_entry(self, entry_id: str) -> None:
        """Delete a memory entry by its ID.
        
        Args:
            entry_id: ID of the entry to delete
        """
        if not self.is_active:
            return
            
        for file_name in self.required_files:
            file_path = self.docs_path / file_name
            if not file_path.exists():
                continue
                
            content = file_path.read_text()
            section_start = content.find(f"## {entry_id}")
            if section_start == -1:
                continue
                
            next_section_start = content.find("\n## ", section_start + 1)
            if next_section_start == -1:
                next_section_start = len(content)
                
            new_content = content[:section_start] + content[next_section_start:]
            file_path.write_text(new_content)
            return

    def list_entries(self, file_name: Optional[str] = None) -> List[Dict[str, str]]:
        """List memory entries.
        
        Args:
            file_name: Optional file name to filter by
        
        Returns:
            List of entries with file, section, and timestamp
        """
        entries = []
        files_to_check = [file_name] if file_name else self.required_files
        
        for fname in files_to_check:
            if fname not in self.required_files:
                continue
                
            file_path = self.docs_path / fname
            if not file_path.exists():
                continue
                
            content = file_path.read_text()
            sections = content.split("\n## ")[1:]  # Skip header
            
            for section in sections:
                if not section.strip():
                    continue
                    
                section_lines = section.split("\n")
                section_id = section_lines[0].strip()
                timestamp = ""
                
                for line in section_lines:
                    if line.startswith("Timestamp:"):
                        timestamp = line.split(":", 1)[1].strip()
                        break
                
                entries.append({
                    "file": fname,
                    "section": section_id,
                    "timestamp": timestamp or "N/A"
                })
                
        return sorted(entries, key=lambda x: x["timestamp"] if x["timestamp"] != "N/A" else "")

    def check_token_limit(self) -> bool:
        """Check if current token count exceeds limit.
        
        Returns:
            bool: True if within token limit, False otherwise
        """
        return self.current_tokens <= self.max_tokens

    def increment_tokens(self, count: int) -> None:
        """Increment token count.
        
        Args:
            count: Number of tokens to add
        """
        self.current_tokens += count

    def decrement_tokens(self, count: int) -> None:
        """Decrement token count.
        
        Args:
            count: Number of tokens to remove
        """
        self.current_tokens = max(0, self.current_tokens - count)

    def reset(self) -> None:
        """Reset memory bank state.
        
        Deletes all context files and resets token count to zero.
        """
        self.current_tokens = 0
        for file_name in self.required_files:
            file_path = self.docs_path / file_name
            if file_path.exists():
                file_path.unlink()
        self.is_active = False

    def update_task(self, title: str, description: str = None, priority: str = None) -> None:
        """Update task details in the memory bank.
        
        Args:
            title: Task title
            description: Optional new description
            priority: Optional new priority
        """
        if not self.is_active:
            return

        task_content = f"\n## Task: {title}\n"
        if priority:
            task_content += f"Priority: {priority}\n"
        if description:
            task_content += f"Description: {description}\n"
            
        self.update_context("progress.md", f"Task_{title}", task_content, mode="replace")
