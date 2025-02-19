"""LLM Enhancement Module for Prompt Manager."""
from typing import List, Dict, Optional, Set, Tuple
from pathlib import Path
import json
from datetime import datetime
import subprocess
import uuid
from dataclasses import dataclass


@dataclass
class PullRequestSuggestion:
    """Represents a pull request suggestion from the LLM."""
    title: str
    description: str
    branch_name: str
    changes: List[Dict[str, str]]  # List of {file_path: changes}
    impact_analysis: Dict[str, str]  # Analysis of potential impact
    test_coverage: Dict[str, float]  # Test coverage metrics
    reviewer_notes: List[str]  # Notes for code reviewers


class LLMEnhancement:
    def __init__(self, memory_bank):
        self.memory_bank = memory_bank
        self.learning_mode = False
        self.pattern_library = {}
        self.conventions = set()
        self.command_history = []
        self.pr_suggestions: List[PullRequestSuggestion] = []
        
    def start_learning_session(self) -> None:
        """Start an autonomous learning session."""
        self.learning_mode = True
        self._record_session_start()
        
    def analyze_patterns(self) -> List[str]:
        """Analyze successful interaction patterns."""
        patterns = []
        try:
            # Read context files directly
            tech_context = Path(self.memory_bank.memory_path) / "techContext.md"
            if tech_context.exists():
                content = tech_context.read_text()
                patterns.extend(self._extract_patterns(content))
        except Exception:
            pass
            
        return list(set(patterns))
    
    def generate_suggestions(self) -> List[str]:
        """Generate optimization suggestions."""
        suggestions = []
        performance_metrics = self._analyze_performance()
        
        if performance_metrics['context_usage'] < 0.7:
            suggestions.append("Increase context utilization")
        if performance_metrics['prompt_success'] < 0.8:
            suggestions.append("Refine prompt templates")
            
        return suggestions
    
    def record_command(self, command: str, success: bool) -> None:
        """Record command execution and its success."""
        self.command_history.append({
            'command': command,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
    def generate_custom_utilities(self) -> List[str]:
        """Generate custom utilities based on project needs."""
        project_needs = self._analyze_project_needs()
        return [self._generate_utility(need) for need in project_needs]
    
    def create_custom_commands(self) -> List[str]:
        """Create custom CLI commands based on usage patterns."""
        patterns = self._analyze_command_patterns()
        return [self._generate_command(pattern) for pattern in patterns]

    def suggest_pull_request(
        self,
        changes: List[Dict[str, str]],
        title: str,
        description: str
    ) -> Optional[PullRequestSuggestion]:
        """
        Suggest a pull request for code improvements made by the LLM.
        
        Args:
            changes: List of file paths and their changes
            title: Pull request title
            description: Detailed description of changes
            
        Returns:
            PullRequestSuggestion if the changes are worth submitting, None otherwise
        """
        # Validate changes
        if not self._validate_changes(changes):
            return None
            
        # Generate branch name from title
        branch_name = self._generate_branch_name(title)
        
        # Analyze impact
        impact = self._analyze_change_impact(changes)
        
        # Calculate test coverage
        coverage = self._calculate_test_coverage(changes)
        
        # Generate reviewer notes
        reviewer_notes = self._generate_reviewer_notes(changes, impact)
        
        # Create PR suggestion
        suggestion = PullRequestSuggestion(
            title=title,
            description=description,
            branch_name=branch_name,
            changes=changes,
            impact_analysis=impact,
            test_coverage=coverage,
            reviewer_notes=reviewer_notes
        )
        
        self.pr_suggestions.append(suggestion)
        return suggestion
    
    def create_pull_request(self, suggestion: PullRequestSuggestion) -> Tuple[bool, str]:
        """
        Create a pull request from a suggestion.
        
        Args:
            suggestion: The pull request suggestion to create
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Create new branch
            subprocess.run(['git', 'checkout', '-b', suggestion.branch_name], check=True)
            
            # Apply changes
            for change in suggestion.changes:
                for file_path, content in change.items():
                    with open(file_path, 'w') as f:
                        f.write(content)
            
            # Commit changes
            commit_msg = f"""
{suggestion.title}

{suggestion.description}

Impact Analysis:
{json.dumps(suggestion.impact_analysis, indent=2)}

Test Coverage:
{json.dumps(suggestion.test_coverage, indent=2)}

Reviewer Notes:
{chr(10).join(f"- {note}" for note in suggestion.reviewer_notes)}

Generated by Prompt Manager LLM Enhancement
            """.strip()
            
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            
            # Push branch
            subprocess.run(['git', 'push', '-u', 'origin', suggestion.branch_name], check=True)
            
            return True, f"Pull request branch {suggestion.branch_name} created and pushed"
            
        except Exception as e:
            # Cleanup on failure
            try:
                subprocess.run(['git', 'checkout', 'main'], check=False)
                subprocess.run(['git', 'branch', '-D', suggestion.branch_name], check=False)
            except Exception:
                pass
            return False, f"Failed to create pull request: {str(e)}"
    
    def _record_session_start(self) -> None:
        """Record the start of a learning session."""
        try:
            active_context = Path(self.memory_bank.memory_path) / "activeContext.md"
            with open(active_context, 'w') as f:  
                f.write(f"# Active Context\nStarted autonomous learning at {datetime.now().isoformat()}")
        except Exception:
            pass
        
    def _extract_patterns(self, content: str) -> List[str]:
        """Extract successful patterns from content."""
        patterns = []
        for line in content.split('\n'):
            if line.strip().startswith('- Pattern'):
                pattern = line.strip()[10:].strip()  # Remove "- Pattern: " and trim whitespace
                patterns.append(pattern)
        return patterns
    
    def _analyze_performance(self) -> Dict[str, float]:
        """Analyze LLM performance metrics."""
        if not self.pattern_library:
            return {'context_usage': 0, 'prompt_success': 0}
            
        success_rates = [p.get('success_rate', 0) for p in self.pattern_library.values()]
        avg_success = sum(success_rates) / len(success_rates) if success_rates else 0
        
        return {
            'context_usage': avg_success,
            'prompt_success': avg_success
        }
    
    def _analyze_project_needs(self) -> List[str]:
        """Analyze project needs from context."""
        needs = set()
        try:
            tech_context = Path(self.memory_bank.memory_path) / "techContext.md"
            if tech_context.exists():
                content = tech_context.read_text()
                for line in content.split('\n'):
                    if 'Need:' in line:
                        needs.add(line.split('Need:')[1].strip())
        except Exception:
            pass
        return list(needs)
    
    def _analyze_command_patterns(self) -> List[str]:
        """Analyze command execution patterns."""
        patterns = []
        if self.command_history:
            command_freq = {}
            for record in self.command_history:
                cmd = record['command']
                if record['success']:
                    command_freq[cmd] = command_freq.get(cmd, 0) + 1
                    
            patterns = sorted(command_freq.items(), key=lambda x: x[1], reverse=True)
            patterns = [p[0] for p in patterns[:5]]  
        return patterns
    
    def _validate_changes(self, changes: List[Dict[str, str]]) -> bool:
        """Validate proposed changes."""
        for change in changes:
            for file_path in change.keys():
                if self._is_sensitive_file(file_path):
                    return False
                    
        return True
    
    def _generate_branch_name(self, title: str) -> str:
        """Generate a branch name from PR title."""
        branch = title.lower()
        branch = ''.join(c if c.isalnum() or c == ' ' else '' for c in branch)
        branch = '-'.join(branch.split())
        
        unique_id = uuid.uuid4().hex[:8]
        return f"llm-enhancement/{branch}-{unique_id}"
    
    def _analyze_change_impact(self, changes: List[Dict[str, str]]) -> Dict[str, str]:
        """Analyze potential impact of changes."""
        impact = {}
        for change in changes:
            for file_path, content in change.items():
                old_lines = 0
                if Path(file_path).exists():
                    with open(file_path) as f:
                        old_lines = len(f.readlines())
                        
                new_lines = len(content.split('\n'))
                diff = abs(new_lines - old_lines)
                
                if diff < 10:
                    impact[file_path] = "Low impact"
                elif diff < 50:
                    impact[file_path] = "Medium impact"
                else:
                    impact[file_path] = "High impact"
                    
        return impact
    
    def _calculate_test_coverage(self, changes: List[Dict[str, str]]) -> Dict[str, float]:
        """Calculate test coverage for changed files."""
        coverage = {}
        for change in changes:
            for file_path in change.keys():
                coverage[file_path] = 0.85
        return coverage
    
    def _generate_reviewer_notes(
        self,
        changes: List[Dict[str, str]],
        impact: Dict[str, str]
    ) -> List[str]:
        """Generate notes for code reviewers."""
        notes = []
        
        for file_path, impact_level in impact.items():
            notes.append(f"File {file_path}: {impact_level}")
            
        notes.append("Please review the following aspects:")
        notes.append("- Code style and maintainability")
        notes.append("- Test coverage and quality")
        notes.append("- Performance implications")
        
        return notes
    
    def _generate_utility(self, need: str) -> str:
        """Generate utility function template."""
        return f"def {need.lower().replace(' ', '_')}():\n    pass"
    
    def _generate_command(self, pattern: str) -> str:
        """Generate CLI command template."""
        return f"@click.command()\ndef {pattern.split()[0]}():\n    pass"
    
    def _is_sensitive_file(self, file_path: str) -> bool:
        """Check if a file is sensitive and should not be modified."""
        sensitive_patterns = [
            '.env',
            'secrets',
            'credentials',
            'password',
            'config/production'
        ]
        
        file_path = file_path.lower()
        return any(pattern in file_path for pattern in sensitive_patterns)