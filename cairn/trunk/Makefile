####
#### CAIRN top level makefile
####

TOPDIR=.
include $(TOPDIR)/Makefile.vars


#### Vars
BUILD_DIRS=build build/python build/lib build/bin build/src
DIRS=src


all: prep $(DIRS) #python

prep: $(BUILD_DIRS)

$(BUILD_DIRS):
	mkdir $@

$(DIRS):
	make -C $@


#### Python

python: $(PYTHON_INST)/lib/libpython$(PYTHON_VER).so

$(PYTHON_BUILD):
	tar -jxf $(PYTHON_SRC) -C build
	touch $(PYTHON_BUILD)

$(PYTHON_INST)/lib/libpython$(PYTHON_VER).so: $(PYTHON_BUILD)
	(INST=`pwd`/$(PYTHON_INST); cd $(PYTHON_BUILD); ./configure --enable-shared --prefix=$${INST})
	make -C $(PYTHON_BUILD)
	make -C $(PYTHON_BUILD) install


clean:
	rm -rf build


include $(TOPDIR)/Makefile.rules

.PHONY: $(SUBDIRS) $(DIRS) python
