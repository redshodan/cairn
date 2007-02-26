/*
 * plppedfilesystem.c - implementation of PedFileSystem
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
#include "plppedfilesystem.h"
#include "plppedgeometry.h"
#include "plppedconstraint.h"
#include "plppeddevice.h"
#include "plppedexception.h"
#include "plppedtimer.h"
#include "plppedfilesystemtype.h"

/* plpPedFileSystem factory function */

plpPedFileSystem *new_plppedfilesystem(PedFileSystem *fs)
{
  plpPedFileSystem *ret;

  if (!(ret = (plpPedFileSystem *)plpPedFileSystemType.tp_alloc(&plpPedFileSystemType, 0)))
    return NULL;

  ret->fs = fs;

  return ret;
}

/* plpPedFileSystem methods */

PyDoc_STRVAR(copy__doc__,
"Description: copies the contents of the file system to\n"
"             another geometry\n"
"Receives: (plpgeom, plptimer) or (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"          if supplied, plptimer must be a PedTimer object\n"
"Returns: the PedFileSystem object for the new filesystem\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *copy(plpPedFileSystem *s, PyObject *args)
{
  plpPedTimer *plptimer = NULL;
  plpPedGeometry *plpgeom;
  PedFileSystem *dst_fs;
  PedTimer *timer;

  if (!PyArg_ParseTuple(args, "O!|O!",
			&plpPedGeometryType, &plpgeom,
			&plpPedTimerType, &plptimer))
    return NULL;

  timer = (!plptimer ? NULL : plptimer->timer);

  if (!(dst_fs = ped_file_system_copy(s->fs, plpgeom->geom, timer))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppedfilesystem(dst_fs);
}

PyDoc_STRVAR(resize__doc__,
"Description: resizes the filesystem to a new geometry\n"
"Receives: (plpgeom, plptimer) or (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"          if supplied, plptimer must be a PedTimer object\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *resize(plpPedFileSystem *s, PyObject *args)
{
  plpPedTimer *plptimer = NULL;
  plpPedGeometry *plpgeom;
  PedTimer *timer;

  if (!PyArg_ParseTuple(args, "O!|O!",
			&plpPedGeometryType, &plpgeom,
			&plpPedTimerType, &plptimer))
    return NULL;

  timer = (!plptimer ? NULL : plptimer->timer);

  if (!ped_file_system_resize(s->fs, plpgeom->geom, timer)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(check__doc__,
"Description: checks the filesystem for errors\n"
"Receives: nothing or (plptimer)\n"
"          if supplied, plptimer must be a PedTimer object\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *check(plpPedFileSystem *s, PyObject *args)
{
  plpPedTimer *plptimer = NULL;
  PedTimer *timer;

  if (!PyArg_ParseTuple(args, "|O!", &plpPedTimerType, &plptimer))
    return NULL;

  timer = (!plptimer ? NULL : plptimer->timer);

  if (!ped_file_system_check(s->fs, timer)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(isChecked__doc__,
"Description: returns whether or not the filesystem was checked\n"
"Receives: nothing\n"
"Returns: true if the filesystem was already checked\n"
"         and false otherwise\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *isChecked(plpPedFileSystem *s)
{
  if (s->fs->checked) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(getResizeConstraint__doc__,
"Description: returns all the possible ways the filesystem\n"
"             can be resized\n"
"Receives: nothing\n"
"Returns: a PedConstraint object or None\n");
static PyObject *getResizeConstraint(plpPedFileSystem *s)
{
  PedConstraint *constraint;

  constraint = ped_file_system_get_resize_constraint(s->fs);
  if (!constraint) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return (PyObject *)new_plppedconstraint(constraint);
}

PyDoc_STRVAR(getCopyConstraint__doc__,
"Description: returns the constraint on copying the filesystem\n"
"             to somewhere on a device\n"
"Receives: (plpdev)\n"
"          plpdev must be a PedDevice object\n"
"Returns: a PedConstraint object or None\n");
static PyObject *getCopyConstraint(plpPedFileSystem *s, PyObject *args)
{
  PedConstraint *constraint;
  plpPedDevice *plpdev;

  if (!PyArg_ParseTuple(args, "O!", &plpPedDeviceType, &plpdev))
    return NULL;

  constraint = ped_file_system_get_copy_constraint(s->fs, plpdev->dev);
  if (!constraint) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return (PyObject *)new_plppedconstraint(constraint);
}

PyDoc_STRVAR(getGeometry__doc__,
"Description: returns the filesystem geometry\n"
"Receives: nothing\n"
"Returns: a PedGeometry object\n");
static PyObject *getGeometry(plpPedFileSystem *s)
{
  return (PyObject *)new_plppedgeometry(s->fs->geom, 1);
}

PyDoc_STRVAR(getFsType__doc__,
"Description: returns the filesystem type\n"
"Receives: nothing\n"
"Returns: a PedFileSystemType object\n");
static PyObject *getFsType(plpPedFileSystem *s)
{
  return (PyObject *)new_plppedfilesystemtype(s->fs->type);
}

static PyMethodDef plpPedFileSystem_methods[] = {
  { "copy", (PyCFunction)copy, METH_VARARGS, copy__doc__ },
  { "resize", (PyCFunction)resize, METH_VARARGS, resize__doc__ },
  { "check", (PyCFunction)check, METH_VARARGS, check__doc__ },
  { "isChecked", (PyCFunction)isChecked, METH_NOARGS, isChecked__doc__ },
  { "getResizeConstraint", (PyCFunction)getResizeConstraint, METH_NOARGS,
    getResizeConstraint__doc__ },
  { "getCopyConstraint", (PyCFunction)getCopyConstraint, METH_VARARGS,
    getCopyConstraint__doc__ },
  { "getGeometry", (PyCFunction)getGeometry, METH_NOARGS, getGeometry__doc__ },
  { "getFsType", (PyCFunction)getFsType, METH_NOARGS, getFsType__doc__ },
  { NULL }
};

/* plpPedFileSystem type */

static void plpPedFileSystem_dealloc(plpPedFileSystem *s)
{
  if (s->fs)
    ped_file_system_close(s->fs);
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *plpPedFileSystem_new(PyTypeObject *type, PyObject *args,
				      PyObject *kwds)
{
  plpPedFileSystem *s;

  if (!(s = (plpPedFileSystem *)type->tp_alloc(type, 0)))
    return NULL;

  s->fs = NULL;

  return (PyObject *)s;
}

static int plpPedFileSystem_init(plpPedFileSystem *s,
				 PyObject *args, PyObject *kwds)
{
  _plpPedFileSystemType *plpfstype;
  plpPedTimer *plptimer = NULL;
  plpPedGeometry *plpgeom;
  PedFileSystem *fs;
  PedTimer *timer;

  if (!PyArg_ParseTuple(args, "O!O!|O!",
			&plpPedGeometryType, &plpgeom,
			&plpPedFileSystemTypeType, &plpfstype,
			&plpPedTimerType, &plptimer))
    return -1;

  timer = (!plptimer ? NULL : plptimer->timer);

  if (!(fs = ped_file_system_create(plpgeom->geom, plpfstype->fstype, timer))) {
    plp_set_error_from_ped_exception();
    return -1;
  }

  s->fs = fs;

  return 0;
}

PyDoc_STRVAR(plpPedFileSystem__doc__,
"Description: a PedFileSystem object represents a filesystem on\n"
"             some geometry\n"
"\n"
"A filesystem can be created on a geometry and a PedFileSystem\n"
"object returned with:\n"
"\n"
"  obj = pylibparted.PedFileSystem(plpgeom, plpfstype[, plptimer])\n"
"  (plpgeom must be a PedGeometry object,\n"
"   plpfstype must be a PedFileSystemType object and\n"
"   plptimer, if supplied, must be a PedTimer object)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedFileSystemType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedFileSystem",
  .tp_basicsize      = sizeof(plpPedFileSystem),
  .tp_dealloc        = (destructor)plpPedFileSystem_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedFileSystem__doc__,
  .tp_methods        = plpPedFileSystem_methods,
  .tp_init           = (initproc)plpPedFileSystem_init,
  .tp_new            = plpPedFileSystem_new
};
