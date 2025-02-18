# Prompt Manager

A powerful AI-assisted workflow management system with advanced task tracking and debugging capabilities.

## Features

- **Memory Bank System**: Maintains perfect documentation and project context
- **Task Tracking**: Advanced task management and progress monitoring
- **Debugging Tools**: Comprehensive debugging and troubleshooting support
- **GitHub Integration**: Seamless integration with existing GitHub repositories
- **IDE Support**: VSCode integration for enhanced development workflow

## Installation

```bash
pip install prompt-manager
```

## Quick Start

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

## Documentation

- [Getting Started](docs/getting-started.md)
- [Memory Bank Guide](docs/ide-integrations/cline/cline-memorybank.md)
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
- Special thanks to the Codeium engineering team
