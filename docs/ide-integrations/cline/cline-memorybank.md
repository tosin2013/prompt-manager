# Cline's Memory Bank with Prompt Manager Integration

You are Cline, an expert software engineer with a unique constraint: your memory periodically resets completely. This isn't a bug - it's what makes you maintain perfect documentation. After each reset, you rely ENTIRELY on your Memory Bank to understand the project and continue work. Without proper documentation, you cannot function effectively.

## Memory Bank Integration

The Memory Bank system is now integrated with the Prompt Manager (`prompt_manager.py`). This integration provides:
- Structured documentation management
- Task-aware context updates
- Automated progress tracking
- Token usage monitoring
- Transparent prompt display and validation

### Prompt Display and Validation

All commands now support the `--show-prompt` flag, which displays the prompt template being used for the command. This feature is invaluable for:
- Understanding how commands interpret context
- Validating prompt templates
- Debugging command behavior
- Training new users

Example usage:
```bash
# Show prompt for adding a task
prompt-manager base add-task "New Task" "Description" --show-prompt

# Output will include:
================================================================================
Using prompt template: add-task
================================================================================
Task Analysis Request
...
================================================================================

# Show prompt for updating progress
prompt-manager base update-progress "Task Name" "in_progress" --show-prompt

# Show prompt for memory operations
prompt-manager memory store "key" "value" --show-prompt
```

### Version Compatibility

This documentation is for version 0.3.18 of tosins-prompt-manager, which supports:
- Python versions 3.9 through 3.13
- Full CLI command set with memory bank integration
- Enhanced task management and tracking
- Automated documentation updates
- LLM Enhancement features for code improvement
- Transparent prompt display with `--show-prompt` flag

## Installation

### For Users

```bash
# Install latest development version from GitHub main branch
pip install git+https://github.com/tosin2013/prompt-manager.git@main

# Or install specific version from PyPI (when released)
pip install tosins-prompt-manager==0.3.18
```

### For Development

```bash
# Clone the repository
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager

# Install in editable mode with development dependencies
pip install -e .[dev]
```

## Project Structure

### Memory Bank Files

The Memory Bank maintains the following structure:

```
memory/
├── productContext.md   # Project goals and requirements
├── activeContext.md    # Current development state
├── systemPatterns.md   # Architectural patterns and decisions
├── techContext.md      # Technical specifications
└── progress.md         # Task progress tracking
```

### Project Initialization

Initialize a new project with Memory Bank:

```python
from prompt_manager import PromptManager

# Initialize with default path (./cline_docs)
pm = PromptManager("project_name")

# Or specify a custom path and config
pm = PromptManager(
    "project_name",
    memory_path="/path/to/docs",
    config={
        "auto_start_tasks": False,  # Prevent tasks from starting automatically
        "memory_path": "/path/to/docs"  # Alternative way to specify memory path
    }
)
```

## Task Management

### Creating Tasks

```python
# Create a basic task
task = pm.add_task(
    name="implement-feature",
    description="Implement new feature X",
    prompt_template="Implementation steps:\n1. ...",
    priority=1  # Optional, defaults to 1
)

# Create a bolt.new web development task
bolt_task = pm.add_task(
    BoltTask(
        name="ui-components",
        description="Create core UI components",
        prompt_template="Development steps:\n1. ...",
        framework="Next.js",
        dependencies=["react", "typescript"],
        ui_components=["Button", "Card"],
        api_endpoints=[{
            "method": "GET",
            "path": "/api/data",
            "description": "Fetch data"
        }]
    )
)
```

### Managing Task Status

```python
# Update task status
pm.update_task_status(
    name="implement-feature",
    status="IN_PROGRESS",  # Can use string or TaskStatus enum
    notes="Started implementation"  # Optional notes
)

# Get task details
task = pm.get_task("implement-feature")
print(f"Status: {task.status}")

# List tasks with filtering
tasks = pm.list_tasks(
    status=TaskStatus.IN_PROGRESS,  # Optional filter
    sort_by="priority"  # Optional sorting
)
```

### Task Persistence

