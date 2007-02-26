/*
 * plppedexception.c - implementation of PedException
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
#include "plppedexception.h"

#include <stdlib.h>
#include <string.h>

/* plpPedException factory function */

plpPedException *new_plppedexception(PedException *e)
{
  plpPedException *ret;

  if (!(ret = (plpPedException *)plpPedExceptionType.tp_alloc(&plpPedExceptionType, 0)))
    return NULL;

  ret->e = e;

  return ret;
}

/* plpPedException methods */

static PyObject *getMessage(plpPedException *s)
{
  return PyString_FromString(s->e->message);
}

static PyObject *getType(plpPedException *s)
{
  return PyInt_FromLong(s->e->type);
}

static PyObject *getTypeString(plpPedException *s)
{
  return PyString_FromString(ped_exception_get_type_string(s->e->type));
}

static PyObject *getOptions(plpPedException *s)
{
  return PyInt_FromLong(s->e->options);
}

static PyMethodDef plpPedException_methods[] = {
  { "getMessage", (PyCFunction)getMessage, METH_NOARGS, NULL },
  { "getType", (PyCFunction)getType, METH_NOARGS, NULL },
  { "getTypeString", (PyCFunction)getTypeString, METH_NOARGS, NULL },
  { "getOptions", (PyCFunction)getOptions, METH_NOARGS, NULL },
  { NULL }
};

/* plpPedException type */

PyTypeObject plpPedExceptionType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedException",
  .tp_basicsize      = sizeof(plpPedException),
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_methods        = plpPedException_methods,
};


/*
 * pylibparted exception object and handling functions
 * 
 * Some exception handling code taken from Matt Wilson's pyparted. Thanks. :-)
 */

PyObject *plpError, *plpExceptionHandler;
static char *plp_exception_string = NULL;

int plp_exception_string_check(void)
{
  return (plp_exception_string != NULL);
}

void plp_exception_string_clear(void)
{
  if (plp_exception_string != NULL) {
    free(plp_exception_string);
    plp_exception_string = NULL;
  }
}

void plp_set_error_from_ped_exception(void)
{
  if (plp_exception_string != NULL) {
    PyErr_SetString(plpError, plp_exception_string);
    plp_exception_string_clear();
    return;
  }
  PyErr_SetString(plpError, "unknown error occurred");
}

PedExceptionOption plp_exception_handler(PedException *e)
{
  PyObject *args, *res;
  char *type, *buf;
  long ret;
  int len;

  plp_exception_string_clear();

  type = ped_exception_get_type_string(e->type);
  len = strlen(type) + strlen(e->message) + 3;
  buf = (char *)malloc(len);
  snprintf(buf, len, "%s: %s", type, e->message);
  plp_exception_string = buf;

  if (plpExceptionHandler == NULL)  /* we don't have a python handler */
    return PED_EXCEPTION_UNHANDLED;

  args = Py_BuildValue("(N)", (PyObject *)new_plppedexception(e));
  res = PyEval_CallObject(plpExceptionHandler, args);
  Py_XDECREF(args);

  if (res == NULL) {
    PyErr_Print();
    PyErr_Clear();
    return PED_EXCEPTION_UNHANDLED;
  }

  if (!PyInt_Check(res)) {
    fprintf (stderr,
	     "Error: python exception handler did not return an int value\n");
    return PED_EXCEPTION_UNHANDLED;
  }

  ret = PyInt_AsLong(res);
  Py_DECREF(res);

  return (PedExceptionOption)ret;
}
