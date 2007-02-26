/*
 * plppedconstraint.c - implementation of PedConstraint
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
#include "plppedconstraint.h"
#include "plppedgeometry.h"
#include "plppedalignment.h"
#include "plppedexception.h"

/* plpPedConstraint factory function */

plpPedConstraint *new_plppedconstraint(PedConstraint *constraint)
{
  plpPedConstraint *ret;

  if (!(ret = (plpPedConstraint *)plpPedConstraintType.tp_alloc(&plpPedConstraintType, 0)))
    return NULL;

  ret->constraint = constraint;

  return ret;
}

/* plpPedConstraint methods */

PyDoc_STRVAR(duplicate__doc__,
"Description: duplicates the PedConstraint object\n"
"Receives: nothing\n"
"Returns: a new copy of the PedConstraint object\n");
static PyObject *duplicate(plpPedConstraint *s)
{
  PedConstraint *c;

  c = ped_constraint_duplicate(s->constraint);

  return (PyObject *)new_plppedconstraint(c);
}

PyDoc_STRVAR(intersect__doc__,
"Description: returns a PedConstraint object such that a PedGeometry\n"
"             is a solution to the constraint, if and only if it is a\n"
"             solution to this PedConstraint object and the\n"
"             PedConstraint object received\n"
"Receives: nothing or (plpconst)\n"
"          if nothing is supplied, NULL will be used\n"
"          if plpconst is supplied, it must be a PedConstraint object\n"
"Returns: a PedConstraint object or None if no intersection was found\n");
static PyObject *intersect(plpPedConstraint *s, PyObject *args)
{
  plpPedConstraint *plpb = NULL;
  PedConstraint *c, *b;

  if (!PyArg_ParseTuple(args, "|O!", &plpPedConstraintType, &plpb))
    return NULL;

  b = (!plpb ? NULL : plpb->constraint);

  c = ped_constraint_intersect(s->constraint, b);
  if (!c) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return (PyObject *)new_plppedconstraint(c);
}

PyDoc_STRVAR(getStartAlign__doc__,
"Receives: nothing\n"
"Returns: a PedAlignment object representing the start alignment\n"
"         of the PedConstraint object\n");
static PyObject *getStartAlign(plpPedConstraint *s)
{
  return (PyObject *)new_plppedalignment(s->constraint->start_align);
}

PyDoc_STRVAR(getEndAlign__doc__,
"Receives: nothing\n"
"Returns: a PedAlignment object representing the end alignment\n"
"         of the PedConstraint object\n");
static PyObject *getEndAlign(plpPedConstraint *s)
{
  return (PyObject *)new_plppedalignment(s->constraint->end_align);
}

PyDoc_STRVAR(getStartRange__doc__,
"Receives: nothing\n"
"Returns: a PedGeometry object representing the start range\n"
"         of the PedConstraint object\n");
static PyObject *getStartRange(plpPedConstraint *s)
{
  return (PyObject *)new_plppedgeometry(s->constraint->start_range, 0);
}

PyDoc_STRVAR(getEndRange__doc__,
"Receives: nothing\n"
"Returns: a PedGeometry object representing the end range\n"
"         of the PedConstraint object\n");
static PyObject *getEndRange(plpPedConstraint *s)
{
  return (PyObject *)new_plppedgeometry(s->constraint->end_range, 0);
}

PyDoc_STRVAR(getMinSize__doc__,
"Receives: nothing\n"
"Returns: a long object representing the min size of the\n"
"         PedConstraint object\n");
static PyObject *getMinSize(plpPedConstraint *s)
{
  return PyLong_FromLongLong(s->constraint->min_size);
}

PyDoc_STRVAR(getMaxSize__doc__,
"Receives: nothing\n"
"Returns: a long object representing the max size of the\n"
"         PedConstraint object\n");
static PyObject *getMaxSize(plpPedConstraint *s)
{
  return PyLong_FromLongLong(s->constraint->max_size);
}

PyDoc_STRVAR(solveMax__doc__,
"Description: returns the largest solution of the constraint\n"
"             (geometry with maximum length)\n"
"Receives: nothing\n"
"Returns: a PedGeometry object or None if there is no solution\n");
static PyObject *solveMax(plpPedConstraint *s)
{
  PedGeometry *ret;

  ret = ped_constraint_solve_max(s->constraint);
  if (!ret) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return (PyObject *)new_plppedgeometry(ret, 0);
}

