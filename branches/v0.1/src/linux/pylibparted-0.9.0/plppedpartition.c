/*
 * plppedpartition.c - implementation of PedPartition
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
#include "plppedpartition.h"
#include "plppedgeometry.h"
#include "plppedconstraint.h"
#include "plppedexception.h"
#include "plppedfilesystemtype.h"
#include "plppeddisk.h"

#include <string.h>

/* plpPedPartition factory function */

plpPedPartition *new_plppedpartition(PedPartition *part, int native)
{
  plpPedPartition *ret;

  if (!(ret = (plpPedPartition *)plpPedPartitionType.tp_alloc(&plpPedPartitionType, 0)))
    return NULL;

  ret->part = part;
  ret->native = native;

  return ret;
}

/* plpPedPartition methods */

PyDoc_STRVAR(isActive__doc__,
"Description: checks if the partition is active\n"
"Receives: nothing\n"
"Returns: true if the partition is active\n"
"         or false if it is not\n");
static PyObject *isActive(plpPedPartition *s)
{
  if (ped_partition_is_active(s->part)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(isBusy__doc__,
"Description: checks if the partition is busy (i.e. mounted)\n"
"Receives: nothing\n"
"Returns: true if the partition is busy\n"
"         or false if it is not\n");
static PyObject *isBusy(plpPedPartition *s)
{
  if (ped_partition_is_busy(s->part)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(getPath__doc__,
"Description: returns a path to address the partition in the\n"
"             operating system\n"
"Receives: nothing\n"
"Returns: a string object\n");
static PyObject *getPath(plpPedPartition *s)
{
  return PyString_FromString(ped_partition_get_path(s->part));
}

PyDoc_STRVAR(getTypeName__doc__,
"Description: returns a name for the partition type\n"
"Receives: nothing\n"
"Returns: a string object\n");
static PyObject *getTypeName(plpPedPartition *s)
{
  return PyString_FromString(ped_partition_type_get_name(s->part->type));
}

PyDoc_STRVAR(getFlagsNames__doc__,
"Description: returns the partition flags names\n"
"Receives: nothing\n"
"Returns: a string list\n");
static PyObject *getFlagsNames(plpPedPartition *s)
{
  PedPartitionFlag flag;
  PyObject *ret;

  ret = PyList_New(0);

  if (!ped_partition_is_active(s->part))  /* avoid seg fault :-) */
    return ret;

  flag = 0;
  while ((flag = ped_partition_flag_next(flag))) {
    if (ped_partition_is_flag_available(s->part, flag) &&
	ped_partition_get_flag(s->part, flag))
      if (PyList_Append(ret, PyString_FromString(ped_partition_flag_get_name(flag))) < 0)
	return NULL;
  }

  return ret;
}

PyDoc_STRVAR(getGeometry__doc__,
"Description: returns the partition geometry\n"
"Receives: nothing\n"
"Returns: a PedGeometry object\n");
static PyObject *getGeometry(plpPedPartition *s)
{
  return (PyObject *)new_plppedgeometry(&s->part->geom, 1);
}

PyDoc_STRVAR(getNum__doc__,
"Description: returns the partition number\n"
"Receives: nothing\n"
"Returns: an integer object\n");
static PyObject *getNum(plpPedPartition *s)
{
  return PyInt_FromLong(s->part->num);
}

PyDoc_STRVAR(setNum__doc__,
"Description: sets the partition number\n"
"Receives: an integer object\n"
"Returns: nothing\n");
static PyObject *setNum(plpPedPartition *s, PyObject *args)
{
    int num;

    if (!PyArg_ParseTuple(args, "i", &num))
        return NULL;
    s->part->num = num;

    Py_INCREF(Py_None);
    return Py_None;
}

PyDoc_STRVAR(getFsType__doc__,
"Description: returns the filesystem type on the partition\n"
"Receives: nothing\n"
"Returns: a PedFileSystemType object or None if it is unknown\n");
static PyObject *getFsType(plpPedPartition *s)
{
  if (s->part->fs_type)
    return (PyObject *)new_plppedfilesystemtype(s->part->fs_type);

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(getId__doc__,
"Description: returns the partition ID\n"
"             (only for msdos disk types)\n"
"Receives: nothing\n"
"Returns: an integer object\n"
"         Note: zero is returned for free space partitions\n"
"               and -1 is returned for metadata partitions\n");
static PyObject *getId(plpPedPartition *s)
{
  PedPartition *part;
  DosPartitionData *dosdata;
  unsigned long ptype;

  part = s->part;

  if (!part->disk || strcmp(part->disk->type->name, "msdos")) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  /* Active partitions */
  if (ped_partition_is_active(part)) {
    dosdata = (DosPartitionData *)part->disk_specific;
    ptype = (long)dosdata->orig->raw_part.type;

    return PyInt_FromLong(ptype);
  }

  /* Free space partition */
  if (part->type & PED_PARTITION_FREESPACE)
    return PyInt_FromLong(0);

  /* Metadata partition */
  return PyInt_FromLong(-1);
}

PyDoc_STRVAR(setGeometry__doc__,
"Description: sets the partition geometry subject to a constraint\n"
"Receives: (plpconst, start_sector, end_sector)\n"
"          plpconst must be a PedConstraint object\n"
"          start_sector and end_sector must be long objects\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *setGeometry(plpPedPartition *s, PyObject *args)
{
  plpPedConstraint *plpconstraint;
  PedSector start, end;

  if (!PyArg_ParseTuple(args, "O!LL", &plpPedConstraintType, &plpconstraint,
			&start, &end))
    return NULL;

  if (!ped_disk_set_partition_geom(s->part->disk, s->part,
				   plpconstraint->constraint,
				   start, end)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(maximize__doc__,
"Description: grows the partition to the maximum possible subject\n"
"             to a constraint\n"
"Receives: (plpconst)\n"
"          plpconst must be a PedConstraint object\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *maximize(plpPedPartition *s, PyObject *args)
{
  plpPedConstraint *plpconstraint;

  if (!PyArg_ParseTuple(args, "O!", &plpPedConstraintType, &plpconstraint))
    return NULL;

  if (!ped_disk_maximize_partition(s->part->disk, s->part,
				   plpconstraint->constraint)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(getMaxGeometry__doc__,
"Description: returns the maximum geometry the partition can be\n"
"             grown to subject to a constraint\n"
"Receives: (plpconst)\n"
"          plpconst must be a PedConstraint object\n"
"Returns: a PedGeometry object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getMaxGeometry(plpPedPartition *s, PyObject *args)
{
  plpPedConstraint *plpconstraint;
  PedGeometry *geom;

  if (!PyArg_ParseTuple(args, "O!", &plpPedConstraintType, &plpconstraint))
    return NULL;

  if (!(geom = ped_disk_get_max_partition_geometry(s->part->disk, s->part,
						   plpconstraint->constraint))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppedgeometry(geom, 0);
}

PyDoc_STRVAR(getDisk__doc__,
"Description: returns the partition table (disk)\n"
"Receives: nothing\n"
"Returns: a PedDisk object\n");
static PyObject *getDisk(plpPedPartition *s)
{
  return (PyObject *)new_plppeddisk(s->part->disk, 1);
}

PyDoc_STRVAR(getType__doc__,
"Description: returns the partition type\n"
"Receives: nothing\n"
"Returns: an integer object\n");
static PyObject *getType(plpPedPartition *s)
{
  return PyInt_FromLong(s->part->type);
}

PyDoc_STRVAR(setFsType__doc__,
"Description: sets the filesystem for the partition\n"
"Receives: (plpfstype)\n"
"          plpfstype must be a PedFileSystemType object\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *setFsType(plpPedPartition *s, PyObject *args)
{
  _plpPedFileSystemType *plpfstype;

  if (!PyArg_ParseTuple(args, "O!", &plpPedFileSystemTypeType, &plpfstype))
    return NULL;

  if (!ped_partition_set_system(s->part, plpfstype->fstype)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(isFlagAvailable__doc__,
"Description: checks if a flag is available on the partition\n"
"Receives: (flag)\n"
"          flag must be an integer object\n"
"Returns: true if the flag is available\n"
"         or false if it is not\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *isFlagAvailable(plpPedPartition *s, PyObject *args)
{
  int flag, value;

  if (!PyArg_ParseTuple(args, "i", &flag))
    return NULL;

  plp_exception_string_clear();
  value = ped_partition_is_flag_available(s->part, flag);
  if (plp_exception_string_check()) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  if (value) {
    Py_INCREF(Py_True);
    return Py_True;
  }
  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(getFlag__doc__,
"Description: returns the state of a flag on the partition\n"
"Receives: (flag)\n"
"          flag must be an integer object\n"
"Returns: an integer object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getFlag(plpPedPartition *s, PyObject *args)
{
  int flag, value;

  if (!PyArg_ParseTuple(args, "i", &flag))
    return NULL;

  plp_exception_string_clear();
  value = ped_partition_get_flag(s->part, flag);
  if (plp_exception_string_check()) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return PyInt_FromLong(value);
}

PyDoc_STRVAR(setFlag__doc__,
"Description: sets the state of a flag on the partition\n"
"Receives: (flag, state)\n"
"          flag and state must be integer objects\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *setFlag(plpPedPartition *s, PyObject *args)
{
  int flag, state;

  if (!PyArg_ParseTuple(args, "ii", &flag, &state))
    return NULL;

  if (!ped_partition_set_flag(s->part, flag, state)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(getName__doc__,
"Description: returns the partition name\n"
"Receives: nothing\n"
"Returns: a string object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getName(plpPedPartition *s)
{
  const char *name;

  if (!(name = ped_partition_get_name(s->part))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return PyString_FromString(name);
}

PyDoc_STRVAR(setName__doc__,
"Description: sets the partition name\n"
"Receives: (name)\n"
"          name must be a string object\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *setName(plpPedPartition *s, PyObject *args)
{
  char *name;

  if (!PyArg_ParseTuple(args, "s", &name))
    return NULL;

  if (!ped_partition_set_name(s->part, name)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef plpPedPartition_methods[] = {
  { "isActive", (PyCFunction)isActive, METH_NOARGS, isActive__doc__ },
  { "isBusy", (PyCFunction)isBusy, METH_NOARGS, isBusy__doc__ },
  { "getPath", (PyCFunction)getPath, METH_NOARGS, getPath__doc__ },
  { "getTypeName", (PyCFunction)getTypeName, METH_NOARGS, getTypeName__doc__ },
  { "getFlagsNames", (PyCFunction)getFlagsNames, METH_NOARGS,
    getFlagsNames__doc__ },
  { "getGeometry", (PyCFunction)getGeometry, METH_NOARGS, getGeometry__doc__ },
  { "getNum", (PyCFunction)getNum, METH_NOARGS, getNum__doc__ },
  { "setNum", (PyCFunction)setNum, METH_VARARGS, setNum__doc__ },
  { "getFsType", (PyCFunction)getFsType, METH_NOARGS, getFsType__doc__ },
  { "getId", (PyCFunction)getId, METH_NOARGS, getId__doc__ },
  { "setGeometry", (PyCFunction)setGeometry, METH_VARARGS,
    setGeometry__doc__ },
  { "maximize", (PyCFunction)maximize, METH_VARARGS, maximize__doc__ },
  { "getMaxGeometry", (PyCFunction)getMaxGeometry, METH_VARARGS,
    getMaxGeometry__doc__ },
  { "getDisk", (PyCFunction)getDisk, METH_NOARGS, getDisk__doc__ },
  { "getType", (PyCFunction)getType, METH_NOARGS, getType__doc__ },
  { "setFsType", (PyCFunction)setFsType, METH_VARARGS, setFsType__doc__ },
  { "isFlagAvailable", (PyCFunction)isFlagAvailable, METH_VARARGS,
    isFlagAvailable__doc__ },
  { "getFlag", (PyCFunction)getFlag, METH_VARARGS, getFlag__doc__ },
  { "setFlag", (PyCFunction)setFlag, METH_VARARGS, setFlag__doc__ },
  { "getName", (PyCFunction)getName, METH_NOARGS, getName__doc__ },
  { "setName", (PyCFunction)setName, METH_VARARGS, setName__doc__ },
  { NULL }
};

/* plpPedPartition type */

static void plpPedPartition_dealloc(plpPedPartition *s)
{
  if (s->part && !s->native)
    ped_partition_destroy(s->part);
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *plpPedPartition_new(PyTypeObject *type, PyObject *args,
				     PyObject *kwds)
{
  plpPedPartition *s;

  if (!(s = (plpPedPartition *)type->tp_alloc(type, 0)))
    return NULL;

  s->part = NULL;

  return (PyObject *)s;
}

static int plpPedPartition_init(plpPedPartition *s,
				PyObject *args, PyObject *kwds)
{
  const PedFileSystemType *fstype = NULL;
  _plpPedFileSystemType *plpfstype;
  PedSector start, end;
  PedPartitionType ptype;
  plpPedDisk *plpdisk;
  PedPartition *part;

  if (!PyArg_ParseTuple(args, "O!iOLL",
			&plpPedDiskType, &plpdisk, &ptype,
			&plpfstype, &start, &end))
    return -1;

  if (plpfstype != (_plpPedFileSystemType *)Py_None &&
      plpfstype->ob_type != &plpPedFileSystemTypeType) {
    PyErr_SetString(PyExc_TypeError,
		    "the second parameter should be either "
		    "None or a PedFileSystemType object");
    return -1;
  }

  if (plpfstype != (_plpPedFileSystemType *)Py_None)
    fstype = plpfstype->fstype;

  if (!(part = ped_partition_new(plpdisk->disk, ptype, fstype, start, end))) {
    plp_set_error_from_ped_exception();
    return -1;
  }

  s->part = part;
  s->native = 0;

  return 0;
}

PyDoc_STRVAR(plpPedPartition__doc__,
"Description: a PedPartition object represents a partition\n"
"\n"
"A new PedPartition object can be created with:\n"
"\n"
"  obj = pylibparted.PedPartition(plpdisk, ptype, plpfstype,\n"
"                                 start_sector, end_sector)\n"
"  (plpdisk must be a PedDisk object,\n"
"   ptype is the partition type and must be an integer object,\n"
"   plpfstype must be a PedFileSystemType object or None,\n"
"   start_sector and end_sector must be long objects)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedPartitionType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedPartition",
  .tp_basicsize      = sizeof(plpPedPartition),
  .tp_dealloc        = (destructor)plpPedPartition_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedPartition__doc__,
  .tp_methods        = plpPedPartition_methods,
  .tp_init           = (initproc)plpPedPartition_init,
  .tp_new            = plpPedPartition_new
};
