#include "Semaphore.hpp"


namespace cairn
{
namespace base
{


  Semaphore::Semaphore() :
    myValue(0),
    mySemaphore()
  {
    mySemaphore=CreateSemaphore(0, 0, 100, 0);
  }

  Semaphore::~Semaphore()
  {
    CloseHandle(mySemaphore);
  }

  void Semaphore::wait()
  {
    WaitForSingleObject(mySemaphore, INFINITE);
    --myValue;
  }

  bool Semaphore::tryWait()
  {
    if (WaitForSingleObject(mySemaphore, 1) == WAIT_OBJECT_0)
    {
      --myValue;
      return false;
    }
    else
    {
      --myValue;
      return true;
    }
  }

  void Semaphore::post()
  {
    ReleaseSemaphore(mySemaphore, 1, &myValue);
    ++myValue;
  }

  int Semaphore::getValue()
  {
    return myValue;
  }


} // namespace base
} // namespace cairn
