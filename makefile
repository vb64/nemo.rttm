.PHONY: all setup
# make >debug.log 2>&1
# git remote prune origin
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

SOURCE = source
TESTS = tests

FLAKE8 = $(PYTHON) -m flake8
PYLINT = $(PYTHON) -m pylint
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
PIP = $(PYTHON) -m pip install

MP3 = \
xxx.mp3 \

RTTM = $(addprefix build/,$(subst .mp3,.rttm,$(MP3)))

all: tests

flake8:
	$(FLAKE8) $(TESTS)/test
	$(FLAKE8) $(SOURCE)

lint:
	$(PYLINT) $(SOURCE)
	$(PYLINT) $(TESTS)/test

pep257:
	$(PYTHON) -m pydocstyle $(TESTS)/test
	$(PYTHON) -m pydocstyle $(SOURCE)

test:
	$(PTEST) -s $(TESTS)/test/$(T)

tests: flake8 pep257 lint
	$(PYTEST) -m "not longrunning" --durations=5 $(TESTS)

cover: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

build/%.rttm: build/%.mp3
	$(PYTHON) $(SOURCE)/to_rttm.py --config nemo.config/diar_infer_telephonic.yaml --temp_folder build/temp $< $@

rttm: $(RTTM)

setup: setup_python setup_pip

setup_win10: setup_python setup_pip_win10

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -c constraints.txt -r requirements.txt
	$(PIP) -r dev.txt

setup_pip_win10:
	$(PIP) --upgrade pip
	$(PIP) -c constraints_win10.txt -r requirements.txt
	$(PIP) -r dev.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
