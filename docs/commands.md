Usage: prompt-manager [OPTIONS] COMMAND [ARGS]...

  Prompt Manager CLI - Development workflow management system.

Options:
  --version           Show the version and exit.
  --project-dir PATH  Project directory
  --help              Show this message and exit.

Commands:
  add-task         Add a new task.
  base             Base commands.
  debug            Debug commands.
  improve          Self-improvement commands.
  init             Initialize a new project.
  list-tasks       List all tasks.
  llm              LLM commands.
  memory           Memory commands.
  repo             Repository commands.
  update-progress  Update task progress status.
Usage: prompt-manager add-task [OPTIONS] TITLE [DESCRIPTION]

  Add a new task.

Options:
  -t, --template TEXT             Task template
  -p, --priority [low|medium|high]
                                  Task priority
  --help                          Show this message and exit.
Usage: prompt-manager base [OPTIONS] COMMAND [ARGS]...

  Base commands.

Options:
  --help  Show this message and exit.

Commands:
  add-dependency       Add a dependency between tasks.
  add-task             Add a new task.
  backup-memory        Create a backup of memory files.
  export-tasks         Export tasks to a file.
  generate-bolt-tasks  Generate tasks for a bolt.new project.
  init                 Initialize a new project.
  list-dependencies    List task dependencies.
  list-tasks           List tasks with filtering and sorting.
  restore-memory       Restore memory from a backup.
  update-context       Update project context with a message.
  update-progress      Update task progress status.
Usage: prompt-manager debug [OPTIONS] COMMAND [ARGS]...

  Debug commands.

Options:
  --help  Show this message and exit.

Commands:
  analyze-dependencies  Analyze dependencies of a file.
  analyze-file          Analyze a file for potential issues.
  find-root-cause       Find root cause from error log.
  test-roadmap          Generate test roadmap for a file.
  trace-error           Trace error through the codebase.
Usage: prompt-manager improve [OPTIONS] COMMAND [ARGS]...

  Self-improvement commands.

Options:
  --help  Show this message and exit.

Commands:
  enhance  Enhance system components.
Usage: prompt-manager llm [OPTIONS] COMMAND [ARGS]...

  LLM commands.

Options:
  --help  Show this message and exit.

Commands:
  analyze-impact        Analyze impact of changes in a file.
  analyze-repo          Analyze repository changes.
  create-pr             Create a pull request.
  generate-commands     Generate CLI commands from file.
  list-templates        List all available prompt templates.
  suggest-improvements  Suggest code improvements.
Usage: prompt-manager memory [OPTIONS] COMMAND [ARGS]...

  Memory commands.

Options:
  --help  Show this message and exit.

Commands:
  list-all  List all stored memories.
  retrieve  Retrieve value from memory.
  store     Store value in memory.
Usage: prompt-manager repo [OPTIONS] COMMAND [ARGS]...

  Repository commands.

Options:
  --help  Show this message and exit.

Commands:
  analyze-repo   Analyze repository changes.
  learn-session  Start a learning session for repository understanding.
Usage: prompt-manager update-progress [OPTIONS] TITLE {not_started|in_progress
                                      |completed|blocked|cancelled}

  Update task progress status.

Options:
  -n, --note TEXT  Progress note
  --help           Show this message and exit.
