#include "Mutex.hpp"


namespace cairn
{
namespace base
{


  Mutex::Mutex() :
    myMutex()
  {
    myMutex = CreateMutex(0, true, 0);
    unlock();
  }

  Mutex::~Mutex()
  {
    CloseHandle(myMutex);
  }

  void Mutex::lock()
  {
    WaitForSingleObject(myMutex, INFINITE);
  }

  bool Mutex::tryLock()
  {
    if (WaitForSingleObject(myMutex, 1) != WAIT_OBJECT_0)
      return false;
    else
      return true;
  }

  void Mutex::unlock()
  {
    ReleaseMutex(myMutex);
  }

  MUTEX_T* Mutex::getMutex()
  {
    return &myMutex;
  }


} // namespace base
} // namespace cairn
