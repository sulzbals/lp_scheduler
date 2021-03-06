SHELL := bash
PYTHON := python3
PIP := pip3

.DEFAULT_GOAL := all
.PHONY := install all clean purge

venv:
	virtualenv -p $(PYTHON) $@

install: venv
	source $</bin/activate && $(PIP) install .

exemplo%.txt:
	ln -s assets/$@ $@

tarefas: venv install
	echo "#! /usr/bin/env bash" > tarefas
	echo "source $</bin/activate" >> tarefas
	echo "lp-schedule" >> tarefas
	echo "deactivate" >> tarefas
	chmod a+x tarefas

all: exemplo1.txt exemplo2.txt tarefas

clean:
	-rm exemplo*.txt 2&> /dev/null || true
	-rm tarefas 2&> /dev/null || true

purge: clean
	-rm -rf venv 2&> /dev/null || true
