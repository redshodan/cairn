TOPDIR=../../../..
include $(TOPDIR)/Makefile.vars

FILEEXT=c
COMPILER=gcc
FLAGS=-Wall
OBJDIR=build

SRCTARGETS=$(shell find . -maxdepth 1 -name '*.$(FILEEXT)' -print)
OBJTARGETS=$(patsubst %.$(FILEEXT),$(OBJDIR)/%.o,$(SRCTARGETS))


all: $(BUILD_LIB)/libvolumeid.a

build:
	mkdir build

$(BUILD_LIB)/libvolumeid.a: build/libvolumeid.a
	cp $< $@
	strip --strip-debug --strip-unneeded $@

build/libvolumeid.a: $(OBJTARGETS)
	ar r $@ $(OBJTARGETS)

clean:
	rm -rf build $(BUILD_LIB)/libvolumeid.a

$(OBJDIR)/%.o : %.$(FILEEXT) build
	$(COMPILER) -c $(FLAGS) $< -o $@
