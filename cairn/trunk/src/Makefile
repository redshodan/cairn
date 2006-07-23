####
#### CAIRN src makefile
####

TOPDIR=..
include $(TOPDIR)/Makefile.vars


# Vars for auto dir targs
ifeq ($(OS), Linux)
include linux/Makefile.vars
endif
include python/Makefile.vars


all: $(DIR_TARGS)


# Dep rules for auto dir targs
ifeq ($(OS), Linux)
include linux/Makefile.deps
endif
include python/Makefile.deps


include $(TOPDIR)/Makefile.rules
