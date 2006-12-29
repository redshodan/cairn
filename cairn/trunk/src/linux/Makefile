####
#### CAIRN src/linux makefile
####

TOPDIR=../..
include $(TOPDIR)/Makefile.vars

include Makefile.vars

LIBS=$(BUILD_LIB)/libparted.a $(BUILD_LIB)/pylibparted.so $(BUILD_LIB)/klogctl.so

#### Auto dir targs
DIRS=$(PARTED) $(PYPARTED) klogctl
$(PYPARTED)=$(PYPARTED)/build


all: $(LIBS)


#### klogctl
$(BUILD_LIB)/klogctl.so:
	make -C klogctl

#### pylibparted
$(PYPARTED):
	make -C $(PYPARTED)

$(PYPARTED)/build/lib*/pylibparted.so: $(BUILD_LIB)/libparted.a $(PYPARTED)

$(BUILD_LIB)/pylibparted.so: $(PYPARTED)/build/lib*/pylibparted.so
	cp $< $@
	strip --strip-debug --strip-unneeded $@


$(PYPARTED)/build: $(PYPARTED)
$(BUILD_LIB)/pylibparted.so: $(PYPARTED)

#### libparted
$(PARTED)/Makefile:
	(cd $(PARTED); ./configure --prefix=`pwd`/../$(BUILD) --without-readline --disable-dependency-tracking --enable-shared=no --disable-nls)

$(BUILD_LIB)/libparted.a: $(PARTED)/Makefile
	make -C $(PARTED)
	make -C $(PARTED) install

clean:
	for a in $(DIRS); do make -C $$a distclean; make -C $$a clean; done
	rm -f $(LIBS)


include $(TOPDIR)/Makefile.rules

.PHONY: $(PYPARTED)
