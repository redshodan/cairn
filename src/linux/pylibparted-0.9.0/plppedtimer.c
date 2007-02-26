/*
 * plppedtimer.c - implementation of PedTimer
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
#include "plppedtimer.h"
#include "plppedexception.h"

/* generic timer handler */

static void plp_timer_handler(PedTimer *timer, void *context)
{
  plpPedTimer *s = (plpPedTimer *)context;
  PyObject *args, *res;

  args = Py_BuildValue("(NN)", s, s->context);
  res = PyEval_CallObject(s->handler, args);
  Py_XDECREF(args);
  Py_XDECREF(res);
}

/* plpPedTimer methods */

PyDoc_STRVAR(getFrac__doc__,
"Description: returns the fraction of operation done\n"
"Receives: nothing\n"
"Returns: a float object\n");
static PyObject *getFrac(plpPedTimer *s)
{
  return PyFloat_FromDouble(s->timer->frac);
}

PyDoc_STRVAR(getTime__doc__,
"Description: returns the time of last update (now)\n"
"Receives: nothing\n"
"Returns: an integer object\n");
static PyObject *getTime(plpPedTimer *s)
{
  return PyInt_FromLong(s->timer->now);
}

static PyMethodDef plpPedTimer_methods[] = {
  { "getFrac", (PyCFunction)getFrac, METH_NOARGS, getFrac__doc__ },
  { "getTime", (PyCFunction)getTime, METH_NOARGS, getTime__doc__ },
  { NULL }
};

/* plpPedTimer type */

static void plpPedTimer_dealloc(plpPedTimer *s)
{
  if (s->timer) {
    Py_DECREF(s->handler);
    Py_DECREF(s->context);
    ped_timer_destroy(s->timer);
  }
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *plpPedTimer_new(PyTypeObject *type, PyObject *args,
				 PyObject *kwds)
{
  plpPedTimer *s;

  if (!(s = (plpPedTimer *)type->tp_alloc(type, 0)))
    return NULL;

  s->timer = NULL;

  return (PyObject *)s;
}

static int plpPedTimer_init(plpPedTimer *s, PyObject *args, PyObject *kwds)
{
  PyObject *handler, *context;
  PedTimer *timer;

  if (!PyArg_ParseTuple(args, "OO", &handler, &context))
    return -1;

  if (!PyCallable_Check(handler)) {
    PyErr_SetString(PyExc_TypeError, "first parameter must be "
		                     "a callable object");
    return -1;
  }

  if (!(timer = ped_timer_new(plp_timer_handler, (void *)s))) {
    PyErr_SetString(plpError, "could not create a PedTimer object");
    return -1;
  }

  Py_INCREF(handler);
  Py_INCREF(context);

  s->timer = timer;
  s->handler = handler;
  s->context = context;

  return 0;
}

PyDoc_STRVAR(plpPedTimer__doc__,
"Description: a PedTimer object keeps track of the progress\n"
"             of an operation\n"
"\n"
"A new PedTimer object can be created with:\n"
"\n"
"  obj = pylibparted.PedTimer(handler, context)\n"
"  (handler will be the callback, so it must be a callable\n"
"   object and context must be any object to be passed to the\n"
"   callback whenever an update occurs)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedTimerType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedTimer",
  .tp_basicsize      = sizeof(plpPedTimer),
  .tp_dealloc        = (destructor)plpPedTimer_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedTimer__doc__,
  .tp_methods        = plpPedTimer_methods,
  .tp_init           = (initproc)plpPedTimer_init,
  .tp_new            = plpPedTimer_new
};
