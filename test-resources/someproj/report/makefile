# latex document creation make file

# type of project
PROJ_TYPE=		tex
# make modules to add functionality to a build; add tex-index for indexes
PROJ_MODULES=		tex-biber
#PROJ_LOCAL_MODULES=	tex-table tex-graffle
PROJ_LOCAL_MODULES=	tex-graffle

# per make file vars
TEX=			report
TIPATH +=		$(abspath ../sty)
BIB_FILE =		$(abspath ../sty/someproj.bib)

# distribution file name (no extension, post pended by `slides', `report' etc)
FINAL_NAME=		WRITE_ME_Report
# Preview.app top x, y, width, height
PREV_LOC ?=		0 0 1100 1500
# control verbosity
# TEX_QUIET=0

# make build dependencies
_ :=	$(shell cd .. && [ ! -d .git ] && git init ; [ ! -d zenbuild ] && \
	  git submodule add https://github.com/plandes/zenbuild && make gitinit )

include ../zenbuild/main.mk
