/*
 * plppeddisk.c - implementation of PedDisk
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
#include "plppeddisk.h"
#include "plppeddevice.h"
#include "plppeddisktype.h"
#include "plppedpartition.h"
#include "plppedconstraint.h"
#include "plppedexception.h"

/* plpPedDisk factory function */

plpPedDisk *new_plppeddisk(PedDisk *disk, int native)
{
  plpPedDisk *ret;

  if (!(ret = (plpPedDisk *)plpPedDiskType.tp_alloc(&plpPedDiskType, 0)))
    return NULL;

  ret->disk = disk;
  ret->native = native;

  return ret;
}

/* plpPedDisk methods */

PyDoc_STRVAR(commit__doc__,
"Description: writes the partition table to disk and informs the\n"
"             operating system\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *commit(plpPedDisk *s)
{
  if (!ped_disk_commit(s->disk)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(duplicate__doc__,
"Description: duplicates the PedDisk object\n"
"Receives: nothing\n"
"Returns: a new copy of the PedDisk object\n");
static PyObject *duplicate(plpPedDisk *s)
{
  return (PyObject *)new_plppeddisk(ped_disk_duplicate(s->disk), 1);
}

PyDoc_STRVAR(check__doc__,
"Description: checks for simple errors on the partition table\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *check(plpPedDisk *s)
{
  if (!ped_disk_check(s->disk)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(getPartitions__doc__,
"Description: returns a list with all partitions in the disk\n"
"Receives: nothing\n"
"Returns: a list of PedPartitions objects\n");
static PyObject *getPartitions(plpPedDisk *s)
{
  PedPartition *part;
  PyObject *ret;

  ret = PyList_New(0);

  part = NULL;
  while ((part = ped_disk_next_partition(s->disk, part))) {
    if (PyList_Append(ret, (PyObject *)new_plppedpartition(part, 1)) < 0)
      return NULL;
  }

  return ret;
}

PyDoc_STRVAR(getExtendedPartition__doc__,
"Description: returns the extended partition when it exists\n"
"Receives: nothing\n"
"Returns: a PedPartition object or None if there is\n"
"         no extended partition\n");
static PyObject *getExtendedPartition(plpPedDisk *s)
{
  PedPartition *part;

  if ((part = ped_disk_extended_partition(s->disk)))
    return (PyObject *)new_plppedpartition(part, 1);

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(getMaxPrimaryPartitionCount__doc__,
"Description: returns the maximum number of primary partitions\n"
"             the partition table can have\n"
"Receives: nothing\n"
"Returns: an integer object\n");
static PyObject *getMaxPrimaryPartitionCount(plpPedDisk *s)
{
  return PyInt_FromLong((long)ped_disk_get_max_primary_partition_count(s->disk));
}

PyDoc_STRVAR(getPrimaryPartitionCount__doc__,
"Description: returns the number of primary partitions\n"
"Receives: nothing\n"
"Returns: an integer object\n");
static PyObject *getPrimaryPartitionCount(plpPedDisk *s)
{
  return PyInt_FromLong((long)ped_disk_get_primary_partition_count(s->disk));
}

PyDoc_STRVAR(getLastPartitionNum__doc__,
"Description: returns the highest partition number of all\n"
"Receives: nothing\n"
"Returns: an integer object\n");
static PyObject *getLastPartitionNum(plpPedDisk *s)
{
  return PyInt_FromLong((long)ped_disk_get_last_partition_num(s->disk));
}

PyDoc_STRVAR(minimizeExtendedPartition__doc__,
"Description: tries to shrink the extended partition\n"
"             to the minimum possible size\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *minimizeExtendedPartition(plpPedDisk *s)
{
  if (!ped_disk_minimize_extended_partition(s->disk)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(addPartition__doc__,
"Description: adds a partition to the partition table\n"
"Receives: (plppart, plpconst)\n"
"          plppart must be a PedPartition object\n"
"          plpconst must be a PedConstraint object\n"
"          Note: plppart's geometry might change, subject to\n"
"                plpconst\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *addPartition(plpPedDisk *s, PyObject *args)
{
  plpPedConstraint *plpconstraint;
  plpPedPartition *plppart;

  if (!PyArg_ParseTuple(args, "O!O!",
			&plpPedPartitionType, &plppart,
			&plpPedConstraintType, &plpconstraint))
    return NULL;

  if (!ped_disk_add_partition(s->disk, plppart->part,
			      plpconstraint->constraint)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }
  plppart->native = 1;  /* protect from double free */

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(delPartition__doc__,
"Description: deletes a partition from the partition table\n"
"Receives: (plppart)\n"
"          plppart must be a PedPartition object\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *delPartition(plpPedDisk *s, PyObject *args)
{
  plpPedPartition *plppart;

  if (!PyArg_ParseTuple(args, "O!", &plpPedPartitionType, &plppart))
    return NULL;

  if (!ped_disk_delete_partition(s->disk, plppart->part)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }
  plppart->native = 1;  /* protect from double free */

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(delAllPartitions__doc__,
"Description: deletes all partitions from the partition table\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *delAllPartitions(plpPedDisk *s)
{
  if (!ped_disk_delete_all(s->disk)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(getType__doc__,
"Description: returns the disk type\n"
"Receives: nothing\n"
"Returns: a PedDiskType object\n");
static PyObject *getType(plpPedDisk *s)
{
  return (PyObject *)new_plppeddisktype(s->disk->type);
}

PyDoc_STRVAR(getDevice__doc__,
"Description: returns the device\n"
"Receives: nothing\n"
"Returns: a PedDevice object\n");
static PyObject *getDevice(plpPedDisk *s)
{
  return (PyObject *)new_plppeddevice(s->disk->dev, 1);
}

PyDoc_STRVAR(getPartition__doc__,
"Description: returns a partition by its number\n"
"Receives: (num)\n"
"          num must be an integer object\n"
"Returns: a PedPartition object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getPartition(plpPedDisk *s, PyObject *args)
{
  PedPartition *part;
  int num;

  if (!PyArg_ParseTuple(args, "i", &num))
    return NULL;

  if (!(part = ped_disk_get_partition(s->disk, num))) {
    PyErr_SetString(plpError, "partition does not exist");
    return NULL;
  }

  return (PyObject *)new_plppedpartition(part, 1);
}

PyDoc_STRVAR(getPartitionBySector__doc__,
"Description: returns the partition that owns a sector\n"
"Receives: (sector)\n"
"          sector must be a long object\n"
"Returns: a PedPartition object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getPartitionBySector(plpPedDisk *s, PyObject *args)
{
  PedPartition *part;
  PedSector sector;

  if (!PyArg_ParseTuple(args, "L", &sector))
    return NULL;

  if (!(part = ped_disk_get_partition_by_sector(s->disk, sector))) {
    PyErr_SetString(plpError, "partition does not exist");
    return NULL;
  }

  return (PyObject *)new_plppedpartition(part, 1);
}

static PyMethodDef plpPedDisk_methods[] = {
  { "commit", (PyCFunction)commit, METH_NOARGS, commit__doc__ },
  { "duplicate", (PyCFunction)duplicate, METH_NOARGS, duplicate__doc__ },
  { "check", (PyCFunction)check, METH_NOARGS, check__doc__ },
  { "getPartitions", (PyCFunction)getPartitions, METH_NOARGS,
    getPartitions__doc__ },
  { "getExtendedPartition", (PyCFunction)getExtendedPartition, METH_NOARGS,
    getExtendedPartition__doc__ },
  { "getMaxPrimaryPartitionCount", (PyCFunction)getMaxPrimaryPartitionCount,
    METH_NOARGS, getMaxPrimaryPartitionCount__doc__ },
  { "getPrimaryPartitionCount", (PyCFunction)getPrimaryPartitionCount,
    METH_NOARGS, getPrimaryPartitionCount__doc__ },
  { "getLastPartitionNum", (PyCFunction)getLastPartitionNum, METH_NOARGS,
    getLastPartitionNum__doc__ },
  { "minimizeExtendedPartition", (PyCFunction)minimizeExtendedPartition,
    METH_NOARGS, minimizeExtendedPartition__doc__ },
  { "addPartition", (PyCFunction)addPartition, METH_VARARGS,
    addPartition__doc__ },
  { "delPartition", (PyCFunction)delPartition, METH_VARARGS,
    delPartition__doc__ },
  { "delAllPartitions", (PyCFunction)delAllPartitions, METH_NOARGS,
    delAllPartitions__doc__ },
  { "getType", (PyCFunction)getType, METH_NOARGS, getType__doc__ },
  { "getDevice", (PyCFunction)getDevice, METH_NOARGS, getDevice__doc__ },
  { "getPartition", (PyCFunction)getPartition, METH_VARARGS,
    getPartition__doc__ },
  { "getPartitionBySector", (PyCFunction)getPartitionBySector, METH_VARARGS,
    getPartitionBySector__doc__ },
  { NULL }
};

/* plpPedDisk type */

static void plpPedDisk_dealloc(plpPedDisk *s)
{
  if (s->disk && !s->native)
    ped_disk_destroy(s->disk);
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *plpPedDisk_new(PyTypeObject *type, PyObject *args,
				PyObject *kwds)
{
  plpPedDisk *s;

  if (!(s = (plpPedDisk *)type->tp_alloc(type, 0)))
    return NULL;

  s->disk = NULL;

  return (PyObject *)s;
}

static int plpPedDisk_init(plpPedDisk *s, PyObject *args, PyObject *kwds)
{
  _plpPedDiskType *plptype;
  plpPedDevice *plpdev;
  PedDisk *disk;

  if (!PyArg_ParseTuple(args, "O!O!",
			&plpPedDeviceType, &plpdev,
			&plpPedDiskTypeType, &plptype))
    return -1;

  disk = ped_disk_new_fresh(plpdev->dev, plptype->type);
  if (!disk) {
    plp_set_error_from_ped_exception();
    return -1;
  }

  s->disk = disk;
  s->native = 0;

  return 0;
}

PyDoc_STRVAR(plpPedDisk__doc__,
"Description: a PedDisk is always associated with a device and has a\n"
"             partition table\n"
"\n"
"You can create a new partition table on a device and get the\n"
"PedDisk object with:\n"
"\n"
"  obj = pylibparted.PedDisk(plpdev, plptype)\n"
"  (plpdev must be a PedDevice object and\n"
"   plptype must be a PedDiskType object)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n"
"\n"
"  Note: if you wanna read the partition table from a device\n"
"        you must use the diskNew() method from PedDevice.\n");
PyTypeObject plpPedDiskType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedDisk",
  .tp_basicsize      = sizeof(plpPedDisk),
  .tp_dealloc        = (destructor)plpPedDisk_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedDisk__doc__,
  .tp_methods        = plpPedDisk_methods,
  .tp_init           = (initproc)plpPedDisk_init,
  .tp_new            = plpPedDisk_new
};
