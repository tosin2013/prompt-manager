# Bolt.new Integration with Cline's Memory Bank

The Memory Bank system now integrates with bolt.new through the Prompt Manager, enabling AI-powered task generation for web application development. This integration leverages the Memory Bank's context awareness to create detailed, contextually relevant development tasks.

## Prompt Display and Validation

All bolt.new commands support the `--show-prompt` flag for transparent prompt inspection. This feature helps you:
- Understand how tasks are generated
- Validate prompt templates
- Debug task generation
- Train new developers

Example usage:
```bash
# Generate tasks with prompt display
prompt-manager generate-bolt-tasks "Create a blog with auth" --framework Next.js --show-prompt

# Output will include:
================================================================================
Using prompt template: generate-bolt-tasks
================================================================================
Task Generation Request
======================

Project Description: Create a blog with auth
Target Framework: Next.js
...
================================================================================

# Analyze web components with prompt display
prompt-manager llm analyze-impact components/Button.tsx --show-prompt

# Get component suggestions with prompt
prompt-manager llm suggest-improvements components/Button.tsx --show-prompt
```

## Installation

### For Users

```bash
# Install latest development version from GitHub main branch
pip install git+https://github.com/tosin2013/prompt-manager.git@main

# Or install specific version from PyPI (when released)
pip install tosins-prompt-manager==0.3.18
```

### For Development

```bash
# Clone the repository
git clone https://github.com/tosin2013/prompt-manager.git
cd prompt-manager

# Install in editable mode with development dependencies
pip install -e .[dev]
```

## Core Features

- Structured task generation for web applications
- Framework-specific task templates
- Automatic task prioritization
- Detailed technical specifications
- Memory-aware development context
- Transparent prompt inspection with `--show-prompt`

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

## LLM Enhancement for Web Development

### Code Analysis and Improvement

```python
from prompt_manager import PromptManager

# Initialize project with bolt.new integration
pm = PromptManager("web_project")

# Generate tasks with LLM enhancement
tasks = pm.generate_bolt_tasks(
    project_name="My Web App",
    framework="Next.js",
    llm_enhanced=True  # Enable LLM enhancement
)

# Analyze web components
impact = pm.llm.analyze_impact(["components/Button.tsx"])

# Get component improvement suggestions
suggestions = pm.llm.suggest_improvements(
    file_path="components/Button.tsx",
    max_suggestions=5
)

# Create PR for component improvements
pr = pm.llm.suggest_pull_request(
    changes=[{"components/Button.tsx": "updated content"}],
    title="Enhance Button Component",
    description="Improve accessibility and performance"
)
```

### Command Line Interface for Web Development

```bash
# Generate enhanced bolt.new tasks
prompt-manager generate-bolt-tasks "Create a blog with auth" --framework Next.js --llm-enhanced

# Analyze web components
prompt-manager llm analyze-impact components/Button.tsx

# Get component suggestions
prompt-manager llm suggest-improvements components/Button.tsx

# Create component PR
prompt-manager llm create-pr "Enhance Button" "Improve component"

# Self-improvement for web components
prompt-manager improve enhance components/ --type tests
prompt-manager improve enhance pages/ --type commands
```

### Memory Bank Integration for Web Development

The Memory Bank now tracks web development specific information:

```python
# Update technical context with component analysis
pm.memory_bank.update_context(
    "techContext.md",
    "Component Analysis",
    {
        "components": {
            "Button": {
                "impact_analysis": impact,
                "suggestions": suggestions,
                "test_coverage": test_coverage
            }
        }
    }
)

# Track learning sessions for web development
pm.memory_bank.update_context(
    "activeContext.md",
    "Learning Sessions",
    {
        "web_components": learning_sessions,
        "api_endpoints": api_analysis,
        "performance_metrics": metrics
    }
)
```

### Enhanced Task Generation

The bolt.new task generation now includes:

1. Code Quality Analysis
   - Component structure review
   - Performance optimization
   - Accessibility compliance

2. Testing Strategy
   - Unit test generation
   - Integration test planning
   - E2E test scenarios

3. Documentation
   - Component API docs
   - Usage examples
   - Best practices

4. Deployment
   - Build optimization
   - CI/CD integration
   - Performance monitoring

```python
# Generate enhanced tasks with testing focus
tasks = pm.generate_bolt_tasks(
    project_name="My Web App",
    framework="Next.js",
    enhancement_focus="testing"
)

# Generate tasks with accessibility focus
tasks = pm.generate_bolt_tasks(
    project_name="My Web App",
    framework="Next.js",
    enhancement_focus="accessibility"
)
```

### Self-Improvement and Code Modification

The bolt.new integration includes self-improvement capabilities specifically for web development:

