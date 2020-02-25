DOCPATH    = ./docs
COV_FMT   ?= html
PIP       ?= $(VENV)/bin/pip
RM         = rm -f

all: help

clean:
	$(RM) -r *~ ./xoinvader/*~ ./xoinvader/tests/*~ ./xoinvader/*.pyc ./xoinvader/tests/*.pyc ./dist ./build
	$(RM) -r *.egg-info
	$(RM) -r ./htmlcov ./docs/build/

install:
	$(PIP) install .

devel:
	poetry install

help:
	@printf "USAGE: make [params]\n"

lint:
	@printf "Warnings are disabled. To full check use 'make lint-full'\n"
	poetry run pytest --pylint -m pylint -vvvv $(PYTEST_ARGS) --pylint-error-types CREF

lint-full:
	poetry run pytest --pylint -m pylint -vvvv $(PYTEST_ARGS) --pylint-error-types CREWF

test:
	poetry run pytest --cov=./xoinvader --cov-report=$(COV_FMT) --strict -v $(PYTEST_ARGS)

view_cov: test
	@xdg-open ./htmlcov/index.html

docs:
	poetry run $(MAKE) -C $(DOCPATH) -f Makefile html SPHINXBUILD=sphinx-build

view_docs: docs
	@xdg-open $(DOCPATH)/build/html/index.html

count:
	@printf "Sources:\n" && git ls-files "*.py" | grep -v "tests\/" | xargs wc -l
	@printf "Tests:\n" && git ls-files "*/tests/*.py" | xargs wc -l
	@printf "Configs:\n" && git ls-files "*.json" | xargs wc -l
	@printf "Documentation:\n" && git ls-files "*.rst" | xargs wc -l
	@printf "All files:\n" && git ls-files "*.rst" "*.py" "*.json" | xargs wc -l | tail -n 1

.PHONY: all clean install devel help lint lint-full test view count docs \
	view_docs
