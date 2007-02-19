#define _GNU_SOURCE

#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/mount.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include "libvolume_id.h"

#undef _POSIX_C_SOURCE
#undef _GNU_SOURCE
#include <Python.h>

extern int replace_untrusted_chars(char *str);


PyDoc_STRVAR(pyprobe__doc__,
"Receives: filename\n"
"Returns: (usage, type, version, uuid, label, label_safe) or tuple of None values.\n");

static PyObject *pyprobe(PyObject *s, PyObject *args)
{
    char buff[1024];
	static char label_safe[VOLUME_ID_LABEL_SIZE];
    const char* filename = NULL;
	struct volume_id *vid = NULL;
	uint64_t size;
    PyObject* ret = NULL;

    if (!PyArg_ParseTuple(args, "s", &filename))
    {
        PyErr_SetString(PyExc_TypeError, "parameter must be a string");
        return NULL;
    }

	vid = volume_id_open_node(filename);
    if (!vid)
    {
        sprintf(buff, "volume_id_open_node: %s", strerror(errno));
        PyErr_SetString(PyExc_OSError, buff);
        return NULL;
    }

	if (ioctl(vid->fd, BLKGETSIZE64, &size) != 0)
    {
        sprintf(buff, "ioctl(BLKGETSIZE64): %s", strerror(errno));
        PyErr_SetString(PyExc_OSError, buff);
        return NULL;
    }

	if (volume_id_probe_all(vid, 0, size) != 0)
    {
        sprintf(buff, "volume_id_probe_all: %s", strerror(errno));
        PyErr_SetString(PyExc_OSError, buff);
        return NULL;
    }

    memset(label_safe, 0, sizeof(label_safe));
	volume_id_set_str(label_safe, vid->label, sizeof(vid->label));
	replace_untrusted_chars(label_safe);

    ret = Py_BuildValue("(ssssss)", vid->usage, vid->type, vid->type_version,
                        vid->uuid, vid->label, label_safe);

    volume_id_close(vid);

    return ret;
}

static PyMethodDef volumeidModuleMethods[] =
{
    {"probe", (PyCFunction)pyprobe, METH_VARARGS, pyprobe__doc__},
    {NULL}
};

PyDoc_STRVAR(modvolumeid__doc__,
	     "volumeid provides python bindings for accessing volume's label, uuid and other information.\n");

void initvolumeid(void)
{
  if (!Py_InitModule3("volumeid", volumeidModuleMethods, modvolumeid__doc__))
  {
      PyErr_SetString(PyExc_ImportError,
                      "Py_InitModule3(\"volumeid\") failed");
      return;
  }
}