```python
from prompt_manager import PromptManager

# Initialize with web-focused self-improvement
pm = PromptManager(
    "web_project",
    enable_self_improvement=True,
    improvement_focus="web_development"
)

# Analyze and improve web-specific templates
web_improvements = pm.llm.analyze_web_templates()
for improvement in web_improvements:
    # Apply template improvements
    pm.llm.improve_template(
        template_name=improvement["template"],
        changes=improvement["changes"],
        framework="Next.js"
    )

# Analyze and improve web components
component_improvements = pm.llm.analyze_component_quality(
    target="components/",
    aspects=[
        "accessibility",
        "performance",
        "reusability",
        "testing"
    ]
)

# Create pull request with web-focused improvements
pr = pm.llm.create_improvement_pr(
    title="Enhancement: Improved web components and templates",
    description="Automated improvements to web development workflow",
    changes={
        "templates": web_improvements,
        "components": component_improvements
    },
    target_repo="tosin2013/prompt-manager",
    target_branch="main"
)
```

### Command Line Interface for Web Development Improvements

```bash
# Analyze and improve web templates
prompt-manager improve web-templates

# Analyze and improve components
prompt-manager improve components --focus accessibility

# Create web-focused improvement PR
prompt-manager improve create-pr --focus web-development

# Enhance specific web components
prompt-manager improve enhance components/ --type react
prompt-manager improve enhance pages/ --type next
```

### Memory Bank Integration for Web Improvements

The Memory Bank tracks web-specific improvements:

```python
# Track web component improvements
pm.memory_bank.update_context(
    "systemPatterns.md",
    "Web Component Improvements",
    {
        "component_improvements": component_history,
        "accessibility_fixes": accessibility_improvements,
        "performance_optimizations": performance_history
    }
)

# Track successful web patterns
pm.memory_bank.update_context(
    "techContext.md",
    "Web Development Patterns",
    {
        "successful_components": successful_components,
        "reusable_patterns": reusable_code,
        "optimization_techniques": performance_patterns
    }
)
```

### Automated Pull Request Creation for Web Development

The system can automatically create web-focused pull requests:

```python
# Configure GitHub credentials
pm.configure_github(
    token=os.getenv("GITHUB_TOKEN"),
    username="your-username"
)

# Create and submit web-focused improvements
improvements = pm.llm.suggest_web_improvements()
if improvements:
    pr = pm.llm.create_pull_request(
        title="Enhancement: Web development improvements",
        description="""
        This PR contains automated web development improvements:
        - Component optimizations
        - Accessibility enhancements
        - Performance improvements
        - Testing coverage
        """,
        changes=improvements,
        base_repo="tosin2013/prompt-manager",
        base_branch="main"
    )
    
    # Track PR in memory bank
    pm.memory_bank.track_pull_request(pr)
```

### Best Practices for Web Development Modifications

1. **Accessibility First**: Ensure all component improvements maintain or enhance accessibility
2. **Performance Impact**: Analyze performance impact of changes
3. **Cross-browser Testing**: Include cross-browser compatibility in test coverage
4. **Mobile Responsiveness**: Verify improvements work on all device sizes
5. **Documentation**: Update component documentation and examples

### Learning Session Prompts for Web Development

The learning session prompts can be displayed and customized for web development:

```bash
# Start web-focused learning session and display prompt
prompt-manager repo learn-session . --focus web --show-prompt

# Example output:
================================================================================
Using prompt template: web-learn-session
================================================================================
Web Development Learning Analysis Request
======================================

Repository: {repo_path}
Framework: {framework}
Component Count: {component_count}
API Endpoints: {api_endpoints}

Previous Analysis:
{previous_analysis}

Please analyze this web application focusing on:

1. Component Architecture
   - Component hierarchy
   - State management
   - Props structure
   - Event handling

2. Frontend Patterns
   - Reusable components
   - Styling approach
   - Responsive design
   - Accessibility patterns

3. API Integration
   - Data fetching
   - Error handling
   - Caching strategy
   - Authentication flow

4. Performance Optimization
   - Bundle size
   - Load time
   - Rendering optimization
   - Resource usage

5. Testing Coverage
   - Unit tests
   - Integration tests
   - E2E tests
   - Performance tests

Please provide specific, actionable insights that can be used to:
- Improve component architecture
- Enhance user experience
- Optimize performance
- Strengthen testing
================================================================================
```

The web development prompt can be customized:

```python
# Create custom web learning session prompt
pm.memory_bank.update_context(
    "prompts.md",
    "Web Learning Session",
    """
    Custom web learning session template:
    {your_custom_template}
    """
)

# Use custom prompt in web session
pm.llm.start_learning_session(
    focus="web",
    use_custom_prompt=True
)
```

Access web-specific prompts programmatically:

```python
# Get current web learning session prompt
prompt = pm.llm.get_session_prompt(focus="web")
print(prompt)

# Get prompt with specific web context
prompt = pm.llm.get_session_prompt(
    focus="web",
    context={
        "framework": "Next.js",
        "focus_areas": ["components", "api"],
        "analysis_depth": "detailed"
    }
)
print(prompt)
```
