"""
Memory management system for the prompt manager.

This module provides functionality for managing persistent memory and context
across development sessions. It handles file-based storage with token limits
and section management.
"""

from pathlib import Path
from typing import Union, List


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
        ]

    def initialize(self) -> None:
        """Initialize the memory bank by creating required files.
        
        Creates the documentation directory and all required files if they don't exist.
        Sets the memory bank to active state.
        """
        self.docs_path.mkdir(parents=True, exist_ok=True)
        for file_name in self.required_files:
            file_path = self.docs_path / file_name
            if not file_path.exists():
                file_path.touch()
        self.is_active = True

    def update_context(self, file_name: str, section: str, content: str, mode: str = "append") -> None:
        """Update a specific context file with new content.
        
        Args:
            file_name: Name of the file to update
            section: Section name within the file
            content: Content to add or replace
            mode: Update mode - either 'append' or 'replace'
        """
        if not self.is_active:
            return

        file_path = self.docs_path / file_name
        if not file_path.exists():
            return

        if mode == "append":
            with open(file_path, "a") as f:
                f.write(f"\n\n## {section}\n{content}")
        else:  # mode == "replace"
            current_content = file_path.read_text()
            section_start = current_content.find(f"## {section}")
            if section_start == -1:
                # Section doesn't exist, append it
                with open(file_path, "a") as f:
                    f.write(f"\n\n## {section}\n{content}")
                return

            # Find the start of the next section or end of file
            next_section_start = current_content.find("\n## ", section_start + 1)
            if next_section_start == -1:
                next_section_start = len(current_content)

            # Replace the section content
            new_content = (
                current_content[:section_start]
                + f"## {section}\n{content}"
                + current_content[next_section_start:]
            )
            file_path.write_text(new_content)

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
