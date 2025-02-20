#!/bin/bash

# Set up error handling
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
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

# Function to validate prompt display
validate_prompt_display() {
  local output=$1
  local template_name=$2
  
  if echo "$output" | grep -q "Using prompt template: $template_name"; then
    echo -e "${GREEN}✅ Found prompt template header for $template_name${NC}"
    if echo "$output" | grep -q "==================="; then
      echo -e "${GREEN}✅ Found prompt formatting${NC}"
      return 0
    else
      echo -e "${RED}❌ Missing prompt formatting${NC}"
      return 1
    fi
  else
    echo -e "${RED}❌ Missing prompt template header for $template_name${NC}"
    return 1
  fi
}

# Function to verify memory files
verify_memory_files() {
  local memory_dir="$1/memory"
  local files=("tasks.json" "prompts.json" "context.json")
  
  echo -e "\n${YELLOW}Verifying memory files...${NC}"
  
  # Check memory directory exists
  if [ ! -d "$memory_dir" ]; then
    echo -e "${RED}❌ Memory directory not found${NC}"
    return 1
  fi
  echo -e "${GREEN}✅ Memory directory exists${NC}"
  
  # Check each required file exists and is not empty
  for file in "${files[@]}"; do
    if [ ! -f "$memory_dir/$file" ]; then
      echo -e "${RED}❌ Memory file $file not found${NC}"
      return 1
    fi
    if [ ! -s "$memory_dir/$file" ]; then
      echo -e "${RED}❌ Memory file $file is empty${NC}"
      return 1
    fi
    echo -e "${GREEN}✅ Memory file $file exists and has content${NC}"
  done
  
  return 0
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

# Change into test directory
cd "$TEST_DIR"

# Initialize project
echo -e "${BLUE}Initializing test environment...${NC}"
test_command "init" "--path ."

# Test base commands with prompt validation
echo -e "\n${YELLOW}Testing base commands with prompts...${NC}"

# Test add-task with prompt and verify
output=$(prompt-manager base add-task "test-task" "Test task description")
if ! validate_prompt_display "$output" "add-task"; then
  echo -e "${RED}❌ Add task prompt validation failed${NC}"
  exit 1
fi

# Debug output
echo -e "${YELLOW}Task creation output:${NC}"
prompt-manager base list-tasks

# Verify task was created
if ! prompt-manager base list-tasks | grep -q "not_started: test-task"; then
  echo -e "${RED}❌ Task creation verification failed${NC}"
  echo -e "${YELLOW}Expected to find 'not_started: test-task' in output${NC}"
  exit 1
fi

# Test update-progress with prompt
output=$(prompt-manager base update-progress "test-task" "in_progress" --note "Making progress")
if ! validate_prompt_display "$output" "update-progress"; then
  echo -e "${RED}❌ Update progress prompt validation failed${NC}"
  exit 1
fi

# Verify task status was updated
if ! prompt-manager base list-tasks | grep -q "in_progress: test-task"; then
  echo -e "${RED}❌ Task status update verification failed${NC}"
  exit 1
fi

# Test list-tasks with prompt
output=$(prompt-manager base list-tasks)
validate_prompt_display "$output" "list-tasks"

# Test debug commands with prompt validation
echo -e "\n${YELLOW}Testing debug commands with prompts...${NC}"

# Create a test file for analysis
echo "def test_function():" > test_file.py
echo "    print('Hello, World!')" >> test_file.py
echo "    return 'test'" >> test_file.py

# Test analyze-file with prompt
output=$(prompt-manager debug analyze-file test_file.py)
if ! validate_prompt_display "$output" "analyze-file"; then
  echo -e "${RED}❌ Analyze file prompt validation failed${NC}"
  exit 1
fi

# Test find-root-cause with prompt
output=$(prompt-manager debug find-root-cause "Test error" --file-path test_file.py)
if ! validate_prompt_display "$output" "find-root-cause"; then
  echo -e "${RED}❌ Find root cause prompt validation failed${NC}"
  exit 1
fi

# Test test-roadmap with prompt
output=$(prompt-manager debug test-roadmap test_file.py)
if ! validate_prompt_display "$output" "test-roadmap"; then
  echo -e "${RED}❌ Test roadmap prompt validation failed${NC}"
  exit 1
fi

# Test repo commands with prompt validation
echo -e "\n${YELLOW}Testing repo commands with prompts...${NC}"

# Initialize git repo for testing
git init > /dev/null 2>&1
git add test_file.py > /dev/null 2>&1
git commit -m "Initial commit" > /dev/null 2>&1

# Test analyze-repo with prompt
output=$(prompt-manager repo analyze-repo test_file.py)
validate_prompt_display "$output" "analyze-repo"

# Test learn-session with prompt
output=$(prompt-manager repo learn-session test_file.py --duration 1)
validate_prompt_display "$output" "learn-session"

# Verify memory files before cleanup
verify_memory_files "."

# Store memory files in a backup directory
BACKUP_DIR="../test_memory_backup"
mkdir -p "$BACKUP_DIR"
cp -r memory/ "$BACKUP_DIR/"

# Clean up test directory
cd ..
rm -rf "$TEST_DIR"

echo -e "\n${GREEN}All tests completed!${NC}"
echo -e "${BLUE}Memory files backed up to $BACKUP_DIR${NC}"
