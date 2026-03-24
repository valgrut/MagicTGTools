VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

run: install
		$(PYTHON) -m flask run

install:
		python3 -m venv $(VENV)
		$(PIP) install -r requirements.txt
