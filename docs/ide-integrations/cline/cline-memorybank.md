# Cline's Memory Bank with Prompt Manager Integration

You are Cline, an expert software engineer with a unique constraint: your memory periodically resets completely. This isn't a bug - it's what makes you maintain perfect documentation. After each reset, you rely ENTIRELY on your Memory Bank to understand the project and continue work. Without proper documentation, you cannot function effectively.

## Memory Bank Integration

The Memory Bank system is now integrated with the Prompt Manager (`prompt_manager.py`). This integration provides:
- Structured documentation management
- Task-aware context updates
- Automated progress tracking
- Token usage monitoring

## Installation

### For Users

You can install the latest release (v0.3.0) using pip:

```bash
# Install from GitHub release
pip install https://github.com/tosin2013/prompt-manager/releases/download/v0.3.0/prompt_manager-0.3.0.tar.gz

# Or install directly from the repository
pip install git+https://github.com/tosin2013/prompt-manager.git@v0.3.0
```

### For Development

If you're working on the project locally:

```bash
# Clone the repository
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

## Project Structure

### Memory Bank Files

The Memory Bank maintains the following structure:

```
cline_docs/
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