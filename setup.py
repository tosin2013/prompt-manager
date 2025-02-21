from setuptools import setup, find_packages

setup(
    name="tosins-prompt-manager",
    version="0.3.18",  # Match the latest tag
    packages=find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests",
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
            'prompt-manager=prompt_manager.cli.__init__:cli',
        ],
    },
    python_requires='>=3.9,<3.14',  # Match pyproject.toml version constraint
    author="Windsurf Team",
    description="A prompt engineering and development workflow management system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="prompt-engineering, development-workflow, ai-assisted, llm-enhancement",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
