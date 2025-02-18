"""
Tests for the MemoryBank component.
"""
import pytest
from pathlib import Path
from prompt_manager import MemoryBank

@pytest.fixture
def memory_bank(test_data_dir):
    """Create a MemoryBank instance for testing."""
    return MemoryBank(test_data_dir)

def test_memory_bank_initialization(memory_bank, test_data_dir):
    """Test that memory bank initializes correctly."""
    memory_bank.initialize()
    assert memory_bank.is_active

    # Check all required files are created
    for file in memory_bank.required_files:
        assert (test_data_dir / file).exists()
        content = (test_data_dir / file).read_text()
        assert content.startswith(f"# {file[:-3]}\n\n")

def test_context_update(memory_bank):
    """Test context file updates."""
    memory_bank.initialize()

    test_section = "Test Section"
    test_content = "Test content for section"

    # Test append mode
    memory_bank.update_context(
        "productContext.md", 
        test_section, 
        test_content,
        mode="append"
    )
    content = (memory_bank.docs_path / "productContext.md").read_text()
    assert f"## {test_section}" in content
    assert test_content in content

    # Test replace mode
    new_content = "New test content"
    memory_bank.update_context(
        "productContext.md",
        test_section,
        new_content,
        mode="replace"
    )
    content = (memory_bank.docs_path / "productContext.md").read_text()
    assert test_content not in content
    assert new_content in content

def test_token_limit(memory_bank):
    """Test token limit checking and tracking."""
    memory_bank.initialize()

    # Should not exceed limit initially
    assert not memory_bank.check_token_limit()
    initial_tokens = memory_bank.current_tokens

    # Add tokens up to limit
    memory_bank.increment_tokens(memory_bank.max_tokens - initial_tokens)
    assert memory_bank.check_token_limit()

    # Test token reduction
    memory_bank.decrement_tokens(1000)
    assert memory_bank.current_tokens == memory_bank.max_tokens - 1000

def test_inactive_memory_bank(memory_bank):
    """Test behavior when memory bank is not active."""
    # Don't initialize
    memory_bank.update_context(
        "productContext.md",
        "Test Section",
        "Should not be written"
    )
    
    # File should not exist since bank wasn't initialized
    assert not (memory_bank.docs_path / "productContext.md").exists()

def test_memory_bank_reset(memory_bank):
    """Test memory bank reset functionality."""
    memory_bank.initialize()
    
    # Add some content
    memory_bank.update_context(
        "productContext.md",
        "Test Section",
        "Test content"
    )
    
    # Reset memory bank
    memory_bank.reset()
    assert not memory_bank.is_active
    
    # Reinitialize and verify clean state
    memory_bank.initialize()
    content = (memory_bank.docs_path / "productContext.md").read_text()
    assert "Test content" not in content

def test_invalid_file_operations(memory_bank):
    """Test handling of invalid file operations."""
    memory_bank.initialize()
    
    # Test invalid file name
    with pytest.raises(ValueError):
        memory_bank.update_context(
            "invalid.md",
            "Test Section",
            "Test content"
        )
    
    # Test invalid mode
    with pytest.raises(ValueError):
        memory_bank.update_context(
            "productContext.md",
            "Test Section",
            "Test content",
            mode="invalid"
        )
