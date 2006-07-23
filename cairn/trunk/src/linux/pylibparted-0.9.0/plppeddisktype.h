/*
 * plppeddisktype.h - definition for PedDiskType
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

#ifndef PLPPEDDISKTYPE_H
#define PLPPEDDISKTYPE_H

#include <Python.h>
#include <parted/parted.h>

struct _plpPedDiskType {
  PyObject_HEAD
  const PedDiskType *type;
};

typedef struct _plpPedDiskType _plpPedDiskType;
extern _plpPedDiskType *new_plppeddisktype(const PedDiskType *);
extern PyTypeObject plpPedDiskTypeType;

#endif /* PLPPEDDISKTYPE_H */
