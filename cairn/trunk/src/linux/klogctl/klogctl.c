#include <sys/klog.h>
#include <errno.h>
#include <string.h>
#include <Python.h>


PyDoc_STRVAR(pyklogctl__doc__,
"Receives: action, size\n"
"Returns: string containing kernel message buffer contents, or None\n");

static PyObject *pyklogctl(PyObject *s, PyObject *args)
{
    int action=-1, size=-1, ret;

    if (!PyArg_ParseTuple(args, "ii", &action, &size))
    {
        PyErr_SetString(PyExc_TypeError, "parameters must be two integers");
        return NULL;
    }

    if ((action < 0) || (action > 9))
    {
        PyErr_SetString(PyExc_TypeError,
                        "parameter action must be a value between 0 and 9");
        return NULL;
    }
    if ((size < 0) || (size > 4096))
    {
        PyErr_SetString(PyExc_TypeError,
                        "parameter size must be a value between 0 and 4096");
        return NULL;
    }

    char buff[4097];
    ret = klogctl(action, buff, size);
    if (ret < 0)
    {
        PyErr_SetString(PyExc_OSError, strerror(errno));
        return NULL;
    }
    else if (ret == 0)
    {
        Py_INCREF(Py_None);
        return Py_None;
    }
    else
    {
        buff[ret] = 0;
        return PyString_FromString(buff);
    }
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
