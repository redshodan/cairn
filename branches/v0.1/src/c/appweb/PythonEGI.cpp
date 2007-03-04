#include <Python.h>
#include "PythonEGI.hpp"


namespace cairn
{
namespace appweb
{


  PythonEGI::PythonEGI(char *name) : MaEgiForm(name)
  {
  }

  PythonEGI::~PythonEGI()
  {
  }
/*
  void PythonEGI::run(MaRequest *req, char *script, char *path, char *query, 
		      char *postData, int postLen)
  {
    mprPrintf("In MyEgi::run, thread %s\n", mprGetCurrentThreadName());
    mprPrintf("script=%s path=%s query=%s postData=%s postLen=%d\n",
	      script, path, query, postData, postLen);

    PyRun_SimpleString("from time import time,ctime\n"
		       "print 'Today is',ctime(time())\n");

    req->write("<HTML><TITLE>simpleEgi</TITLE><BODY>\r\n");
    req->writeFmt("<p>Name: %s</p>\n", 
		 req->getVar(MA_FORM_OBJ, "name", "-")); 
    req->writeFmt("<p>Address: %s</p>\n", 
		 req->getVar(MA_FORM_OBJ, "address", "-")); 
    req->write("</BODY></HTML>\r\n");

    mprPrintf("Exiting thread %s\n", mprGetCurrentThreadName());
  }
*/


  void PythonEGI::run(MaRequest *req, char *script, char *path, char *query, 
		      char *postData, int postLen)
  {
    PyObject *pModule, *pDict, *pFunc;
    PyObject *pArgs, *pValue;
    int i;

    mprPrintf("In MyEgi::run, thread %s\n", mprGetCurrentThreadName());
    mprPrintf("script=%s path=%s query=%s postData=%s postLen=%d\n",
	      script, path, query, postData, postLen);

    pModule = PyImport_ImportModule("foo");

    if (pModule != NULL) {
        pDict = PyModule_GetDict(pModule);
        /* pDict is a borrowed reference */

        pFunc = PyDict_GetItemString(pDict, "handle");
        /* pFun: Borrowed reference */

        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(5);
	    char* cargs[]={script, path, query, postData};
            for (i = 0; i < 4; ++i) {
                pValue = PyString_FromString(cargs[i]);
                /* pValue reference stolen here: */
                PyTuple_SetItem(pArgs, i, pValue);
            }
	    PyTuple_SetItem(pArgs, i, PyInt_FromLong(postLen));
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) {
                printf("Result of call: %s\n", PyString_AsString(pValue));
                req->write(PyString_AsString(pValue));
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
            }
            /* pDict and pFunc are borrowed and must not be Py_DECREF-ed */
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function\n");
        }
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load module\n");
    }

    mprPrintf("Exiting thread %s\n", mprGetCurrentThreadName());
  }


} // namespace appweb
} // namespace cairn
