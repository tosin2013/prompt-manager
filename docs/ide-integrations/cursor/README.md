# Cursor IDE Integration

This directory contains documentation and resources for integrating the CLI tool with Cursor IDE.

## Setup Instructions

### 1. Install Prerequisites

Since Prompt Manager is currently in development, you'll need to install it directly from the Git repository:

```bash
```bash
% python3 -m venv venv
% source venv/bin/activate
% pip install git+https://github.com/tosin2013/prompt-manager.git@main
# Verify installation
prompt-manager --version
```

#### Development Dependencies
Make sure you have the following installed:
- Python 3.8 or higher
- Git
- pip (Python package manager)
- virtualenv (recommended)

### 2. Cursor IDE Configuration

1. Open Cursor IDE
2. Press `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows/Linux) to open the command palette
3. Type "Settings" and select "Preferences: Open Settings (JSON)"
4. Add the following configuration to your settings:

```json
{
  "promptManager.enabled": true,
  "promptManager.memoryBankPath": "~/.prompt-manager/memories",
  "promptManager.autoComplete": true,
  "promptManager.shortcuts": {
    "openMemoryBank": "cmd+shift+m",
    "createMemory": "cmd+shift+n",
    "searchMemories": "cmd+shift+f"
  }
}
```

### 3. Install the Extension

1. Open Cursor IDE
2. Press `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows/Linux)
3. Type "Install Extension"
4. Search for "Prompt Manager"
5. Click "Install"
6. Restart Cursor IDE

### 4. Verify Installation

1. Press `Cmd + Shift + M` (Mac) or `Ctrl + Shift + M` (Windows/Linux) to open the memory bank
2. If the memory bank panel appears, the installation was successful

## Features

- Memory Bank Integration: Seamless access to your prompt memory bank directly from Cursor IDE
- Command Palette Integration: Quick access to CLI commands through Cursor's command palette
- Custom Keybindings: Configurable shortcuts for frequently used commands

## Usage

### Basic Commands

- `Cmd + Shift + M` (Mac) / `Ctrl + Shift + M` (Windows/Linux): Open memory bank
- `Cmd + Shift + N` (Mac) / `Ctrl + Shift + N` (Windows/Linux): Create new memory
- `Cmd + Shift + F` (Mac) / `Ctrl + Shift + F` (Windows/Linux): Search memories

### Quick Actions

1. **Create Memory**:
   - Select code or text
   - Right-click
   - Choose "Add to Memory Bank"

2. **Insert Memory**:
   - Place cursor where you want to insert
   - Press `Cmd + Shift + M` (Mac) / `Ctrl + Shift + M` (Windows/Linux)
   - Select memory to insert

3. **Search and Filter**:
   - Use tags in search: `#tag`
   - Filter by category: `category:`
   - Search by date: `date:`

## Directory Structure

- `memory-bank.md`: Documentation for memory bank integration and usage
- `keybindings.json`: Example keybinding configurations
- `settings.json`: Example settings for Cursor IDE integration

## Troubleshooting

### Common Issues

1. **Memory Bank Not Appearing**
   - Verify extension installation
   - Check if prompt-manager is running (`prompt-manager status`)
   - Restart Cursor IDE

2. **Keybindings Not Working**
   - Check for conflicts in Settings → Keyboard Shortcuts
   - Verify settings.json configuration
   - Try resetting keybindings to defaults

3. **Integration Not Working**
   - Ensure prompt-manager service is running
   - Check logs: `~/.prompt-manager/logs/cursor.log`
   - Verify permissions on memory bank directory

## Support

For issues and feature requests related to Cursor IDE integration:
1. Check the [GitHub Issues](https://github.com/yourusername/prompt-manager/issues)
2. Join our [Discord Community](https://discord.gg/promptmanager)
3. Submit a bug report through Cursor IDE (Help → Report Issue)

For detailed information about specific features, please refer to `memory-bank.md` in this directory.
