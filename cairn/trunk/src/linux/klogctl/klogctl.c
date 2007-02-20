/*
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/klog.h>
#include <errno.h>
#include <string.h>
#include <Python.h>


PyDoc_STRVAR(pyfileMajorMinor__doc__,
"Receives: filename\n"
"Returns: major and minor of file. (0,0) on non-device files.\n");

// python's os.stat() doesnt seem to support st_rdev and decoding the major
// and minor. So do that here.
static PyObject *pyfileMajorMinor(PyObject *s, PyObject *args)
{
    const char* filename=NULL;
    int fmajor=0, fminor=0;
    struct stat sbuf;

    if (!PyArg_ParseTuple(args, "s", &filename))
    {
        PyErr_SetString(PyExc_TypeError, "parameters must be a string");
        return NULL;
    }

    if (stat(filename, &sbuf) != 0)
    {
        PyErr_SetString(PyExc_OSError, strerror(errno));
        return NULL;
    }

    fmajor=major(sbuf.st_rdev);
    fminor=minor(sbuf.st_rdev);

    return Py_BuildValue("(ii)", fmajor, fminor);
}

PyDoc_STRVAR(pyklogctl__doc__,
"Receives: action, size\n"
"Returns: string containing kernel message buffer contents, or None\n");

static PyObject *pyklogctl(PyObject *s, PyObject *args)
{
    int action=-1, size=-1;

    if (!PyArg_ParseTuple(args, "ii", &action, &size))
    {
        PyErr_SetString(PyExc_TypeError, "parameters must be two integers");
        return NULL;
    }

    if ((action < 0) || (action > 10))
    {
        PyErr_SetString(PyExc_TypeError,
                        "parameter action must be a value between 0 and 9");
        return NULL;
    }
    // Put a sanity limit on the buffer size
    if ((size < 0) || (size > 524288))
    {
        PyErr_SetString(PyExc_TypeError,
                        "parameter size must be a value between 0 and 524288");
        return NULL;
    }

    PyObject *ret = NULL;
    char *buff = NULL;
    int kret;

    if (size)
    {
        buff = (char*)malloc(size + 1);
    }
    kret = klogctl(action, buff, size);
    if (kret < 0)
    {
        PyErr_SetString(PyExc_OSError, strerror(errno));
    }
    else if (kret == 0)
    {
        Py_INCREF(Py_None);
        ret = Py_None;
    }
    else if (action == 10)
    {
        ret = PyInt_FromLong(kret);
    }
    else
    {
        buff[kret] = 0;
        ret = PyString_FromString(buff);
    }

    if (buff)
    {
        free(buff);
    }

    return ret;
}

static PyMethodDef klogctlModuleMethods[] =
{
    {"klogctl", (PyCFunction)pyklogctl, METH_VARARGS, pyklogctl__doc__},
    {"fileMajorMinor", (PyCFunction)pyfileMajorMinor, METH_VARARGS,
     pyfileMajorMinor__doc__},
    {NULL}
};

PyDoc_STRVAR(modklogctl__doc__,
	     "klogctl provides python bindings for the klogctl system call.\n");

void initklogctl(void)
{
  if (!Py_InitModule3("klogctl", klogctlModuleMethods, modklogctl__doc__))
  {
      PyErr_SetString(PyExc_ImportError,
                      "Py_InitModule3(\"klogctl\") failed");
      return;
  }
}
