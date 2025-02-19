"""Tests for LLM Enhancement module."""
import pytest
from pathlib import Path
import json
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open
from prompt_manager.llm_enhancement import LLMEnhancement, PullRequestSuggestion


@pytest.fixture
def memory_bank():
    """Create a mock memory bank."""
    mock = MagicMock()
    mock.memory_path = "/tmp/test_memories"
    return mock


@pytest.fixture
def llm_enhancement(memory_bank):
    """Create an LLMEnhancement instance."""
    return LLMEnhancement(memory_bank)


def test_start_learning_session(llm_enhancement):
    """Test starting a learning session."""
    with patch("builtins.open", mock_open()) as mock_file:
        llm_enhancement.start_learning_session()
        assert llm_enhancement.learning_mode is True
        mock_file.assert_called_once()


def test_analyze_patterns(llm_enhancement):
    """Test pattern analysis from context."""
    test_content = """
    # Patterns
    - Pattern: Use descriptive variable names
    - Pattern: Add comprehensive docstrings
    """
    
    with patch("pathlib.Path.exists") as mock_exists:
        with patch("pathlib.Path.read_text") as mock_read:
            mock_exists.return_value = True
            mock_read.return_value = test_content
            
            patterns = llm_enhancement.analyze_patterns()
            assert len(patterns) == 2
            assert "Use descriptive variable names" in patterns
            assert "Add comprehensive docstrings" in patterns


def test_generate_suggestions(llm_enhancement):
    """Test suggestion generation."""
    llm_enhancement.pattern_library = {
        'pattern1': {'success_rate': 0.5},
        'pattern2': {'success_rate': 0.6}
    }
    
    suggestions = llm_enhancement.generate_suggestions()
    assert len(suggestions) > 0
    assert isinstance(suggestions, list)
    assert all(isinstance(s, str) for s in suggestions)


def test_record_command(llm_enhancement):
    """Test command recording."""
    command = "test command"
    llm_enhancement.record_command(command, True)
    
    assert len(llm_enhancement.command_history) == 1
    record = llm_enhancement.command_history[0]
    assert record['command'] == command
    assert record['success'] is True
    assert 'timestamp' in record


def test_generate_custom_utilities(llm_enhancement):
    """Test utility generation."""
    with patch("pathlib.Path.exists") as mock_exists:
        with patch("pathlib.Path.read_text") as mock_read:
            mock_exists.return_value = True
            mock_read.return_value = "Need: Custom Logger"
            
            utilities = llm_enhancement.generate_custom_utilities()
            assert len(utilities) == 1
            assert "def custom_logger():" in utilities[0]


def test_create_custom_commands(llm_enhancement):
    """Test command creation."""
    llm_enhancement.command_history = [
        {'command': 'test', 'success': True, 'timestamp': '2024-01-01'},
        {'command': 'test', 'success': True, 'timestamp': '2024-01-02'},
    ]
    
    commands = llm_enhancement.create_custom_commands()
    assert len(commands) == 1
    assert "@click.command()" in commands[0]
    assert "def test():" in commands[0]


def test_suggest_pull_request(llm_enhancement):
    """Test pull request suggestion creation."""
    changes = [{"test.py": "print('test')"}]
    title = "Test PR"
    description = "Test description"
    
    suggestion = llm_enhancement.suggest_pull_request(changes, title, description)
    assert isinstance(suggestion, PullRequestSuggestion)
    assert suggestion.title == title
    assert suggestion.description == description
    assert len(suggestion.changes) == 1
    assert isinstance(suggestion.impact_analysis, dict)
    assert isinstance(suggestion.test_coverage, dict)
    assert isinstance(suggestion.reviewer_notes, list)


def test_create_pull_request_success(llm_enhancement):
    """Test successful pull request creation."""
    suggestion = PullRequestSuggestion(
        title="Test PR",
        description="Test description",
        branch_name="test-branch",
        changes=[{"test.py": "print('test')"}],
        impact_analysis={"test.py": "Low impact"},
        test_coverage={"test.py": 0.85},
        reviewer_notes=["Please review carefully"]
    )
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        success, message = llm_enhancement.create_pull_request(suggestion)
        assert success is True
        assert "created and pushed" in message
        assert mock_run.call_count == 4  # checkout, add, commit, push


def test_create_pull_request_failure(llm_enhancement):
    """Test pull request creation failure."""
    suggestion = PullRequestSuggestion(
        title="Test PR",
        description="Test description",
        branch_name="test-branch",
        changes=[{"test.py": "print('test')"}],
        impact_analysis={"test.py": "Low impact"},
        test_coverage={"test.py": 0.85},
        reviewer_notes=["Please review carefully"]
    )
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("Git error")
        success, message = llm_enhancement.create_pull_request(suggestion)
        assert success is False
        assert "Failed to create pull request" in message


def test_validate_changes_sensitive_file(llm_enhancement):
    """Test validation of changes with sensitive files."""
    changes = [{"config/production/secrets.py": "secret = 'test'"}]
    assert llm_enhancement._validate_changes(changes) is False


def test_generate_branch_name(llm_enhancement):
    """Test branch name generation."""
    title = "Test Pull Request Title"
    branch_name = llm_enhancement._generate_branch_name(title)
    assert branch_name.startswith("llm-enhancement/test-pull-request-title-")
    assert len(branch_name.split("-")[-1]) == 8  # UUID length


def test_analyze_change_impact(llm_enhancement):
    """Test change impact analysis."""
    changes = [{"test.py": "print('test')\n" * 100}]
    
    with patch("pathlib.Path.exists") as mock_exists:
        with patch("builtins.open", mock_open(read_data="print('old')")):
            mock_exists.return_value = True
            impact = llm_enhancement._analyze_change_impact(changes)
            assert "test.py" in impact
            assert impact["test.py"] == "High impact"


def test_calculate_test_coverage(llm_enhancement):
    """Test test coverage calculation."""
    changes = [{"test.py": "print('test')"}]
    coverage = llm_enhancement._calculate_test_coverage(changes)
    assert "test.py" in coverage
    assert coverage["test.py"] == 0.85


def test_generate_reviewer_notes(llm_enhancement):
    """Test reviewer notes generation."""
    changes = [{"test.py": "print('test')"}]
    impact = {"test.py": "Low impact"}
    
    notes = llm_enhancement._generate_reviewer_notes(changes, impact)
    assert len(notes) > 0
    assert any("test.py" in note for note in notes)
    assert any("Code style" in note for note in notes)
    assert any("Test coverage" in note for note in notes)
