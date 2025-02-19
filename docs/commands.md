# Prompt Manager CLI Commands

The Prompt Manager CLI provides a comprehensive set of commands for managing your development workflow. Here's a complete reference of all available commands.

## Basic Commands

### Initialize Project
```bash
prompt-manager init [--path PATH]
```
Initialize a new project in the specified directory (defaults to current directory).

### Analyze Repository
```bash
prompt-manager analyze-repo PATH
```
Analyze a repository to gather project context and setup the memory bank.

## Task Management

### Add Task
```bash
prompt-manager add-task NAME DESCRIPTION PROMPT [--priority PRIORITY]
```
Add a new task to the project.
- `NAME`: Name of the task
- `DESCRIPTION`: Description of what the task does
- `PROMPT`: Template for generating the task's output
- `--priority`: Task priority (default: 1)

### Update Progress
```bash
prompt-manager update-progress NAME STATUS
```
Update the status of a task.
- `NAME`: Name of the task
- `STATUS`: New status (pending/in_progress/completed/failed)

### List Tasks
```bash
prompt-manager list-tasks [--status STATUS] [--sort-by FIELD]
```
List all tasks with optional filtering and sorting.
- `--status`: Filter by status (pending/in_progress/completed/failed)
- `--sort-by`: Sort by field (priority/created/updated)

### Export Tasks
```bash
prompt-manager export-tasks --output PATH
```
Export tasks to a JSON file.
- `--output`: Path to the output file

## Bolt.new Integration

### Generate Bolt Tasks
```bash
prompt-manager generate-bolt-tasks PROJECT_DESCRIPTION [--framework FRAMEWORK]
```
Generate a sequence of development tasks for bolt.new projects.
- `PROJECT_DESCRIPTION`: Description of the project
- `--framework`: Target framework (default: Next.js)

## LLM Enhancement

### Start Learning Session
```bash
prompt-manager learn-session [--duration MINUTES]
```
Start an autonomous learning session to analyze code patterns.
- `--duration`: Duration in minutes (default: continuous)

### Generate Suggestions
```bash
prompt-manager suggest-improvements [--path PATH] [--max-suggestions NUM]
```
Generate code improvement suggestions.
- `--path`: Path to analyze (default: current directory)
- `--max-suggestions`: Maximum number of suggestions (default: 10)

### Create Pull Request
```bash
prompt-manager create-pr [--title TITLE] [--description DESC] [--changes FILE...]
```
Create a pull request from suggestions.
- `--title`: Pull request title
- `--description`: Pull request description
- `--changes`: Files to include in the pull request

### Analyze Impact
```bash
prompt-manager analyze-impact [--files FILE...]
```
Analyze the potential impact of changes.
- `--files`: Files to analyze

### Generate Custom Commands
```bash
prompt-manager generate-commands [--output PATH]
```
Generate custom CLI commands based on usage patterns.
- `--output`: Path to save generated commands

## Advanced Features

### Startup
```bash
prompt-manager startup [--interactive]
```
Start the prompt manager with optional interactive mode.
- `--interactive`: Start in interactive mode with a menu-driven interface

### Reflect
```bash
prompt-manager reflect
```
Analyze LLM's interaction patterns and effectiveness to improve future responses.

### Learn Mode
```bash
prompt-manager learn-mode
```
Enable autonomous learning mode for continuous improvement.

### Meta Program
```bash
prompt-manager meta-program
```
Allow the system to modify and improve its own tooling based on usage patterns.

## Environment Variables

The following environment variables can be used to configure the Prompt Manager:

- `PROMPT_MANAGER_PATH`: Default project path
- `PROMPT_MANAGER_CONFIG`: Path to custom configuration file
- `PROMPT_MANAGER_DEBUG`: Enable debug mode (set to "1" or "true")
- `PROMPT_MANAGER_LLM_MODE`: LLM Enhancement mode (learning/suggesting/auto)

## Examples

1. Initialize a new project:
```bash
prompt-manager init --path ./my-project
```

2. Add a new high-priority task:
```bash
prompt-manager add-task "Setup Auth" "Implement user authentication" "Create authentication system using {framework}" --priority 1
```

3. List all in-progress tasks sorted by priority:
```bash
prompt-manager list-tasks --status in_progress --sort-by priority
```

4. Generate tasks for a new Next.js project:
```bash
prompt-manager generate-bolt-tasks "Create a blog with user authentication" --framework Next.js
```

5. Export tasks to a file:
```bash
prompt-manager export-tasks --output tasks-backup.json
```

6. Start a learning session and create pull requests:
```bash
# Start learning session
prompt-manager learn-session --duration 30

# Generate and apply improvements
prompt-manager suggest-improvements --path ./src
prompt-manager create-pr --title "Code Improvements" --description "Enhance error handling" --changes src/core.py
```

7. Analyze impact of changes:
```bash
prompt-manager analyze-impact --files src/core.py tests/test_core.py
```

## Error Handling

The CLI will exit with a non-zero status code if an error occurs. Common error codes:
- `1`: General error
- `2`: Invalid arguments
- `3`: File system error
- `4`: Configuration error
- `5`: LLM Enhancement error

## Configuration

The Prompt Manager can be configured using a `prompt_manager.yaml` file in your project directory. Example configuration:

```yaml
output_dir: ./outputs
memory_path: ./prompt_manager_data
debug_mode: false
max_tokens: 2000000
llm_enhancement:
  learning_mode: auto
  max_suggestions: 10
  protected_paths:
    - config/
    - .env
    - secrets/
```

## Getting Help

For detailed information about any command, use the `--help` option:
```bash
prompt-manager --help
prompt-manager COMMAND --help
