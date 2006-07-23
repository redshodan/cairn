/*
 * plppedfilesystemtype.c - implementation of PedFileSystemType
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
#include "plppedfilesystemtype.h"
#include "plppedconstraint.h"
#include "plppeddevice.h"
#include "plppedexception.h"

/* _plpPedFileSystemType factory function */

_plpPedFileSystemType *new_plppedfilesystemtype(const PedFileSystemType *fstype)
{
  _plpPedFileSystemType *ret;

  if (!(ret = (_plpPedFileSystemType *)plpPedFileSystemTypeType.tp_alloc(&plpPedFileSystemTypeType, 0)))
    return NULL;

  ret->fstype = fstype;

  return ret;
}

/* _plpPedFileSystemType methods */

PyDoc_STRVAR(getName__doc__,
"Receives: nothing\n"
"Returns: a string with the filesystem type name\n");
static PyObject *getName(_plpPedFileSystemType *s)
{
  return PyString_FromString(s->fstype->name);
}

PyDoc_STRVAR(getCreateConstraint__doc__,
"Description: returns the constraint for creating the filesystem\n"
"             on the received device\n"
"Receives: (plpdev)\n"
"          plpdev must be a PedDevice object\n"
"Returns: a PedConstraint object or None if it is not\n"
"         possible to create the filesystem\n");
static PyObject *getCreateConstraint(_plpPedFileSystemType *s, PyObject *args)
{
  PedConstraint *constraint;
  plpPedDevice *plpdev;

  if (!PyArg_ParseTuple(args, "O!", &plpPedDeviceType, &plpdev))
    return NULL;

  constraint = ped_file_system_get_create_constraint(s->fstype, plpdev->dev);
  if (!constraint) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return (PyObject *)new_plppedconstraint(constraint);
}

static PyMethodDef _plpPedFileSystemType_methods[] = {
  { "getName", (PyCFunction)getName, METH_NOARGS, getName__doc__ },
  { "getCreateConstraint", (PyCFunction)getCreateConstraint, METH_VARARGS,
    getCreateConstraint__doc__ },
  { NULL }
};

/* _plpPedFileSystemType type */

static void _plpPedFileSystemType_dealloc(_plpPedFileSystemType *s)
{
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *_plpPedFileSystemType_new(PyTypeObject *type, PyObject *args,
					   PyObject *kwds)
{
  _plpPedFileSystemType *s;

  if (!(s = (_plpPedFileSystemType *)type->tp_alloc(type, 0)))
    return NULL;

  return (PyObject *)s;
}

static int _plpPedFileSystemType_init(_plpPedFileSystemType *s,
				      PyObject *args, PyObject *kwds)
{
  char *name;

  if (!PyArg_ParseTuple(args, "s", &name))
    return -1;

  if (!(s->fstype = ped_file_system_type_get(name))) {
    PyErr_SetString(plpError, "unknown file system type");
    return -1;
  }

  return 0;
}

PyDoc_STRVAR(_plpPedFileSystemType__doc__,
"Description: a PedFileSystemType object represents a filesystem type\n"
"\n"
"A new PedFileSystemType object can be created with:\n"
"\n"
"  obj = pylibparted.PedFileSystemType(type_name)\n"
"  (type_name must be a string with the filesystem type name)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedFileSystemTypeType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedFileSystemType",
  .tp_basicsize      = sizeof(_plpPedFileSystemType),
  .tp_dealloc        = (destructor)_plpPedFileSystemType_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = _plpPedFileSystemType__doc__,
  .tp_methods        = _plpPedFileSystemType_methods,
  .tp_init           = (initproc)_plpPedFileSystemType_init,
  .tp_new            = _plpPedFileSystemType_new
};
