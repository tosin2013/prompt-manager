#!/bin/bash

# Set up error handling
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create and activate a virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Install package in development mode
pip install -e .

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
        test_command "$full_cmd" "'High Priority Task' 'Important task' --template 'Test Template' --priority 1"  # high priority
        test_command "$full_cmd" "'Low Priority Task' 'Optional task' --template 'Test Template' --priority 3"  # low priority
        ;;
      "base update-progress")
        # First create a task to update
        test_command "base add-task" "'Progress Task' 'Task to update' --template 'Test Template' --priority 2"
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
      *)
        echo -e "${BLUE}Skipping execution test for $full_cmd${NC}"
        ;;
    esac
  done
}

# Create test directory
TEST_DIR="test_cli_project"
echo -e "${BLUE}Creating test directory: $TEST_DIR${NC}"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# Initialize test environment
echo -e "${BLUE}Initializing test environment...${NC}"
test_command "init" "--path $TEST_DIR"

# Test version and help
echo -e "\n${BLUE}Testing version...${NC}"
test_command "--version" ""

echo -e "\n${BLUE}Testing main help...${NC}"
test_command "--help" ""

# Test all commands and subcommands
echo -e "\n${BLUE}Testing all commands and subcommands:${NC}"
test_subcommands

# Clean up
rm -rf "$TEST_DIR"
deactivate
rm -rf "$VENV_DIR"
