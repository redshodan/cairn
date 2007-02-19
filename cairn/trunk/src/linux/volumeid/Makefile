TOPDIR=../../..
include $(TOPDIR)/Makefile.vars


all: $(BUILD_LIB)/volumeid.so

$(BUILD_LIB)/volumeid.so: build/lib*/volumeid.so
	cp $< $@
	strip --strip-debug --strip-unneeded $@

build/lib*/volumeid.so: volumeid.c setup.py $(BUILD_LIB)/libvolumeid.a
	python setup.py clean
	python setup.py build

$(BUILD_LIB)/libvolumeid.a:
	make -C volume_id

clean:
	rm -rf build
	make -C volume_id clean
