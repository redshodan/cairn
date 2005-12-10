####
#### CAIRN src makefile
####

TOPDIR=..
include $(TOPDIR)/Makefile.vars


#### Targets
DIRS=base appweb util python

base=$(LIBDIR)/libcairnbase.a
appweb=$(LIBDIR)/libcairnappweb.a
util=$(BINDIR)/cutil
python=$(BINDIR)/ccopy


#### Automatic vars
TARGETS=$(foreach TARG,$(DIRS),$($(TARG)))
PYTHON_FILES=$(shell find python -name '*.py')


all: $(TARGETS)


#### Targets dependencies
$(LIBDIR)/libcairnbase.a: base base/*
$(LIBDIR)/libcairnappweb.a: appweb appweb/*
$(BINDIR)/cutil: util util/* $(LIBDIR)/libcairnbase.a $(LIBDIR)/libcairnappweb.a
$(BINDIR)/ccopy: python $(PYTHON_FILES) scripts/runcairn.sh


$(TARGETS):
	make -C $<

base: 


#### recursion
recurse: $(DO)
	for a in $(DIRS); do cd $$a; make $(DO); cd ..; done

deprecurse: dep
	make

dep:
	for a in $(DIRS); do cd $$a; make dep; cd ..; done

clean:
	for a in $(DIRS); do cd $$a; make clean; cd ..; done
