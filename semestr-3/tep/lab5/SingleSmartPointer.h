#ifndef COURSEWORK_WUST_SINGLE_SMART_POINTER_H
#define COURSEWORK_WUST_SINGLE_SMART_POINTER_H
#include <set>
#include <stdexcept>

template <typename T>
class SingleSmartPointer
{
public:
    SingleSmartPointer();
    SingleSmartPointer(SingleSmartPointer& other) = delete;
    explicit SingleSmartPointer(T* pointer);
    ~SingleSmartPointer();
    SingleSmartPointer(SingleSmartPointer&& other) noexcept;
    T& operator*() { return *_pointer; }
    T* operator->() { return _pointer; }
    SingleSmartPointer& operator=(const SingleSmartPointer& other) = delete;
    SingleSmartPointer& operator=(SingleSmartPointer&& other) noexcept;

    bool is_empty() const;
    static bool is_invalid(T* pointer);

private:
    T* _pointer;
    static std::set<T*> _used_pointers;
};

template <typename T>
std::set<T*> SingleSmartPointer<T>::_used_pointers{};

template <typename T>
SingleSmartPointer<T>::SingleSmartPointer() : _pointer(nullptr)
{
}

template <typename T>
SingleSmartPointer<T>::SingleSmartPointer(T* pointer)
{
    if (is_invalid(pointer))
    {
        throw std::invalid_argument("duplikacja wskaźników");
    }
    _pointer = pointer;
    _used_pointers.insert(pointer);
}

template <typename T>
SingleSmartPointer<T>::SingleSmartPointer(SingleSmartPointer&& other) noexcept
{
    _pointer = other._pointer;
    other._pointer = nullptr;
}

template <typename T>
SingleSmartPointer<T>& SingleSmartPointer<T>::operator=(SingleSmartPointer&& other) noexcept
{
    if (this == &other)
    {
        return *this;
    }
    if (!is_empty())
    {
        _used_pointers.erase(_pointer);
        delete _pointer;
    }
    _pointer = other._pointer;
    other._pointer = nullptr;
    return *this;
}

template <typename T>
bool SingleSmartPointer<T>::is_empty() const
{
    return _pointer == nullptr;
}

template <typename T>
bool SingleSmartPointer<T>::is_invalid(T* pointer)
{
    return _used_pointers.contains(pointer);
}

template <typename T>
SingleSmartPointer<T>::~SingleSmartPointer()
{
    if (!is_empty())
    {
        _used_pointers.erase(_pointer);
        delete _pointer;
    }
}

#endif //COURSEWORK_WUST_SINGLE_SMART_POINTER_H
