/*
 * plppeddevice.c - implementation of PedDevice
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
#include "plppedconstraint.h"
#include "plppedexception.h"

/* plpPedDevice factory function */

plpPedDevice *new_plppeddevice(PedDevice *dev, int native)
{
  plpPedDevice *ret;

  if (!(ret = (plpPedDevice *)plpPedDeviceType.tp_alloc(&plpPedDeviceType, 0)))
    return NULL;

  ret->dev = dev;
  ret->native = native;

  return ret;
}

/* plpPedDevice methods */

PyDoc_STRVAR(getModel__doc__,
"Receives: nothing\n"
"Returns: a string with the hardware manufacturer and model\n"
"         of the device\n");
static PyObject *getModel(plpPedDevice *s)
{
  return PyString_FromString(s->dev->model);
}

PyDoc_STRVAR(getPath__doc__,
"Receives: nothing\n"
"Returns: a string with the block device (eg. /dev/hda)\n");
static PyObject *getPath(plpPedDevice *s)
{
  return PyString_FromString(s->dev->path);
}

PyDoc_STRVAR(getLength__doc__,
"Receives: nothing\n"
"Returns: a long object with the size of the device (in sectors)\n");
static PyObject *getLength(plpPedDevice *s)
{
  return PyLong_FromLongLong(s->dev->length);
}

PyDoc_STRVAR(getSectorSize__doc__,
"Receives: nothing\n"
"Returns: an integer object with the sector size of the device\n"
"         (in bytes)\n");
static PyObject *getSectorSize(plpPedDevice *s)
{
  return PyInt_FromLong(s->dev->sector_size);
}

PyDoc_STRVAR(getBiosCHS__doc__,
"Receives: nothing\n"
"Returns: a tuple with the BIOS reported CHS of the device\n");
static PyObject *getBiosCHS(plpPedDevice *s)
{
  return Py_BuildValue("(lll)",
		       s->dev->bios_geom.cylinders,
		       s->dev->bios_geom.heads,
		       s->dev->bios_geom.sectors);
}

PyDoc_STRVAR(getHwCHS__doc__,
"Receives: nothing\n"
"Returns: a tuple with the hardware CHS of the device\n");
static PyObject *getHwCHS(plpPedDevice *s)
{
  return Py_BuildValue("(lll)",
		       s->dev->hw_geom.cylinders,
		       s->dev->hw_geom.heads,
		       s->dev->hw_geom.sectors);
}

