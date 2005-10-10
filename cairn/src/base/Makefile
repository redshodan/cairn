####  General variables. We dont use the default make variables for the
####  compiler and flags because we make our own compile rules.

TOPDIR=../..
include $(TOPDIR)/Makefile.vars

OBJDIR=$(OBJBASE)/base


####
####  Target variables and rules
####
LIB_TARGETS=$(LIBDIR)/libcairnbase.a
BIN_TARGETS=
TARGETS=$(LIB_TARGETS) $(BIN_TARGETS)

$(LIBDIR)/libcairnbase.a=\
	MutexLinux.cpp SemaphoreLinux.cpp

####

OBJTARGETS1=$(foreach TARG,$(TARGETS),$($(TARG)))
OBJTARGETS=$(foreach FILE, $(OBJTARGETS1), $(patsubst %.$(FILEEXT),$(OBJDIR)/%.o,$(FILE)))
LS=$(shell echo * | awk '{split($$0,arr); for (i in arr) printf("-name %s -o ", arr[i]);}')
LIST=$(shell find . \( $(LS) -name x \) -prune -type d -print)


####  Rules for make

ifeq (Makefile.dep,$(wildcard Makefile.dep))
all: $(OBJDIR) $(TARGETS)
else
all: deprecurse
endif


$(OBJDIR):
	mkdir -p $(OBJDIR)

$(BIN_TARGETS): $(OBJTARGETS)
	$(COMPILER) $(FLAGS) -o $(@) $(patsubst %.$(FILEEXT),$(OBJDIR)/%.o,$($(@))) $(LIBFLAGS) $(LIBS)

$(LIB_TARGETS): $(OBJTARGETS)
	ar rc $(@) $(patsubst %.$(FILEEXT),$(OBJDIR)/%.o,$($(@)))
	ranlib $(@)

clean:
	-rm -f Makefile.dep core *.o *~ $(OBJDIR)/*.o $(TARGETS)

recurse: $(DO)
	for a in $(LIST); do cd $$a; make $(DO); cd ..; done

deprecurse: dep
	make

dep: clean
	$(COMPILER) $(FLAGS) -MM *.$(FILEEXT) | \
	awk '$$1 ~ /:/{printf "$(OBJDIR)/%s\n", $$0} $$1 !~ /:/' > Makefile.dep

$(OBJDIR)/%.o : %.$(FILEEXT)
	$(COMPILER) -c $(FLAGS) $< -o $@

ifeq (Makefile.dep,$(wildcard Makefile.dep))
include Makefile.dep
endif
