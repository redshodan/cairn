/*
    libparted - a library for manipulating disk partitions
    Copyright (C) 2000 Free Software Foundation, Inc.

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

#include "config.h"

#include <parted/parted.h>
#include <parted/endian.h>

#if ENABLE_NLS
#  include <libintl.h>
#  define _(String) dgettext (PACKAGE, String)
#else
#  define _(String) (String)
#endif /* ENABLE_NLS */

#include <unistd.h>
#include <string.h>


#define NTFS_BLOCK_SIZES       ((int[2]){512, 0})

#define NTFS_SIGNATURE	"NTFS"

static PedGeometry*
ntfs_probe (PedGeometry* geom)
{
	char	buf[512];

	if (!ped_geometry_read (geom, buf, 0, 1))
		return 0;

	if (strncmp (NTFS_SIGNATURE, buf + 3, strlen (NTFS_SIGNATURE)) == 0)
		return ped_geometry_new (geom->dev, geom->start,
					 PED_LE64_TO_CPU (*(uint64_t*)
						 	  (buf + 0x28)));
	else
		return NULL;
}

#ifndef DISCOVER_ONLY
static int
ntfs_clobber (PedGeometry* geom)
{
	char	buf[512];

	memset (buf, 0, 512);
	return ped_geometry_write (geom, buf, 0, 1);
}
#endif /* !DISCOVER_ONLY */

static PedFileSystemOps ntfs_ops = {
	probe:		ntfs_probe,
#ifndef DISCOVER_ONLY
	clobber:	ntfs_clobber,
#else
	clobber:	NULL,
#endif 
	open:		NULL,
	create:		NULL,
	close:		NULL,
	check:		NULL,
	copy:		NULL,
	resize:		NULL,
	get_create_constraint:	NULL,
	get_resize_constraint:	NULL,
	get_copy_constraint:	NULL
};

static PedFileSystemType ntfs_type = {
	next:	NULL,
	ops:	&ntfs_ops,
	name:	"ntfs",
	block_sizes: NTFS_BLOCK_SIZES
};

void
ped_file_system_ntfs_init ()
{
	ped_file_system_type_register (&ntfs_type);
}

void
ped_file_system_ntfs_done ()
{
	ped_file_system_type_unregister (&ntfs_type);
}


