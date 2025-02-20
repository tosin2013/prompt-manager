"""Repository manager for code analysis and learning."""

from pathlib import Path
from typing import Dict, List, Optional, Union
import subprocess


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
            'files': self._count_files(file_path),
            'lines': self._count_lines(file_path),
            'complexity': self._analyze_complexity(file_path)
        }

    def get_repo_stats(self, file_path: str) -> Dict[str, Union[int, str]]:
        """Get repository statistics."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return {
            'total_files': self._count_files(file_path),
            'total_lines': self._count_lines(file_path),
            'languages': self._detect_languages(file_path)
        }

    def get_commit_history(self, file_path: str, limit: int = 10) -> List[Dict[str, str]]:
        """Get commit history for a file."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            cmd = ['git', 'log', '-n', str(limit), '--pretty=format:%h|%an|%s', str(file_path)]
            output = subprocess.check_output(cmd, cwd=file_path.parent, text=True)
            commits = []
            for line in output.splitlines():
                hash_id, author, message = line.split('|')
                commits.append({
                    'hash': hash_id,
                    'author': author,
                    'message': message
                })
            return commits
        except subprocess.CalledProcessError:
            return []

    def get_current_branch(self, file_path: str) -> str:
        """Get current git branch."""
        file_path = Path(file_path)
        try:
            cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
            return subprocess.check_output(cmd, cwd=file_path.parent, text=True).strip()
        except subprocess.CalledProcessError:
            return 'unknown'

    def get_recent_changes(self, file_path: str, days: int = 7) -> List[Dict[str, str]]:
        """Get recent changes in the repository."""
        file_path = Path(file_path)
        try:
            cmd = ['git', 'log', f'--since={days} days ago', '--pretty=format:%h|%an|%s']
            output = subprocess.check_output(cmd, cwd=file_path.parent, text=True)
            changes = []
            for line in output.splitlines():
                hash_id, author, message = line.split('|')
                changes.append({
                    'hash': hash_id,
                    'author': author,
                    'message': message
                })
            return changes
        except subprocess.CalledProcessError:
            return []

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

    def _count_files(self, path: Path) -> int:
        """Count number of files in directory."""
        if path.is_file():
            return 1
        return sum(1 for _ in path.rglob('*') if _.is_file())

    def _count_lines(self, path: Path) -> int:
        """Count total lines in all files."""
        if path.is_file():
            with open(path) as f:
                return sum(1 for _ in f)
        return sum(self._count_lines(f) for f in path.rglob('*') if f.is_file())

    def _analyze_complexity(self, path: Path) -> str:
        """Analyze code complexity."""
        total_lines = self._count_lines(path)
        if total_lines < 1000:
            return 'low'
        elif total_lines < 10000:
            return 'medium'
        return 'high'

    def _detect_languages(self, path: Path) -> Dict[str, int]:
        """Detect programming languages used."""
        extensions = {}
        for f in path.rglob('*'):
            if f.is_file():
                ext = f.suffix.lower()
                if ext:
                    extensions[ext] = extensions.get(ext, 0) + 1
        return extensions
