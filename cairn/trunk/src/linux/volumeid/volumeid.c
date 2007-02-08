#define _GNU_SOURCE

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include "libvolume_id.h"

#undef _POSIX_C_SOURCE
#undef _GNU_SOURCE
#include <Python.h>

extern int replace_untrusted_chars(char *str);


static void set_str(char *to, const char *from, size_t count)
{
	size_t i, j, len;

	/* strip trailing whitespace */
	len = strnlen(from, count);
	while (len && isspace(from[len-1]))
		len--;

	/* strip leading whitespace */
	i = 0;
	while (isspace(from[i]) && (i < len))
		i++;

	j = 0;
	while (i < len) {
		/* substitute multiple whitespace */
		if (isspace(from[i])) {
			while (isspace(from[i]))
				i++;
			to[j++] = '_';
		}
		/* skip chars */
		if (from[i] == '/') {
			i++;
			continue;
		}
		to[j++] = from[i++];
	}
	to[j] = '\0';
}


PyDoc_STRVAR(pyprobe__doc__,
"Receives: filename\n"
"Returns: (usage, type, version, uuid, label, label_safe) or tuple of None values.\n");

static PyObject *pyprobe(PyObject *s, PyObject *args)
{
	static char label_safe[VOLUME_ID_LABEL_SIZE];
    const char* filename = NULL;
	struct volume_id *vid = NULL;

    if (!PyArg_ParseTuple(args, "s", &filename))
    {
        PyErr_SetString(PyExc_TypeError, "parameter must be a string");
        return NULL;
    }

	vid = volume_id_open_node(filename);
    if (!vid)
    {
        PyErr_SetString(PyExc_OSError, strerror(errno));
        return NULL;
    }

	set_str(label_safe, vid->label, sizeof(vid->label));
	replace_untrusted_chars(label_safe);

    return Py_BuildValue("(ssssss)", vid->usage, vid->type, vid->type_version,
                         vid->uuid, label_safe);
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
