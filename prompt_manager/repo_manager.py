"""Repository manager for code analysis and learning."""

from pathlib import Path
from typing import Dict, List, Optional, Union
import subprocess
import os


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
        
        try:
            return {
                'files': self._count_files(file_path),
                'lines': self._count_lines(file_path),
                'complexity': self._analyze_complexity(file_path)
            }
        except UnicodeDecodeError as e:
            # Handle non-UTF-8 encoded content
            return {
                'error': f"Unable to analyze repository due to encoding issues: {str(e)}",
                'files': 0,
                'lines': 0,
                'complexity': 'unknown'
            }

    def get_repo_stats(self, file_path: str) -> Dict[str, Union[int, str]]:
        """Get repository statistics."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            return {
                'total_files': self._count_files(file_path),
                'total_lines': self._count_lines(file_path),
                'languages': self._detect_languages(file_path)
            }
        except UnicodeDecodeError as e:
            return {
                'error': f"Unable to get repository stats due to encoding issues: {str(e)}",
                'total_files': 0,
                'total_lines': 0,
                'languages': []
            }

    def get_commit_history(self, file_path: str, limit: int = 10) -> List[Dict[str, str]]:
        """Get commit history for a file."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            # Use -C to set git directory and --git-dir to handle submodules
            git_dir = self._find_git_dir(file_path)
            if not git_dir:
                return [{'error': 'Not a git repository'}]

            cmd = ['git', '--git-dir', str(git_dir), 'log', '-n', str(limit), '--pretty=format:%h|%an|%s']
            if str(file_path) != str(file_path.parent):
                cmd.append(str(file_path.relative_to(file_path.parent)))
            
            output = subprocess.check_output(
                cmd, 
                cwd=file_path.parent, 
                text=True, 
                errors='replace'
            )
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
            return [{'error': 'Failed to get commit history'}]
        except Exception as e:
            return [{'error': f'Error getting commit history: {str(e)}'}]

    def get_current_branch(self, file_path: str) -> str:
        """Get current git branch."""
        try:
            git_dir = self._find_git_dir(file_path)
            if not git_dir:
                return 'Not a git repository'

            cmd = ['git', '--git-dir', str(git_dir), 'rev-parse', '--abbrev-ref', 'HEAD']
            return subprocess.check_output(cmd, cwd=Path(file_path).parent, text=True, errors='replace').strip()
        except subprocess.CalledProcessError:
            return 'Unknown'

    def get_recent_changes(self, file_path: str, days: int = 7) -> List[Dict[str, str]]:
        """Get recent changes in the repository."""
        try:
            git_dir = self._find_git_dir(file_path)
            if not git_dir:
                return [{'error': 'Not a git repository'}]

            since_date = f'--since="{days} days ago"'
            cmd = ['git', '--git-dir', str(git_dir), 'log', '--pretty=format:%h|%an|%ad|%s', '--date=short', since_date]
            output = subprocess.check_output(cmd, cwd=Path(file_path).parent, text=True, errors='replace')
            
            changes = []
            for line in output.splitlines():
                hash_id, author, date, message = line.split('|')
                changes.append({
                    'hash': hash_id,
                    'author': author,
                    'date': date,
                    'message': message
                })
            return changes
        except subprocess.CalledProcessError:
            return [{'error': 'Failed to get recent changes'}]
        except Exception as e:
            return [{'error': f'Error getting recent changes: {str(e)}'}]

    def learn_session(self, file_path: str, duration: int = 30) -> Dict[str, str]:
        """Start a learning session for repository understanding."""
        try:
            stats = self.get_repo_stats(file_path)
            history = self.get_commit_history(file_path, limit=5)
            branch = self.get_current_branch(file_path)
            changes = self.get_recent_changes(file_path, days=duration)
            
            return {
                'stats': stats,
                'recent_history': history,
                'current_branch': branch,
                'recent_changes': changes
            }
        except Exception as e:
            return {'error': f'Error during learning session: {str(e)}'}

    def _find_git_dir(self, path: Union[str, Path]) -> Optional[Path]:
        """Find the .git directory for a repository."""
        path = Path(path)
        if not path.exists():
            return None

        current = path if path.is_dir() else path.parent
        while current != current.parent:
            git_dir = current / '.git'
            if git_dir.exists() and git_dir.is_dir():
                return git_dir
            current = current.parent
        return None

    def _count_files(self, path: Path) -> int:
        """Count number of files in directory."""
        try:
            if path.is_file():
                return 1
            return sum(1 for _ in path.rglob('*') if _.is_file())
        except Exception:
            return 0

    def _count_lines(self, path: Path) -> int:
        """Count total lines in all files."""
        try:
            if path.is_file():
                with open(path, 'r', errors='replace') as f:
                    return sum(1 for _ in f)
            return sum(self._count_lines(f) for f in path.rglob('*') if f.is_file())
        except Exception:
            return 0

    def _analyze_complexity(self, path: Path) -> str:
        """Analyze code complexity."""
        try:
            lines = self._count_lines(path)
            if lines < 1000:
                return 'low'
            elif lines < 10000:
                return 'medium'
            else:
                return 'high'
        except Exception:
            return 'unknown'

    def _detect_languages(self, path: Path) -> List[str]:
        """Detect programming languages in repository."""
        try:
            extensions = set()
            for f in path.rglob('*'):
                if f.is_file():
                    ext = f.suffix.lower()
                    if ext and ext != '.':
                        extensions.add(ext[1:])  # Remove the leading dot
            return sorted(list(extensions))
        except Exception:
            return []
