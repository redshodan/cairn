//#include <stdlib.h>
//#include <stdio.h>
#include <Python.h>
#include "appweb/Server.hpp"

using namespace cairn;
using namespace cairn::appweb;


int main(int argc, char* argv[])
{
  Py_SetPythonHome("/home/baron/cairn/cairn/tmp");
  Py_Initialize();
  PySys_SetPath("/home/baron/cairn/cairn/tmp/lib/python2.4/:.");

  Server* server=Server::get();

  server->run();

  Py_Finalize();

  return 0;
}
