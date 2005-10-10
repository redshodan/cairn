#ifndef _MUTEX_H
#define _MUTEX_H


#ifdef linux
#include <pthread.h>
#endif


namespace cairn
{
namespace base
{


  class Mutex
  {
  public:

    #ifdef WIN32
    typedef HANDLE MUTEX_T;
    #else
    typedef pthread_mutex_t MUTEX_T;
    #endif

    Mutex();
    virtual ~Mutex();
/*
    virtual void lock();
    virtual bool tryLock();
    virtual void unlock();
    virtual MUTEX_T* getMutex();
*/

  protected:

    MUTEX_T myMutex;
  };


} // namespace base
} // namespace cairn


#endif // _MUTEX_H
