#include "Mutex.hpp"


namespace cairn
{
namespace base
{


  Mutex::Mutex() :
    myMutex()
  {
    pthread_mutex_init(&myMutex, 0);
    //unlock();
  }

  Mutex::~Mutex()
  {
    pthread_mutex_destroy(&myMutex);
  }
/*
  void Mutex::lock()
  {
    pthread_mutex_lock(&myMutex);
  }

  bool Mutex::tryLock()
  {
    if (pthread_mutex_trylock(&myMutex) == 0)
      return true;
    else
      return false;
  }

  void Mutex::unlock()
  {
    pthread_mutex_unlock(&myMutex);
  }

  Mutex::MUTEX_T* Mutex::getMutex()
  {
    return &myMutex;
  }
*/

} // namespace base
} // namespace cairn
