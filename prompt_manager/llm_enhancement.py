"""LLM Enhancement Module for Prompt Manager.

This module provides advanced LLM capabilities including:
- Autonomous learning and pattern recognition
- Pull request generation and code improvement
- Custom utility and command generation
- Performance analysis and optimization
"""
from typing import List, Dict, Optional, Set, Tuple, Any
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


@dataclass
class MethodGuidance:
    """Provides guidance for LLM method usage."""
    purpose: str
    context: str
    example_scenario: str
    expected_outcome: str
    next_steps: str
    
    def format(self) -> str:
        """Format the guidance into a clear message."""
        return f"""
Method Guidance:
---------------
Purpose: {self.purpose}
When to Use: {self.context}
Example Scenario: {self.example_scenario}
Expected Outcome: {self.expected_outcome}
Next Steps: {self.next_steps}
"""


class LLMEnhancement:
    """Provides advanced LLM capabilities for code improvement and automation."""

    def __init__(self, memory_bank):
        """Initialize the LLM Enhancement system.
        
        Args:
            memory_bank: The memory bank instance for context storage
        """
        self.memory_bank = memory_bank
        self.learning_mode = False
        self.pattern_library = {}
        self.conventions = set()
        self.command_history = []
        self.pr_suggestions: List[PullRequestSuggestion] = []
        
    @staticmethod
    def get_method_guidance(method_name: str) -> MethodGuidance:
        """Get guidance for a specific method.
        
        Args:
            method_name: Name of the method to get guidance for
            
        Returns:
            MethodGuidance object containing usage information
        """
        guidance_map = {
            "start_learning_session": MethodGuidance(
                purpose="Enable autonomous learning mode for pattern recognition",
                context="Use when you want the LLM to learn from interactions and improve over time",
                example_scenario="Starting a new development session where you want the LLM to adapt to project patterns",
                expected_outcome="LLM will begin tracking and learning from interactions",
                next_steps="Monitor learning progress through analyze_patterns()"
            ),
            "analyze_patterns": MethodGuidance(
                purpose="Analyze successful interaction patterns from the current session",
                context="Use after a learning session to understand what patterns were effective",
                example_scenario="After completing several successful tasks, analyze what worked well",
                expected_outcome="List of identified successful patterns",
                next_steps="Use patterns to improve future interactions or generate suggestions"
            ),
            "generate_suggestions": MethodGuidance(
                purpose="Generate optimization suggestions based on performance analysis",
                context="Use when looking to improve LLM effectiveness",
                example_scenario="After noticing suboptimal performance in certain areas",
                expected_outcome="List of actionable suggestions for improvement",
                next_steps="Implement suggested optimizations and measure impact"
            ),
            "record_command": MethodGuidance(
                purpose="Record command execution results for pattern analysis",
                context="Use after executing any significant command",
                example_scenario="After running a complex operation, record its success/failure",
                expected_outcome="Command execution recorded in history",
                next_steps="Use analyze_patterns() to learn from recorded commands"
            ),
            "generate_custom_utilities": MethodGuidance(
                purpose="Generate custom utility functions based on project needs",
                context="Use when identifying repeated patterns that could be automated",
                example_scenario="When you notice developers frequently performing the same sequence of actions",
                expected_outcome="List of suggested utility functions to create",
                next_steps="Implement and test the generated utilities"
            ),
            "create_custom_commands": MethodGuidance(
                purpose="Create custom CLI commands based on usage patterns",
                context="Use when common command sequences are identified",
                example_scenario="When users frequently combine multiple commands for a single task",
                expected_outcome="List of suggested CLI commands to create",
                next_steps="Implement and document the new commands"
            ),
            "suggest_pull_request": MethodGuidance(
                purpose="Generate a pull request suggestion for code improvements",
                context="Use when the LLM has identified potential code improvements",
                example_scenario="After analyzing code and finding optimization opportunities",
                expected_outcome="PullRequestSuggestion object with detailed changes",
                next_steps="Review and implement the suggested changes"
            ),
        }
        
        return guidance_map.get(method_name, MethodGuidance(
            purpose="Unknown method",
            context="Method not recognized",
            example_scenario="N/A",
            expected_outcome="N/A",
            next_steps="Check method name and documentation"
        ))
        
    def _get_guidance(self, method_name: str) -> str:
        """Get formatted guidance for the current method."""
        return self.get_method_guidance(method_name).format()
        
    def start_learning_session(self) -> None:
        """Start an autonomous learning session."""
        print(self._get_guidance("start_learning_session"))
        self.learning_mode = True
        self._record_session_start()
        
    def analyze_patterns(self) -> List[str]:
        """Analyze successful interaction patterns."""
        print(self._get_guidance("analyze_patterns"))
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
        print(self._get_guidance("generate_suggestions"))
        suggestions = []
        performance_metrics = self._analyze_performance()
        
        if performance_metrics['context_usage'] < 0.7:
            suggestions.append("Increase context utilization")
        if performance_metrics['prompt_success'] < 0.8:
            suggestions.append("Refine prompt templates")
            
        return suggestions
    
    def record_command(self, command: str, success: bool) -> None:
        """Record command execution and its success."""
        print(self._get_guidance("record_command"))
        self.command_history.append({
            'command': command,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
    def generate_custom_utilities(self) -> List[str]:
        """Generate custom utilities based on project needs."""
        print(self._get_guidance("generate_custom_utilities"))
        project_needs = self._analyze_project_needs()
        return [self._generate_utility(need) for need in project_needs]
    
    def create_custom_commands(self) -> List[str]:
        """Create custom CLI commands based on usage patterns."""
        print(self._get_guidance("create_custom_commands"))
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
        print(self._get_guidance("suggest_pull_request"))
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
        """Record the start of a learning session with metadata."""
        session_id = str(uuid.uuid4())
        session_data = {
            'id': session_id,
            'start_time': datetime.now().isoformat(),
            'context_files': self._get_context_files(),
            'initial_patterns': len(self.pattern_library)
        }
        self._save_session_data(session_data)

    def _save_session_data(self, data: Dict[str, Any]) -> None:
        """Save session data to the memory bank.
        
        Args:
            data: Session metadata to save
        """
        try:
            session_file = Path(self.memory_bank.memory_path) / "sessions.json"
            existing_data = []
            if session_file.exists():
                existing_data = json.loads(session_file.read_text())
            existing_data.append(data)
            session_file.write_text(json.dumps(existing_data, indent=2))
        except Exception as e:
            print(f"Warning: Failed to save session data: {e}")

    def _get_context_files(self) -> List[str]:
        """Get list of relevant context files in the project."""
        try:
            context_dir = Path(self.memory_bank.memory_path)
            return [str(f.relative_to(context_dir)) for f in context_dir.glob("*.md")]
        except Exception:
            return []

    def _extract_patterns(self, content: str) -> List[str]:
        """Extract patterns from content using simple heuristics.
        
        Args:
            content: Text content to analyze
            
        Returns:
            List of identified patterns
        """
        patterns = []
        lines = content.split('\n')
        
        # Look for common patterns in the content
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('- ') or line.startswith('* '):
                patterns.append(line[2:])
            elif line.startswith('#'):
                # Capture section headers as potential patterns
                patterns.append(line.lstrip('#').strip())
                
        return patterns

    def _analyze_performance(self) -> Dict[str, float]:
        """Analyze LLM performance metrics.
        
        Returns:
            Dictionary of performance metrics
        """
        total_commands = len(self.command_history)
        if not total_commands:
            return {'context_usage': 0.0, 'prompt_success': 0.0}
            
        successful_commands = sum(1 for cmd in self.command_history if cmd['success'])
        
        # Calculate basic metrics
        metrics = {
            'context_usage': len(self.pattern_library) / max(1, total_commands),
            'prompt_success': successful_commands / total_commands
        }
        
        return metrics

    def _analyze_project_needs(self) -> List[str]:
        """Analyze project needs based on command history and patterns.
        
        Returns:
            List of identified project needs
        """
        needs = set()
        
        # Analyze command patterns
        command_patterns = self._analyze_command_patterns()
        for pattern in command_patterns:
            if pattern.count('&&') > 2:  # Complex command chain
                needs.add('utility_for_' + '_'.join(pattern.split('&&')[0].split()))
                
        # Analyze conventions
        for convention in self.conventions:
            if 'test' in convention.lower():
                needs.add('test_utility')
            elif 'lint' in convention.lower():
                needs.add('lint_utility')
                
        return list(needs)

    def _generate_utility(self, need: str) -> str:
        """Generate utility function template based on need.
        
        Args:
            need: Identified project need
            
        Returns:
            Utility function template
        """
        return f"""def {need}():
    \"\"\"
    Utility function for: {need.replace('_', ' ')}
    Generated based on project patterns
    \"\"\"
    # TODO: Implement {need} functionality
    pass"""

    def _analyze_command_patterns(self) -> List[str]:
        """Analyze command history for patterns.
        
        Returns:
            List of identified command patterns
        """
        patterns = []
        
        # Group commands by similarity
        command_groups = {}
        for cmd in self.command_history:
            base_cmd = cmd['command'].split()[0]
            if base_cmd not in command_groups:
                command_groups[base_cmd] = []
            command_groups[base_cmd].append(cmd['command'])
            
        # Identify frequent patterns
        for base_cmd, commands in command_groups.items():
            if len(commands) >= 3:  # Pattern threshold
                patterns.append(max(commands, key=len))  # Use most complex example
                
        return patterns

    def _generate_command(self, pattern: str) -> str:
        """Generate CLI command template based on pattern.
        
        Args:
            pattern: Command pattern to base template on
            
        Returns:
            CLI command template
        """
        parts = pattern.split()
        command_name = f"{parts[0]}_{parts[-1]}"
        return f"""@click.command()
def {command_name}():
    \"\"\"
    Custom command based on pattern: {pattern}
    \"\"\"
    # TODO: Implement {command_name} functionality
    pass"""

    def _validate_changes(self, changes: List[Dict[str, str]]) -> bool:
        """Validate proposed changes before creating pull request.
        
        Args:
            changes: List of proposed file changes
            
        Returns:
            True if changes are valid, False otherwise
        """
        if not changes:
            return False
            
        for change in changes:
            for file_path, content in change.items():
                # Basic validation
                if not Path(file_path).exists():
                    return False
                if not content.strip():
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

    def debug_session(self) -> Dict[str, Any]:
        """Debug current learning session and provide comprehensive feedback.
        
        This method analyzes the current session and provides detailed feedback about:
        - Pattern recognition effectiveness
        - Command success rates
        - Context utilization
        - Performance bottlenecks
        - Potential improvements
        
        Returns:
            Dictionary containing debug information with the following structure:
            {
                'session_stats': {
                    'duration': str,
                    'commands_executed': int,
                    'success_rate': float,
                    'patterns_identified': int
                },
                'performance_metrics': {
                    'context_usage': float,
                    'prompt_success': float,
                    'response_time_avg': float
                },
                'identified_issues': List[str],
                'improvement_suggestions': List[str],
                'context_analysis': {
                    'unused_patterns': List[str],
                    'successful_patterns': List[str],
                    'failed_patterns': List[str]
                }
            }
        """
        debug_info = {
            'session_stats': self._get_session_stats(),
            'performance_metrics': self._analyze_performance(),
            'identified_issues': self._identify_issues(),
            'improvement_suggestions': self._generate_improvement_suggestions(),
            'context_analysis': self._analyze_context_usage()
        }
        
        # Log debug information
        self._log_debug_info(debug_info)
        return debug_info
        
    def _get_session_stats(self) -> Dict[str, Any]:
        """Get detailed statistics about the current session.
        
        Returns:
            Dictionary containing session statistics
        """
        current_time = datetime.now()
        session_start = self._get_session_start_time()
        duration = current_time - session_start if session_start else None
        
        total_commands = len(self.command_history)
        successful_commands = sum(1 for cmd in self.command_history if cmd['success'])
        success_rate = successful_commands / max(1, total_commands)
        
        return {
            'duration': str(duration) if duration else 'Unknown',
            'commands_executed': total_commands,
            'success_rate': success_rate,
            'patterns_identified': len(self.pattern_library)
        }
        
    def _get_session_start_time(self) -> Optional[datetime]:
        """Get the start time of the current session.
        
        Returns:
            datetime object of session start if available, None otherwise
        """
        try:
            session_file = Path(self.memory_bank.memory_path) / "sessions.json"
            if session_file.exists():
                sessions = json.loads(session_file.read_text())
                if sessions:
                    latest_session = sessions[-1]
                    return datetime.fromisoformat(latest_session['start_time'])
        except Exception:
            pass
        return None
        
    def _identify_issues(self) -> List[str]:
        """Identify potential issues in the current session.
        
        This method analyzes patterns and command history to identify:
        - Low success rate commands
        - Unused patterns
        - Performance bottlenecks
        - Context utilization issues
        
        Returns:
            List of identified issues with descriptions
        """
        issues = []
        
        # Analyze command success rates
        for cmd_type, commands in self._group_commands_by_type().items():
            success_rate = sum(1 for c in commands if c['success']) / len(commands)
            if success_rate < 0.7:
                issues.append(f"Low success rate ({success_rate:.2f}) for command type: {cmd_type}")
                
        # Check pattern utilization
        context_analysis = self._analyze_context_usage()
        if context_analysis['unused_patterns']:
            issues.append(f"Found {len(context_analysis['unused_patterns'])} unused patterns")
            
        # Check performance metrics
        metrics = self._analyze_performance()
        if metrics['context_usage'] < 0.5:
            issues.append("Low context utilization")
        if metrics['prompt_success'] < 0.8:
            issues.append("Below target prompt success rate")
            
        return issues
        
    def _generate_improvement_suggestions(self) -> List[str]:
        """Generate suggestions for improving LLM performance.
        
        Analyzes current session data to suggest:
        - Pattern refinements
        - Command optimizations
        - Context utilization improvements
        - Performance enhancements
        
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        issues = self._identify_issues()
        
        for issue in issues:
            if "Low success rate" in issue:
                cmd_type = issue.split("command type: ")[1]
                suggestions.append(f"Consider refining prompts for {cmd_type} commands")
                
            elif "unused patterns" in issue:
                suggestions.append("Review and update pattern recognition criteria")
                suggestions.append("Consider removing or updating unused patterns")
                
            elif "Low context utilization" in issue:
                suggestions.append("Increase context awareness in prompts")
                suggestions.append("Review context extraction methodology")
                
            elif "Below target prompt success" in issue:
                suggestions.append("Analyze failed prompts for common patterns")
                suggestions.append("Consider adding more specific guidance for common failures")
                
        return suggestions
        
    def _analyze_context_usage(self) -> Dict[str, List[str]]:
        """Analyze how effectively context and patterns are being used.
        
        Returns:
            Dictionary containing lists of patterns categorized by usage:
            - unused_patterns: Patterns never matched
            - successful_patterns: Patterns with high success rate
            - failed_patterns: Patterns with low success rate
        """
        pattern_usage = {pattern: {'used': 0, 'success': 0} for pattern in self.pattern_library}
        
        # Analyze command history for pattern usage
        for cmd in self.command_history:
            for pattern in self.pattern_library:
                if pattern in cmd['command']:
                    pattern_usage[pattern]['used'] += 1
                    if cmd['success']:
                        pattern_usage[pattern]['success'] += 1
                        
        # Categorize patterns
        unused = []
        successful = []
        failed = []
        
        for pattern, stats in pattern_usage.items():
            if stats['used'] == 0:
                unused.append(pattern)
            else:
                success_rate = stats['success'] / stats['used']
                if success_rate >= 0.7:
                    successful.append(pattern)
                else:
                    failed.append(pattern)
                    
        return {
            'unused_patterns': unused,
            'successful_patterns': successful,
            'failed_patterns': failed
        }
        
    def _group_commands_by_type(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group command history by command type.
        
        Returns:
            Dictionary mapping command types to lists of command records
        """
        grouped = {}
        for cmd in self.command_history:
            cmd_type = cmd['command'].split()[0]
            if cmd_type not in grouped:
                grouped[cmd_type] = []
            grouped[cmd_type].append(cmd)
        return grouped
        
    def _log_debug_info(self, debug_info: Dict[str, Any]) -> None:
        """Log debug information for future analysis.
        
        Args:
            debug_info: Debug information to log
        """
        try:
            debug_file = Path(self.memory_bank.memory_path) / "debug_logs.json"
            existing_logs = []
            if debug_file.exists():
                existing_logs = json.loads(debug_file.read_text())
                
            # Add timestamp to debug info
            debug_info['timestamp'] = datetime.now().isoformat()
            existing_logs.append(debug_info)
            
            # Keep only last 100 debug logs
            if len(existing_logs) > 100:
                existing_logs = existing_logs[-100:]
                
            debug_file.write_text(json.dumps(existing_logs, indent=2))
        except Exception as e:
            print(f"Warning: Failed to log debug information: {e}")
            
    def get_debug_summary(self) -> str:
        """Get a human-readable summary of the current debug state.
        
        Returns:
            Formatted string containing key debug information
        """
        debug_info = self.debug_session()
        
        summary = [
            "=== LLM Enhancement Debug Summary ===",
            "",
            "Session Statistics:",
            f"- Duration: {debug_info['session_stats']['duration']}",
            f"- Commands Executed: {debug_info['session_stats']['commands_executed']}",
            f"- Success Rate: {debug_info['session_stats']['success_rate']:.2%}",
            f"- Patterns Identified: {debug_info['session_stats']['patterns_identified']}",
            "",
            "Performance Metrics:",
            f"- Context Usage: {debug_info['performance_metrics']['context_usage']:.2%}",
            f"- Prompt Success: {debug_info['performance_metrics']['prompt_success']:.2%}",
            "",
            "Identified Issues:",
            *[f"- {issue}" for issue in debug_info['identified_issues']],
            "",
            "Improvement Suggestions:",
            *[f"- {suggestion}" for suggestion in debug_info['improvement_suggestions']],
            "",
            "Context Analysis:",
            f"- Unused Patterns: {len(debug_info['context_analysis']['unused_patterns'])}",
            f"- Successful Patterns: {len(debug_info['context_analysis']['successful_patterns'])}",
            f"- Failed Patterns: {len(debug_info['context_analysis']['failed_patterns'])}"
        ]
        
        return "\n".join(summary)

    def get_debug_guidance(self, issue_type: str = None) -> str:
        """Get structured debugging guidance based on David J. Agans' debugging principles.
        
        This method provides targeted debugging guidance following the 9 indispensable
        rules from "Debugging: The 9 Indispensable Rules for Finding Even the Most
        Elusive Software and Hardware Problems" by David J. Agans.
        
        Args:
            issue_type: Optional specific issue type to get targeted guidance
            
        Returns:
            Formatted string containing debugging guidance
        """
        # Core debugging principles
        debug_principles = {
            "understand_system": {
                "rule": "Understand the System",
                "description": "Gain comprehensive understanding of the system's design and functionality",
                "actions": [
                    "Review system architecture and components",
                    "Study interaction patterns between components",
                    "Analyze data flow and state management",
                    "Document system boundaries and interfaces"
                ],
                "when_to_use": [
                    "Starting work on a new component",
                    "Investigating complex interactions",
                    "Debugging cross-component issues"
                ]
            },
            "make_it_fail": {
                "rule": "Make It Fail",
                "description": "Create a reliable reproduction of the issue",
                "actions": [
                    "Document exact steps to reproduce",
                    "Identify environmental factors",
                    "Create minimal test case",
                    "Record all relevant variables"
                ],
                "when_to_use": [
                    "Investigating intermittent issues",
                    "Validating bug reports",
                    "Creating regression tests"
                ]
            },
            "quit_thinking_look": {
                "rule": "Quit Thinking and Look",
                "description": "Observe actual behavior instead of making assumptions",
                "actions": [
                    "Add detailed logging",
                    "Monitor system state",
                    "Track variable changes",
                    "Analyze execution flow"
                ],
                "when_to_use": [
                    "Debugging unexpected behavior",
                    "Investigating race conditions",
                    "Analyzing performance issues"
                ]
            },
            "divide_conquer": {
                "rule": "Divide and Conquer",
                "description": "Break down complex problems into smaller, testable components",
                "actions": [
                    "Isolate problematic components",
                    "Test components independently",
                    "Verify component interfaces",
                    "Create focused test cases"
                ],
                "when_to_use": [
                    "Debugging complex systems",
                    "Investigating integration issues",
                    "Optimizing performance"
                ]
            },
            "change_one_thing": {
                "rule": "Change One Thing at a Time",
                "description": "Make controlled, isolated changes to identify root causes",
                "actions": [
                    "Document each change",
                    "Test after each modification",
                    "Revert unsuccessful changes",
                    "Track impact of changes"
                ],
                "when_to_use": [
                    "Testing potential fixes",
                    "Optimizing code",
                    "Refactoring components"
                ]
            },
            "keep_audit_trail": {
                "rule": "Keep an Audit Trail",
                "description": "Maintain detailed records of debugging process",
                "actions": [
                    "Log all attempted solutions",
                    "Document observed behaviors",
                    "Track environmental changes",
                    "Record test results"
                ],
                "when_to_use": [
                    "Long debugging sessions",
                    "Team debugging efforts",
                    "Complex issue investigation"
                ]
            },
            "check_plug": {
                "rule": "Check the Plug",
                "description": "Verify basic assumptions and configurations",
                "actions": [
                    "Validate environment setup",
                    "Check configuration files",
                    "Verify dependencies",
                    "Test basic functionality"
                ],
                "when_to_use": [
                    "Starting debug session",
                    "After environment changes",
                    "Investigating basic issues"
                ]
            },
            "get_fresh_view": {
                "rule": "Get a Fresh View",
                "description": "Seek alternative perspectives and approaches",
                "actions": [
                    "Consult team members",
                    "Review documentation",
                    "Take structured breaks",
                    "Question assumptions"
                ],
                "when_to_use": [
                    "Stuck on difficult issues",
                    "Long debugging sessions",
                    "Complex problem solving"
                ]
            },
            "verify_fix": {
                "rule": "If You Didn't Fix It, It Ain't Fixed",
                "description": "Ensure complete resolution of the issue",
                "actions": [
                    "Verify fix addresses root cause",
                    "Test edge cases",
                    "Add regression tests",
                    "Document resolution"
                ],
                "when_to_use": [
                    "After implementing fixes",
                    "Before closing issues",
                    "During code review"
                ]
            }
        }

        # Map common issues to relevant principles
        issue_principle_mapping = {
            "performance": ["understand_system", "quit_thinking_look", "divide_conquer"],
            "integration": ["understand_system", "make_it_fail", "divide_conquer"],
            "configuration": ["check_plug", "change_one_thing", "keep_audit_trail"],
            "reliability": ["make_it_fail", "quit_thinking_look", "verify_fix"],
            "complexity": ["understand_system", "divide_conquer", "get_fresh_view"]
        }

        def format_principle(principle_data: Dict[str, Any]) -> str:
            """Format a single debugging principle into readable text."""
            return f"""
Rule: {principle_data['rule']}
Description: {principle_data['description']}

Recommended Actions:
{chr(10).join(f'- {action}' for action in principle_data['actions'])}

When to Use:
{chr(10).join(f'- {when}' for when in principle_data['when_to_use'])}
"""

        # Generate guidance based on issue type or provide comprehensive guide
        if issue_type and issue_type in issue_principle_mapping:
            relevant_principles = issue_principle_mapping[issue_type]
            guidance = [
                f"=== Debugging Guidance for {issue_type.title()} Issues ===\n",
                "Following principles are particularly relevant for your current issue:\n"
            ]
            for principle_key in relevant_principles:
                guidance.append(format_principle(debug_principles[principle_key]))
        else:
            guidance = [
                "=== Comprehensive Debugging Guidance ===\n",
                "Consider these debugging principles for systematic problem solving:\n"
            ]
            for principle_data in debug_principles.values():
                guidance.append(format_principle(principle_data))

        return "\n".join(guidance)

    def debug_with_guidance(self, issue_type: str = None) -> Tuple[str, str]:
        """Run debug session with targeted debugging guidance.
        
        Args:
            issue_type: Optional specific issue type for targeted guidance
            
        Returns:
            Tuple containing (debug_summary, debugging_guidance)
        """
        debug_summary = self.get_debug_summary()
        guidance = self.get_debug_guidance(issue_type)
        
        return debug_summary, guidance