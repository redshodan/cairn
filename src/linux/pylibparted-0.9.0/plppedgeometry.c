/*
 * plppedgeometry.c - implementation of PedGeometry
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

#include "plp.h"
#include "plppedgeometry.h"
#include "plppeddevice.h"
#include "plppedfilesystemtype.h"
#include "plppedalignment.h"
#include "plppedconstraint.h"
#include "plppedfilesystem.h"
#include "plppedexception.h"
#include "plppedtimer.h"

/* plpPedGeometry factory function */

plpPedGeometry *new_plppedgeometry(PedGeometry *geom, int native)
{
  plpPedGeometry *ret;

  if (!(ret = (plpPedGeometry *)plpPedGeometryType.tp_alloc(&plpPedGeometryType, 0)))
    return NULL;

  ret->geom = geom;
  ret->native = native;

  return ret;
}

/* plpPedGeometry methods */

PyDoc_STRVAR(getStart__doc__,
"Description: returns the start of the region (in sectors)\n"
"Receives: nothing\n"
"Returns: a long object\n");
static PyObject *getStart(plpPedGeometry *s)
{
  return PyLong_FromLongLong(s->geom->start);
}

PyDoc_STRVAR(getEnd__doc__,
"Description: returns the end of the region (in sectors)\n"
"Receives: nothing\n"
"Returns: a long object\n");
static PyObject *getEnd(plpPedGeometry *s)
{
  return PyLong_FromLongLong(s->geom->end);
}

PyDoc_STRVAR(getLength__doc__,
"Description: returns the length of the region (in sectors)\n"
"Receives: nothing\n"
"Returns: a long object\n");
static PyObject *getLength(plpPedGeometry *s)
{
  return PyLong_FromLongLong(s->geom->length);
}

