/*
 * plppedfilesystemtype.h - definition for PedFileSystemType
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

#ifndef PLPPEDFILESYSTEMTYPE_H
#define PLPPEDFILESYSTEMTYPE_H

#include <Python.h>
#include <parted/parted.h>

struct _plpPedFileSystemType {
  PyObject_HEAD
  const PedFileSystemType *fstype;
};

typedef struct _plpPedFileSystemType _plpPedFileSystemType;
extern _plpPedFileSystemType *new_plppedfilesystemtype(const PedFileSystemType *);
extern PyTypeObject plpPedFileSystemTypeType;

#endif /* PLPPEDFILESYSTEMTYPE_H */
