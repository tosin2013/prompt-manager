"""Memory Bank module for managing persistent memory storage."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import logging


class MemoryBank:
    """Manages persistent memory storage for the prompt manager."""

    def __init__(self, data_dir: Path):
        """
        Initialize the memory bank.
        
        Args:
            data_dir: Directory to store memory files
        """
        self.data_dir = Path(data_dir)
        self.docs_path = self.data_dir / "docs"
        self.is_active = False
        self.required_files = [
            "context.json",
            "memories.json",
            "tokens.json"
        ]
        self.max_tokens = 4096
        self.current_tokens = 0

    def initialize(self) -> None:
        """Initialize the memory bank by creating required files."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.docs_path.mkdir(parents=True, exist_ok=True)
        
        for file in self.required_files:
            file_path = self.data_dir / file
            if not file_path.exists():
                with open(file_path, "w") as f:
                    f.write(f"# {file[:-3]}\n\n")
        
        # Create initial product context file
        context_file = self.docs_path / "productContext.md"
        if not context_file.exists():
            with open(context_file, "w") as f:
                f.write("# Product Context\n\n")
        
        self.is_active = True

    def update_context(self, filename: str, section: str, content: str, mode: str = "replace") -> None:
        """
        Update the context file with new information.
        
        Args:
            filename: Name of the context file to update
            section: Section name to update
            content: Content to add/update
            mode: Update mode ('replace' or 'append')
        """
        if not self.is_active:
            return
            
        if not filename.endswith(".md"):
            raise ValueError("Context files must have .md extension")
            
        if mode not in ["replace", "append"]:
            raise ValueError("Mode must be 'replace' or 'append'")
            
        if filename != "productContext.md":
            raise ValueError("Invalid context file name")
            
        file_path = self.docs_path / filename
        try:
            if not file_path.exists():
                with open(file_path, "w") as f:
                    f.write(f"# {filename[:-3]}\n\n")
                    
            with open(file_path, "r") as f:
                current = f.read()
                
            if mode == "append":
                new_content = f"{current}\n## {section}\n{content}\n"
            else:
                sections = current.split("\n## ")
                header = sections[0]
                other_sections = [s for s in sections[1:] if not s.startswith(section)]
                new_content = f"{header}\n## {section}\n{content}\n"
                for s in other_sections:
                    new_content += f"\n## {s}"
                    
            with open(file_path, "w") as f:
                f.write(new_content)
                
        except Exception as e:
            logging.error(f"Failed to update context: {str(e)}")
            raise

    def reset(self) -> None:
        """Reset the memory bank by clearing all stored data."""
        if not self.is_active:
            return
            
        for file in self.required_files:
            file_path = self.data_dir / file
            try:
                with open(file_path, "w") as f:
                    f.write(f"# {file[:-5]}\n\n")
            except Exception as e:
                logging.error(f"Failed to reset {file}: {str(e)}")
                raise
                
        # Clear docs directory
        for file in self.docs_path.glob("*.md"):
            try:
                file.unlink()
            except Exception as e:
                logging.error(f"Failed to delete {file}: {str(e)}")
                
        self.current_tokens = 0
        self.is_active = False

    def check_token_limit(self) -> bool:
        """
        Check if current token count is at limit.
        
        Returns:
            True if at limit, False otherwise
        """
        return self.current_tokens >= self.max_tokens

    def increment_tokens(self, amount: int) -> None:
        """
        Increment the token count.
        
        Args:
            amount: Number of tokens to add
        """
        if not self.is_active:
            return
        self.current_tokens = min(self.current_tokens + amount, self.max_tokens)

    def decrement_tokens(self, amount: int) -> None:
        """
        Decrement the token count.
        
        Args:
            amount: Number of tokens to remove
        """
        if not self.is_active:
            return
        self.current_tokens = max(0, self.current_tokens - amount)
