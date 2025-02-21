"""Test constants for the prompt manager project."""

# Task Constants
TASK_TITLE = "Test Task"
TASK_DESCRIPTION = "This is a test task"
TASK_TEMPLATE = "Test template"
TASK_PRIORITY = "medium"

# Task Status Values (matching base_commands.py implementation)
TASK_STATUS_PENDING = "todo"
TASK_STATUS_IN_PROGRESS = "in_progress"
TASK_STATUS_DONE = "done"
TASK_STATUS_BLOCKED = "blocked"

# Success Messages
TASK_ADDED_MSG = f"Task '{TASK_TITLE}' added successfully"
TASK_STATUS_UPDATED_MSG = f"Task '{TASK_TITLE}' status updated to {TASK_STATUS_IN_PROGRESS}"
PROJECT_INITIALIZED_MSG = "Initialized project at"

# Error Messages
TASK_NOT_FOUND_ERROR = "Task not found"
INVALID_STATUS_ERROR = "Invalid status"
VALIDATION_ERROR = "Validation error"

# File paths and directories
DEFAULT_EXPORT_PATH = "tasks_export.json"