PyDoc_STRVAR(setStart__doc__,
"Description: sets the start of the region (in sectors)\n"
"Receives: (start_sector)\n"
"          start_sector must be a long object\n"
"Returns: None\n");
static PyObject *setStart(plpPedGeometry *s, PyObject *args)
{
  PedSector start;

  if (!PyArg_ParseTuple(args, "L", &start))
    return NULL;

  ped_geometry_set_start(s->geom, start);

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(setEnd__doc__,
"Description: sets the end of the region (in sectors)\n"
"Receives: (end_sector)\n"
"          end_sector must be a long object\n"
"Returns: None\n");
static PyObject *setEnd(plpPedGeometry *s, PyObject *args)
{
  PedSector end;

  if (!PyArg_ParseTuple(args, "L", &end))
    return NULL;

  ped_geometry_set_end(s->geom, end);

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(set__doc__,
"Description: sets the region of the geometry\n"
"Receives: (start_sector, length)\n"
"          start_sector and length must be a long objects\n"
"Returns: None\n");
static PyObject *set(plpPedGeometry *s, PyObject *args)
{
  PedSector start, length;

  if (!PyArg_ParseTuple(args, "LL", &start, &length))
    return NULL;

  ped_geometry_set(s->geom, start, length);

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(testOverlap__doc__,
"Description: tests if the geometry overlaps with another geometry\n"
"Receives: (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"Returns: true if the geometries overlap\n"
"         or false if they do not\n");
static PyObject *testOverlap(plpPedGeometry *s, PyObject *args)
{
  plpPedGeometry *other;

  if (!PyArg_ParseTuple(args, "O!", &plpPedGeometryType, &other))
    return NULL;

  if (ped_geometry_test_overlap(s->geom, other->geom)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(testInside__doc__,
"Description: tests if the geometry lies inside another geometry\n"
"Receives: (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"Returns: true if the geometry is inside of plpgeom\n"
"         or false if it is not\n");
static PyObject *testInside(plpPedGeometry *s, PyObject *args)
{
  plpPedGeometry *other;

  if (!PyArg_ParseTuple(args, "O!", &plpPedGeometryType, &other))
    return NULL;

  if (ped_geometry_test_inside(other->geom, s->geom)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(testEqual__doc__,
"Description: tests if two geometries refer to the same\n"
"             physical region\n"
"Receives: (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"Returns: true if they refer to the same region\n"
"         or false they do not\n");
static PyObject *testEqual(plpPedGeometry *s, PyObject *args)
{
  plpPedGeometry *other;

  if (!PyArg_ParseTuple(args, "O!", &plpPedGeometryType, &other))
    return NULL;

  if (ped_geometry_test_equal(s->geom, other->geom)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(testSectorInside__doc__,
"Description: tests if a sector is inside the geometry\n"
"Receives: (sector)\n"
"          sector must be a long object\n"
"Returns: true if the sector is inside the geometry\n"
"         or false if it is not\n");
static PyObject *testSectorInside(plpPedGeometry *s, PyObject *args)
{
  PedSector sect;

  if (!PyArg_ParseTuple(args, "L", &sect))
    return NULL;

  if (ped_geometry_test_sector_inside(s->geom, sect)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(probeFsType__doc__,
"Description: attempts to detect a filesystem on the geometry\n"
"Receives: nothing\n"
"Returns: a PedFileSystemType object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *probeFsType(plpPedGeometry *s)
{
  PedFileSystemType *fstype;

  if (!(fstype = ped_file_system_probe(s->geom))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppedfilesystemtype(fstype);
}

PyDoc_STRVAR(probeSpecificFsType__doc__,
"Description: attempts to find a specific filesystem\n"
"             on the geometry\n"
"Receives: (plpfstype)\n"
"          plpfstype must be a PedFileSystemType object\n"
"Returns: a PedGeometry object describing the region the\n"
"         filesystem believes it occupies or None if the\n"
"         filesystem was not found\n");
static PyObject *probeSpecificFsType(plpPedGeometry *s, PyObject *args)
{
  _plpPedFileSystemType *plpfstype;
  PedGeometry *geom;

  if (!PyArg_ParseTuple(args, "O!", &plpPedFileSystemTypeType, &plpfstype))
    return NULL;

  if ((geom = ped_file_system_probe_specific(plpfstype->fstype, s->geom)))
    return (PyObject *)new_plppedgeometry(geom, 0);

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(clobberFileSystem__doc__,
"Description: destroys all filesystem signatures on the geometry\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *clobberFileSystem(plpPedGeometry *s)
{
  if (!ped_file_system_clobber(s->geom)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(duplicate__doc__,
"Description: duplicates the geometry\n"
"Receives: nothing\n"
"Returns: a PedGeometry object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *duplicate(plpPedGeometry *s)
{
  PedGeometry *geom;

  if (!(geom = ped_geometry_duplicate(s->geom))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppedgeometry(geom, 0);
}

PyDoc_STRVAR(intersect__doc__,
"Description: if the geometry overlaps with another geometry,\n"
"             it returns the overlapping region\n"
"Receives: (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"Returns: a PedGeometry object describing the overlapping region\n"
"         or None if there is no overlap\n");
static PyObject *intersect(plpPedGeometry *s, PyObject *args)
{
  plpPedGeometry *other;
  PedGeometry *geom;

  if (!PyArg_ParseTuple(args, "O!", &plpPedGeometryType, &other))
    return NULL;

  if ((geom = ped_geometry_intersect(s->geom, other->geom)))
    return (PyObject *)new_plppedgeometry(geom, 0);

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(alignUp__doc__,
"Description: returns the closest sector to another sector that\n"
"             lies within the geometry and satisfies an alignment\n"
"             restriction (sectors not smaller than that one are\n"
"             always closer)\n"
"Receives: (plpalign, sector)\n"
"          plpalign must be a PedAlignment object\n"
"          sector must be a long object\n"
"Returns: a long object or None if there is no such sector\n");
static PyObject *alignUp(plpPedGeometry *s, PyObject *args)
{
  plpPedAlignment *plpalign;
  PedSector sector, ret;

  if (!PyArg_ParseTuple(args, "O!L",
			&plpPedAlignmentType, &plpalign, &sector))
    return NULL;

  if ((ret = ped_alignment_align_up(plpalign->align, s->geom, sector)) < 0) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return PyLong_FromLongLong(ret);
}

PyDoc_STRVAR(alignDown__doc__,
"Description: returns the closest sector to another sector that\n"
"             lies within the geometry and satisfies an alignment\n"
"             restriction (sectors not greater than that one are\n"
"             always closer)\n"
"Receives: (plpalign, sector)\n"
"          plpalign must be a PedAlignment object\n"
"          sector must be a long object\n"
"Returns: a long object or None if there is no such sector\n");
static PyObject *alignDown(plpPedGeometry *s, PyObject *args)
{
  plpPedAlignment *plpalign;
  PedSector sector, ret;

  if (!PyArg_ParseTuple(args, "O!L",
			&plpPedAlignmentType, &plpalign, &sector))
    return NULL;

  if ((ret = ped_alignment_align_down(plpalign->align, s->geom, sector)) < 0) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return PyLong_FromLongLong(ret);
}

PyDoc_STRVAR(alignNearest__doc__,
"Description: returns the closest sector to another sector that\n"
"             lies within the geometry and satisfies an alignment\n"
"             restriction\n"
"Receives: (plpalign, sector)\n"
"          plpalign must be a PedAlignment object\n"
"          sector must be a long object\n"
"Returns: a long object or None if there is no such sector\n");
static PyObject *alignNearest(plpPedGeometry *s, PyObject *args)
{
  plpPedAlignment *plpalign;
  PedSector sector, ret;

  if (!PyArg_ParseTuple(args, "O!L",
			&plpPedAlignmentType, &plpalign, &sector))
    return NULL;

  if ((ret = ped_alignment_align_nearest(plpalign->align,
					 s->geom, sector)) < 0) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return PyLong_FromLongLong(ret);
}

PyDoc_STRVAR(isAligned__doc__,
"Description: tests if a sector is within the geometry and satisfies\n"
"             an alignment restriction\n"
"Receives: (plpalign, sector)\n"
"          plpalign must be a PedAlignment object\n"
"          sector must be a long object\n"
"Returns: true if the sector satisfies all the restrictions\n"
"         or false if it does not\n");
static PyObject *isAligned(plpPedGeometry *s, PyObject *args)
{
  plpPedAlignment *plpalign;
  PedSector sector;

  if (!PyArg_ParseTuple(args, "O!L",
			&plpPedAlignmentType, &plpalign, &sector))
    return NULL;

  if (ped_alignment_is_aligned(plpalign->align, s->geom, sector)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(getExactConstraint__doc__,
"Description: returns a constraint that has the geometry as its\n"
"             unique solution\n"
"Receives: nothing\n"
"Returns: a PedConstraint object\n");
static PyObject *getExactConstraint(plpPedGeometry *s)
{
  return (PyObject *)new_plppedconstraint(ped_constraint_exact(s->geom));
}

PyDoc_STRVAR(openFileSystem__doc__,
"Description: opens a filesystem on the geometry\n"
"Receives: nothing\n"
"Returns: a PedFileSystem object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *openFileSystem(plpPedGeometry *s)
{
  PedFileSystem *fs;

  if (!(fs = ped_file_system_open(s->geom))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppedfilesystem(fs);
}

PyDoc_STRVAR(createFileSystem__doc__,
"Description: creates a new filesystem on the geometry\n"
"Receives: (plpfstype, plptimer) or (plpfstype)\n"
"          plpfstype must be a PedFileSystemType object\n"
"          if supplied, plptimer must be a PedTimer object\n"
"Returns: a PedFileSystem object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *createFileSystem(plpPedGeometry *s, PyObject *args)
{
  _plpPedFileSystemType *plpfstype;
  plpPedTimer *plptimer = NULL;
  PedFileSystem *fs;
  PedTimer *timer;

  if (!PyArg_ParseTuple(args, "O!|O!",
			&plpPedFileSystemTypeType, &plpfstype,
			&plpPedTimerType, &plptimer))
    return NULL;

  timer = (!plptimer ? NULL : plptimer->timer);

  if (!(fs = ped_file_system_create(s->geom, plpfstype->fstype, timer))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppedfilesystem(fs);
}

static PyMethodDef plpPedGeometry_methods[] = {
  { "getStart", (PyCFunction)getStart, METH_NOARGS, getStart__doc__ },
  { "getEnd", (PyCFunction)getEnd, METH_NOARGS, getEnd__doc__ },
  { "getLength", (PyCFunction)getLength, METH_NOARGS, getLength__doc__ },
  { "setStart", (PyCFunction)setStart, METH_VARARGS, setStart__doc__ },
  { "setEnd", (PyCFunction)setEnd, METH_VARARGS, setEnd__doc__ },
  { "set", (PyCFunction)set, METH_VARARGS, set__doc__ },
  { "testOverlap", (PyCFunction)testOverlap, METH_VARARGS,
    testOverlap__doc__ },
  { "testInside", (PyCFunction)testInside, METH_VARARGS, testInside__doc__ },
  { "testEqual", (PyCFunction)testEqual, METH_VARARGS, testEqual__doc__ },
  { "testSectorInside", (PyCFunction)testSectorInside, METH_VARARGS,
    testSectorInside__doc__ },
  { "probeFsType", (PyCFunction)probeFsType, METH_NOARGS, probeFsType__doc__ },
  { "probeSpecificFsType", (PyCFunction)probeSpecificFsType, METH_VARARGS,
    probeSpecificFsType__doc__ },
  { "clobberFileSystem", (PyCFunction)clobberFileSystem, METH_NOARGS,
    clobberFileSystem__doc__ },
  { "duplicate", (PyCFunction)duplicate, METH_NOARGS, duplicate__doc__ },
  { "intersect", (PyCFunction)intersect, METH_VARARGS, intersect__doc__ },
  { "alignUp", (PyCFunction)alignUp, METH_VARARGS, alignUp__doc__ },
  { "alignDown", (PyCFunction)alignDown, METH_VARARGS, alignDown__doc__ },
  { "alignNearest", (PyCFunction)alignNearest, METH_VARARGS,
    alignNearest__doc__ },
  { "isAligned", (PyCFunction)isAligned, METH_VARARGS, isAligned__doc__ },
  { "getExactConstraint", (PyCFunction)getExactConstraint, METH_NOARGS,
    getExactConstraint__doc__ },
  { "openFileSystem", (PyCFunction)openFileSystem, METH_NOARGS,
    openFileSystem__doc__ },
  { "createFileSystem", (PyCFunction)createFileSystem, METH_VARARGS,
    createFileSystem__doc__ },
  { NULL }
};

/* plpPedGeometry type */

static void plpPedGeometry_dealloc(plpPedGeometry *s)
{
  if (s->geom && !s->native)
    ped_geometry_destroy(s->geom);
  s->ob_type->tp_free((PyObject *)s);
}

static PyObject *plpPedGeometry_new(PyTypeObject *type, PyObject *args,
				    PyObject *kwds)
{
  plpPedGeometry *s;

  if (!(s = (plpPedGeometry *)type->tp_alloc(type, 0)))
    return NULL;

  s->geom = NULL;

  return (PyObject *)s;
}

static int plpPedGeometry_init(plpPedGeometry *s, PyObject *args, PyObject *kwds)
{
  PedSector start, length;
  plpPedDevice *plpdev;
  PedGeometry *geom;

  if (!PyArg_ParseTuple(args, "O!LL", &plpPedDeviceType, &plpdev,
			&start, &length))
    return -1;

  geom = ped_geometry_new(plpdev->dev, start, length);
  if (!geom) {
    plp_set_error_from_ped_exception();
    return -1;
  }

  s->geom = geom;
  s->native = 0;

  return 0;
}

PyDoc_STRVAR(plpPedGeometry__doc__,
"Description: a PedGeometry object represents a continuous region\n"
"             on a device\n"
"\n"
"A new PedGeometry object can be created with:\n"
"\n"
"  obj = pylibparted.PedGeometry(plpdev, start, length)\n"
"  (plpdev must be a PedDevice object,\n"
"   start and length must be long objects)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedGeometryType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedGeometry",
  .tp_basicsize      = sizeof(plpPedGeometry),
  .tp_dealloc        = (destructor)plpPedGeometry_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedGeometry__doc__,
  .tp_methods        = plpPedGeometry_methods,
  .tp_init           = (initproc)plpPedGeometry_init,
  .tp_new            = plpPedGeometry_new
};
