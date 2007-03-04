#include "Semaphore.hpp"


namespace cairn
{
namespace base
{


  Semaphore::Semaphore() :
    mySemaphore()
  {
    sem_init(&mySemaphore, 0, 0);
  }

  Semaphore::~Semaphore()
  {
    sem_destroy(&mySemaphore);
  }

  void Semaphore::wait()
  {
    sem_wait(&mySemaphore);
  }

  bool Semaphore::tryWait()
  {
    if (sem_trywait(&mySemaphore) < 0)
      return false;
    else
      return true;
  }

  void Semaphore::post()
  {
    sem_post(&mySemaphore);
  }

  int Semaphore::getValue()
  {
    int value=0;

    sem_getvalue(&mySemaphore, &value);

    return value;
  }


} // namespace base
} // namespace cairn
