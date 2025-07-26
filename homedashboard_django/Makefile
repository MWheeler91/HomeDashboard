SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

PROJECT_NAME=homedashboard
VENV=~/venv/$(PROJECT_NAME)
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

# Set up virtual environment and install requirements
install:
	@echo "Creating venv at $(VENV)"
	python3 -m venv $(VENV)
	@echo "Installing requirements"
	$(PIP) install -r z_requirements/linux_requirements.txt

# Show command to activate the venv
activate:
	@echo "Run: source $(VENV)/bin/activate"

# Run Django dev server
run:
	$(PYTHON) manage.py runserver

# Apply migrations
migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

# Run unit tests
test:
	$(PYTHON) manage.py test

# Format code with black
format:
	black .

# Collect static files
collectstatic:
	$(PYTHON) manage.py collectstatic --noinput

# Clean Python cache files
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

rebuild:
	rm -rf $(VENV)
	$(MAKE) install
