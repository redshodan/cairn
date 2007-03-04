#include "Server.hpp"
#include "PythonEGI.hpp"


namespace cairn
{
namespace appweb
{


  Server* Server::ourServer = NULL;


  Server* Server::get()
  {
    if (!ourServer)
      ourServer = new Server();
    return ourServer;
  }


  Server::Server() :
    myMutex()
  {
  }

  Server::~Server()
  {
  }

  void Server::run()
  {
    MaServer *server;
    Mpr mpr("CAIRN Utility");

    mpr.addListener(new MprLogToFile());
    mpr.setLogSpec("stdout:4");

    mpr.start(0);
    myHTTP = new MaHttp();
    server = new MaServer(myHTTP, "default", ".");

    new MaCopyModule(0);
    new MaEgiModule(0);

    if (server->configure("cairn.conf") < 0)
    {
      mprFprintf(MPR_STDERR, 
		 "Can't configure the AppWeb server. Error on line %d\n", 
		 server->getLine());
      exit(1);
    }

    new PythonEGI("/python.egi");

    if (myHTTP->start() < 0)
    {
      mprFprintf(MPR_STDERR, "Can't start the AppWeb server\n");
      exit(1);
    }

    // Tell the MPR to loop servicing incoming requests.
    mpr.serviceEvents(0, -1);

    myHTTP->stop();
    delete server;
    delete myHTTP;
    myHTTP=NULL;
  }

  void Server::stop()
  {
    lock();
    if (myHTTP)
      myHTTP->stop();
    unlock();
  }

  void Server::lock()
  {
//    myMutex.lock();
  }

  void Server::unlock()
  {
//    myMutex.unlock();
  }


} // namespace appweb
} // namespace cairn
