# Using Prompt Manager with AI Book Writer

This guide demonstrates how to use Prompt Manager to track and manage development tasks for the [AI Book Writer](https://github.com/decision-crafters/ai-book-writer) project.

## Project Overview

AI Book Writer is a Python-based tool that uses AI to generate book outlines and content. The project includes:

- Book generation pipeline
- Outline generation
- Multiple LLM integrations
- Streamlit web interface

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/decision-crafters/ai-book-writer.git
   cd ai-book-writer
   ```

2. Set up Bazel build environment:
   ```bash
   # Install Bazelisk for reproducible builds
   brew install bazelisk

   # Create Bazel workspace
   echo 'workspace(name = "ai_book_writer")' > WORKSPACE

   # Create .bazelrc with build settings
   cat > .bazelrc << EOL
   build --incompatible_strict_action_env
   build --enable_platform_specific_config
   build --python_version=PY3
   test --test_output=errors
   EOL
   ```

3. Install Prompt Manager:
   ```bash
   bazel run //:pip -- install prompt-manager
   ```

4. Initialize Prompt Manager for the repository:
   ```bash
   python -m prompt_manager.cli analyze-repo .
   ```

This will:
- Create a `cline_docs` directory for tracking development context
- Add `cline_docs/` to `.gitignore`
- Initialize the memory bank with required files

## Build and Test Configuration

1. Create a root BUILD file:
   ```python
   # BUILD
   load("@rules_python//python:defs.bzl", "py_library", "py_test")

   py_library(
       name = "ai_book_writer_lib",
       srcs = glob(["*.py"]),
       deps = [
           "//llm:llm_lib",
           "//config:config_lib",
       ],
   )

   py_test(
       name = "all_tests",
       srcs = glob(["tests/**/*.py"]),
       deps = [
           ":ai_book_writer_lib",
           "@pytest",
       ],
   )
   ```

2. Set up Pytest configuration:
   ```ini
   # pytest.ini
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   addopts = --strict-markers -v --cov=. --cov-report=xml
   ```

## Example Tasks

Here are some example tasks you can track with Prompt Manager:

1. Add New Genre Support:
   ```bash
   python -m prompt_manager.cli add-task \
     "add-fantasy-genre" \
     "Add support for fantasy genre with specialized prompts" \
     "Implementation requirements:
      1. Add fantasy genre option in select_genre.py
      2. Create fantasy-specific prompt templates
      3. Add comprehensive Pytest test suite:
         - Test genre selection
         - Validate prompt templates
         - Check edge cases
      4. Update BUILD files for new components
      5. Document new genre in README.md
      6. Add integration tests"
   ```

2. Improve Book Generation:
   ```bash
   python -m prompt_manager.cli add-task \
     "enhance-chapter-generation" \
     "Improve chapter generation with better continuity" \
     "Enhancement requirements:
      1. Update book_generator.py:
         - Add context tracking between chapters
         - Implement character consistency checks
         - Add plot thread validation
      2. Create comprehensive test suite:
         - Unit tests for each component
         - Integration tests for full pipeline
         - Performance benchmarks
      3. Update BUILD dependencies
      4. Document technical decisions in cline_docs"
   ```

## Project Structure in Memory Bank

The Prompt Manager will organize project information in the following structure:

```
cline_docs/
├── productContext.md      # High-level project understanding
├── activeContext.md      # Current development state
├── systemPatterns.md     # Code patterns and conventions
├── techContext.md        # Technical decisions and dependencies
└── progress.md          # Development progress tracking
```

### Example Content

1. `systemPatterns.md`:
   ```markdown
   # System Patterns and Conventions

   ## Build System
   - Using Bazel 8.1.0 for all builds
   - Strict dependency management
   - Modular BUILD files per directory

   ## Testing Standards
   - Pytest for all test suites
   - Required test coverage > 80%
   - Integration tests for all features
   - Performance benchmarks for LLM calls

   ## Code Organization
   - Modular architecture
   - Clear separation of concerns
   - Comprehensive documentation
   ```

2. `techContext.md`:
   ```markdown
   # Technical Context

   ## Build Configuration
   - Bazel workspace setup
   - Python version requirements
   - External dependencies

   ## Testing Framework
   - Pytest configuration
   - Coverage requirements
   - CI/CD integration

   ## Development Tools
   - Prompt Manager for tracking
   - Bazel for building
   - Pre-commit hooks
   ```

## Best Practices

1. **Task Management**:
   - Create focused, specific tasks
   - Include clear acceptance criteria
   - Reference specific files and BUILD targets

2. **Testing Requirements**:
   - Write tests before implementation
   - Maintain high coverage
   - Include performance tests
   - Document test cases

3. **Build System**:
   - Keep BUILD files up to date
   - Document dependencies
   - Use consistent naming

4. **Progress Tracking**:
   ```bash
   python -m prompt_manager.cli update-progress \
     "add-fantasy-genre" \
     "In Progress" \
     "Completed test suite, updating BUILD files"
   ```

## Debugging Guide

1. **Environment Setup**:
   ```bash
   # Clean Bazel cache
   bazel clean --expunge

   # Run tests with debug output
   bazel test --test_output=all //...
   ```

2. **Test Debugging**:
   ```bash
   # Run specific test with debug info
   bazel test --test_output=streamed --test_arg="-v" //tests:test_genre_selection
   ```

3. **Performance Analysis**:
   ```bash
   # Run benchmarks
   bazel run //tests:benchmarks
   ```

## Common Commands

1. Build and Test:
   ```bash
   # Build all targets
   bazel build //...

   # Run all tests
   bazel test //...
   ```

2. View Task Status:
   ```bash
   python -m prompt_manager.cli get-task "add-fantasy-genre"
   ```

3. Update Progress:
   ```bash
   python -m prompt_manager.cli update-progress \
     "enhance-chapter-generation" \
     "Complete" \
     "All tests passing, coverage at 85%"
   ```

## Contributing

When contributing to AI Book Writer:

1. Create a task for your contribution
2. Write tests first (TDD approach)
3. Update BUILD files
4. Maintain documentation
5. Ensure all tests pass
6. Meet coverage requirements

## Resources

- [AI Book Writer Repository](https://github.com/decision-crafters/ai-book-writer)
- [Bazel Documentation](https://bazel.build/docs)
- [Pytest Documentation](https://docs.pytest.org)
- [Development Guidelines](https://github.com/decision-crafters/ai-book-writer/blob/main/dev.md)
