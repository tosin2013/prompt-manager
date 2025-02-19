# Prompt Manager CLI Commands

## Basic Commands

### Version
```bash
prompt-manager --version
```
Shows the current version of Prompt Manager.

### Help
```bash
prompt-manager --help
```
Shows general help information and available commands.

## Project Management

### Initialize Project
```bash
prompt-manager init
```
Initialize a new Prompt Manager project in the current directory.

### Add Task
```bash
prompt-manager add-task [OPTIONS]
```
Add a new task to the project.

Options:
- `--title TEXT`: Task title [required]
- `--description TEXT`: Task description
- `--priority TEXT`: Task priority (low/medium/high)
- `--status TEXT`: Task status

### List Tasks
```bash
prompt-manager list-tasks
```
List all tasks in the current project.

### Update Progress
```bash
prompt-manager update-progress [OPTIONS]
```
Update task progress.

Options:
- `--task-id TEXT`: Task ID [required]
- `--status TEXT`: New status [required]
- `--notes TEXT`: Progress notes

### Export Tasks
```bash
prompt-manager export-tasks [OPTIONS]
```
Export tasks to a file.

Options:
- `--format TEXT`: Export format (json/yaml/markdown)
- `--output TEXT`: Output file path

## Repository Analysis

### Analyze Repository
```bash
prompt-manager analyze-repo [OPTIONS]
```
Analyze the current repository.

Options:
- `--depth INTEGER`: Analysis depth
- `--output TEXT`: Output file path

### Generate Bolt Tasks
```bash
prompt-manager generate-bolt-tasks [OPTIONS]
```
Generate tasks from Bolt specifications.

Options:
- `--framework TEXT`: Target framework
- `--output TEXT`: Output file path

## LLM Enhancement Commands

### Learn Session
```bash
prompt-manager llm learn-session [OPTIONS]
```
Start an autonomous learning session.

Options:
- `--duration INTEGER`: Duration in minutes (default: continuous)

### Analyze Impact
```bash
prompt-manager llm analyze-impact [OPTIONS]
```
Analyze the potential impact of changes.

Options:
- `--files PATH`: Files to analyze (can be specified multiple times)

### Suggest Improvements
```bash
prompt-manager llm suggest-improvements [OPTIONS]
```
Generate code improvement suggestions.

Options:
- `--max-suggestions INTEGER`: Maximum number of suggestions (default: 10)

### Create Pull Request
```bash
prompt-manager llm create-pr [OPTIONS]
```
Create a pull request from suggestions.

Options:
- `--title TEXT`: Pull request title [required]
- `--description TEXT`: Pull request description [required]
- `--changes PATH`: Files to include in PR (can be specified multiple times) [required]

### Generate Commands
```bash
prompt-manager llm generate-commands [OPTIONS]
```
Generate custom CLI commands based on usage patterns.

Options:
- `--output TEXT`: Output file for generated commands
