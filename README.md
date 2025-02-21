# Prompt Manager

A development workflow management system with memory tracking and LLM enhancement capabilities.

## Features

- Task management with memory persistence
- LLM-powered code analysis and improvement
- Debug assistance with error tracing
- Repository analysis and learning
- Self-improvement capabilities
- Transparent prompt inspection with `--show-prompt`

## Installation
### Recommened currently still in development 
```
% python3 -m venv venv
% source venv/bin/activate
% pip install git+https://github.com/tosin2013/prompt-manager.git@main
```

### Using pip
```bash
pip install tosins-prompt-manager
```

## Quick Start

```bash
# Initialize a new project
prompt-manager init my-project

# Add a task (with prompt display)
prompt-manager base add-task "Setup CI/CD" "Configure GitHub Actions" --show-prompt

# Update task progress (with prompt display)
prompt-manager base update-progress "Setup CI/CD" "in_progress" --show-prompt

# List tasks (with prompt display)
prompt-manager base list-tasks --show-prompt
```

## Command Groups

### Base Commands
```bash
# Task Management
prompt-manager base add-task "Task Name" "Description"
prompt-manager base update-progress "Task Name" "in_progress"
prompt-manager base list-tasks
prompt-manager base export-tasks --output tasks.json

# Add --show-prompt to any command to see the prompt template:
prompt-manager base add-task "Task Name" "Description" --show-prompt
```

### Debug Commands
```bash
# Debugging
prompt-manager debug analyze-file path/to/file.py
prompt-manager debug find-root-cause error.log
prompt-manager debug test-roadmap path/to/file.py

# Add --show-prompt to see analysis prompts:
prompt-manager debug analyze-file path/to/file.py --show-prompt
```

### LLM Commands
```bash
# LLM Enhancement
prompt-manager llm analyze-impact file.py
prompt-manager llm suggest-improvements file.py
prompt-manager llm create-pr "Title" "Description"

# Add --show-prompt to inspect LLM prompts:
prompt-manager llm analyze-impact file.py --show-prompt
```

### Memory Commands
```bash
# Memory Operations
prompt-manager memory store key value
prompt-manager memory retrieve key
prompt-manager memory list-all

# Add --show-prompt to see memory operation prompts:
prompt-manager memory store key value --show-prompt
```

## Understanding Prompts

The `--show-prompt` flag is available on all commands and shows the prompt template being used. This is useful for:

1. **Debugging**: Understand how commands interpret your input
2. **Learning**: See how the system structures tasks and analysis
3. **Validation**: Verify prompt templates are correct
4. **Training**: Help new users understand the system

Example output with `--show-prompt`:
```bash
$ prompt-manager base add-task "New Feature" "Add authentication" --show-prompt

================================================================================
Using prompt template: add-task
================================================================================
Task Analysis Request
====================

New Task:
- Title: New Feature
- Description: Add authentication
...
================================================================================
```

## Documentation

For detailed documentation, see:
- [Memory Bank Integration](docs/ide-integrations/cline/cline-memorybank.md)
- [Bolt.new Integration](docs/ide-integrations/cline/bolt-new-cline-memorybank.md)
- [IDE Integration Guide](docs/ide-integrations/README.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
