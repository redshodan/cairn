# This file is part of GNU Parted
# Copyright (C) 1999, 2000, 2001 Free Software Foundation, Inc.
#
# This file may be modified and/or distributed without restriction.

SUBDIRS       = amiga ext2 ufs fat ntfs hfs linux_swap xfs jfs reiserfs # bfs

LIBS = @INTLLIBS@ @LIBS@

partedincludedir      =	-I$(top_srcdir)/include
noinst_LTLIBRARIES    =	libfs.la
libfs_la_LDFLAGS  = -version-info $(LT_CURRENT):$(LT_REVISION):$(LT_AGE) \
 			-release $(LT_RELEASE)

libfs_la_LIBADD   = @UUID_LIBS@			\
		    @OS_LIBS@			\
		    @REISER_LIBS@		\
		    amiga/libamigafs.la		\
		    ext2/libext2.la		\
		    ufs/libufs.la		\
		    fat/libfat.la		\
		    ntfs/libntfs.la		\
		    hfs/libhfs.la		\
		    linux_swap/liblinuxswap.la	\
		    xfs/libxfs.la		\
		    jfs/libjfs.la		\
		    reiserfs/libreiserfs.la	
#		    bfs/libbfs.la

libfs_la_SOURCES   = 

INCLUDES = $(partedincludedir) @INTLINCS@

