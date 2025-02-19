# LLM Enhancement Guide

The LLM Enhancement module provides powerful capabilities for autonomous code improvement and pull request generation. This guide will walk you through its key features and best practices.

## Overview

The LLM Enhancement module uses machine learning to:
- Learn from your codebase patterns
- Suggest code improvements
- Generate and validate pull requests
- Analyze code impact
- Calculate test coverage
- Generate reviewer notes

## Key Components

### LLMEnhancement Class

The main class that provides all enhancement functionality:

```python
from prompt_manager import LLMEnhancement

llm = LLMEnhancement(memory_bank)
```

### PullRequestSuggestion Class

A data class that represents pull request suggestions:

```python
from prompt_manager import PullRequestSuggestion

suggestion = PullRequestSuggestion(
    title="Improve error handling",
    description="Add comprehensive error handling to core functions",
    branch_name="llm-enhancement/error-handling",
    changes=[...],
    impact_analysis={...},
    test_coverage={...},
    reviewer_notes=[...]
)
```

## Features

### 1. Learning Mode

Start an autonomous learning session to analyze your codebase:

```python
llm.start_learning_session()
```

The learning mode will:
- Record successful patterns
- Analyze code conventions
- Track command usage
- Build context understanding

### 2. Pattern Analysis

Analyze successful patterns in your codebase:

```python
patterns = llm.analyze_patterns()
for pattern in patterns:
    print(f"Found pattern: {pattern}")
```

### 3. Suggestion Generation

Generate code improvement suggestions:

```python
suggestions = llm.generate_suggestions()
for suggestion in suggestions:
    print(f"Suggestion: {suggestion}")
```

### 4. Pull Request Creation

Create and submit pull requests:

```python
# Create suggestion
pr = llm.suggest_pull_request(
    changes=[
        {"src/core.py": "updated_content"},
        {"tests/test_core.py": "new_tests"}
    ],
    title="Enhance core functionality",
    description="Improve performance and add tests"
)

# Submit if valid
if pr:
    success, message = llm.create_pull_request(pr)
    print(f"PR Status: {message}")
```

### 5. Custom Utilities

Generate custom utilities based on project needs:

```python
utilities = llm.generate_custom_utilities()
for utility in utilities:
    print(f"Generated utility:\n{utility}")
```

### 6. Command Pattern Analysis

Analyze and create custom commands:

```python
commands = llm.create_custom_commands()
for command in commands:
    print(f"Generated command:\n{command}")
```

## Best Practices

1. **Start with Learning**
   - Always start a learning session before making suggestions
   - Give the system time to understand your codebase

2. **Validate Changes**
   - Review suggested changes before applying
   - Check impact analysis and test coverage
   - Consider reviewer notes

3. **Sensitive Files**
   - The system automatically protects sensitive files
   - Never override these protections
   - Add custom patterns if needed

4. **Branch Management**
   - Use descriptive branch names
   - Clean up branches after merging
   - Follow your team's branching strategy

5. **Code Review**
   - Always review generated code
   - Check for maintainability
   - Verify test coverage
   - Consider performance implications

## Error Handling

The module includes comprehensive error handling:

```python
try:
    pr = llm.suggest_pull_request(changes, title, description)
    if pr:
        success, message = llm.create_pull_request(pr)
        if not success:
            print(f"Failed to create PR: {message}")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Integration Examples

### 1. Continuous Improvement Pipeline

```python
def improve_codebase():
    llm = LLMEnhancement(memory_bank)
    llm.start_learning_session()
    
    # Analyze and generate suggestions
    patterns = llm.analyze_patterns()
    suggestions = llm.generate_suggestions()
    
    # Create PRs for each suggestion
    for suggestion in suggestions:
        pr = llm.suggest_pull_request(
            changes=suggestion.get_changes(),
            title=f"Improvement: {suggestion.title}",
            description=suggestion.description
        )
        if pr:
            llm.create_pull_request(pr)
```

### 2. Custom Command Generation

```python
def create_project_commands():
    llm = LLMEnhancement(memory_bank)
    
    # Record common commands
    for command in common_commands:
        llm.record_command(command, success=True)
    
    # Generate custom commands
    return llm.create_custom_commands()
```

## Troubleshooting

1. **Invalid Changes**
   - Check file permissions
   - Verify file paths
   - Ensure changes follow project conventions

2. **Failed Pull Requests**
   - Check git configuration
   - Verify branch permissions
   - Review error messages

3. **Poor Suggestions**
   - Increase learning session duration
   - Add more context to memory bank
   - Review and update patterns

## Contributing

We welcome contributions to improve the LLM Enhancement module:

1. Fork the repository
2. Create your feature branch
3. Add tests for new features
4. Submit a pull request

## Support

For issues and questions:
- Check the [GitHub Issues](https://github.com/tosin2013/prompt-manager/issues)
- Join our [Discord Community](https://discord.gg/prompt-manager)
- Email support@prompt-manager.com