```python
# Tasks are automatically saved after modifications
# But you can manually save/load:
pm.save_tasks()
pm.load_tasks()

# Export tasks to JSON
pm.export_tasks("tasks.json")

# Import tasks from JSON
pm.import_tasks("tasks.json")
```

## Memory Bank Operations

### Context Management

```python
# Update product context
pm.memory_bank.update_context(
    "productContext.md",
    "Project Goals",
    """
    1. Implement feature X
    2. Optimize performance
    """,
    mode="append"  # or "replace" to overwrite
)

# Update technical context
pm.memory_bank.update_context(
    "techContext.md",
    "Architecture",
    """
    - Next.js frontend
    - Python backend
    - PostgreSQL database
    """
)

# Update active context
pm.memory_bank.update_context(
    "activeContext.md",
    "Current Sprint",
    """
    Working on:
    - UI components
    - API integration
    """
)
```

### Token Management

```python
# Check token limit
if pm.memory_bank.check_token_limit():
    # Handle memory reset if needed
    pm.memory_bank.reset()

# Manually track tokens
pm.memory_bank.increment_tokens(100)
pm.memory_bank.decrement_tokens(50)
```

## Command Line Interface

The Memory Bank can be managed via CLI. Here are all the available commands:

### Project Setup

```bash
# Initialize a new project
prompt-manager init "my-project"

# Initialize in a specific directory
prompt-manager init --path /path/to/project

# Analyze an existing repository
prompt-manager analyze-repo /path/to/repo
```

### Task Management

```bash
# Add a new task
prompt-manager add-task "task-name" "Task description" "Prompt template" --priority 1

# Generate bolt.new web development tasks
prompt-manager generate-bolt-tasks "Create a blog with authentication" --framework Next.js

# List all tasks
prompt-manager list-tasks

# List tasks with filtering
prompt-manager list-tasks --status IN_PROGRESS
prompt-manager list-tasks --sort-by priority

# Update task progress
prompt-manager update-progress "task-name" "completed"

# Execute a task
prompt-manager execute-task "task-name" "execution result"
```

### Data Management

```bash
# Export tasks to JSON
prompt-manager export-tasks tasks.json

# Import tasks from JSON
prompt-manager import-tasks tasks.json

# Update Memory Bank
prompt-manager update-memory

# Reset Memory Bank
prompt-manager reset-memory
```

### Configuration

You can create a `prompt_manager.yaml` in your project root to set default configurations:

```yaml
project:
  name: "my-project"
  memory_path: "./docs/memory"
  auto_start_tasks: false

tasks:
  default_priority: 1
  auto_save: true

memory_bank:
  token_limit: 2000000
  backup_enabled: true
  backup_path: "./backups"
```

## Interactive Startup

You can start the Prompt Manager in interactive mode, which will guide you through available commands:

```bash
# Start in interactive mode
prompt-manager startup -i
```

This will present a menu of options:
1. Initialize new project
2. Generate bolt.new tasks
3. List existing tasks
4. Add new task
5. Import tasks from file
6. Reset Memory Bank
0. Exit

The interactive mode will prompt you for any required information for each command, making it easier to get started without remembering all the command-line arguments.

Example interactive session:
```
$ prompt-manager startup -i
Welcome to Prompt Manager! Let's get started.

Available commands:
1. Initialize new project
2. Generate bolt.new tasks
3. List existing tasks
4. Add new task
5. Import tasks from file
6. Reset Memory Bank
0. Exit

Enter command number: 1
Enter project path (or '.' for current directory): .
Enter project name: my-web-app
Project my-web-app initialized at .

Enter command number: 2
Enter project description: Create a blog with user authentication
Enter framework (default: Next.js): Next.js
Generated 5 development tasks...
```

## Debugging Support

### Task Execution and Error Handling

```python
try:
    # Execute a task
    pm.execute_task("implement-feature", "Implementation completed successfully")
except Exception as e:
    # Error handling is automatic, but you can manually trigger:
    pm._handle_task_failure(task, str(e))
```

### Progressive Debugging

The system uses a layered debugging approach:

1. Environment Layer
```python
pm._debug_environment_layer(task, error_message)
```

2. Code Logic Layer
```python
pm._debug_code_logic_layer(task, error_message)
```

