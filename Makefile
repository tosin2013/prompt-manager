.PHONY: setup test clean build install dev-install

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
PIP=${VENV_NAME}/bin/pip

setup: ${VENV_NAME}/bin/activate

${VENV_NAME}/bin/activate:
	python3 -m venv ${VENV_NAME}
	${PIP} install --upgrade pip
	${PIP} install hatchling
	${PIP} install -e .[dev]

test: setup
	${PYTHON} -m pytest tests/ --cov=prompt_manager -v

clean:
	rm -rf ${VENV_NAME}
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

build: clean setup
	${PYTHON} -m build

install: setup
	${PIP} install -e .

dev-install: setup
	${PIP} install -e .[dev]

lint: setup
	${PYTHON} -m flake8 prompt_manager tests
	${PYTHON} -m black prompt_manager tests --check
	${PYTHON} -m mypy prompt_manager tests

format: setup
	${PYTHON} -m black prompt_manager tests

watch-tests: setup
	${PYTHON} -m pytest-watch -- tests/ -v

.DEFAULT_GOAL := setup
