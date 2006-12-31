#include <sys/klog.h>
#include <errno.h>
#include <string.h>
#include <Python.h>


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
