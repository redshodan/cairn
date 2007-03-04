/*
 * plppedalignment.c - implementation of PedAlignment
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
#include "plppedalignment.h"
#include "plppedexception.h"

/* plpPedAlignment factory function */

plpPedAlignment *new_plppedalignment(PedAlignment *align)
{
  plpPedAlignment *ret;

  if (!(ret = (plpPedAlignment *)plpPedAlignmentType.tp_alloc(&plpPedAlignmentType, 0)))
    return NULL;

  ret->align = align;

  return ret;
}

/* plpPedAlignment methods */

PyDoc_STRVAR(duplicate__doc__,
"Description: duplicates the PedAlignment object\n"
"Receives: nothing\n"
"Returns: a new copy of the PedAlignment object\n");
static PyObject *duplicate(plpPedAlignment *s)
{
  return (PyObject *)new_plppedalignment(ped_alignment_duplicate(s->align));
}

PyDoc_STRVAR(intersect__doc__,
"Description: returns a PedAlignment object such that a PedSector\n"
"             is a solution, if and only if it is a solution to\n"
"             this PedAlignment object and the PedAlignment object\n"
"             received\n"
"Receives: nothing or (plpalign)\n"
"          if nothing is supplied, NULL will be used\n"
"          if plpalign is supplied, it must be a PedAlignment object\n"
"Returns: a PedAlignment object or None if no intersection was found\n");
static PyObject *intersect(plpPedAlignment *s, PyObject *args)
{
  plpPedAlignment *plpb = NULL;
  PedAlignment *align, *b;

  if (!PyArg_ParseTuple(args, "|O!", &plpPedAlignmentType, &plpb))
    return NULL;

  b = (!plpb ? NULL : plpb->align);

  align = ped_alignment_intersect(s->align, b);
  if (!align) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return (PyObject *)new_plppedalignment(align);
}

PyDoc_STRVAR(getOffset__doc__,
"Receives: nothing\n"
"Returns: a long object representing the offset of the\n"
"         PedAlignment object\n");
static PyObject *getOffset(plpPedAlignment *s)
{
  return PyLong_FromLongLong(s->align->offset);
}

PyDoc_STRVAR(getGrainSize__doc__,
"Receives: nothing\n"
"Returns: a long object representing the grain size of the\n"
"         PedAlignment object\n");
static PyObject *getGrainSize(plpPedAlignment *s)
{
  return PyLong_FromLongLong(s->align->grain_size);
}

static PyMethodDef plpPedAlignment_methods[] = {
  { "duplicate", (PyCFunction)duplicate, METH_NOARGS, duplicate__doc__ },
  { "intersect", (PyCFunction)intersect, METH_VARARGS, intersect__doc__ },
  { "getOffset", (PyCFunction)getOffset, METH_NOARGS, getOffset__doc__ },
  { "getGrainSize", (PyCFunction)getGrainSize, METH_NOARGS,
    getGrainSize__doc__ },
  { NULL }
};

/* plpPedAlignment type */

static void plpPedAlignment_dealloc(plpPedAlignment *s)
{
  if (s->align)
    ped_alignment_destroy(s->align);
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *plpPedAlignment_new(PyTypeObject *type, PyObject *args,
				     PyObject *kwds)
{
  plpPedAlignment *s;

  if (!(s = (plpPedAlignment *)type->tp_alloc(type, 0)))
    return NULL;

  s->align = NULL;

  return (PyObject *)s;
}

static int plpPedAlignment_init(plpPedAlignment *s, PyObject *args, PyObject *kwds)
{
  PedSector offset, grain_size;

  if (!PyArg_ParseTuple(args, "LL", &offset, &grain_size))
    return -1;

  if (!(s->align = ped_alignment_new(offset, grain_size))) {
    PyErr_SetString(plpError, "could not create a PedAlignment object");
    return -1;
  }

  return 0;
}

PyDoc_STRVAR(plpPedAlignment__doc__,
"Description: alignments are restrictions on the location of a sector\n"
"\n"
"A new PedAlignment object can be created with:\n"
"\n"
"  obj = pylibparted.PedAlignment(offset, grain_size)\n"
"  (offset and grain_size must be long objects)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedAlignmentType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedAlignment",
  .tp_basicsize      = sizeof(plpPedAlignment),
  .tp_dealloc        = (destructor)plpPedAlignment_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedAlignment__doc__,
  .tp_methods        = plpPedAlignment_methods,
  .tp_init           = (initproc)plpPedAlignment_init,
  .tp_new            = plpPedAlignment_new
};
