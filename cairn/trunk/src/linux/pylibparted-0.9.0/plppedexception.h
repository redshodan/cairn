/*
 * plppedexception.h - definition for PedException
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

#ifndef PLPPEDEXCEPTION_H
#define PLPPEDEXCEPTION_H

#include <Python.h>
#include <parted/parted.h>

struct _plpPedException {
  PyObject_HEAD
  PedException *e;
};

typedef struct _plpPedException plpPedException;
extern plpPedException *new_plppedexception(PedException *);
extern PyTypeObject plpPedExceptionType;

/* pylibparted exception object and handling functions */
extern PyObject *plpError;
extern PyObject *plpExceptionHandler;
extern int plp_exception_string_check(void);
extern void plp_exception_string_clear(void);
extern void plp_set_error_from_ped_exception(void);
extern PedExceptionOption plp_exception_handler(PedException *);

/* PedException documentation string */
#define plpPedException__doc__					     \
  "A PedException object represents a libparted exception. The\n"    \
  "PedException available methods are:\n"			     \
  "\n"								     \
  "getMessage(...)\n"						     \
  "Description: returns the exception message\n"		     \
  "Receives: nothing\n"						     \
  "Returns: a string object\n"					     \
  "\n"								     \
  "getType(...)\n"						     \
  "Description: returns the exception type\n"			     \
  "Receives: nothing\n"						     \
  "Returns: an integer object\n"				     \
  "\n"								     \
  "getTypeString(...)\n"					     \
  "Description: returns a string describing the exception type\n"    \
  "Receives: nothing\n"						     \
  "Returns: a string object\n"					     \
  "\n"								     \
  "getOptions(...)\n"						     \
  "Description: returns the ways the exception can be resolved\n"    \
  "Receives: nothing\n"						     \
  "Returns: an integer object\n"				     \
  "\n";

#endif /* PLPPEDEXCEPTION_H */
