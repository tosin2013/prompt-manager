from setuptools import setup, find_packages

setup(
    name="prompt-manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0.1",
        "typing-extensions>=4.7.1",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
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
            'prompt-manager=prompt_manager:main',
        ],
    },
    python_requires='>=3.8',
    author="Windsurf Team",
    description="A prompt engineering and development workflow management system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="prompt-engineering, development-workflow, ai-assisted",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
