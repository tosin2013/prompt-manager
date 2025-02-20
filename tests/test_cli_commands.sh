#!/bin/bash

# Set up error handling
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test command with prompt
test_command_with_prompt() {
    local cmd=$1
    local args=$2
    local prompt_name=$3
    
    echo -e "${BLUE}Testing: prompt-manager $cmd $args --show-prompt${NC}"
    
    # Run command and capture output
    output=$(eval "prompt-manager $cmd $args --show-prompt 2>&1")
    exit_code=$?
    
    # Print output for debugging
    echo "$output"
    
    # Check if command succeeded
    if [ $exit_code -eq 0 ]; then
        # Validate prompt display
        if echo "$output" | grep -q "Using prompt template: $prompt_name"; then
            echo -e "${GREEN}✅ Found prompt template header for $prompt_name${NC}"
            if echo "$output" | grep -q "==================="; then
                echo -e "${GREEN}✅ Found prompt formatting${NC}"
                echo -e "${GREEN}✅ prompt-manager $cmd $args --show-prompt passed${NC}"
                return 0
            else
                echo -e "${RED}❌ Missing prompt formatting${NC}"
                return 1
            fi
        else
            echo -e "${RED}❌ Missing prompt template header for $prompt_name${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Command failed with exit code $exit_code${NC}"
        return 1
    fi
}

# Function to test command without prompt
test_command() {
    local cmd=$1
    local args=$2
    
    echo -e "${BLUE}Testing: prompt-manager $cmd $args${NC}"
    
    # Run command and capture output
    output=$(eval "prompt-manager $cmd $args 2>&1")
    exit_code=$?
    
    # Print output for debugging
    echo "$output"
    
    # Check if command succeeded
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ prompt-manager $cmd $args passed${NC}"
        return 0
    else
        echo -e "${RED}❌ Command failed with exit code $exit_code${NC}"
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

# Test add-task with and without --show-prompt
test_command_with_prompt "base add-task" "'test-task' 'Test task description'" "add-task"
test_command "base add-task" "'another-task' 'Another description'"

# Test update-progress with and without --show-prompt
test_command_with_prompt "base update-progress" "'test-task' 'in_progress' --note 'Started working'" "update-progress"
test_command "base update-progress" "'another-task' 'in_progress'"

# Test list-tasks with and without --show-prompt
test_command_with_prompt "base list-tasks" "" "list-tasks"
test_command "base list-tasks" ""

# Test export-tasks with and without --show-prompt
test_command_with_prompt "base export-tasks" "--output tasks_export.json" "export-tasks"
test_command "base export-tasks" "--output tasks_export2.json"

# Test generate-bolt-tasks with and without --show-prompt
test_command_with_prompt "base generate-bolt-tasks" "'Create a simple blog' --framework Next.js" "generate-bolt-tasks"
test_command "base generate-bolt-tasks" "'Create another blog' --framework Next.js"

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

# Test analyze-file with and without --show-prompt
test_command_with_prompt "debug analyze-file" "test_file.py" "analyze-file"
test_command "debug analyze-file" "test_file.py"

# Test find-root-cause with and without --show-prompt
test_command_with_prompt "debug find-root-cause" "test_error.log" "find-root-cause"
test_command "debug find-root-cause" "test_error.log"

# Test test-roadmap with and without --show-prompt
test_command_with_prompt "debug test-roadmap" "test_file.py" "test-roadmap"
test_command "debug test-roadmap" "test_file.py"

# Test repo commands with prompts
echo -e "\n${YELLOW}Testing repo commands with prompts...${NC}"

# Test analyze-repo with and without --show-prompt
test_command_with_prompt "repo analyze-repo" "." "analyze-repo"
test_command "repo analyze-repo" "."

# Test learn-session with various combinations
test_command_with_prompt "repo learn-session" "." "learn-session"
test_command "repo learn-session" "."
test_command_with_prompt "repo learn-session" ". --duration 5" "learn-session"
test_command "repo learn-session" ". --duration 5"

# Test LLM commands with prompts
echo -e "\n${YELLOW}Testing LLM commands with prompts...${NC}"

# Test analyze-impact with and without --show-prompt
test_command_with_prompt "llm analyze-impact" "test_file.py" "analyze-impact"
test_command "llm analyze-impact" "test_file.py"

# Test suggest-improvements with and without --show-prompt
test_command_with_prompt "llm suggest-improvements" "test_file.py --max-suggestions 2" "suggest-improvements"
test_command "llm suggest-improvements" "test_file.py --max-suggestions 2"

# Test create-pr with and without --show-prompt
echo "# Added comment" >> test_file.py
git add test_file.py
test_command_with_prompt "llm create-pr" "'Test PR' 'Test Description'" "create-pr"
test_command "llm create-pr" "'Another PR' 'Another Description'"

# Test generate-commands with and without --show-prompt
test_command_with_prompt "llm generate-commands" "test_file.py" "generate-commands"
test_command "llm generate-commands" "test_file.py"

# Test self-improvement commands with prompts
echo -e "\n${YELLOW}Testing self-improvement commands with prompts...${NC}"

# Test enhance command for tests with and without --show-prompt
test_command_with_prompt "improve enhance" "test_file.py --type tests --no-pr" "enhance-system"
test_command "improve enhance" "test_file.py --type tests --no-pr"

# Test enhance command for commands with and without --show-prompt
test_command_with_prompt "improve enhance" ". --type commands --no-pr" "enhance-system"
test_command "improve enhance" ". --type commands --no-pr"

# Test enhance command for plugins with and without --show-prompt
mkdir -p plugins
touch plugins/test_plugin.py
test_command_with_prompt "improve enhance" "plugins --type plugins --no-pr" "enhance-system"
test_command "improve enhance" "plugins --type plugins --no-pr"

# Verify memory files
verify_memory_files "."

echo -e "\n${GREEN}All tests completed!${NC}"

# Backup memory files
BACKUP_DIR="../test_memory_backup"
mkdir -p "$BACKUP_DIR"
cp -r memory/* "$BACKUP_DIR/"
echo "Memory files backed up to $BACKUP_DIR"
