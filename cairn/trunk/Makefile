####
#### CAIRN top level makefile
####

TOPDIR=.
include $(TOPDIR)/Makefile.vars


#### Vars
3RDPARTY=appweb python
DIRS=build build/appWeb build/python build/lib build/bin build/src
SUBDIRS=src


all: prep $(3RDPARTY) $(SUBDIRS)

prep: $(DIRS)

$(DIRS):
	mkdir $@

$(SUBDIRS):
	make -C $@

#### AppWeb

appweb: $(APPWEB_INST)/lib/libappWebStatic.a

$(APPWEB_BUILD):
	tar -zxf $(APPWEB_SRC) -C build
	touch $(APPWEB_BUILD)

$(APPWEB_INST)/lib/libappWebStatic.a: $(APPWEB_BUILD)
	(INST=`pwd`/$(APPWEB_INST); cd $(APPWEB_BUILD); ./configure --prefix=$${INST} --sbinDir=$${INST}/bin --incDir=$${INST}/include --libDir=$${INST}/lib --webDir=$${INST}/var/web)
	make -C $(APPWEB_BUILD)
	make -C $(APPWEB_BUILD) install-dev


#### Python

python: $(PYTHON_INST)/lib/libpython$(PYTHON_VER).so

$(PYTHON_BUILD):
	tar -jxf $(PYTHON_SRC) -C build
	touch $(PYTHON_BUILD)

$(PYTHON_INST)/lib/libpython$(PYTHON_VER).so: $(PYTHON_BUILD)
	(INST=`pwd`/$(PYTHON_INST); cd $(PYTHON_BUILD); ./configure --enable-shared --prefix=$${INST})
	make -C $(PYTHON_BUILD)
	make -C $(PYTHON_BUILD) install


#### recursion
recurse: $(DO)
	for a in $(SUBDIRS); do cd $$a; make $(DO); cd ..; done

deprecurse: dep
	make

clean:
	rm -f *~
	find build -maxdepth 1 | grep -v CVS | grep -v '^build$$' | grep -v .cvsignore | xargs rm -rf

.PHONY: $(SUBDIRS) appweb python


#### subversion
svnignore:
	misc/svnignore-update.sh