PyDoc_STRVAR(diskNew__doc__,
"Description: attempts to read a partition table from the device\n"
"Receives: nothing\n"
"Returns: a PedDisk object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *diskNew(plpPedDevice *s)
{
  PedDisk *disk;

  if (!(disk = ped_disk_new(s->dev))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppeddisk(disk, 1);
}

PyDoc_STRVAR(getAnyConstraint__doc__,
"Description: returns a constraint such that any geometry on\n"
"             device is a solution\n"
"Receives: nothing\n"
"Returns: a PedConstraint object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *getAnyConstraint(plpPedDevice *s)
{
  PedConstraint *c;

  if (!(c = ped_constraint_any(s->dev))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppedconstraint(c);
}

PyDoc_STRVAR(clobber__doc__,
"Description: overwrites all partition table signatures on device\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *clobber(plpPedDevice *s)
{
  if (!ped_disk_clobber(s->dev)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(diskProbe__doc__,
"Description: detects the type of partition table on device\n"
"Receives: nothing\n"
"Returns: a PedDiskType object\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *diskProbe(plpPedDevice *s)
{
  PedDiskType *type;

  if (!(type = ped_disk_probe(s->dev))) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  return (PyObject *)new_plppeddisktype(type);
}

PyDoc_STRVAR(isBusy__doc__,
"Receives: nothing\n"
"Returns: true if the device is busy\n"
"         or false if the device is not busy\n");
static PyObject *isBusy(plpPedDevice *s)
{
  if (ped_device_is_busy(s->dev)) {
    Py_INCREF(Py_True);
    return Py_True;
  }

  Py_INCREF(Py_False);
  return Py_False;
}

PyDoc_STRVAR(getType__doc__,
"Receives: nothing\n"
"Returns: the device type\n");
static PyObject *getType(plpPedDevice *s)
{
  return PyInt_FromLong(s->dev->type);
}

PyDoc_STRVAR(plp_open__doc__,
"Description: attempts to open the device\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *plp_open(plpPedDevice *s)
{
  if (!ped_device_open(s->dev)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(plp_close__doc__,
"Description: closes the device\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *plp_close(plpPedDevice *s)
{
  if (!ped_device_close(s->dev)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(plp_sync__doc__,
"Description: flushes the device write cache\n"
"Receives: nothing\n"
"Returns: None\n"
"Throws: pylibparted.plpError exception on error\n");
static PyObject *plp_sync(plpPedDevice *s)
{
  if (!ped_device_sync(s->dev)) {
    plp_set_error_from_ped_exception();
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef plpPedDevice_methods[] = {
  { "getModel", (PyCFunction)getModel, METH_NOARGS, getModel__doc__ },
  { "getPath", (PyCFunction)getPath, METH_NOARGS, getPath__doc__ },
  { "getLength", (PyCFunction)getLength, METH_NOARGS, getLength__doc__ },
  { "getSectorSize", (PyCFunction)getSectorSize, METH_NOARGS,
    getSectorSize__doc__ },
  { "getBiosCHS", (PyCFunction)getBiosCHS, METH_NOARGS, getBiosCHS__doc__ },
  { "getHwCHS", (PyCFunction)getHwCHS, METH_NOARGS, getHwCHS__doc__ },
  { "diskNew", (PyCFunction)diskNew, METH_NOARGS, diskNew__doc__ },
  { "getAnyConstraint", (PyCFunction)getAnyConstraint, METH_NOARGS,
    getAnyConstraint__doc__ },
  { "clobber", (PyCFunction)clobber, METH_NOARGS, clobber__doc__ },
  { "diskProbe", (PyCFunction)diskProbe, METH_NOARGS, diskProbe__doc__ },
  { "isBusy", (PyCFunction)isBusy, METH_NOARGS, isBusy__doc__ },
  { "getType", (PyCFunction)getType, METH_NOARGS, getType__doc__ },
  { "open", (PyCFunction)plp_open, METH_NOARGS, plp_open__doc__ },
  { "close", (PyCFunction)plp_close, METH_NOARGS, plp_close__doc__ },
  { "sync", (PyCFunction)plp_sync, METH_NOARGS, plp_sync__doc__ },
  { NULL }
};

/* plpPedDevice type */

static void plpPedDevice_dealloc(plpPedDevice *s)
{
  if (s->dev && !s->native)
    ped_device_destroy(s->dev);
  s->ob_type->tp_free((PyObject*)s);
}

static PyObject *plpPedDevice_new(PyTypeObject *type, PyObject *args,
				  PyObject *kwds)
{
  plpPedDevice *s;

  if (!(s = (plpPedDevice *)type->tp_alloc(type, 0)))
    return NULL;

  s->dev = NULL;

  return (PyObject *)s;
}

static int plpPedDevice_init(plpPedDevice *s, PyObject *args, PyObject *kwds)
{
  char *path;

  if (!PyArg_ParseTuple(args, "s", &path))
    return -1;

  if (!(s->dev = ped_device_get(path))) {
    plp_set_error_from_ped_exception();
    return -1;
  }
  s->native = 1;

  return 0;
}

PyDoc_STRVAR(plpPedDevice__doc__,
"Description: a PedDevice object represents a storage device\n"
"\n"
"A new PedDevice object can be created with:\n"
"\n"
"  obj = pylibparted.PedDevice(device_path)\n"
"  (device_path must be a string with the block device)\n"
"\n"
"  It throws a pylibparted.plpError exception on error.\n");
PyTypeObject plpPedDeviceType = {
  plp_PyObject_EXTRA_INIT
  .ob_refcnt         = 1,
  .ob_type           = &PyType_Type,
  .tp_name           = "pylibparted.PedDevice",
  .tp_basicsize      = sizeof(plpPedDevice),
  .tp_dealloc        = (destructor)plpPedDevice_dealloc,
  .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  .tp_doc            = plpPedDevice__doc__,
  .tp_methods        = plpPedDevice_methods,
  .tp_init           = (initproc)plpPedDevice_init,
  .tp_new            = plpPedDevice_new
};
