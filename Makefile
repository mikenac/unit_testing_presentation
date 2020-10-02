VIRTUALENV = virtualenv --python=python3
VENV_DIR = .venv
VENV := $(if $(VIRTUAL_ENV),$(VIRTUAL_ENV),$(VENV_DIR))
PYTHON = $(VENV)/bin/python
REQ_STAMP = $(VENV)/.req_stamp

# editable
MODULE_PATH=$(shell pwd)/todo_module

.DEFAULT: help
help:
	@echo "make init"
	@echo "		prepare development environment and create virtualenv"
	@echo "make test"
	@echo "		run lint and unit tests"
	@echo "make lint"
	@echo "		run lint only"
	@echo "make dep"
	@echo "		dump the current pip packages to requirements.txt"
	@echo "make clean"
	@echo "		clean compiled files and the virtual environment"

virtualenv: $(PYTHON) # creates a virtual environment

# one time virtualenv setup
$(PYTHON):
	@$(VIRTUALENV) $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install --upgrade setuptools
	@$(VENV)/bin/pip install pylint
	@$(VENV)/bin/pip install coverage

init: virtualenv $(REQ_STAMP) # will run any time the requirements.txt file has been updated

$(REQ_STAMP): requirements.txt # install all module requirements
	@$(VENV)/bin/pip install -Ur requirements.txt
	@touch $(REQ_STAMP)

lint:
	@$(VENV)/bin/pylint -j 4 ${MODULE_PATH}/*.py

test: init
		@$(VENV)/bin/coverage erase
		@$(VENV)/bin/coverage run -m unittest discover -s tests/unit
		@$(VENV)/bin/coverage report

int_test: init
	@$(VENV)/bin/python -m unittest discover -s tests/integration
	
dep:
	@$(VENV)/bin/pip freeze > requirements.txt

clean:
	@rm -rf $(VENV)
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name .coverage -delete

.PHONY: init test lint dep

 