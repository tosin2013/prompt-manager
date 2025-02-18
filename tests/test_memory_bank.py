import pytest
from prompt_manager import MemoryBank


@pytest.fixture
def memory_bank(tmp_path):
    return MemoryBank(tmp_path)


def test_memory_bank_initialization(memory_bank):
    """Test that memory bank initializes correctly"""
    memory_bank.initialize()
    assert memory_bank.is_active

    # Check all required files are created
    for file in memory_bank.required_files:
        assert (memory_bank.docs_path / file).exists()


def test_context_update(memory_bank):
    """Test context file updates"""
    memory_bank.initialize()

    # Update context
    memory_bank.update_context(
        "productContext.md", "Project Purpose", "Test project purpose"
    )

    # Verify update
    content = (memory_bank.docs_path / "productContext.md").read_text()
    assert "Test project purpose" in content
    assert "## Project Purpose" in content


def test_token_limit(memory_bank):
    """Test token limit checking"""
    memory_bank.initialize()

    # Should not exceed limit initially
    assert not memory_bank.check_token_limit()

    # Add tokens up to limit
    memory_bank.increment_tokens(memory_bank.max_tokens)
    assert memory_bank.check_token_limit()


def test_inactive_memory_bank(memory_bank):
    """Test behavior when memory bank is not active"""
    # Don't initialize
    memory_bank.update_context(
        "productContext.md", "Project Purpose", "Should not be written"
    )

    # File should not exist
    assert not (memory_bank.docs_path / "productContext.md").exists()
