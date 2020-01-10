## makefile automates the build and deployment for python projects

# type of project
PROJ_TYPE=	python
BIB_FILE=	test-resources/someproj/sty/someproj.bib
TEX_PATH=	test-resources/someproj

include ./zenbuild/main.mk

.PHONY:		testbibkeys
testbibkeys:
	make PYTHON_BIN_ARGS="printbib -m $(BIB_FILE)" run

.PHONY:		testtexkeys
testtexkeys:
	make PYTHON_BIN_ARGS="printtex -t $(TEX_PATH)" run

.PHONY:		testexportkeys
testexportkeys:
	make PYTHON_BIN_ARGS="printexport -m $(BIB_FILE) -t $(TEX_PATH)" run

.PHONY:		testexport
testexport:
	make PYTHON_BIN_ARGS="export -m $(BIB_FILE) -t $(TEX_PATH)" run
