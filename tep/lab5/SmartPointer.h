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
    SmartPointer& operator=(const SmartPointer& other);

private:
    RefCounter* _counter;
    T* _pointer;
    void _copy(const SmartPointer& other);
    void _deallocate() const;
};

template <typename T>
SmartPointer<T>::SmartPointer(T* pointer) :
    _counter(new RefCounter()),
    _pointer(pointer)
{
    _counter->increment();
}

template <typename T>
SmartPointer<T>::SmartPointer(const SmartPointer& other)
{
    _copy(other);
}

template <typename T>
SmartPointer<T>::~SmartPointer()
{
    _deallocate();
}

template <typename T>
SmartPointer<T>& SmartPointer<T>::operator=(const SmartPointer& other)
{
    if (this == &other)
    {
        return *this;
    }
    _deallocate();
    _copy(other);
    return *this;
}

template <typename T>
void SmartPointer<T>::_copy(const SmartPointer& other)
{
    _counter = other._counter;
    _pointer = other._pointer;
    _counter->increment();
}

template <typename T>
void SmartPointer<T>::_deallocate() const
{
    if (_counter->decrement() == 0)
    {
        delete _pointer;
        delete _counter;
    }
}

#endif //COURSEWORK_WUST_SMART_POINTER_H
