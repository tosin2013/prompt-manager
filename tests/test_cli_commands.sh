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

# Install package in development mode with all dependencies
pip install -e .[dev]
pip install gitpython>=3.1.0

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

# Test add-task
output=$(prompt-manager base add-task "test-task" "Test task description")
if ! validate_prompt_display "$output" "add-task"; then
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

# Test update-progress
output=$(prompt-manager base update-progress "test-task" "in_progress" --note "Started working")
if ! validate_prompt_display "$output" "update-progress"; then
  exit 1
fi

# Test list-tasks
output=$(prompt-manager base list-tasks)
if ! validate_prompt_display "$output" "list-tasks"; then
  exit 1
fi

# Test export-tasks
echo -e "\n${YELLOW}Testing export-tasks command...${NC}"
output=$(prompt-manager base export-tasks --output tasks_export.json)
if ! validate_prompt_display "$output" "export-tasks"; then
  exit 1
fi
if [ ! -f "tasks_export.json" ]; then
  echo -e "${RED}❌ Export file not created${NC}"
  exit 1
fi

# Test generate-bolt-tasks
echo -e "\n${YELLOW}Testing generate-bolt-tasks command...${NC}"
output=$(prompt-manager base generate-bolt-tasks "Create a simple blog" --framework Next.js)
if ! validate_prompt_display "$output" "generate-bolt-tasks"; then
  exit 1
fi

# Test debug commands with prompt validation
echo -e "\n${YELLOW}Testing debug commands with prompts...${NC}"

# Create test files
echo "def test_function():
    print('Hello World')
    return True" > test_file.py

echo "Error: Something went wrong
Traceback (most recent call last):
  File 'test_file.py', line 2
    print('Hello World')
TypeError: str object is not callable" > test_error.log

# Initialize git repository for testing
git init
git add .
git config --global user.email "test@example.com"
git config --global user.name "Test User"
git commit -m "Initial commit"

# Test analyze-file
output=$(prompt-manager debug analyze-file "test_file.py")
if ! validate_prompt_display "$output" "analyze-file"; then
  exit 1
fi

# Test find-root-cause
output=$(prompt-manager debug find-root-cause "test_error.log")
if ! validate_prompt_display "$output" "find-root-cause"; then
  exit 1
fi

# Test test-roadmap
output=$(prompt-manager debug test-roadmap "test_file.py")
if ! validate_prompt_display "$output" "test-roadmap"; then
  exit 1
fi

# Test repo commands with prompts
echo -e "\n${YELLOW}Testing repo commands with prompts...${NC}"

# Test analyze-repo
output=$(prompt-manager repo analyze-repo ".")
if ! validate_prompt_display "$output" "analyze-repo"; then
  exit 1
fi

# Test learn-session
output=$(prompt-manager repo learn-session "." --duration 5)
if ! validate_prompt_display "$output" "learn-session"; then
  exit 1
fi

# Test LLM commands
echo -e "\n${YELLOW}Testing LLM commands with prompts...${NC}"

# Test analyze-impact
output=$(prompt-manager llm analyze-impact test_file.py)
if ! validate_prompt_display "$output" "analyze-impact"; then
  exit 1
fi

# Test suggest-improvements
output=$(prompt-manager llm suggest-improvements test_file.py --max-suggestions 2)
if ! validate_prompt_display "$output" "suggest-improvements"; then
  exit 1
fi

# Test create-pr
# First make some changes
echo "# Added comment" >> test_file.py
git add test_file.py
output=$(prompt-manager llm create-pr "Test PR" "Test Description")
if ! validate_prompt_display "$output" "create-pr"; then
  exit 1
fi

# Test generate-commands
output=$(prompt-manager llm generate-commands test_file.py)
if ! validate_prompt_display "$output" "generate-commands"; then
  exit 1
fi

# Test self-improvement commands
echo -e "\n${YELLOW}Testing self-improvement commands...${NC}"

# Test enhance command for tests
output=$(prompt-manager improve enhance test_file.py --type tests --no-pr)
if ! validate_prompt_display "$output" "enhance-system"; then
  exit 1
fi

# Test enhance command for commands
output=$(prompt-manager improve enhance . --type commands --no-pr)
if ! validate_prompt_display "$output" "enhance-system"; then
  exit 1
fi

# Test enhance command for plugins
mkdir -p plugins
touch plugins/test_plugin.py
output=$(prompt-manager improve enhance plugins --type plugins --no-pr)
if ! validate_prompt_display "$output" "enhance-system"; then
  exit 1
fi

# Verify memory files
verify_memory_files "."

echo -e "\n${GREEN}All tests completed!${NC}"

# Backup memory files
BACKUP_DIR="../test_memory_backup"
mkdir -p "$BACKUP_DIR"
cp -r memory/* "$BACKUP_DIR/"
echo "Memory files backed up to $BACKUP_DIR"
