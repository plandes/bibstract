# GNU make file to automate build of all latex documents

SUBS=paper report slides letter

all:		pdf

# generate all PDFs
.PHONY:		pdf
pdf:
		@for i in $(SUBS) ; do \
			if [ -d $$i ] ; then \
				make -C $$i pdf ; \
			fi \
		done

.PHONY:		dist
dist:		pdf
		@for i in $(SUBS) ; do \
			if [ -d $$i ] ; then \
				cp $$i/target/$$i.pdf $(HOME)/Desktop ; \
			fi \
		done

# generate and show all PDFs
.PHONY:		showpdf
showpdf:
		@for i in $(SUBS) ; do \
			[ -d $$i ] && make -C $$i showpdf ; \
		done

# clean up all generated objects
.PHONY:		clean
clean:
		@for i in $(SUBS) ; do \
			[ -d $$i ] && make -C $$i clean ; \
		done

# select a paper project
.PHONY:		keeppaper
keeppaper:
		rm -rf report slides letter

# select a slides project
.PHONY:		keepslides
keepslides:
		rm -rf paper report letter

# select a academic project
.PHONY:		keepacademic
keepacademic:
		rm -rf report letter

# select a letter
.PHONY:		keepletter
keepletter:
		rm -rf paper report slides graffle vec sty
