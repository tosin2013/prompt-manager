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
  if prompt-manager $cmd $args; then
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
    prompt-manager --help | grep -A 100 "Commands:" | tail -n +2 | grep "^  [a-z]" | awk '{print $1}'
  else
    prompt-manager $cmd --help | grep -A 100 "Commands:" | tail -n +2 | grep "^  [a-z]" | awk '{print $1}'
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
      "add-task")
        # Test add-task with all options
        test_command "$full_cmd" "\"Test Task\" --description \"Test Description\" --priority medium"
        test_command "$full_cmd" "\"High Priority Task\" --description \"Important task\" --priority high"
        test_command "$full_cmd" "\"Low Priority Task\" --description \"Optional task\" --priority low"
        ;;
      "update-progress")
        # First create a task to update
        test_command "add-task" "\"Progress Task\" --description \"Task to update\" --priority medium"
        # Test all status transitions
        test_command "$full_cmd" "\"Progress Task\" todo"
        test_command "$full_cmd" "\"Progress Task\" in_progress"
        test_command "$full_cmd" "\"Progress Task\" blocked"
        test_command "$full_cmd" "\"Progress Task\" done"
        ;;
      "list-tasks")
        # Test list-tasks with different filters
        test_command "$full_cmd" ""  # No filter
        test_command "$full_cmd" "--status todo"
        test_command "$full_cmd" "--status in_progress"
        test_command "$full_cmd" "--status done"
        test_command "$full_cmd" "--status blocked"
        ;;
      "export-tasks")
        # Test export-tasks with different formats
        test_command "$full_cmd" "tasks.json"
        test_command "$full_cmd" "tasks.yaml"
        ;;
      "generate-bolt-tasks")
        # Test generate-bolt-tasks with different frameworks
        test_command "$full_cmd" "\"Create a new feature\""
        test_command "$full_cmd" "\"Build API endpoint\" --framework fastapi"
        test_command "$full_cmd" "\"Create React component\" --framework react"
        ;;
      "analyze-repo")
        # Test analyze-repo with current directory
        test_command "$full_cmd" "."
        ;;
      "debug")
        # Test debug commands
        test_command "$full_cmd" "info"
        test_command "$full_cmd" "list-memories"
        ;;
      "llm")
        # Test LLM commands that don't require API keys
        test_command "$full_cmd" "list-models"
        test_command "$full_cmd" "list-contexts"
        ;;
      *)
        # Test help for unknown commands
        test_command "$full_cmd" "--help"
        ;;
    esac
    
    # If this is a command with known subcommands, test them
    if [[ "$full_cmd" != "llm"* ]]; then  # Skip llm as it's handled separately
      local sub_subcommands=$(get_subcommands "$full_cmd")
      if [ ! -z "$sub_subcommands" ]; then
        echo -e "\n${BLUE}Testing subcommands for: $full_cmd${NC}"
        test_subcommands "$full_cmd"
      fi
    fi
  done
}

# Create test directory
TEST_DIR="test_cli_project"
echo -e "${BLUE}Creating test directory: $TEST_DIR${NC}"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Initialize test environment
echo -e "${BLUE}Initializing test environment...${NC}"
prompt-manager init

# Test version and main help
echo -e "\n${BLUE}Testing version...${NC}"
test_command "--version" ""

echo -e "\n${BLUE}Testing main help...${NC}"
test_command "--help" ""

# Test all commands and their subcommands
echo -e "\n${BLUE}Testing all commands and subcommands:${NC}"
test_subcommands

echo -e "\n${GREEN}All CLI command tests completed!${NC}"

# Clean up
cd ..
rm -rf "$TEST_DIR"
