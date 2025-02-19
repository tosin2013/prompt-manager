# Test Fixes Tracking

## Failed Tests (12)

### Core Functionality (Priority 1)
- [ ] test_list_tasks_command
  - Issue: Task listing output is empty
  - Error: AssertionError: assert 'test task' in ''
  - Status: In Progress

- [ ] test_export_tasks_command
  - Issue: Export file not created
  - Error: AssertionError: assert False (file does not exist)
  - Status: Not Started

### Analysis Commands (Priority 2)
- [ ] test_analyze_repo_command
  - Issue: Command exits with code 2
  - Error: assert 2 == 0
  - Status: Not Started

- [ ] test_llm_commands
  - Issue: Command exits with code 2
  - Error: assert 2 == 0
  - Status: Not Started

### Debug Commands (Priority 3)
- [ ] test_debug_analyze_file
- [ ] test_debug_analyze_file_with_error
- [ ] test_debug_find_root_cause
- [ ] test_debug_iterative_fix
- [ ] test_debug_test_roadmap
- [ ] test_debug_analyze_dependencies
- [ ] test_debug_trace_error
- [ ] test_debug_with_file_purpose
  - Common Issue: All debug commands exit with code 2
  - Error: assert 2 == 0
  - Status: Not Started

## Passed Tests (6)
✅ test_version
✅ test_help
✅ test_init_command
✅ test_add_task_command
✅ test_update_progress_command
✅ test_generate_bolt_tasks_command

## Progress
- Total Tests: 18
- Passed: 6
- Failed: 12
- Success Rate: 33.33%
