DOCPATH=./docs
PIP = pip3
PYTHON = python3
PYTEST = py.test-3.4
VENV = ./env
VENV_CMD = virtualenv --python=python3
RM = rm -f

all: help

clean:
	${RM} -r *~ ./xoinvader/*~ ./xoinvader/tests/*~
	${RM} -r ${VENV} *.egg-info
	${RM} -r ./htmlcov

install:
	${PIP} install .

devel: clean_devel
	${VENV_CMD} ${VENV}
	${PYTHON} setup.py --editable install .

help:
	@printf "USAGE: make [params]\n"

lint:
	@find . -name "*.py" -exec pylint -f colorized {} \;

test:
	@${PYTEST} --cov=./xoinvader --cov-report=html --strict -v

view_cov: test
	@xdg-open ./htmlcov/index.html

docs:
	${MAKE} -C ${DOCPATH} -f Makefile html

view_docs: docs
	@xdg-open ${DOCPATH}/build/html/index.html

count:
	@find . -name "*.py" -not -path "./xoinvader/tests/*" | xargs wc -l game
	@find ./xoinvader/tests -name "*.py" | xargs wc -l
	@find . -name "*.json" | xargs wc -l

.PHONY: all clean install devel help lint test view count docs view_docs
