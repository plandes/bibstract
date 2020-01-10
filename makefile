## makefile automates the build and deployment for python projects

# type of project
PROJ_TYPE=	python
CONF_FILE=	resources/test.bib

include ./zenbuild/main.mk

.PHONY:		testrun
testrun:
	make PYTHON_BIN_ARGS="print -m $(CONF_FILE)" run
