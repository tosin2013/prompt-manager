"""
PromptManager class for managing code analysis and debugging.
"""
from typing import Optional, List, Dict, Any
from prompt_manager.llm_enhancement import LLMEnhancement
from prompt_manager.memory_bank import MemoryBank

class PromptManager:
    """Manages code analysis and debugging operations."""
    
    def __init__(self):
        """Initialize the PromptManager."""
        self.llm = LLMEnhancement()
        self.memory = MemoryBank()

    def analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a code file for potential issues."""
        return self.llm.analyze_code(file_path)

    def analyze_error(self, error_message: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Analyze an error message to find its root cause."""
        return self.llm.analyze_error(error_message, file_path)

    def suggest_code_fixes(self, file_path: str) -> List[Dict[str, Any]]:
        """Suggest fixes for code issues."""
        return self.llm.suggest_fixes(file_path)

    def generate_test_roadmap(self, file_path: str) -> Dict[str, Any]:
        """Generate a testing roadmap for a file."""
        return self.llm.generate_test_plan(file_path)

    def analyze_dependencies(self, file_path: str, recursive: bool = False) -> Dict[str, Any]:
        """Analyze file dependencies."""
        return self.llm.analyze_dependencies(file_path, recursive)

    def trace_error(self, error_message: str, file_path: Optional[str] = None, 
                   line_number: Optional[int] = None) -> Dict[str, Any]:
        """Trace an error through the codebase."""
        return self.llm.trace_error(error_message, file_path, line_number)

    def add_task(self, title: str, description: str, priority: str = "medium") -> None:
        """Add a new task."""
        self.memory.add_task(title, description, priority)

    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks."""
        return self.memory.list_tasks()

    def update_task_progress(self, task_id: str, progress: str) -> None:
        """Update task progress."""
        self.memory.update_task_progress(task_id, progress)

    def analyze_repo(self, repo_path: str) -> Dict[str, Any]:
        """Analyze a repository."""
        return self.llm.analyze_repository(repo_path)

    def learn_session(self, duration: int) -> Dict[str, Any]:
        """Learn from a coding session."""
        return self.llm.learn_from_session(duration)

    def analyze_impact(self, changes: List[str]) -> Dict[str, Any]:
        """Analyze impact of code changes."""
        return self.llm.analyze_impact(changes)

    def suggest_improvements(self, max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """Suggest code improvements."""
        return self.llm.suggest_improvements(max_suggestions)

    def create_pr(self, title: str, description: str, changes: List[str]) -> Dict[str, Any]:
        """Create a pull request."""
        return self.llm.create_pull_request(title, description, changes)
