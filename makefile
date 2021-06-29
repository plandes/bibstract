## makefile automates the build and deployment for python projects

## build config
PROJ_TYPE =		python
PROJ_MODULES =		python-all
PROJ_MODULES =		git python-resources python-cli python-doc 
INFO_TARGETS +=		appinfo

include ./zenbuild/main.mk

.PHONY:			appinfo
appinfo:
			@echo "app-resources-dir: $(RESOURCES_DIR)"
