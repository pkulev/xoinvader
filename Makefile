all: help

install:
	pip3 install .

devel:
	python3 setup.py --editable install .

help:
	@printf "USAGE: make [params]\"

lint:
	@find . -name "*.py" -exec pylint -f colorized {} \;

count:
	@find . -name "*.py" | xargs wc -l
	@find . -name "*.json" | xargs wc -l

.PHONY: help lint count all
