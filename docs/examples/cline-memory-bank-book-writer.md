# Cline Memory Bank Integration with AI Book Writer

This guide demonstrates how to integrate Cline's Memory Bank system with the [AI Book Writer](https://github.com/decision-crafters/ai-book-writer.git) project, showcasing how the Memory Bank enhances development workflow and maintains project context.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/decision-crafters/ai-book-writer.git
cd ai-book-writer
```

2. Initialize Prompt Manager with Memory Bank:
```python
from prompt_manager import PromptManager

# Initialize with project name
pm = PromptManager("ai_book_writer")
```

## Memory Bank Structure

The Memory Bank automatically creates this structure for AI Book Writer:

```
cline_docs/
├── productContext.md      # Project overview and goals
├── activeContext.md      # Current development state
├── systemPatterns.md     # Code patterns and architecture
├── techContext.md        # Technical decisions and stack
└── progress.md          # Development tracking
```

### Example Memory Bank Content

1. `productContext.md`:
```markdown
# AI Book Writer - Product Context

## Core Purpose
AI Book Writer is an advanced book generation system that leverages LLMs to create 
coherent, engaging books across multiple genres.

## Key Components
1. Book Generation Pipeline
   - Outline Generation
   - Chapter Development
   - Narrative Consistency Checking
   - Genre-Specific Templating

2. LLM Integration Layer
   - Multiple Model Support
   - Context Management
   - Token Usage Optimization

3. User Interface
   - Streamlit Web Interface
   - CLI Tools
   - Progress Monitoring

## Project Goals
- Generate high-quality, coherent books
- Support multiple genres and writing styles
- Maintain narrative consistency
- Optimize token usage and costs
- Provide intuitive user experience
```

2. `systemPatterns.md`:
```markdown
# System Patterns and Architecture

## Code Organization
1. Core Modules
   - book_generator.py: Main generation pipeline
   - outline_generator.py: Book outline creation
   - genre_manager.py: Genre-specific logic
   - llm_interface.py: LLM integration layer

2. Design Patterns
   - Factory Pattern for genre-specific generators
   - Strategy Pattern for LLM model selection
   - Observer Pattern for progress tracking
   - Builder Pattern for book construction

3. Testing Strategy
   - Unit tests for each component
   - Integration tests for full pipeline
   - Mock LLM responses for testing
   - Performance benchmarks

## Code Standards
1. Documentation
   - Docstrings for all public interfaces
   - Type hints throughout
   - README for each major component
   - Examples in /docs/examples

2. Error Handling
   - Custom exceptions for each module
   - Graceful degradation
   - Detailed error messages
   - Recovery strategies
```

## Development Workflow Examples

### 1. Adding a New Genre

```python
# Start task tracking
task = pm.add_task(
    name="add-mystery-genre",
    description="Implement mystery genre support",
    details="""
    Requirements:
    1. Create mystery genre templates
    2. Implement plot twist generation
    3. Add character tracking
    4. Update genre selection UI
    """
)

# Update technical context
pm.memory_bank.update_tech_context("""
# Mystery Genre Implementation

## Technical Approach
- Using GPT-4 for plot twist generation
- Implementing character relationship graph
- Adding mystery-specific prompt templates
- Enhancing context management for clues

## Dependencies
- networkx for character relationships
- nltk for narrative analysis
- pytest for testing suite
""")

# Track implementation progress
pm.update_progress(
    task_name="add-mystery-genre",
    status="in_progress",
    details="Completed character relationship graph implementation"
)
```

### 2. Debugging Token Usage

```python
# Create debugging task
debug_task = pm.add_task(
    name="optimize-token-usage",
    description="Investigate and optimize high token usage in chapter generation",
    details="""
    Steps:
    1. Profile token usage per chapter
    2. Identify inefficient prompt patterns
    3. Implement token-saving strategies
    4. Add token usage monitoring
    """
)

# Record debugging findings
pm.memory_bank.add_debug_note(
    task_name="optimize-token-usage",
    note="""
    Root Cause Analysis:
    1. Redundant context in chapter prompts
    2. Inefficient character descriptions
    3. Unnecessary scene recaps
    
    Solution:
    - Implemented context compression
    - Added character reference caching
    - Optimized scene transition prompts
    
    Results:
    - 40% reduction in token usage
    - Maintained output quality
    """
)
```

### 3. Implementing Cross-Chapter Consistency

```python
# Track consistency implementation
consistency_task = pm.add_task(
    name="enhance-narrative-consistency",
    description="Improve consistency across chapters",
    details="""
    Features:
    1. Character trait tracking
    2. Plot thread validation
    3. Timeline verification
    4. Setting consistency checks
    """
)

# Update system patterns
pm.memory_bank.update_system_patterns("""
# Narrative Consistency System

## Implementation Pattern
1. ConsistencyManager class
   - Tracks character states
   - Validates plot threads
   - Manages timelines
   - Checks setting details

2. Validation Pipeline
   - Pre-generation validation
   - Post-generation checks
   - Consistency repair suggestions

3. Data Structures
   - Character State Graph
   - Plot Thread DAG
   - Timeline Tree
   - Setting Hash Map
""")
```

## Best Practices

1. **Regular Context Updates**
   ```python
   # After significant changes
   pm.memory_bank.update_active_context(
       "Implemented character relationship tracking"
   )
   ```

2. **Technical Decision Recording**
   ```python
   # When making architectural decisions
   pm.memory_bank.record_decision(
       title="Token Usage Optimization",
       decision="Implement sliding window context",
       rationale="Reduces token usage while maintaining coherence"
   )
   ```

3. **Progress Tracking**
   ```python
   # Track milestones
   pm.update_progress(
       task_name="enhance-narrative-consistency",
       status="completed",
       details="All consistency checks implemented and tested"
   )
   ```

## Debugging and Troubleshooting

1. **Memory Bank Status Check**
   ```python
   # Verify Memory Bank state
   if pm.memory_bank.is_active:
       print("Memory Bank Status:", pm.memory_bank.get_status())
       print("Last Update:", pm.memory_bank.last_update)
   ```

2. **Context Recovery**
   ```python
   # If context seems missing
   pm.memory_bank.rebuild_context()
   ```

3. **Task History**
   ```python
   # Review task history
   history = pm.get_task_history("add-mystery-genre")
   print("Task Timeline:", history.timeline)
   print("Key Decisions:", history.decisions)
   ```

## Integration Points

1. **With Book Generation Pipeline**
   ```python
   # Hook into generation process
   pm.memory_bank.track_generation(
       chapter_id="chapter_1",
       genre="mystery",
       token_usage=1234,
       consistency_score=0.95
   )
   ```

2. **With Testing Framework**
   ```python
   # Track test results
   pm.memory_bank.record_test_results(
       test_suite="mystery_genre",
       passed=15,
       failed=0,
       coverage=0.89
   )
   ```

3. **With User Interface**
   ```python
   # Track UI interactions
   pm.memory_bank.log_user_interaction(
       component="genre_selector",
       action="selected_mystery",
       result="success"
   )
   ```

## Resources

- [AI Book Writer Repository](https://github.com/decision-crafters/ai-book-writer)
- [Prompt Manager Documentation](docs/prompt-manager.md)
- [Memory Bank API Reference](docs/memory-bank-api.md)
- [Development Guidelines](docs/development.md)
