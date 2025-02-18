# Prompt Manager

A powerful AI-assisted workflow management system with advanced task tracking and debugging capabilities.

## Features

- **Memory Bank System**: Maintains perfect documentation and project context
- **Task Tracking**: Advanced task management and progress monitoring
- **Debugging Tools**: Comprehensive debugging and troubleshooting support
- **GitHub Integration**: Seamless integration with existing GitHub repositories
- **IDE Support**: VSCode integration for enhanced development workflow
- **bolt.new Integration**: AI-powered task generation for web applications

## Installation

You can install the latest release (v0.3.0) using pip:

```bash
pip install prompt-manager==0.3.0
```

Or download directly from GitHub releases:
```bash
# Clone the repository
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager

# Checkout the latest release
git checkout v0.3.0

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

- [Getting Started](docs/getting-started.md)
- [Memory Bank Guide](docs/ide-integrations/cline/cline-memorybank.md)
- [bolt.new Integration](docs/ide-integrations/cline/bolt-new-cline-memorybank.md)
- [API Reference](docs/api-reference.md)
- [Examples](docs/examples/)
  - [AI Book Writer Integration](docs/examples/ai-book-writer-integration.md)
  - [Cline Memory Bank Integration](docs/examples/cline-memory-bank-book-writer.md)

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

## Latest Release (v0.3.0)

### What's New
- **bolt.new Integration**: Generate structured development tasks for web applications
- **Enhanced Task Management**: Improved task tracking and organization
- **Memory Bank Updates**: Better context management for web development
- **New Documentation**: Comprehensive guide for bolt.new features

### Breaking Changes
None

### Bug Fixes
- Improved task persistence
- Enhanced test coverage
- Fixed CLI command handling

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
