"""
LLM guidance module for providing context and instructions to LLMs about command usage.
"""
from typing import Dict, Optional

class LLMGuidance:
    """Provides guidance and context to LLMs about command usage."""
    
    @staticmethod
    def get_command_guidance(command: str) -> Dict[str, str]:
        """Get guidance for a specific command.
        
        Args:
            command: The command name to get guidance for
            
        Returns:
            Dictionary containing:
                - purpose: What the command is used for
                - context: When to use this command
                - example_scenario: A concrete example of when and how to use it
                - expected_outcome: What the LLM should expect after running it
                - next_steps: What the LLM should consider doing after running it
        """
        guidance_map = {
            "init": {
                "purpose": "Initialize a new project with prompt manager configuration",
                "context": "Use this when starting a new project or integrating prompt manager into an existing one",
                "example_scenario": "When a user asks to set up prompt manager for their project",
                "expected_outcome": "A new prompt manager configuration will be created in the specified directory",
                "next_steps": "Consider analyzing the repository or adding initial tasks"
            },
            "analyze_repo": {
                "purpose": "Analyze a repository to understand its structure and context",
                "context": "Use this after initialization or when needing to update project understanding",
                "example_scenario": "When a user wants to integrate prompt manager with an existing codebase",
                "expected_outcome": "Project structure and context will be stored in the memory bank",
                "next_steps": "Review the analysis results and consider creating relevant tasks"
            },
            "add_task": {
                "purpose": "Create a new task with associated prompt and metadata",
                "context": "Use this when the user wants to track a new development task or feature",
                "example_scenario": "When a user requests to implement a new feature or fix a bug",
                "expected_outcome": "A new task will be created and tracked in the system",
                "next_steps": "Consider updating task status as work progresses"
            },
            "update_progress": {
                "purpose": "Update the status of an existing task",
                "context": "Use this when task state changes (e.g., starts, completes, gets blocked)",
                "example_scenario": "When code changes are committed or a feature is completed",
                "expected_outcome": "Task status will be updated and progress tracked",
                "next_steps": "Consider updating related tasks or starting new ones"
            },
            "list_tasks": {
                "purpose": "Display all tasks with optional filtering and sorting",
                "context": "Use this to check project progress or find specific tasks",
                "example_scenario": "When reviewing project status or finding blocked tasks",
                "expected_outcome": "List of tasks matching the specified criteria",
                "next_steps": "Consider updating task statuses or adding new tasks"
            },
            "export_tasks": {
                "purpose": "Export tasks to various formats for external use",
                "context": "Use this when needing to share task information outside the system",
                "example_scenario": "When generating reports or sharing progress with stakeholders",
                "expected_outcome": "Tasks exported to the specified format",
                "next_steps": "Consider how to use the exported data effectively"
            },
            "generate_bolt_tasks": {
                "purpose": "Generate structured development tasks for web applications",
                "context": "Use this when planning web development work with bolt.new integration",
                "example_scenario": "When starting a new web project or feature",
                "expected_outcome": "A sequence of well-defined development tasks",
                "next_steps": "Review and customize generated tasks as needed"
            },
            "startup": {
                "purpose": "Start the prompt manager with optional interactive mode",
                "context": "Use this for ongoing development sessions",
                "example_scenario": "When beginning a new development session",
                "expected_outcome": "Prompt manager ready for interactive use",
                "next_steps": "Begin adding or updating tasks"
            },
            "reflect": {
                "purpose": "Analyze LLM's interaction patterns and effectiveness",
                "context": "Use this to improve LLM performance and understanding",
                "example_scenario": "When wanting to optimize LLM interactions",
                "expected_outcome": "Analysis of LLM performance patterns",
                "next_steps": "Apply insights to improve future interactions"
            },
            "learn_mode": {
                "purpose": "Enable autonomous learning mode for the LLM",
                "context": "Use this to improve LLM's understanding over time",
                "example_scenario": "When wanting the LLM to learn from interactions",
                "expected_outcome": "LLM will start learning from interactions",
                "next_steps": "Monitor learning progress and adjust as needed"
            },
            "meta_program": {
                "purpose": "Allow LLM to modify its own tooling",
                "context": "Use this for advanced LLM self-improvement",
                "example_scenario": "When the LLM needs to adapt its capabilities",
                "expected_outcome": "LLM can modify its own tools and behaviors",
                "next_steps": "Review and validate any self-modifications"
            }
        }
        
        return guidance_map.get(command, {
            "purpose": "Unknown command",
            "context": "Command not recognized",
            "example_scenario": "N/A",
            "expected_outcome": "N/A",
            "next_steps": "Check command name and documentation"
        })

    @staticmethod
    def format_guidance(guidance: Dict[str, str]) -> str:
        """Format guidance into a clear message for the LLM.
        
        Args:
            guidance: The guidance dictionary to format
            
        Returns:
            Formatted guidance string
        """
        return f"""
Command Guidance:
----------------
Purpose: {guidance['purpose']}
When to Use: {guidance['context']}
Example Scenario: {guidance['example_scenario']}
Expected Outcome: {guidance['expected_outcome']}
Next Steps: {guidance['next_steps']}
"""
