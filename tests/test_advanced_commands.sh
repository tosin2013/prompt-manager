#!/bin/bash

# Test advanced CLI commands for prompt-manager

# Import common test functions
source tests/test_cli_commands.sh

# Set up test environment with sample tasks
setup_advanced_env() {
    echo "Setting up advanced test environment"
    test_env

    # Add tasks with dependencies and tags
    prompt-manager base add-task "frontend-task" "Implement frontend components" --priority 2 --template "frontend"
    prompt-manager base add-task "backend-task" "Implement backend API" --priority 1 --template "backend"
    prompt-manager base add-task "database-task" "Set up database schema" --priority 1 --template "database"
    
    # Update task statuses
    prompt-manager base update-progress "frontend-task" "in_progress" --note "Started frontend work"
    prompt-manager base update-progress "database-task" "completed" --note "Database schema completed"
}

# Test bolt task generation
test_bolt_tasks() {
    echo "Testing bolt task generation"
    
    # Test with framework specified
    test_command_with_prompt 'prompt-manager base generate-bolt-tasks "Create a React dashboard" --framework react --show-prompt' \
        "generate-bolt-tasks" "Generated tasks"
    
    # Test without framework
    test_command 'prompt-manager base generate-bolt-tasks "Create an API endpoint"' "Generated tasks"
    
    # Test with output file
    test_command 'prompt-manager base generate-bolt-tasks "Create a login page" --output bolt_tasks.json' \
        "Tasks exported to bolt_tasks.json"
}

# Test task filtering and sorting
test_task_filtering() {
    echo "Testing task filtering and sorting"
    
    # Test filtering by status
    test_command 'prompt-manager base list-tasks --status completed' "database-task"
    test_command 'prompt-manager base list-tasks --status in_progress' "frontend-task"
    
    # Test sorting
    test_command 'prompt-manager base list-tasks --sort-by priority' "backend-task"
    test_command 'prompt-manager base list-tasks --sort-by status' "database-task"
}

# Test task dependencies
test_task_dependencies() {
    echo "Testing task dependencies"
    
    # Add dependencies between tasks
    test_command 'prompt-manager base add-dependency frontend-task backend-task' \
        "Added dependency: frontend-task -> backend-task"
    
    # List dependencies
    test_command 'prompt-manager base list-dependencies frontend-task' "backend-task"
    
    # Test circular dependency detection
    test_command 'prompt-manager base add-dependency backend-task frontend-task' \
        "Error: Circular dependency detected"
}

# Test memory operations
test_memory_operations() {
    echo "Testing memory operations"
    
    # Test context updates
    test_command 'prompt-manager base update-context "Added new feature requirements"' \
        "Context updated"
    
    # Test memory backup
    test_command 'prompt-manager base backup-memory' "Memory backup created"
    
    # Test memory restore
    test_command 'prompt-manager base restore-memory --backup latest' \
        "Memory restored from backup"
}

# Run advanced tests
echo "Running advanced command tests..."

setup_advanced_env
test_bolt_tasks
test_task_filtering
test_task_dependencies
test_memory_operations

echo "Advanced tests completed!" 