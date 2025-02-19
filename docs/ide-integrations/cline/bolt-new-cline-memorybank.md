# Bolt.new Integration with Cline's Memory Bank

The Memory Bank system now integrates with bolt.new through the Prompt Manager, enabling AI-powered task generation for web application development. This integration leverages the Memory Bank's context awareness to create detailed, contextually relevant development tasks.

## Installation

### For Users

You can install the latest release (v0.3.0) using pip:

```bash
# Install from GitHub release
pip install https://github.com/tosin2013/prompt-manager/releases/download/v0.3.0/prompt_manager-0.3.0.tar.gz

# Or install directly from the repository
pip install git+https://github.com/tosin2013/prompt-manager.git@v0.3.0
```

### For Development

If you're working on the project locally:

```bash
# Clone the repository
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

## Core Features

- Structured task generation for web applications
- Framework-specific task templates
- Automatic task prioritization
- Detailed technical specifications
- Memory-aware development context

## Task Generation Workflow

### 1. Initialize Project

```python
from prompt_manager import PromptManager

# Create new project with bolt.new integration
pm = PromptManager("web_project")
```

### 2. Generate Development Tasks

```python
# Generate structured bolt.new tasks
tasks = pm.generate_bolt_tasks(
    project_name="My Web App",
    framework="Next.js"  # Optional, defaults to Next.js
)

# Tasks are automatically added to Memory Bank
```

Generated tasks follow this sequence:
1. Initial Project Setup
2. UI Component Development
3. API Integration
4. Testing Implementation
5. Deployment Setup

### 3. Task Structure

Each bolt.new task includes:

```python
bolt_task = BoltTask(
    name="UI Component Development",
    description="Create core UI components",
    framework="Next.js",
    dependencies=["react", "typescript", "tailwindcss"],
    ui_components=["Layout", "Navigation", "Card"],
    api_endpoints=[
        {
            "method": "GET",
            "path": "/api/data",
            "description": "Fetch data"
        }
    ]
)
```

### 4. Memory Bank Integration

The Memory Bank automatically tracks:
- Technical stack decisions
- Component dependencies
- API specifications
- Development progress

```python
# Update technical context with bolt.new specifications
pm.memory_bank.update_context(
    "techContext.md",
    "Framework Configuration",
    """
    Framework: Next.js
    Key Dependencies:
    - TypeScript
    - TailwindCSS
    - React Query
    """
)
```

## Command Line Interface

Generate tasks using the CLI:

```bash
# Generate bolt.new tasks
prompt-manager generate-bolt-tasks "Create a blog application" --framework Next.js

# View generated tasks
prompt-manager list-tasks
```

## Best Practices

1. **Context First**: Always review Memory Bank context before generating tasks
2. **Framework Consistency**: Maintain consistent framework choices across tasks
3. **Component Reuse**: Leverage Memory Bank to track reusable components
4. **API Documentation**: Keep API endpoints documented in techContext.md
5. **Progress Tracking**: Update task status regularly to maintain accurate context

## Example Workflow

1. Start new project:
```bash
prompt-manager init "blog-app"
```

2. Generate bolt.new tasks:
```bash
prompt-manager generate-bolt-tasks "Create a blog with authentication and markdown support"
```

3. Track progress:
```bash
prompt-manager update-progress "Initial Project Setup" "completed"
prompt-manager list-tasks
```

4. View technical context:
```bash
cat cline_docs/techContext.md
```

## Memory Bank Structure

The bolt.new integration enhances the Memory Bank structure:

```
cline_docs/
├── productContext.md     # Project requirements and goals
├── activeContext.md      # Current development state
├── systemPatterns.md     # Architectural patterns
├── techContext.md        # Technical specifications
└── progress.md          # Task progress tracking
```

### Context Updates

The Memory Bank automatically updates:

1. **techContext.md**:
   - Framework configuration
   - Dependencies
   - Component library
   - API specifications

2. **systemPatterns.md**:
   - Component architecture
   - API patterns
   - Testing strategies
   - Deployment workflows

3. **activeContext.md**:
   - Current task status
   - Development blockers
   - Next actions

## Error Handling

The system includes robust error handling:

```python
try:
    tasks = pm.generate_bolt_tasks("project_name")
except Exception as e:
    pm.memory_bank.update_context(
        "activeContext.md",
        "Error State",
        f"Task generation failed: {str(e)}"
    )
```

## Token Management

The Memory Bank monitors token usage during task generation:

```python
# Check token limit before generation
if pm.memory_bank.check_token_limit():
    pm.memory_bank._handle_memory_reset()
    
# Generate tasks
tasks = pm.generate_bolt_tasks("project_name")
```

## Future Enhancements

1. Custom framework templates
2. Component library integration
3. API specification import/export
4. Automated testing setup
5. CI/CD pipeline generation
