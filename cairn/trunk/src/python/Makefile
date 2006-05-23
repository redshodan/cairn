BUILD=../../build
BINDIR=$(BUILD)/bin
LIBDIR=$(BUILD)/lib
SCRIPTS=../scripts
PYTHON_FILES=$(shell find cairn -name '*.py')


all: cairn

cairn: $(BINDIR)/cairn

$(LIBDIR)/cairn.zip: $(PYTHON_FILES) clean
	zip -qr $@ cairn

$(BINDIR)/cairn: $(LIBDIR)/cairn.zip $(SCRIPTS)/runcairn.sh
	cat $(SCRIPTS)/runcairn.sh $(LIBDIR)/cairn.zip > $(BINDIR)/cairn
	chmod +x $(BINDIR)/cairn
	ln -s cairn $(BINDIR)/ccopy
	ln -s cairn $(BINDIR)/crestore

clean:
	find . -name '*.pyc' | xargs rm -f
	find . -name '*~' | xargs rm -f
	rm -f $(BINDIR)/cairn $(BINDIR)/ccopy $(BINDIR)/crestore $(LIBDIR)/cairn.zip

ls:
	find . -type f | grep -v CVS | grep -ve '*.pyc$$'

lsinc:
	find . -type f -name '*.py' | grep -v .svn | xargs grep -h "import" | grep -v "cairn" | sort | uniq
