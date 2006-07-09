BUILD=../../build
BINDIR=$(BUILD)/bin
LIBDIR=$(BUILD)/lib
SRCDIR=$(BUILD)/src
SCRIPTS=../scripts
PYDIRS=cairn thirdparty
PYTHON_FILES=$(shell find $(PYDIRS) -name '*.py')
SVNREV = $(shell svn info | awk '/^Revision:/{print $$2;}')


All: cairn

cairn: $(BINDIR)/cairn

$(LIBDIR)/cairn.zip: $(PYTHON_FILES) clean
	tar --exclude .svn -cf - $(PYDIRS) | tar -C $(SRCDIR) -xf -
	sed -e 's/^SVNREV = .*/SVNREV = $(SVNREV)/' $(SRCDIR)/cairn/Version.py > $(SRCDIR)/cairn/Version.py.tmp
	mv -f $(SRCDIR)/cairn/Version.py.tmp $(SRCDIR)/cairn/Version.py
	(cd $(SRCDIR); zip -qr ../lib/cairn.zip $(PYDIRS))

$(BINDIR)/cairn: $(LIBDIR)/cairn.zip $(SCRIPTS)/runcairn.sh
	cat $(SCRIPTS)/runcairn.sh $(LIBDIR)/cairn.zip > $(BINDIR)/cairn
	chmod +x $(BINDIR)/cairn
	ln -s cairn $(BINDIR)/ccopy
	ln -s cairn $(BINDIR)/crestore
	ln -s cairn $(BINDIR)/cextract

clean:
	find . -name '*.pyc' | xargs rm -f
	find . -name '*~' | xargs rm -f
	rm -f $(BINDIR)/cairn $(BINDIR)/ccopy $(BINDIR)/crestore $(BINDIR)/cextract $(LIBDIR)/cairn.zip
	rm -rf $(SRCDIR)/cairn

ls:
	find . -type f | grep -v .svn | grep -ve '*.pyc$$'

lsinc:
	find . -type f -name '*.py' | grep -v .svn | xargs grep -h "import" | grep -v "cairn" | sort | uniq
