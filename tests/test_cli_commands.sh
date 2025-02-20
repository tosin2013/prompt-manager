#!/bin/bash

# Set up error handling
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to test a command
test_command() {
  local cmd=$1
  local args=$2
  echo -e "${BLUE}Testing: prompt-manager $cmd $args${NC}"
  # Use eval to properly handle quoted arguments
  if eval "prompt-manager $cmd $args"; then
    echo -e "${GREEN}✅ prompt-manager $cmd $args passed${NC}"
    return 0
  else
    echo -e "${RED}❌ prompt-manager $cmd $args failed${NC}"
    return 1
  fi
}

# Create and activate a virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Install package in development mode
pip install -e .

# Create test directory
TEST_DIR="test_cli_project"
echo -e "${BLUE}Creating test directory: $TEST_DIR${NC}"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# Initialize project
echo -e "${BLUE}Initializing test environment...${NC}"
test_command "init" "--path $TEST_DIR"

# Change into test directory
cd "$TEST_DIR"

# Add a test task to generate memory content
test_command "base add-task" "'test-task' 'Test task for memory validation'"

# Change back to original directory
cd ..

# Function to validate memory files
validate_memory_files() {
  local memory_dir="$TEST_DIR/memory"
  echo -e "${BLUE}Validating memory files...${NC}"
  
  # Check if memory directory exists
  if [ ! -d "$memory_dir" ]; then
    echo -e "${RED}❌ Memory directory not found${NC}"
    return 1
  fi
  
  # Required memory files
  local required_files=(
    "productContext.md"
    "activeContext.md"
    "systemPatterns.md"
    "techContext.md"
    "progress.md"
    "commandHistory.md"
  )
  
  # Check each required file
  for file in "${required_files[@]}"; do
    if [ ! -f "$memory_dir/$file" ]; then
      echo -e "${RED}❌ Required memory file not found: $file${NC}"
      return 1
    fi
    
    # Check if file has content (at least a header)
    if [ ! -s "$memory_dir/$file" ]; then
      echo -e "${RED}❌ Memory file is empty: $file${NC}"
      return 1
    fi
    
    # Check if file has proper header
    case "$file" in
      "productContext.md") expected_header="# Product Context" ;;
      "activeContext.md") expected_header="# Active Context" ;;
      "systemPatterns.md") expected_header="# System Patterns" ;;
      "techContext.md") expected_header="# Tech Context" ;;
      "progress.md") expected_header="# Progress" ;;
      "commandHistory.md") expected_header="# Command History" ;;
      *) expected_header="# $(echo ${file%.md} | sed -E 's/([A-Z])/ \1/g' | sed -E 's/^./\U&/g' | sed -E 's/ ([a-z])/\U\1/g')" ;;
    esac
    
    if ! grep -q "^$expected_header" "$memory_dir/$file"; then
      echo -e "${RED}❌ Memory file missing header: $file (expected '$expected_header')${NC}"
      echo -e "${RED}File contents:${NC}"
      cat "$memory_dir/$file"
      return 1
    fi
  done
  
  # Check activeContext.md for task creation
  if ! grep -q "Task: test-task" "$memory_dir/activeContext.md"; then
    echo -e "${RED}❌ No task creation found in activeContext.md${NC}"
    return 1
  fi
  
  # Check commandHistory.md for command tracking
  if ! grep -q "Command:" "$memory_dir/commandHistory.md"; then
    echo -e "${RED}❌ No command tracking found in commandHistory.md${NC}"
    return 1
  fi
  
  echo -e "${GREEN}✅ Memory files validation passed${NC}"
  return 0
}

# Function to get subcommands for a command
get_subcommands() {
  local cmd=$1
  if [ -z "$cmd" ]; then
    # Get top-level commands
    prompt-manager --help | grep -A 100 "Commands:" | tail -n +2 | grep "^  [a-z]" | awk '{print $1}'
  else
    # Get subcommands for a specific command
    prompt-manager $cmd --help 2>/dev/null | grep -A 100 "Commands:" | tail -n +2 | grep "^  [a-z]" | awk '{print $1}' || true
  fi
}

# Function to test all subcommands recursively
test_subcommands() {
  local base_cmd=$1
  
  # Get subcommands
  local subcommands
  if [ -z "$base_cmd" ]; then
    subcommands=$(get_subcommands)
  else
    subcommands=$(get_subcommands "$base_cmd")
  fi
  
  # Test each subcommand
  for subcmd in $subcommands; do
    local full_cmd
    if [ -z "$base_cmd" ]; then
      full_cmd=$subcmd
    else
      full_cmd="$base_cmd $subcmd"
    fi
    
    # Test help for the subcommand
    echo -e "\n${BLUE}Testing help for: $full_cmd${NC}"
    test_command "$full_cmd" "--help"
    
    # Test basic execution where possible
    case "$full_cmd" in
      "init")
        # Skip init as it's already tested in setup
        echo -e "${BLUE}Skipping init execution (already tested in setup)${NC}"
        ;;
      "base")
        # Test base commands
        test_subcommands "$full_cmd"
        ;;
      "base add-task")
        # Test add-task with all options
        test_command "$full_cmd" "'Test Task' 'Test Description' --template 'Test Template'"
        test_command "$full_cmd" "'High Priority Task' 'Important task' --template 'Test Template' --priority high"
        test_command "$full_cmd" "'Low Priority Task' 'Optional task' --template 'Test Template' --priority low"
        ;;
      "base update-progress")
        # First create a task to update
        test_command "base add-task" "'Progress Task' 'Task to update' --template 'Test Template' --priority medium"
        # Test all status transitions
        test_command "$full_cmd" "'Progress Task' todo"
        test_command "$full_cmd" "'Progress Task' in_progress"
        test_command "$full_cmd" "'Progress Task' blocked"
        test_command "$full_cmd" "'Progress Task' done"
        ;;
      "base list-tasks")
        # Test list-tasks with different filters
        test_command "$full_cmd" ""  # No filter
        test_command "$full_cmd" "--status todo"
        test_command "$full_cmd" "--status in_progress"
        test_command "$full_cmd" "--status done"
        test_command "$full_cmd" "--status blocked"
        ;;
      "base export-tasks")
        test_command "$full_cmd" "tasks_export.json"
        ;;
      "llm")
        # Test LLM commands
        test_subcommands "$full_cmd"
        ;;
      "memory")
        # Test memory management commands
        test_subcommands "$full_cmd"
        ;;
      "memory list")
        # Test memory list command
        test_command "$full_cmd" ""  # No filter
        test_command "$full_cmd" "--file progress.md"
        test_command "$full_cmd" "--file commandHistory.md"
        ;;
      *)
        echo -e "${BLUE}Skipping execution test for $full_cmd${NC}"
        ;;
    esac
  done
}

echo -e "\nTesting version..."
test_command "--version" ""

echo -e "\nTesting main help..."
test_command "--help" ""

echo -e "\nTesting all commands and subcommands:"
test_subcommands

# Validate memory files at the end
validate_memory_files

# Clean up
echo -e "\n${BLUE}Cleaning up...${NC}"
rm -rf "$TEST_DIR"
deactivate
rm -rf "$VENV_DIR"

echo -e "\n${GREEN}All tests completed!${NC}"
