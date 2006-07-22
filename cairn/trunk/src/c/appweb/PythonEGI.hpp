#ifndef _PYTHONEGI_HPP
#define _PYTHONEGI_HPP


#include "appWeb.h"


namespace cairn
{
namespace appweb
{


  class PythonEGI : public MaEgiForm
  {
  public:

    PythonEGI(char *egiName);
    virtual ~PythonEGI();

    virtual void run(MaRequest *req, char *script, char *path, char *query, 
		     char *postData, int postLen);
  };


} // namespace appweb
} // namespace cairn


#endif // _PYTHONEGI_HPP