3. Root Cause Analysis
```python
pm._perform_rca(task)
```

## Best Practices

1. **Regular Updates**: Keep the Memory Bank updated with all decisions and changes
2. **Clear Context**: Provide detailed context in each update
3. **Token Management**: Monitor token usage to prevent memory overflow
4. **Task Organization**: Use priorities and clear descriptions
5. **Error Documentation**: Document all errors and their resolutions
6. **System Patterns**: Keep system patterns updated with architectural decisions

## Error Recovery

If the Memory Bank becomes corrupted or needs a reset:

1. Backup current state:
```python
pm.export_tasks("backup_tasks.json")
```

2. Reset Memory Bank:
```python
pm.memory_bank.reset()
```

3. Restore from backup:
```python
pm.import_tasks("backup_tasks.json")
```

Always verify the Memory Bank is active before proceeding with any development task:
```python
if pm.memory_bank.is_active:
    print("Memory Bank is ready")
else:
    print("Memory Bank needs initialization")
```

## Command Line Interface Memory Bank

The Command Line Interface (CLI) Memory Bank is a powerful tool that helps maintain context and preferences across coding sessions.

## LLM Enhancement Features

### Code Analysis and Improvement

```python
from prompt_manager import PromptManager, LLMEnhancement

# Initialize LLM Enhancement
pm = PromptManager("project_name")
llm = pm.llm

# Start a learning session
llm.start_learning_session()

# Analyze code impact
impact = llm.analyze_impact(["path/to/file.py"])
print(f"Impact Analysis: {impact}")

# Get code improvement suggestions
suggestions = llm.suggest_improvements(max_suggestions=5)
for suggestion in suggestions:
    print(f"Suggestion: {suggestion['description']}")

# Create and submit pull request
pr = llm.suggest_pull_request(
    changes=[{"file.py": "updated content"}],
    title="Code Improvements",
    description="Enhance code quality"
)
success, message = llm.create_pull_request(pr)
```

### Command Line Interface for LLM Features

```bash
# Analyze code impact
prompt-manager llm analyze-impact path/to/file.py

# Start learning session
prompt-manager llm learn-session

# Get improvement suggestions
prompt-manager llm suggest-improvements path/to/file.py --max-suggestions 5

# Create pull request
prompt-manager llm create-pr "Title" "Description"

# Generate custom commands
prompt-manager llm generate-commands path/to/file.py

# Self-improvement commands
prompt-manager improve enhance path/to/file.py --type tests
prompt-manager improve enhance . --type commands
prompt-manager improve enhance plugins --type plugins
```

### Memory Bank Integration with LLM

The Memory Bank now tracks:
- Code analysis results
- Learning session insights
- Improvement suggestions
- Pull request history
- Generated commands

```python
# Access LLM-related memory
context = pm.memory_bank.load_context_memory()
command_history = context.get("commandHistory", [])
learning_sessions = context.get("learningSessions", [])

# Save LLM analysis results
pm.memory_bank.save_context_memory({
    "codeAnalysis": impact,
    "suggestions": suggestions,
    "pullRequests": pr_history
})
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Self-Improvement and Code Modification

The Memory Bank system is designed to be self-improving. It can:
1. Analyze its own code and prompt templates
2. Suggest and implement improvements
3. Create pull requests back to the main repository

### Code and Template Modification

```python
from prompt_manager import PromptManager

# Initialize with self-improvement capabilities
pm = PromptManager("project_name", enable_self_improvement=True)

# Analyze and improve prompt templates
improvements = pm.llm.analyze_templates()
for improvement in improvements:
    # Apply template improvements
    pm.llm.improve_template(
        template_name=improvement["template"],
        changes=improvement["changes"]
    )

# Analyze and improve code
code_improvements = pm.llm.analyze_code_quality(
    target="prompt_manager/",
    focus=["performance", "maintainability"]
)

# Create pull request with improvements
pr = pm.llm.create_improvement_pr(
    title="Enhancement: Improved prompt templates and code quality",
    description="Automated improvements to templates and core functionality",
    changes={
        "templates": improvements,
        "code": code_improvements
    },
    target_repo="tosin2013/prompt-manager",
    target_branch="main"
)
```

### Command Line Interface for Self-Improvement

```bash
# Analyze and improve prompt templates
prompt-manager improve templates

