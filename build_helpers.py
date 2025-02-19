"""Helper functions for building the package."""
import os
import shutil
import subprocess
from pathlib import Path


def clean_bazel_artifacts():
    """Clean up all Bazel-related artifacts."""
    # Run bazel clean --expunge
    try:
        subprocess.run(['bazel', 'clean', '--expunge'], check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        pass  # Ignore if bazel is not installed or command fails

    # Get the project root directory
    project_root = Path(__file__).parent.absolute()

    # List of Bazel-related patterns to remove
    bazel_patterns = [
        'bazel-*',
        'bazel-bin',
        'bazel-out',
        'bazel-testlogs',
        'bazel-prompt-manager'
    ]

    # Remove Bazel symlinks and directories
    for pattern in bazel_patterns:
        # Handle exact matches
        path = project_root / pattern
        if path.is_symlink():
            path.unlink()
        elif path.exists():
            shutil.rmtree(path)

        # Handle wildcard patterns
        if '*' in pattern:
            for item in project_root.glob(pattern):
                if item.is_symlink():
                    item.unlink()
                elif item.exists():
                    shutil.rmtree(item)

    # Remove any remaining Bazel symlinks by checking all items in root
    for item in project_root.iterdir():
        if item.is_symlink() and 'bazel' in item.name:
            item.unlink()


if __name__ == '__main__':
    clean_bazel_artifacts()
