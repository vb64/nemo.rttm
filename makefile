.PHONY: all setup
# make >debug.log 2>&1
# git remote prune origin
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
endif

SOURCE = source

FLAKE8 = $(PYTHON) -m flake8
PYLINT = $(PYTHON) -m pylint
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
PIP = $(PYTHON) -m pip install


all:
	$(PYTHON) -m pydocstyle $(SOURCE)
	$(FLAKE8) $(SOURCE)
	$(PYLINT) $(SOURCE)

rttm:
	$(PYTHON) $(SOURCE)/to_rttm.py --config nemo.config/diar_infer_telephonic.yaml --temp_folder build/temp fixtures/mono.wav

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt
	$(PIP) -r dev.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
