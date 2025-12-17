#ifndef COURSEWORK_WUST_SMART_POINTER_H
#define COURSEWORK_WUST_SMART_POINTER_H
#include "RefCounter.h"


template <typename T>
class SmartPointer
{
public:
    explicit SmartPointer(T* pointer);
    SmartPointer(const SmartPointer& other);
    ~SmartPointer();
    T& operator*() { return *_pointer; }
    T* operator->() { return _pointer; }

private:
    RefCounter* _counter;
    T* _pointer;
};

template <typename T>
SmartPointer<T>::SmartPointer(T* pointer)
{
    _pointer = pointer;
    _counter = new RefCounter();
    _counter->increment();
}

template <typename T>
SmartPointer<T>::SmartPointer(const SmartPointer& other)
    : _counter(other._counter), _pointer(other._pointer)
{
    _counter->increment();
}

template <typename T>
SmartPointer<T>::~SmartPointer()
{
    if (_counter->decrement() <= 0)
    {
        delete _pointer;
        delete _counter;
    }
}


#endif //COURSEWORK_WUST_SMART_POINTER_H
