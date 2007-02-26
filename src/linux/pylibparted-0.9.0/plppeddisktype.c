/*
 * plppeddisktype.c - implementation of PedDiskType
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
#include "plppeddisktype.h"
#include "plppedexception.h"

/* _plpPedDiskType factory function */

_plpPedDiskType *new_plppeddisktype(const PedDiskType *type)
{
  _plpPedDiskType *ret;

  if (!(ret = (_plpPedDiskType *)plpPedDiskTypeType.tp_alloc(&plpPedDiskTypeType, 0)))
    return NULL;

  ret->type = type;

  return ret;
}

/* _plpPedDiskType methods */

PyDoc_STRVAR(getName__doc__,
"Receives: nothing\n"
"Returns: a string with the disk type name\n");
static PyObject *getName(_plpPedDiskType *s)
{
  return PyString_FromString(s->type->name);
}

PyDoc_STRVAR(checkFeature__doc__,
"Receives: a feature to be tested\n"
"Returns: true if the disk type supports the received feature\n"
"         or false if it does not support\n");
static PyObject *checkFeature(_plpPedDiskType *s, PyObject *args)
{
  long arg;

  if (!PyArg_ParseTuple(args, "l", &arg))
    return NULL;

  if (ped_disk_type_check_feature(s->type, arg)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

static PyMethodDef _plpPedDiskType_methods[] = {
  { "getName", (PyCFunction)getName, METH_NOARGS, getName__doc__ },
  { "checkFeature", (PyCFunction)checkFeature, METH_VARARGS,
    checkFeature__doc__ },
  { NULL }
};

/* _plpPedDiskType type */

static void _plpPedDiskType_dealloc(_plpPedDiskType *s)
{
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *_plpPedDiskType_new(PyTypeObject *type, PyObject *args,
				     PyObject *kwds)
{
  _plpPedDiskType *s;

  if (!(s = (_plpPedDiskType *)type->tp_alloc(type, 0)))
    return NULL;

  return (PyObject *)s;
}

static int _plpPedDiskType_init(_plpPedDiskType *s, PyObject *args, PyObject *kwds)
{
  char *name;

  if (!PyArg_ParseTuple(args, "s", &name))
    return -1;

  if (!(s->type = ped_disk_type_get(name))) {
    PyErr_SetString(plpError, "unknown disk type");
    return -1;
  }

  return 0;
}

PyDoc_STRVAR(_plpPedDiskType__doc__,
"Description: a PedDiskType object represents a partition table type\n"
"\n"
"A new PedDiskType object can be created with:\n"
"\n"
"  obj = pylibparted.PedDiskType(type_name)\n"
"  (type_name must be a string with the partition table type name)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedDiskTypeType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedDiskType",
  .tp_basicsize      = sizeof(_plpPedDiskType),
  .tp_dealloc        = (destructor)_plpPedDiskType_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = _plpPedDiskType__doc__,
  .tp_methods        = _plpPedDiskType_methods,
  .tp_init           = (initproc)_plpPedDiskType_init,
  .tp_new            = _plpPedDiskType_new
};
