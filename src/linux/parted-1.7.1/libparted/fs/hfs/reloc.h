/*
    libparted - a library for manipulating disk partitions
    Copyright (C) 2004 Free Software Foundation, Inc.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
*/

#ifndef _RELOC_H
#define _RELOC_H

#include <parted/parted.h>
#include <parted/endian.h>
#include <parted/debug.h>

#include "hfs.h"

int
hfs_update_mdb (PedFileSystem *fs);

int
hfs_pack_free_space_from_block (PedFileSystem *fs, unsigned int fblock,
			        PedTimer* timer, unsigned int to_free);

#endif /* _RELOC_H */
