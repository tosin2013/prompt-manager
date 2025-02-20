"""Repository manager for code analysis and learning."""

from pathlib import Path
from typing import Dict, List, Optional, Union
import subprocess
import os
from prompt_manager.models.learning_session import LearningSession


class RepoManager:
    """Manager for repository operations."""

    def __init__(self, project_dir: Optional[str] = None):
        """Initialize repository manager."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.current_session: Optional[LearningSession] = None

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

    def learn_session(self, file_path: str, duration: int = 30) -> Dict[str, Union[Dict, List, str]]:
        """Start a learning session for repository understanding.
        
        Args:
            file_path: Path to the file or directory to analyze
            duration: Duration in minutes for the learning session
            
        Returns:
            Dictionary containing session information and analysis results
            
        Raises:
            ValueError: If duration is less than 1 minute
            FileNotFoundError: If file_path does not exist
        """
        try:
            # Create and start learning session
            self.current_session = LearningSession(duration=duration)
            self.current_session.start()
            
            # Validate file path
            if not Path(file_path).exists():
                return {'error': f'File path does not exist: {file_path}'}

            # Get git directory
            git_dir = self._find_git_dir(file_path)
            if not git_dir:
                return {'error': 'Not a git repository'}

            # Gather repository information
            stats = self.get_repo_stats(file_path)
            if not isinstance(stats, dict):
                stats = {'total_files': 0, 'languages': []}

            # Get commit history
            history = self.get_commit_history(file_path, limit=5)
            if not isinstance(history, list):
                history = [{'error': 'Failed to get commit history'}]
            
            # Format commit history for template
            commit_history = "\n".join([
                f"- [{commit.get('hash', 'unknown')}] {commit.get('message', 'No message')} "
                f"(by {commit.get('author', 'unknown')} on {commit.get('date', 'unknown')})"
                for commit in history if isinstance(commit, dict) and 'error' not in commit
            ]) or "No commit history available"

            # Get current branch
            branch = self.get_current_branch(file_path)
            if not branch:
                branch = 'Unknown'

            # Get recent changes
            changes = self.get_recent_changes(file_path, days=duration)
            if not isinstance(changes, list):
                changes = [{'error': 'Failed to get recent changes'}]

            # Analyze code patterns
            try:
                with open(file_path, 'r', errors='replace') as f:
                    content = f.read()
                code_patterns = self._analyze_code_patterns(content)
            except Exception:
                code_patterns = "Could not analyze code patterns"

            # Get documentation
            documentation = self._get_documentation(Path(file_path))

            # Get test coverage
            test_coverage = self._get_test_coverage(Path(file_path))

            # Include session information in response
            session_info = self.current_session.to_dict()

            return {
                'stats': stats,
                'recent_history': history,
                'current_branch': branch,
                'recent_changes': changes,
                'session': session_info,
                'template_context': {
                    'repo_path': file_path,
                    'file_path': file_path,
                    'duration': duration,
                    'commit_history': commit_history,
                    'code_patterns': code_patterns,
                    'documentation': documentation,
                    'test_coverage': test_coverage,
                    'file_count': stats.get('total_files', 0),
                    'languages': stats.get('languages', []),
                    'recent_changes': changes
                }
            }
        except ValueError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': f'Error starting learning session: {str(e)}'}

    def _analyze_code_patterns(self, content: str) -> str:
        """Analyze code patterns in content."""
        patterns = []
        
        # Check for common patterns
        if 'class ' in content:
            patterns.append("Object-oriented programming")
        if 'def ' in content:
            patterns.append("Function-based organization")
        if 'import ' in content:
            patterns.append("External dependencies")
        if 'try:' in content:
            patterns.append("Error handling")
        if 'test' in content.lower():
            patterns.append("Test-driven development")
        if '#' in content or '"""' in content:
            patterns.append("Documentation practices")
            
        return "\n".join([f"- {pattern}" for pattern in patterns]) if patterns else "No clear patterns detected"

    def _get_documentation(self, path: Path) -> str:
        """Get documentation information."""
        try:
            if not path.exists():
                return "File not found"
                
            doc_files = []
            if path.is_file():
                with open(path, 'r', errors='replace') as f:
                    content = f.read()
                    if '"""' in content or "'''" in content:
                        doc_files.append(f"- {path.name}: Has docstrings")
            else:
                for doc_file in ['README.md', 'DOCS.md', 'API.md']:
                    if (path / doc_file).exists():
                        doc_files.append(f"- {doc_file}: Present")
                        
            return "\n".join(doc_files) if doc_files else "No documentation found"
        except Exception:
            return "Could not analyze documentation"

    def _get_test_coverage(self, path: Path) -> str:
        """Get test coverage information."""
        try:
            if not path.exists():
                return "File not found"
                
            test_files = []
            if path.is_file():
                test_path = path.parent / 'tests' / f'test_{path.name}'
                if test_path.exists():
                    test_files.append(f"- {test_path.name}: Present")
            else:
                test_dir = path / 'tests'
                if test_dir.exists():
                    test_files.extend([
                        f"- {f.name}: Present"
                        for f in test_dir.glob('test_*.py')
                    ])
                        
            return "\n".join(test_files) if test_files else "No test files found"
        except Exception:
            return "Could not analyze test coverage"

    def _find_git_dir(self, path: Union[str, Path]) -> Optional[Path]:
        """Find the .git directory for a repository."""
        try:
            path = Path(path)
            if path.is_file():
                path = path.parent
                
            git_path = path / '.git'
            if git_path.exists() and git_path.is_dir():
                return git_path
                
            # Try running git rev-parse to find git dir
            try:
                cmd = ['git', 'rev-parse', '--git-dir']
                output = subprocess.check_output(cmd, cwd=path, text=True, stderr=subprocess.PIPE).strip()
                git_path = Path(output)
                if not git_path.is_absolute():
                    git_path = path / git_path
                return git_path if git_path.exists() else None
            except subprocess.CalledProcessError:
                return None
                
        except Exception:
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
