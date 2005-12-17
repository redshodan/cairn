BUILD=../../build
BINDIR=$(BUILD)/bin
LIBDIR=$(BUILD)/lib
SCRIPTS=../scripts
PYTHON_FILES=$(shell find cairn -name '*.py')


all: ccopy

ccopy: $(BINDIR)/ccopy

$(LIBDIR)/cairn.zip: $(PYTHON_FILES) clean
	zip -qr $@ cairn

$(BINDIR)/ccopy: $(LIBDIR)/cairn.zip $(SCRIPTS)/runcairn.sh
	cat $(SCRIPTS)/runcairn.sh $(LIBDIR)/cairn.zip > $(BINDIR)/ccopy
	chmod +x $(BINDIR)/ccopy


clean:
	find . -name '*.pyc' | xargs rm -f
	find . -name '*~' | xargs rm -f
	rm -f $(BINDIR)/ccopy $(LIBDIR)/cairn.zip

ls:
	find . -type f | grep -v CVS | grep -ve '*.pyc$$'

lsinc:
	find . -type f -name '*.py' | grep -v .svn | xargs grep -h "import" | grep -v "cairn" | sort | uniq
