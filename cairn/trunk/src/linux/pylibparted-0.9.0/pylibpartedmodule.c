/*
 * pylibparted.c - Main file for pylibparted module
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
#include "plppeddevice.h"
#include "plppeddisk.h"
#include "plppeddisktype.h"
#include "plppedgeometry.h"
#include "plppedfilesystemtype.h"
#include "plppedfilesystem.h"
#include "plppedpartition.h"
#include "plppedalignment.h"
#include "plppedconstraint.h"
#include "plppedexception.h"
#include "plppedtimer.h"

PyDoc_STRVAR(probeAllDevices__doc__,
"Receives: nothing\n"
"Returns: string list of all devices found by libparted\n");
static PyObject *probeAllDevices(PyObject *s)
{
  PedDevice *cur;
  PyObject *ret;

  ped_device_probe_all();

  ret = PyList_New(0);

  cur = NULL;
  while ((cur = ped_device_get_next(cur)) != NULL) {
    if (PyList_Append(ret, PyString_FromString(cur->path)) < 0)
      return NULL;
  }

  return ret;
}

PyDoc_STRVAR(getAllFsTypes__doc__,
"Receives: nothing\n"
"Returns: string list of all possible filesystem types\n");
static PyObject *getAllFsTypes(PyObject *s)
{
  PedFileSystemType *fstype;
  PyObject *ret;

  ret = PyList_New(0);

  fstype = NULL;
  while ((fstype = ped_file_system_type_get_next(fstype)) != NULL) {
    if (PyList_Append(ret, PyString_FromString(fstype->name)) < 0)
      return NULL;
  }

  return ret;
}

PyDoc_STRVAR(getAllDiskTypes__doc__,
"Receives: nothing\n"
"Returns: string list of all possible disk types\n");
static PyObject *getAllDiskTypes(PyObject *s)
{
  PedDiskType *type;
  PyObject *ret;

  ret = PyList_New(0);

  type = NULL;
  while ((type = ped_disk_type_get_next(type)) != NULL) {
    if (PyList_Append(ret, PyString_FromString(type->name)) < 0)
      return NULL;
  }

  return ret;
}

PyDoc_STRVAR(getAllPartitionFlags__doc__,
"Receives: nothing\n"
"Returns: integer list of all possible partition flags\n");
static PyObject *getAllPartitionFlags(PyObject *s)
{
  PyObject *ret;
  int flag;

  ret = PyList_New(0);

  flag = 0;
  while ((flag = ped_partition_flag_next(flag)) != 0) {
    if (PyList_Append(ret, PyInt_FromLong(flag)) < 0)
      return NULL;
  }

  return ret;
}

PyDoc_STRVAR(getAllPartitionFlagsNames__doc__,
"Receives: nothing\n"
"Returns: string list of all possible partition flags names\n");
static PyObject *getAllPartitionFlagsNames(PyObject *s)
{
  PyObject *ret;
  int flag;

  ret = PyList_New(0);

  flag = 0;
  while ((flag = ped_partition_flag_next(flag)) != 0) {
    if (PyList_Append(ret, PyString_FromString(ped_partition_flag_get_name(flag))) < 0)
      return NULL;
  }

  return ret;
}

PyDoc_STRVAR(getPartitionFlagByName__doc__,
"Description: gets the flag state for a certain flag name\n"
"Receives: (flag_name)\n"
"          flag_name must be a string\n"
"Returns: an integer object representing the flag state (0 or 1)\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getPartitionFlagByName(PyObject *s, PyObject *args)
{
  char *name;
  int flag;

  if (!PyArg_ParseTuple(args, "s", &name))
    return NULL;

  if (!(flag = ped_partition_flag_get_by_name(name))) {
    PyErr_SetString(plpError, "unknown partition flag name");
    return NULL;
  }

  return PyInt_FromLong(flag);
}

PyDoc_STRVAR(getPartitionFlagName__doc__,
"Description: gets the flag name for a certain flag\n"
"Receives: (flag)\n"
"          flag must be an integer\n"
"Returns: a string with the flag name\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getPartitionFlagName(PyObject *s, PyObject *args)
{
  const char *name;
  int flag;

  if (!PyArg_ParseTuple(args, "i", &flag))
    return NULL;

  plp_exception_string_clear();
  name = ped_partition_flag_get_name(flag);
  if (plp_exception_string_check()) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return PyString_FromString(name);
}

PyDoc_STRVAR(setExceptionHandler__doc__,
"Description: sets the handler for the libparted exceptions\n"
"Receives: (exception_handler)\n"
"          exception_handler must be a callable object\n"
"Returns: None\n"
"Throws: TypeError exception if the supplied object is not callable\n"
"\n"
"Note: exception_handler will be called whenever libparted throws\n"
"      an exception and a PedException object will be passed as an\n"
"      an argument.\n"
"\n"
plpPedException__doc__);
static PyObject *setExceptionHandler(PyObject *s, PyObject *args)
{
  PyObject *eh;

  if (plpExceptionHandler != NULL) {
    Py_DECREF(plpExceptionHandler);
    plpExceptionHandler = NULL;
  }

  if (!PyArg_ParseTuple(args, "O", &eh))
    return NULL;

  if (!PyCallable_Check(eh)) {
    PyErr_SetString(PyExc_TypeError, "parameter must be a callable object");
    return NULL;
  }
  Py_INCREF(eh);
  plpExceptionHandler = eh;

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef pylibpartedModuleMethods[] = {
  { "probeAllDevices", (PyCFunction)probeAllDevices, METH_NOARGS,
    probeAllDevices__doc__ },
  { "getAllFsTypes", (PyCFunction)getAllFsTypes, METH_NOARGS,
    getAllFsTypes__doc__ },
  { "getAllDiskTypes", (PyCFunction)getAllDiskTypes, METH_NOARGS,
    getAllDiskTypes__doc__ },
  { "getAllPartitionFlags", (PyCFunction)getAllPartitionFlags, METH_NOARGS,
    getAllPartitionFlags__doc__ },
  { "getAllPartitionFlagsNames", (PyCFunction)getAllPartitionFlagsNames,
    METH_NOARGS, getAllPartitionFlagsNames__doc__ },
  { "getPartitionFlagByName", (PyCFunction)getPartitionFlagByName,
    METH_VARARGS, getPartitionFlagByName__doc__ },
  { "getPartitionFlagName", (PyCFunction)getPartitionFlagName, METH_VARARGS,
     getPartitionFlagName__doc__ },
  { "setExceptionHandler", (PyCFunction)setExceptionHandler, METH_VARARGS,
    setExceptionHandler__doc__ },
  { NULL }
};

PyDoc_STRVAR(plp__doc__,
	     "pylibparted provides python bindings for libparted.\n");
void initpylibparted(void)
{
  PyObject *m, *d, *o;

  if (PyType_Ready(&plpPedDeviceType) < 0 ||
      PyType_Ready(&plpPedDiskType) < 0 ||
      PyType_Ready(&plpPedDiskTypeType) < 0 ||
      PyType_Ready(&plpPedGeometryType) < 0 ||
      PyType_Ready(&plpPedFileSystemTypeType) < 0 ||
      PyType_Ready(&plpPedFileSystemType) < 0 ||
      PyType_Ready(&plpPedPartitionType) < 0 ||
      PyType_Ready(&plpPedAlignmentType) < 0 ||
      PyType_Ready(&plpPedConstraintType) < 0 ||
      PyType_Ready(&plpPedExceptionType) < 0 ||
      PyType_Ready(&plpPedTimerType) < 0) {
    PyErr_SetString(PyExc_ImportError, "types are not ready");
    return;
  }

  m = Py_InitModule3("pylibparted", pylibpartedModuleMethods,
		     plp__doc__);
  if (!m) {
    PyErr_SetString(PyExc_ImportError, "Py_InitModule3(\"pylibparted\") "
		                       "failed");
    return;
  }

  Py_INCREF(&plpPedDeviceType);
  PyModule_AddObject(m, "PedDevice", (PyObject *)&plpPedDeviceType);

  Py_INCREF(&plpPedDiskType);
  PyModule_AddObject(m, "PedDisk", (PyObject *)&plpPedDiskType);

  Py_INCREF(&plpPedDiskTypeType);
  PyModule_AddObject(m, "PedDiskType", (PyObject *)&plpPedDiskTypeType);

  Py_INCREF(&plpPedGeometryType);
  PyModule_AddObject(m, "PedGeometry", (PyObject *)&plpPedGeometryType);

  Py_INCREF(&plpPedFileSystemTypeType);
  PyModule_AddObject(m, "PedFileSystemType",
		     (PyObject *)&plpPedFileSystemTypeType);

  Py_INCREF(&plpPedFileSystemType);
  PyModule_AddObject(m, "PedFileSystem", (PyObject *)&plpPedFileSystemType);

  Py_INCREF(&plpPedPartitionType);
  PyModule_AddObject(m, "PedPartition", (PyObject *)&plpPedPartitionType);

  Py_INCREF(&plpPedAlignmentType);
  PyModule_AddObject(m, "PedAlignment", (PyObject *)&plpPedAlignmentType);

  Py_INCREF(&plpPedConstraintType);
  PyModule_AddObject(m, "PedConstraint", (PyObject *)&plpPedConstraintType);

  plpError = PyErr_NewException("pylibparted.plpError", NULL, NULL);
  Py_INCREF(plpError);
  PyModule_AddObject(m, "plpError", plpError);

  ped_exception_set_handler(plp_exception_handler);

  Py_INCREF(&plpPedTimerType);
  PyModule_AddObject(m, "PedTimer", (PyObject *)&plpPedTimerType);

  d = PyModule_GetDict(m);

#define REGISTER_ENUM(val) \
        PyDict_SetItemString(d, #val, o=PyInt_FromLong(PED_ ##val)); \
        Py_DECREF(o);

  REGISTER_ENUM(DEVICE_UNKNOWN);
  REGISTER_ENUM(DEVICE_SCSI);
  REGISTER_ENUM(DEVICE_IDE);
  REGISTER_ENUM(DEVICE_DAC960);
  REGISTER_ENUM(DEVICE_CPQARRAY);
  REGISTER_ENUM(DEVICE_FILE);
  REGISTER_ENUM(DEVICE_ATARAID);
  REGISTER_ENUM(DEVICE_I2O);

  REGISTER_ENUM(DISK_TYPE_EXTENDED);
  REGISTER_ENUM(DISK_TYPE_PARTITION_NAME);

  REGISTER_ENUM(DISK_TYPE_FIRST_FEATURE);
  REGISTER_ENUM(DISK_TYPE_LAST_FEATURE);

  REGISTER_ENUM(PARTITION_NORMAL);
  REGISTER_ENUM(PARTITION_LOGICAL);
  REGISTER_ENUM(PARTITION_EXTENDED);
  REGISTER_ENUM(PARTITION_FREESPACE);
  REGISTER_ENUM(PARTITION_METADATA);

  REGISTER_ENUM(PARTITION_BOOT);
  REGISTER_ENUM(PARTITION_ROOT);
  REGISTER_ENUM(PARTITION_SWAP);
  REGISTER_ENUM(PARTITION_HIDDEN);
  REGISTER_ENUM(PARTITION_RAID);
  REGISTER_ENUM(PARTITION_LVM);
  REGISTER_ENUM(PARTITION_LBA);
  REGISTER_ENUM(PARTITION_HPSERVICE);
  REGISTER_ENUM(PARTITION_PALO);
  REGISTER_ENUM(PARTITION_PREP);

  REGISTER_ENUM(PARTITION_FIRST_FLAG);
  REGISTER_ENUM(PARTITION_LAST_FLAG);

  REGISTER_ENUM(EXCEPTION_INFORMATION);
  REGISTER_ENUM(EXCEPTION_WARNING);
  REGISTER_ENUM(EXCEPTION_ERROR);
  REGISTER_ENUM(EXCEPTION_FATAL);
  REGISTER_ENUM(EXCEPTION_BUG);
  REGISTER_ENUM(EXCEPTION_NO_FEATURE);
  REGISTER_ENUM(EXCEPTION_UNHANDLED);
  REGISTER_ENUM(EXCEPTION_FIX);
  REGISTER_ENUM(EXCEPTION_YES);
  REGISTER_ENUM(EXCEPTION_NO);
  REGISTER_ENUM(EXCEPTION_OK);
  REGISTER_ENUM(EXCEPTION_RETRY);
  REGISTER_ENUM(EXCEPTION_IGNORE);
  REGISTER_ENUM(EXCEPTION_CANCEL);
  REGISTER_ENUM(EXCEPTION_OK_CANCEL);
  REGISTER_ENUM(EXCEPTION_YES_NO);
  REGISTER_ENUM(EXCEPTION_YES_NO_CANCEL);
  REGISTER_ENUM(EXCEPTION_IGNORE_CANCEL);
  REGISTER_ENUM(EXCEPTION_RETRY_CANCEL);
  REGISTER_ENUM(EXCEPTION_RETRY_IGNORE_CANCEL);

  REGISTER_ENUM(EXCEPTION_OPTION_FIRST);
  REGISTER_ENUM(EXCEPTION_OPTION_LAST);
}
