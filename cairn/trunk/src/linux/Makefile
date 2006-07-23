####
#### CAIRN src/linux makefile
####

TOPDIR=../..
include $(TOPDIR)/Makefile.vars

include Makefile.vars

LIBS=$(BUILD_LIB)/pylibparted.so

#### Auto dir targs
DIRS=$(PARTED)
$(PARTED)=$(PARTED)/build


all: $(DIR_TARGS) $(LIBS)


#### pylibparted
$(PARTED)/build/lib*/pylibparted.so: $(PARTED)
$(BUILD_LIB)/pylibparted.so: $(PARTED)/build/lib*/pylibparted.so
	cp $< $@

$(PARTED)/build: $(PARTED)
$(BUILD_LIB)/pylibparted.so: $(PARTED)

clean:
	rm $(LIBS)


include $(TOPDIR)/Makefile.rules
