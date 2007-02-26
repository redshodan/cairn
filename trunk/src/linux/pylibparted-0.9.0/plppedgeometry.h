/*
 * plppedgeometry.h - definition for PedGeometry
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

#ifndef PLPPEDGEOMETRY_H
#define PLPPEDGEOMETRY_H

#include <Python.h>
#include <parted/parted.h>

struct _plpPedGeometry {
  PyObject_HEAD
  PedGeometry *geom;
  int native;
};

typedef struct _plpPedGeometry plpPedGeometry;
extern plpPedGeometry *new_plppedgeometry(PedGeometry *, int);
extern PyTypeObject plpPedGeometryType;

#endif /* PLPPEDGEOMETRY_H */
