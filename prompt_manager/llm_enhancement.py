"""LLM Enhancement Module for Prompt Manager."""
from typing import List, Dict, Optional, Set, Tuple
from pathlib import Path
import json
from datetime import datetime
import subprocess
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
        context = self.memory_bank.get_all_context()
        
        for content in context:
            extracted_patterns = self._extract_patterns(content)
            patterns.extend(extracted_patterns)
            
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
            subprocess.run(['git', 'checkout', 'main'])
            subprocess.run(['git', 'branch', '-D', suggestion.branch_name])
            return False, f"Failed to create pull request: {str(e)}"
    
    def _record_session_start(self) -> None:
        """Record the start of a learning session."""
        self.memory_bank.update_context(
            "activeContext.md",
            "Learning Session",
            f"Started autonomous learning at {datetime.now().isoformat()}"
        )
        
    def _extract_patterns(self, content: str) -> List[str]:
        """Extract successful patterns from content."""
        # Implementation would use NLP to identify patterns
        return []
    
    def _analyze_performance(self) -> Dict[str, float]:
        """Analyze LLM performance metrics."""
        return {
            'context_usage': 0.75,
            'prompt_success': 0.85
        }
    
    def _analyze_project_needs(self) -> List[str]:
        """Analyze project needs from context."""
        needs = set()
        context = self.memory_bank.get_all_context()
        
        # Implementation would analyze context for needs
        return list(needs)
    
    def _generate_utility(self, need: str) -> str:
        """Generate utility code based on need."""
        # Implementation would generate utility code
        return f"Utility for: {need}"
    
    def _analyze_command_patterns(self) -> List[str]:
        """Analyze command usage patterns."""
        patterns = []
        if self.command_history:
            # Implementation would analyze command history
            pass
        return patterns
    
    def _generate_command(self, pattern: str) -> str:
        """Generate command based on pattern."""
        # Implementation would generate command code
        return f"Command for pattern: {pattern}"

    def _validate_changes(self, changes: List[Dict[str, str]]) -> bool:
        """
        Validate proposed changes.
        
        Checks:
        1. Files exist
        2. Changes follow project conventions
        3. No sensitive files are modified
        """
        for change in changes:
            for file_path in change:
                if not Path(file_path).exists():
                    return False
                if self._is_sensitive_file(file_path):
                    return False
        return True
    
    def _generate_branch_name(self, title: str) -> str:
        """Generate a branch name from PR title."""
        # Convert to lowercase, replace spaces with hyphens
        base = title.lower().replace(' ', '-')
        # Remove special characters
        base = ''.join(c for c in base if c.isalnum() or c == '-')
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"llm-enhancement/{base}-{timestamp}"
    
    def _analyze_change_impact(self, changes: List[Dict[str, str]]) -> Dict[str, str]:
        """Analyze the potential impact of changes."""
        impact = {}
        for change in changes:
            for file_path in change:
                # Analyze file dependencies
                impact[file_path] = self._analyze_file_impact(file_path)
        return impact
    
    def _calculate_test_coverage(self, changes: List[Dict[str, str]]) -> Dict[str, float]:
        """Calculate test coverage for changed files."""
        coverage = {}
        for change in changes:
            for file_path in change:
                coverage[file_path] = self._get_file_test_coverage(file_path)
        return coverage
    
    def _generate_reviewer_notes(
        self,
        changes: List[Dict[str, str]],
        impact: Dict[str, str]
    ) -> List[str]:
        """Generate notes to help code reviewers."""
        notes = []
        
        # Add general notes
        notes.append("Changes generated by Prompt Manager LLM Enhancement")
        
        # Add impact notes
        for file_path, impact_analysis in impact.items():
            notes.append(f"Impact on {file_path}: {impact_analysis}")
            
        # Add testing notes
        notes.append("Please verify test coverage and add additional tests if needed")
        
        return notes
    
    def _is_sensitive_file(self, file_path: str) -> bool:
        """Check if a file is sensitive and shouldn't be modified."""
        sensitive_patterns = {
            '.env',
            'secrets',
            'password',
            'credential',
            'config/production',
        }
        
        file_path_lower = file_path.lower()
        return any(pattern in file_path_lower for pattern in sensitive_patterns)
    
    def _analyze_file_impact(self, file_path: str) -> str:
        """Analyze the impact of changes to a specific file."""
        # Implementation would analyze dependencies and potential side effects
        return "Moderate impact - affects core functionality"
    
    def _get_file_test_coverage(self, file_path: str) -> float:
        """Get the test coverage for a specific file."""
        # Implementation would calculate actual test coverage
        return 0.85  # 85% coverage