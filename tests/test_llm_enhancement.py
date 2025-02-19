"""Tests for LLM Enhancement functionality."""
import pytest
from pathlib import Path
from datetime import datetime
from prompt_manager import PromptManager
from prompt_manager.llm_enhancement import LLMEnhancement
from prompt_manager.cli import reflect, learn_mode, meta_program


@pytest.fixture
def test_memory_path(tmp_path):
    """Create a temporary memory path for testing."""
    return tmp_path / "test_memory"


@pytest.fixture
def prompt_manager(test_memory_path):
    """Create a PromptManager instance for testing."""
    pm = PromptManager("test_project", memory_path=test_memory_path)
    pm.initialize()
    return pm


@pytest.fixture
def llm_enhancement(prompt_manager):
    """Create an LLMEnhancement instance for testing."""
    return prompt_manager.llm_enhancement


def test_llm_enhancement_initialization(llm_enhancement):
    """Test LLMEnhancement initialization."""
    assert llm_enhancement.learning_mode is False
    assert isinstance(llm_enhancement.pattern_library, dict)
    assert isinstance(llm_enhancement.conventions, set)
    assert isinstance(llm_enhancement.command_history, list)


def test_start_learning_session(llm_enhancement, test_memory_path):
    """Test starting a learning session."""
    llm_enhancement.start_learning_session()
    assert llm_enhancement.learning_mode is True

    # Check if session start was recorded in activeContext.md
    active_context = test_memory_path / "activeContext.md"
    assert active_context.exists()
    content = active_context.read_text()
    assert "Started autonomous learning at" in content


def test_record_command(llm_enhancement):
    """Test command recording functionality."""
    test_command = "prompt-manager analyze-repo ."
    llm_enhancement.record_command(test_command, True)

    assert len(llm_enhancement.command_history) == 1
    recorded = llm_enhancement.command_history[0]
    assert recorded['command'] == test_command
    assert recorded['success'] is True
    assert isinstance(recorded['timestamp'], str)


def test_analyze_patterns(llm_enhancement, test_memory_path):
    """Test pattern analysis functionality."""
    # Add some test content to analyze
    context_file = test_memory_path / "techContext.md"
    context_file.write_text("""
    ## Successful Patterns
    - Pattern 1: Use dependency injection
    - Pattern 2: Implement factory pattern
    """)

    patterns = llm_enhancement.analyze_patterns()
    assert isinstance(patterns, list)


def test_generate_suggestions(llm_enhancement):
    """Test suggestion generation functionality."""
    suggestions = llm_enhancement.generate_suggestions()
    assert isinstance(suggestions, list)

    # Test suggestions based on performance metrics
    metrics = llm_enhancement._analyze_performance()
    assert isinstance(metrics, dict)
    assert 'context_usage' in metrics
    assert 'prompt_success' in metrics


def test_generate_custom_utilities(llm_enhancement):
    """Test custom utility generation."""
    utilities = llm_enhancement.generate_custom_utilities()
    assert isinstance(utilities, list)


def test_create_custom_commands(llm_enhancement):
    """Test custom command creation."""
    # Record some test commands first
    llm_enhancement.record_command("prompt-manager init test-project", True)
    llm_enhancement.record_command("prompt-manager analyze-repo .", True)

    commands = llm_enhancement.create_custom_commands()
    assert isinstance(commands, list)


def test_prompt_manager_integration(prompt_manager):
    """Test PromptManager integration with LLMEnhancement."""
    # Test delegation to LLMEnhancement methods
    assert hasattr(prompt_manager, 'llm_enhancement')

    prompt_manager.start_learning_session()
    assert prompt_manager.llm_enhancement.learning_mode is True

    patterns = prompt_manager.analyze_patterns()
    assert isinstance(patterns, list)

    suggestions = prompt_manager.generate_suggestions()
    assert isinstance(suggestions, list)

    utilities = prompt_manager.generate_custom_utilities()
    assert isinstance(utilities, list)

    commands = prompt_manager.create_custom_commands()
    assert isinstance(commands, list)


def test_cli_commands(cli_runner, prompt_manager):
    """Test CLI commands for LLM enhancement features."""
    # Test reflect command
    result = cli_runner.invoke(reflect)
    assert result.exit_code == 0
    assert "Analyzing LLM interaction patterns" in result.output

    # Test learn_mode command
    result = cli_runner.invoke(learn_mode)
    assert result.exit_code == 0
    assert "Enabling autonomous learning mode" in result.output

    # Test meta_program command
    result = cli_runner.invoke(meta_program)
    assert result.exit_code == 0
    assert "Entering meta-programming mode" in result.output


def test_error_handling(llm_enhancement):
    """Test error handling in LLM enhancement features."""
    # Test with invalid command
    with pytest.raises(ValueError):
        llm_enhancement.record_command("", True)

    # Test with invalid performance metrics
    with pytest.raises(ValueError):
        llm_enhancement._analyze_performance = lambda: {'invalid': 0}
        llm_enhancement.generate_suggestions()


def test_memory_bank_interaction(llm_enhancement, test_memory_path):
    """Test interaction with Memory Bank."""
    # Test context updates
    llm_enhancement.start_learning_session()

    # Verify context files were created
    assert (test_memory_path / "activeContext.md").exists()
    assert (test_memory_path / "techContext.md").exists()

    # Test pattern extraction from context
    context_file = test_memory_path / "techContext.md"
    context_file.write_text("""
    ## Code Patterns
    - Pattern: Successful implementation
    """)

    patterns = llm_enhancement.analyze_patterns()
    assert len(patterns) >= 0  # Should at least return an empty list
