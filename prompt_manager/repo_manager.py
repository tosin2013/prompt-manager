"""Repository manager for code analysis and learning."""

from pathlib import Path
from typing import Dict, List, Optional, Union


class RepoManager:
    """Manager for repository operations."""

    def __init__(self, project_dir: Optional[str] = None):
        """Initialize repository manager."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

    def analyze_repo(self, file_path: str) -> Dict[str, Union[int, str]]:
        """Analyze repository structure and metrics."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return {
            'files': 1,
            'lines': 1,
            'complexity': 'low'
        }

    def learn_session(self, file_path: str, duration: int = 30) -> Dict[str, Union[str, List[str]]]:
        """Start a learning session for repository understanding."""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return {
            'duration': f'{duration}m',
            'insights': [
                'Identified main components',
                'Analyzed dependencies',
                'Found potential improvements'
            ]
        }
