import os
from setuptools import setup, find_packages

# Clean up Bazel symlinks if they exist
bazel_symlinks = ['bazel-bin', 'bazel-out', 'bazel-testlogs', 'bazel-prompt-manager']
for link in bazel_symlinks:
    if os.path.islink(link):
        os.unlink(link)

setup(
    name="prompt-manager",
    version="0.3.4",
    packages=find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests",
        "bazel-*", "bazel-bin", "bazel-out", "bazel-testlogs",
        "*.egg-info", "*.egg-info.*",
        "build", "dist"
    ]),
    package_data={
        "prompt_manager": ["py.typed", "**/*.py", "**/*.pyi"],
    },
    install_requires=[
        "pyyaml>=6.0.1",
        "typing-extensions>=4.7.1",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "click>=8.0.0",
        "gitpython>=3.1.0",
        "uuid>=1.30",
    ],
    extras_require={
        'dev': [
            'black',
            'flake8',
            'mypy',
            'pytest-watch',
        ]
    },
    entry_points={
        'console_scripts': [
            'prompt-manager=prompt_manager.cli:cli',
        ],
    },
    python_requires='>=3.8',
    author="Windsurf Team",
    description="A prompt engineering and development workflow management system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="prompt-engineering, development-workflow, ai-assisted, llm-enhancement",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
