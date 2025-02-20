#!/bin/bash

# Test CLI commands for prompt-manager

# Set up test environment
test_env() {
    echo "test_env"
    # Create test project directory
    rm -rf test_cli_project
    mkdir -p test_cli_project
    cd test_cli_project || exit 1

    # Initialize project
    prompt-manager base init --path .
    
    # Create test file
    echo "Test content" > test_file.py
}

# Test command with prompt validation
test_command_with_prompt() {
    local cmd=$1
    local prompt_name=$2
    local expected_output=$3
    
    echo "Testing: $cmd"
    
    # Run command and capture output
    output=$(eval "$cmd")
    exit_code=$?
    
    # Check exit code
    if [ $exit_code -ne 0 ]; then
        echo "❌ Command failed with exit code $exit_code"
        echo "$output"
        return 1
    fi
    
    # Validate prompt template header
    if echo "$output" | grep -q "Using prompt template: $prompt_name"; then
        echo "✅ Found prompt template header for $prompt_name"
    else
        echo "❌ Missing prompt template header for $prompt_name"
        return 1
    fi
    
    # Validate prompt formatting
    if echo "$output" | grep -q "{.*}"; then
        echo "✅ Found prompt formatting"
    else
        echo "❌ Missing prompt formatting"
        return 1
    fi
    
    # Check expected output if provided
    if [ -n "$expected_output" ] && echo "$output" | grep -q "$expected_output"; then
        echo "✅ Found expected output: $expected_output"
    elif [ -n "$expected_output" ]; then
        echo "❌ Missing expected output: $expected_output"
        return 1
    fi
    
    echo "✅ $cmd passed"
    return 0
}

# Test command without prompt validation
test_command() {
    local cmd=$1
    local expected_output=$2
    
    echo "Testing: $cmd"
    
    # Run command and capture output
    output=$(eval "$cmd")
    exit_code=$?
    
    # Check exit code
    if [ $exit_code -ne 0 ]; then
        echo "❌ Command failed with exit code $exit_code"
        echo "$output"
        return 1
    fi
    
    # Check expected output if provided
    if [ -n "$expected_output" ] && echo "$output" | grep -q "$expected_output"; then
        echo "✅ Found expected output: $expected_output"
    elif [ -n "$expected_output" ]; then
        echo "❌ Missing expected output: $expected_output"
        return 1
    fi
    
    echo "✅ $cmd passed"
    return 0
}

# Run tests
test_env

# Test add-task command
test_command_with_prompt 'prompt-manager base add-task test-task "Test task description" --show-prompt' "add-task" "Added task: test-task"

# Test add-task with named arguments
test_command 'prompt-manager base add-task another-task "Another description"' "Added task: another-task"

# Test update-progress command
test_command_with_prompt 'prompt-manager base update-progress test-task not_started --note "Started working" --show-prompt' "update-progress" "Updated task status: test-task -> not_started"

# Test update-progress without prompt
test_command 'prompt-manager base update-progress another-task not_started' "Updated task status: another-task -> not_started"

# Test list-tasks command
test_command_with_prompt 'prompt-manager base list-tasks --show-prompt' "list-tasks" "not_started: test-task"

# Test list-tasks without prompt
test_command 'prompt-manager base list-tasks' "not_started: test-task"

# Test export-tasks command
test_command_with_prompt 'prompt-manager base export-tasks --output tasks_export.json --show-prompt' "export-tasks" "Exported tasks to: tasks_export.json"

# Test export-tasks without prompt
test_command 'prompt-manager base export-tasks --output tasks_export2.json' "Exported tasks to: tasks_export2.json"

# Verify memory files
verify_memory_files() {
    local memory_dir="prompt_manager_data/memory"
    
    # Check if memory directory exists
    if [ ! -d "$memory_dir" ]; then
        echo "❌ Memory directory not found: $memory_dir"
        return 1
    fi
    
    # Check required files
    for file in "context.json" "tasks.json" "progress.md"; do
        if [ ! -f "$memory_dir/$file" ]; then
            echo "❌ Required memory file not found: $file"
            return 1
        fi
    done
    
    echo "✅ All memory files verified"
    return 0
}

verify_memory_files

echo "All tests completed!"
