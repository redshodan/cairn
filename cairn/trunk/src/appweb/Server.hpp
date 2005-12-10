#ifndef _SERVER_HPP
#define _SERVER_HPP


#include "appWeb.h"
#include "base/Mutex.hpp"


namespace cairn
{
namespace appweb
{


  class Server
  {
  public:

    static Server* get();


    Server();
    virtual ~Server();

    virtual void run();
    virtual void stop();


  protected:

    static Server* ourServer;

    virtual void lock();
    virtual void unlock();

    MaHttp* myHTTP;
    cairn::base::Mutex myMutex;
  };


} // namespace appweb
} // namespace cairn


#endif // _SERVER_HPP
