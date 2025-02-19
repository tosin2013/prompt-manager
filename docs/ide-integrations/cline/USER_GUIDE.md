# Cline Memory Bank User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Project Management](#project-management)
5. [Task Management](#task-management)
6. [Memory Bank Operations](#memory-bank-operations)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)

## Introduction

The Cline Memory Bank is a powerful tool that helps maintain perfect documentation and project context. This guide will walk you through setting up and using the Memory Bank effectively.

### Key Features
- Structured documentation management
- Task-aware context updates
- Automated progress tracking
- Token usage monitoring
- Interactive startup mode

## Installation

### Step 1: Install the Package

Choose one of these installation methods:

```bash
# Install from GitHub release (recommended)
pip install https://github.com/tosin2013/prompt-manager/releases/download/v0.3.0/prompt_manager-0.3.0.tar.gz

# Or install directly from the repository
pip install git+https://github.com/tosin2013/prompt-manager.git@v0.3.0
```

### Step 2: Verify Installation

```bash
prompt-manager --version
```

## Getting Started

### Step 1: Start Interactive Mode

The easiest way to get started is using interactive mode:

```bash
prompt-manager startup -i
```

### Step 2: Initialize Your Project

When prompted, choose option 1 and follow the prompts:
```
Enter command number: 1
Enter project path (or '.' for current directory): .
Enter project name: my-project
```

### Step 3: Configure Your Project (Optional)

Create a `prompt_manager.yaml` in your project root:

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

## Project Management

### Creating a New Project

#### Method 1: Interactive
1. Run `prompt-manager startup -i`
2. Choose option 1
3. Follow the prompts

#### Method 2: Command Line
```bash
prompt-manager init "my-project"
```

### Analyzing Existing Projects
```bash
prompt-manager analyze-repo /path/to/project
```

## Task Management

### Creating Tasks

#### Method 1: Basic Task
```bash
prompt-manager add-task "task-name" "Task description" "Prompt template"
```

#### Method 2: Web Development Task
```bash
prompt-manager generate-bolt-tasks "Create a blog with authentication"
```

### Managing Tasks

1. List tasks:
```bash
prompt-manager list-tasks
```

2. Update progress:
```bash
prompt-manager update-progress "task-name" "completed"
```

3. Execute task:
```bash
prompt-manager execute-task "task-name" "execution result"
```

### Task Organization

1. Filter tasks by status:
```bash
prompt-manager list-tasks --status IN_PROGRESS
```

2. Sort tasks:
```bash
prompt-manager list-tasks --sort-by priority
```

## Memory Bank Operations

### Context Management

1. Update product context:
```python
pm.memory_bank.update_context(
    "productContext.md",
    "Project Goals",
    """
    1. Implement feature X
    2. Optimize performance
    """,
    mode="append"
)
```

2. Monitor token usage:
```python
if pm.memory_bank.check_token_limit():
    pm.memory_bank.reset()
```

### Data Backup

1. Export tasks:
```bash
prompt-manager export-tasks backup.json
```

2. Import tasks:
```bash
prompt-manager import-tasks backup.json
```

## Advanced Features

### Interactive Development

1. Start interactive mode:
```bash
prompt-manager startup -i
```

2. Available commands:
- Initialize project
- Generate tasks
- List/filter tasks
- Import/export data
- Reset Memory Bank

### Bolt.new Integration

Create web development tasks with framework support:

```python
bolt_task = pm.add_task(
    BoltTask(
        name="ui-components",
        description="Create core UI components",
        framework="Next.js",
        dependencies=["react", "typescript"],
        ui_components=["Button", "Card"]
    )
)
```

## Troubleshooting

### Common Issues

1. Memory Bank Not Initializing
```bash
# Reset the Memory Bank
prompt-manager startup -i
# Choose option 6
```

2. Lost Task Data
```bash
# Restore from backup
prompt-manager import-tasks backup.json
```

3. Token Limit Reached
```python
# In your code
pm.memory_bank.reset()
pm.memory_bank.import_tasks("backup.json")
```

### Best Practices

1. Regular Updates
- Keep Memory Bank updated with decisions
- Document changes immediately
- Use clear, descriptive task names

2. Data Management
- Export tasks regularly
- Monitor token usage
- Use appropriate task priorities

3. Context Maintenance
- Update context after significant changes
- Document failures and debugging attempts
- Keep system patterns updated

### Getting Help

1. Check documentation:
```bash
prompt-manager --help
prompt-manager COMMAND --help
```

2. View debug logs:
```bash
prompt-manager --debug startup -i
```

3. Report issues:
Visit our [GitHub repository](https://github.com/tosin2013/prompt-manager) to report issues or contribute.
