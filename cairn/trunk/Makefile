####
#### CAIRN top level makefile
####

#### Notes
#
# You can build in a cross platform fashion by setting the make variable
# TARGET_OS. Current values can be Linux or Darwin. C code will not be compiled
# so prebuilt libraries must be manually copied into build/lib before making
# the final cairn binary.


TOPDIR=.
include $(TOPDIR)/Makefile.vars


#### Vars
BUILD_DIRS=build/python build/lib build/bin build/src build/trac
DIRS=src


all: prep $(DIRS) #python

prep: $(BUILD_DIRS)

build:
	mkdir build

$(BUILD_DIRS): build
	if [ -d $@ ]; then touch $@; else mkdir $@; fi

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

todo: build/trac
	misc/buildtodo $(TOPDIR)/TODO


clean:
	rm -rf build


include $(TOPDIR)/Makefile.rules

.PHONY: $(DIRS) python svnignore todo
