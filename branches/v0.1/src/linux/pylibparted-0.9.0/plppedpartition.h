/*
 * plppedpartition.h - definition for PedPartition
 * Copyright (C) 2005 Ulisses Furquim <ulissesf@gmail.com>
 *
 * This file is part of pylibparted.
 *
 * pylibparted is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * pylibparted is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with pylibparted; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,MA 02110-1301, USA
 */

#ifndef PLPPEDPARTITION_H
#define PLPPEDPARTITION_H

#include <Python.h>
#include <parted/parted.h>

#include <linux/types.h>

struct _plpPedPartition {
  PyObject_HEAD
  PedPartition *part;
  int native;
};

typedef struct _plpPedPartition plpPedPartition;
extern plpPedPartition *new_plppedpartition(PedPartition *, int);
extern PyTypeObject plpPedPartitionType;

/*
 * Ripped from libparted source (version 1.6.22)
 */
typedef struct {
  __u8         head;
  __u8         sector;
  __u8         cylinder;
} __attribute__((packed)) RawCHS;

/* ripped from Linux source */
struct _DosRawPartition {
  __u8            boot_ind;       /* 00:  0x80 - active */
  RawCHS          chs_start;      /* 01: */
  __u8            type;           /* 04: partition type */
  RawCHS          chs_end;        /* 05: */
  __u32           start;          /* 08: starting sector counting from 0 */
  __u32           length;         /* 0c: nr of sectors in partition */
} __attribute__((packed));

typedef struct _DosRawPartition DosRawPartition;

typedef struct {
  PedGeometry     geom;
  DosRawPartition raw_part;
  PedSector       lba_offset;     /* needed for computing start/end for
				   * logical partitions */
} OrigState;

typedef struct {
  unsigned char   system;
  int             boot;
  int             hidden;
  int             raid;
  int             lvm;
  int             lba;
  int             palo;
  int             prep;
  OrigState      *orig;                   /* used for CHS stuff */
} DosPartitionData;

#endif /* PLPPEDPARTITION_H */
