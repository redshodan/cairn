####
#### CAIRN src makefile
####

TOPDIR=../..
include $(TOPDIR)/Makefile.vars

PYDIRS=cairn thirdparty
PYTHON_FILES=$(shell find $(PYDIRS) -name '*.py')
CLIBS=
ifeq ($(TARGET_OS),Linux)
CLIBS+=$(BUILD_LIB)/pylibparted.so $(BUILD_LIB)/klogctl.so
endif


all: cairn

cairn: $(BUILD_BIN)/cairn

$(BUILD_LIB)/cairn.zip: $(PYTHON_FILES) $(CLIBS)
	make clean
	tar --exclude .svn -cf - $(PYDIRS) | tar -C $(BUILD_SRC) -xf -
	sed -e 's/^SVNREV = .*/SVNREV = $(SVNREV)/' $(BUILD_SRC)/cairn/Version.py > $(BUILD_SRC)/cairn/Version.py.tmp
	mv -f $(BUILD_SRC)/cairn/Version.py.tmp $(BUILD_SRC)/cairn/Version.py
ifeq ($(TARGET_OS),Linux)
	cp $(BUILD_LIB)/pylibparted.so $(BUILD_SRC)/thirdparty
	cp $(BUILD_LIB)/klogctl.so $(BUILD_SRC)/thirdparty
endif
	(cd $(BUILD_SRC); zip -qr ../lib/cairn.zip $(PYDIRS))

$(BUILD_BIN)/cairn: $(BUILD_LIB)/cairn.zip $(SCRIPTS)/runcairn.sh
	cat $(SCRIPTS)/runcairn.sh $(BUILD_LIB)/cairn.zip > $(BUILD_BIN)/cairn
	chmod +x $(BUILD_BIN)/cairn
	ln -s cairn $(BUILD_BIN)/ccopy
	ln -s cairn $(BUILD_BIN)/crestore
	ln -s cairn $(BUILD_BIN)/cextract

clean:
	find . -name '*.pyc' | xargs rm -f
	find . -name '*~' | xargs rm -f
	rm -f $(BUILD_BIN)/cairn $(BUILD_BIN)/ccopy $(BUILD_BIN)/crestore $(BUILD_BIN)/cextract $(BUILD_LIB)/cairn.zip
	rm -rf $(BUILD_SRC)/cairn


include $(TOPDIR)/Makefile.rules
