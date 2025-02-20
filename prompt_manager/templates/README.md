# Custom Prompt Templates

This directory contains prompt templates that can be used with the Prompt Manager CLI commands.

## Directory Structure

```
templates/
  ├── default/           # Default templates shipped with the tool
  └── custom/            # Your custom templates
```

## Creating Custom Templates

1. Create a new YAML file in the `custom` directory
2. Follow this template structure:

```yaml
name: your-command-name
description: Brief description of what this prompt does
required_context:
  - context_variable_1
  - context_variable_2

template: |
  Your prompt template here.
  Use {variable_name} for context variables.
  
  The template can be multi-line and supports
  all markdown formatting.
```

## Example

Here's an example custom template for code review:

```yaml
name: review-code
description: Performs a detailed code review with security focus
required_context:
  - file_path
  - file_content
  - previous_reviews

template: |
  You are a senior code reviewer with security expertise.
  
  File: {file_path}
  Content:
  {file_content}
  
  Previous Reviews:
  {previous_reviews}
  
  Please review this code focusing on:
  1. Security vulnerabilities
  2. Best practices
  3. Performance considerations
  4. Code style
```

## Using Custom Templates

Custom templates will automatically be loaded and can be used with the corresponding CLI commands. If a custom template has the same name as a default template, the custom one will take precedence.

## Variables Available by Command

Different commands provide different context variables. Here are the available variables for each command:

### analyze-repo
- repo_path
- current_branch
- last_commit
- file_count
- main_languages
- previous_analysis

### suggest-improvements
- file_path
- file_content
- previous_suggestions
- max_suggestions

### create-pr
- title
- description
- changed_files
- commit_history
- previous_prs

### analyze-impact
- file_path
- changes
- dependencies
- previous_analysis

### generate-commands
- file_path
- file_content
- command_history
