.PHONY: all setup
# make >debug.log 2>&1
# git remote prune origin
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
else
PYTHON = ./venv/bin/python
endif

SOURCE = source

FLAKE8 = $(PYTHON) -m flake8
PYLINT = $(PYTHON) -m pylint
PIP = $(PYTHON) -m pip install

MP3 = \
xxx.mp3 \

RTTM = $(addprefix build/,$(subst .mp3,.rttm,$(MP3)))

all:
	$(PYTHON) -m pydocstyle $(SOURCE)
	$(FLAKE8) $(SOURCE)
	$(PYLINT) $(SOURCE)

build/%.rttm: build/%.mp3
	$(PYTHON) $(SOURCE)/to_rttm.py --config nemo.config/diar_infer_telephonic.yaml --temp_folder build/temp $< $@

rttm: $(RTTM)

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -c constraints.txt -r requirements.txt
	$(PIP) -r dev.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