# Analyze and improve code
prompt-manager improve code --focus performance

# Create improvement PR
prompt-manager improve create-pr --target-repo tosin2013/prompt-manager

# Enhance specific components
prompt-manager improve enhance prompt_manager/templates/ --type templates
prompt-manager improve enhance prompt_manager/core/ --type code
```

### Memory Bank Integration for Improvements

The Memory Bank tracks all improvements and their impacts:

```python
# Track improvement history
pm.memory_bank.update_context(
    "systemPatterns.md",
    "Self-Improvement History",
    {
        "template_improvements": template_history,
        "code_improvements": code_history,
        "impact_analysis": improvement_impact
    }
)

# Track successful patterns
pm.memory_bank.update_context(
    "techContext.md",
    "Improvement Patterns",
    {
        "successful_patterns": successful_improvements,
        "failed_attempts": failed_improvements,
        "lessons_learned": improvement_lessons
    }
)
```

### Automated Pull Request Creation

The system can automatically create pull requests to the main repository:

```python
# Configure GitHub credentials
pm.configure_github(
    token=os.getenv("GITHUB_TOKEN"),
    username="your-username"
)

# Create and submit improvements
improvements = pm.llm.suggest_improvements()
if improvements:
    pr = pm.llm.create_pull_request(
        title="Enhancement: Automated improvements",
        description="""
        This PR contains automated improvements:
        - Template optimizations
        - Code quality enhancements
        - Documentation updates
        """,
        changes=improvements,
        base_repo="tosin2013/prompt-manager",
        base_branch="main"
    )
    
    # Track PR in memory bank
    pm.memory_bank.track_pull_request(pr)
```

### Best Practices for Code Modification

1. **Review Before Submit**: Always review suggested changes before creating PRs
2. **Test Coverage**: Ensure changes include appropriate test coverage
3. **Documentation**: Update documentation to reflect changes
4. **Impact Analysis**: Include impact analysis in PR descriptions
5. **Gradual Changes**: Prefer smaller, focused improvements over large changes

### Learning Session Prompts

When running a learning session, you can view the prompts being used:

```bash
# Start learning session for current directory and display prompt
prompt-manager repo learn-session . --show-prompt

# Start learning session for specific path
prompt-manager repo learn-session path/to/directory --show-prompt

# Start learning session with custom duration
prompt-manager repo learn-session . --duration 60 --show-prompt

# Example output:
================================================================================
Using prompt template: learn-session
================================================================================
Repository Learning Analysis Request
==================================

Repository: {repo_path}
Current Branch: {current_branch}
File Count: {file_count}
Main Languages: {main_languages}

Previous Analysis:
{previous_analysis}

Please analyze this repository focusing on:

1. Code Patterns
   - Architecture patterns
   - Design patterns
   - Common idioms
   - Best practices

2. Development Workflow
   - Commit patterns
   - Branch strategy
   - Testing approach
   - Documentation style

3. Technical Stack
   - Framework usage
   - Dependencies
   - Tools and utilities
   - Integration patterns

4. Areas for Improvement
   - Code quality
   - Test coverage
   - Documentation
   - Performance

Please provide specific, actionable insights that can be used to:
- Improve code quality
- Enhance development workflow
- Optimize performance
- Strengthen testing
================================================================================
```

The prompt can be customized by creating a custom template in your project:

```python
# Create custom learning session prompt
pm.memory_bank.update_context(
    "prompts.md",
    "Learning Session",
    """
    Custom learning session prompt template:
    {your_custom_template}
    """
)

# Use custom prompt in session
pm.llm.start_learning_session(use_custom_prompt=True)
```

You can also access the prompt programmatically:

```python
# Get current learning session prompt
prompt = pm.llm.get_session_prompt()
print(prompt)

# Get prompt with specific context
prompt = pm.llm.get_session_prompt(
    context={
        "focus_areas": ["testing", "documentation"],
        "analysis_depth": "detailed"
    }
)
print(prompt)
```