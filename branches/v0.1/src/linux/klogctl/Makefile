TOPDIR=../../..
include $(TOPDIR)/Makefile.vars


all: $(BUILD_LIB)/klogctl.so

$(BUILD_LIB)/klogctl.so: build/lib*/klogctl.so
	cp $< $@
	strip --strip-debug --strip-unneeded $@

build/lib*/klogctl.so: klogctl.c setup.py
	python setup.py clean
	python setup.py build


clean:
	rm -rf build
