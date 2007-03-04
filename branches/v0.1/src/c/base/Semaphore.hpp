#ifndef _SEMAPHORE_HPP
#define _SEMAPHORE_HPP


#ifdef WIN32
#include "winbase.h"
#else
#include <semaphore.h>
#endif


namespace cairn
{
namespace base
{


  class Semaphore
  {
  public:

    #ifdef WIN32
    typedef HANDLE SEMAPHORE_T;
    #else
    typedef sem_t SEMAPHORE_T;
    #endif

    Semaphore();
    virtual ~Semaphore();

    virtual void wait();
    virtual bool tryWait();
    virtual void post();
    virtual int getValue();


  protected:

    #ifdef WIN32
    int myValue;
    #endif
    SEMAPHORE_T mySemaphore;
  };


} // namespace base
} // namespace cairn


#endif // _SEMAPHORE_HPP
