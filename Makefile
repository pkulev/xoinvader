PIP = pip3
PYTHON = python3
PYTEST = py.test-3.4
VENV = ./env
VENV_CMD = virtualenv --python=python3
RM = rm -f

all: help

clean_devel:
	${RM} -r ${VENV} *.egg-info

install:
	${PIP} install .

devel: clean_devel
	${VENV_CMD} ${VENV}
	${PYTHON} setup.py --editable install .

help:
	@printf "USAGE: make [params]\"

lint:
	@find . -name "*.py" -exec pylint -f colorized {} \;

test:
	@${PYTEST} --cov=./xoinvader --cov-report=html --strict

view: test
	@xdg-open ./htmlcov/index.html

count:
	@find . -name "*.py" -not -path "./xoinvader/tests/*" | xargs wc -l game
	@find ./xoinvader/tests -name "*.py" | xargs wc -l
	@find . -name "*.json" | xargs wc -l

.PHONY: help lint test view count all
