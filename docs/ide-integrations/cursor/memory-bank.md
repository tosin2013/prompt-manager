# Memory Bank Integration for Cursor IDE

This guide explains how to use the Memory Bank feature with Cursor IDE, allowing you to manage and access your prompts directly from your editor.

## Setup

1. Install the CLI tool:
```bash
pip install prompt-manager
```

2. Configure Cursor settings:
   - Open Cursor Settings (⌘,)
   - Add the following to your `settings.json`:
```json
{
  "promptManager.enabled": true,
  "promptManager.memoryBankPath": "~/.prompt-manager/memories",
  "promptManager.autoComplete": true
}
```

## Features

### 1. Quick Access to Memories
- Use `Cmd+Shift+M` (Mac) to open the memory bank panel
- Search through your memories with fuzzy finding
- Insert memories directly into your code or comments

### 2. Memory Management
- Create new memories directly from Cursor
- Tag and categorize memories for better organization
- Edit and update existing memories
- Delete outdated memories

### 3. Context-Aware Suggestions
- Automatic memory suggestions based on your current file
- Smart completion for code snippets
- Integration with Cursor's AI features

## Commands

| Command | Keybinding | Description |
|---------|------------|-------------|
| Memory Bank: Open | `Cmd+Shift+M` | Open memory bank panel |
| Memory Bank: Create | `Cmd+Shift+N` | Create new memory |
| Memory Bank: Search | `Cmd+Shift+F` | Search memories |
| Memory Bank: Insert | `Cmd+Shift+I` | Insert selected memory |

## Usage Examples

### Creating a New Memory
1. Press `Cmd+Shift+N` to open the new memory dialog
2. Enter your memory content
3. Add relevant tags
4. Save the memory

### Searching Memories
1. Press `Cmd+Shift+F` to open the search dialog
2. Type your search query
3. Use arrow keys to navigate results
4. Press Enter to insert the selected memory

### Managing Memories
1. Open the memory bank panel
2. Right-click on any memory to:
   - Edit
   - Delete
   - Copy
   - Share

## Development Setup

Since Prompt Manager is in active development, here are additional setup steps for developers:

### Installing from Source

1. **Clone the Repository**
```bash
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager
```

2. **Set Up Development Environment**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt  # Includes testing and development tools
pip install -e .  # Install in editable mode
```

3. **Configure Development Settings**
```bash
# Create local config for development
mkdir -p ~/.prompt-manager/config
cp config/development.yaml ~/.prompt-manager/config/config.yaml

# Set up development environment variables
export PROMPT_MANAGER_ENV=development
export PROMPT_MANAGER_CONFIG=~/.prompt-manager/config/config.yaml
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_memory_bank.py

# Run with coverage
pytest --cov=prompt_manager tests/
```

### Development Workflow

1. **Create a New Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make Changes and Test**
```bash
# Run linting
flake8 prompt_manager

# Run type checking
mypy prompt_manager

# Run tests
pytest
```

3. **Submit Pull Request**
- Ensure all tests pass
- Update documentation if needed
- Follow the contribution guidelines

### Debugging Tips

1. **Enable Debug Logging**
```bash
export PROMPT_MANAGER_LOG_LEVEL=DEBUG
```

2. **View Logs**
```bash
tail -f ~/.prompt-manager/logs/development.log
```

3. **Use the Development Console**
```bash
prompt-manager console --debug
```

## Best Practices

1. **Consistent Tagging**: Use consistent tags to organize your memories effectively
2. **Regular Cleanup**: Periodically review and clean up outdated memories
3. **Contextual Organization**: Group related memories using similar tags
4. **Version Tracking**: Include version information in memories when relevant

## Troubleshooting

### Common Issues

1. **Memory Bank Not Loading**
   - Verify CLI tool installation
   - Check memory bank path in settings
   - Ensure proper permissions

2. **Keybindings Not Working**
   - Check for keybinding conflicts
   - Verify Cursor settings
   - Restart Cursor IDE

3. **Search Not Finding Results**
   - Verify index is up to date
   - Check search syntax
   - Ensure memories are properly tagged

## Support

For additional support:
- Check the [GitHub repository](https://github.com/yourusername/prompt-manager)
- Submit issues for bugs or feature requests
- Join the community discussion