PyDoc_STRVAR(solveNearest__doc__,
"Description: solves the constraint and returns the nearest\n"
"             solution to the received geometry\n"
"Receives: (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"Returns: a PedGeometry object or None if there is no solution\n");
static PyObject *solveNearest(plpPedConstraint *s, PyObject *args)
{
  plpPedGeometry *plpgeom;
  PedGeometry *ret;

  if (!PyArg_ParseTuple(args, "O!", &plpPedGeometryType, &plpgeom))
    return NULL;

  ret = ped_constraint_solve_nearest(s->constraint, plpgeom->geom);
  if (!ret) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  return (PyObject *)new_plppedgeometry(ret, 0);
}

PyDoc_STRVAR(isSolution__doc__,
"Receives: (plpgeom)\n"
"          plpgeom must be a PedGeometry object\n"
"Returns: true if plpgeom is a solution for the constraint\n"
"         or false if it is not a solution\n");
static PyObject *isSolution(plpPedConstraint *s, PyObject *args)
{
  plpPedGeometry *plpgeom;

  if (!PyArg_ParseTuple(args, "O!", &plpPedGeometryType, &plpgeom))
    return NULL;

  if (ped_constraint_is_solution(s->constraint, plpgeom->geom)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

static PyMethodDef plpPedConstraint_methods[] = {
  { "duplicate", (PyCFunction)duplicate, METH_NOARGS, duplicate__doc__ },
  { "intersect", (PyCFunction)intersect, METH_VARARGS, intersect__doc__ },
  { "getStartAlign", (PyCFunction)getStartAlign, METH_NOARGS,
    getStartAlign__doc__ },
  { "getEndAlign", (PyCFunction)getEndAlign, METH_NOARGS, getEndAlign__doc__ },
  { "getStartRange", (PyCFunction)getStartRange, METH_NOARGS,
    getStartRange__doc__ },
  { "getEndRange", (PyCFunction)getEndRange, METH_NOARGS, getEndRange__doc__ },
  { "getMinSize", (PyCFunction)getMinSize, METH_NOARGS, getMinSize__doc__ },
  { "getMaxSize", (PyCFunction)getMaxSize, METH_NOARGS, getMaxSize__doc__ },
  { "solveMax", (PyCFunction)solveMax, METH_NOARGS, solveMax__doc__ },
  { "solveNearest", (PyCFunction)solveNearest, METH_VARARGS,
    solveNearest__doc__ },
  { "isSolution", (PyCFunction)isSolution, METH_VARARGS, isSolution__doc__ },
  { NULL }
};

/* plpPedConstraint type */

static void plpPedConstraint_dealloc(plpPedConstraint *s)
{
  if (s->constraint)
    ped_constraint_destroy(s->constraint);
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *plpPedConstraint_new(PyTypeObject *type, PyObject *args,
				      PyObject *kwds)
{
  plpPedConstraint *s;

  if (!(s = (plpPedConstraint *)type->tp_alloc(type, 0)))
    return NULL;

  s->constraint = NULL;

  return (PyObject *)s;
}

static int plpPedConstraint_init(plpPedConstraint *s, PyObject *args, PyObject *kwds)
{
  plpPedAlignment *plpalignstart, *plpalignend;
  plpPedGeometry *plpgeomstart, *plpgeomend;
  PedSector min_size, max_size;
  PedConstraint *constraint;

  if (!PyArg_ParseTuple(args, "O!O!O!O!LL",
			&plpPedAlignmentType, &plpalignstart,
			&plpPedAlignmentType, &plpalignend,
			&plpPedGeometryType, &plpgeomstart,
			&plpPedGeometryType, &plpgeomend,
			&min_size, &max_size))
    return -1;

  if (!(constraint = ped_constraint_new(plpalignstart->align,
					plpalignend->align,
					plpgeomstart->geom,
					plpgeomend->geom,
					min_size, max_size))) {
    PyErr_SetString(plpError, "could not create a PedConstraint object");
    return -1;
  }

  s->constraint = constraint;

  return 0;
}

PyDoc_STRVAR(plpPedConstraint__doc__,
"Description: constraints are restrictions on the location and alignment\n"
"             of the start and end of a partition, and the minimum size\n"
"\n"
"A new PedConstraint object can be created with:\n"
"\n"
"  obj = pylibparted.PedConstraint(alignstart, alignend,\n"
"                                  rangestart, rangeend,\n"
"                                  min_size)\n"
"  (alignstart and alignend must be PedAlignment objects\n"
"   rangestart and rangeend must be PedGeometry objects\n"
"   min_size must be a long object)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedConstraintType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedConstraint",
  .tp_basicsize      = sizeof(plpPedConstraint),
  .tp_dealloc        = (destructor)plpPedConstraint_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedConstraint__doc__,
  .tp_methods        = plpPedConstraint_methods,
  .tp_init           = (initproc)plpPedConstraint_init,
  .tp_new            = plpPedConstraint_new
};
