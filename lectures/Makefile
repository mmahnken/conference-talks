# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -c .. -a -n
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

NAME          = $(shell basename $(shell pwd))
SSH_HOST      = fellowship@fellowship.hackbrightacademy.com
SSH_DIR       = fellowship.hackbrightacademy.com/lectures/
SSH_URL       = http://fellowship.hackbrightacademy.com/materials/lectures/
SSH_DIR_SLIDE = fellowship.hackbrightacademy.com/slides/
SSH_URL_SLIDE = http://fellowship.hackbrightacademy.com/materials/slides/

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: help clean revealjs handouts latexpdf linkcheck upload

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  revealjs   to make slides"
	@echo "  handouts   to make standalone HTML files"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  upload     upload to server (builds first)"

clean:
	rm -rf $(BUILDDIR)/*
	rm -f /tmp/$(NAME).zip

revealjsi:
	$(SPHINXBUILD) -b revealjs $(ALLSPHINXOPTS) $(BUILDDIR)/revealjs

revealjs: revealjsi
	@echo
	@echo "Build finished. The slides are in $(BUILDDIR)/revealjs."
	@open $(BUILDDIR)/revealjs/index.html

handoutsi:
	$(SPHINXBUILD) -b handouts $(ALLSPHINXOPTS) $(BUILDDIR)/handouts

handouts: handoutsi
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/handouts."
	open $(BUILDDIR)/handouts/index.html

skiti:
	HANDOUTS_THEME=skit $(SPHINXBUILD) -b handouts $(ALLSPHINXOPTS)/skit $(BUILDDIR)/skit

skit: skiti
	prince $(BUILDDIR)/skit/index.html $(BUILDDIR)/skit/skit.pdf
	open $(BUILDDIR)/skit/skit.pdf

latexpdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."
	open $(BUILDDIR)/latex/[A-Z]*.pdf

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

demozip:
	if [ -d *-demo* ]; then zip -r /tmp/$(NAME).zip *-demo* -x *-demo/env/\*; fi

upload: handoutsi revealjsi demozip
	ssh $(SSH_HOST) rm -rf $(SSH_DIR)$(NAME)
	scp -r _build/handouts $(SSH_HOST):$(SSH_DIR)$(NAME)
	if [ -d *-demo* ]; then scp /tmp/$(NAME).zip $(SSH_HOST):$(SSH_DIR); fi
	open $(SSH_URL)$(NAME)
	ssh $(SSH_HOST) rm -rf $(SSH_DIR_SLIDE)$(NAME)
	scp -r _build/revealjs $(SSH_HOST):$(SSH_DIR_SLIDE)$(NAME)
	open $(SSH_URL_SLIDE)$(NAME)
	rm -f /tmp/$(NAME).zip
	rm -rf $(BUILDDIR)/*

