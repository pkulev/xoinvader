DOCPATH=./docs
PYVERSION ?= 3
VENV = .venv
VENV_CMD = virtualenv --python=python$(PYVERSION)
PYTHON ?= $(VENV)/bin/python$(PYVERSION)
PYTEST = $(VENV)/bin/py.test
PIP ?= $(VENV)/bin/pip
RM = rm -f

all: help

clean:
	$(RM) -r *~ ./xoinvader/*~ ./xoinvader/tests/*~ ./xoinvader/*.pyc ./xoinvader/tests/*.pyc ./dist ./build
	$(RM) -r $(VENV) *.egg-info
	$(RM) -r ./htmlcov ./docs/build/

install:
	$(PIP) install .

devel:
	$(VENV_CMD) $(VENV)
	$(PIP) install -r dev-requirements.txt
	$(PIP) install hg+https://bitbucket.org/pygame/pygame
	$(PIP) install -e .

help:
	@printf "USAGE: make [params]\n"

lint:
	@find . -name "*.py" -exec pylint -f colorized {} \;

test:
	@$(PYTEST) --cov=./xoinvader --cov-report=html --strict -v

view_cov: test
	@xdg-open ./htmlcov/index.html

docs:
	$(MAKE) -C $(DOCPATH) -f Makefile html SPHINXBUILD="$(CURDIR)/$(VENV)/bin/sphinx-build"

view_docs: docs
	@xdg-open $(DOCPATH)/build/html/index.html

count:
	@find . -name "*.py" -not -path "./xoinvader/tests/*" | xargs wc -l game
	@find ./xoinvader/tests -name "*.py" | xargs wc -l
	@find . -name "*.json" | xargs wc -l

.PHONY: all clean install devel help lint test view count docs view_docs
