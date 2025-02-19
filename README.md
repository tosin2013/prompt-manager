# Prompt Manager

A powerful AI-assisted workflow management system with advanced task tracking and debugging capabilities.

## Features

- **Memory Bank System**: Maintains perfect documentation and project context
- **Task Tracking**: Advanced task management and progress monitoring
- **Debugging Tools**: Comprehensive debugging and troubleshooting support
- **GitHub Integration**: Seamless integration with existing GitHub repositories
- **IDE Support**: VSCode integration for enhanced development workflow
- **bolt.new Integration**: AI-powered task generation for web applications
- **LLM Enhancement**: Autonomous code improvement and pull request generation

## Installation

You can install the latest release (v0.3.16) using pip:

```bash
pip install tosins-prompt-manager==0.3.16
```

Or download directly from GitHub releases:
```bash
# Clone the repository
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager

# Checkout the latest release
git checkout v0.3.16

# Install in editable mode
pip install -e .
```

## Quick Start

### Basic Task Management
```python
from prompt_manager import PromptManager

# Initialize project
pm = PromptManager("your_project_name")

# Add a new task
task = pm.add_task(
    name="implement-feature",
    description="Add new feature X",
    details="Implementation requirements..."
)

# Track progress
pm.update_progress(
    task_name="implement-feature",
    status="in_progress",
    details="Completed initial implementation"
)
```

### Generate Web Development Tasks
```python
# Generate structured development tasks with bolt.new
tasks = pm.generate_bolt_tasks(
    project_name="My Web App",
    framework="Next.js"  # Optional, defaults to Next.js
)

# List generated tasks
for task in tasks:
    print(f"{task.name} - Priority: {task.priority}")
```

### Using LLM Enhancement
```python
from prompt_manager import LLMEnhancement

# Initialize LLM Enhancement
llm = LLMEnhancement(memory_bank)

# Start learning session
llm.start_learning_session()

# Generate code improvements
suggestions = llm.generate_suggestions()

# Create pull request
pr = llm.suggest_pull_request(
    changes=[{"path/to/file.py": "new content"}],
    title="Improve code structure",
    description="Enhance modularity and readability"
)

# Submit pull request
success, message = llm.create_pull_request(pr)
```

## Command Line Interface

The package provides a comprehensive CLI for managing your development workflow:

```bash
# Initialize a new project
prompt-manager init [PATH]

# Analyze a repository for project context
prompt-manager analyze-repo PATH

# Add a new task
prompt-manager add-task NAME DESCRIPTION PROMPT [--priority NUMBER]

# Update task progress
prompt-manager update-progress NAME STATUS

# List tasks with optional filtering and sorting
prompt-manager list-tasks [--status STATUS] [--sort-by FIELD]

# Export tasks to a file
prompt-manager export-tasks OUTPUT

# Generate bolt.new development tasks
prompt-manager generate-bolt-tasks PROJECT_DESCRIPTION FRAMEWORK

# Start interactive mode
prompt-manager startup --interactive

# Analyze LLM's interaction patterns
prompt-manager reflect

# Enable autonomous learning mode
prompt-manager learn-mode

# Allow LLM to modify its tooling
prompt-manager meta-program
```

Available task statuses:
- PENDING
- IN_PROGRESS
- COMPLETED
- BLOCKED
- FAILED

Sort fields for list-tasks:
- priority
- created
- updated

### Using the CLI
```bash
# Initialize a new project
prompt-manager init "my-web-app"

# Generate bolt.new tasks
prompt-manager generate-bolt-tasks "Create a blog with authentication" --framework Next.js

# List all tasks
prompt-manager list-tasks
```

## Documentation

For a complete reference of all available commands and their usage, see the [Command Documentation](docs/commands.md).

- [Getting Started](docs/getting-started.md)
- [Memory Bank Guide](docs/ide-integrations/cline/cline-memorybank.md)
- [bolt.new Integration](docs/ide-integrations/cline/bolt-new-cline-memorybank.md)
- [API Reference](docs/api-reference.md)
- [Examples](docs/examples/)
  - [AI Book Writer Integration](docs/examples/ai-book-writer-integration.md)
  - [Cline Memory Bank Integration](docs/examples/cline-memory-bank-book-writer.md)
  - [LLM Enhancement Guide](docs/examples/llm-enhancement-guide.md)

## Development

1. Clone the repository:
```bash
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest tests/
```

## Release Process

Releases are automated via GitHub Actions. To create a new release:

1. Update version in `setup.py`
2. Create and push a new tag:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

The GitHub Action will automatically:
- Run tests across Python versions
- Build the package
- Create a GitHub release
- Upload build artifacts

## Latest Release (v0.3.16)

### What's New
- Added comprehensive CLI command documentation
- Updated Python version support (3.9-3.13)
- Package renamed to tosins-prompt-manager
- **LLM Enhancement**: Autonomous code improvement and pull request generation
- **bolt.new Integration**: Generate structured development tasks for web applications
- **Enhanced Task Management**: Improved task tracking and organization
- **Memory Bank Updates**: Better context management for web development

### Breaking Changes
None

### Bug Fixes
- Improved task persistence
- Enhanced test coverage
- Fixed CLI command handling
- Improved error handling in LLM Enhancement

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Cline](docs/ide-integrations/cline/README.md) integration
- Inspired by AI-assisted development workflows
- Powered by bolt.new for web development task generation
- Enhanced by LLM-driven code improvements
