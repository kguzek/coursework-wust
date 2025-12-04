#ifndef COURSEWORK_WUST_RESULT_H
#define COURSEWORK_WUST_RESULT_H
#include <cstddef>
#include <vector>

#define DEFAULT_FAIL_VALUE NULL


template <typename T, typename E>
class Result
{
public:
    Result(const T& value);
    Result(E* error);
    Result(std::vector<E*>& errors);
    Result(const Result<T, E>& other);
    ~Result();
    static Result<T, E> ok(const T& value);
    static Result<T, E> fail(E* error);
    static Result<T, E> fail(std::vector<E*>& errors);
    Result<T, E>& operator=(const Result<T, E>& other);
    bool is_success() const;
    T get_value() const;
    std::vector<E*>& get_errors();

private:
    T* _value;
    std::vector<E*> _errors;
    void _copy_from(const Result& other);
    void _delete_errors();
};

template <typename T, typename E>
Result<T, E>::Result(const T& value) : _value(new T(value)), _errors()
{
}

template <typename T, typename E>
Result<T, E>::Result(E* error) : _value(DEFAULT_FAIL_VALUE), _errors()
{
    _errors.push_back(error);
}

template <typename T, typename E>
Result<T, E>::Result(std::vector<E*>& errors) : _value(DEFAULT_FAIL_VALUE), _errors(errors)
{
}

template <typename T, typename E>
Result<T, E>::Result(const Result<T, E>& other)
{
    _copy_from(other);
}

template <typename T, typename E>
Result<T, E>::~Result()
{
    delete _value;
    _delete_errors();
}

template <typename T, typename E>
Result<T, E> Result<T, E>::ok(const T& value)
{
    return Result(value);
}

template <typename T, typename E>
Result<T, E> Result<T, E>::fail(E* error)
{
    return Result(error);
}

template <typename T, typename E>
Result<T, E> Result<T, E>::fail(std::vector<E*>& errors)
{
    E error = *errors.back();
    return Result(&error);
}

template <typename T, typename E>
Result<T, E>& Result<T, E>::operator=(const Result<T, E>& other)
{
    if (&other != this)
    {
        delete _value;
        _delete_errors();
        _copy_from(other);
    }
    return *this;
}

template <typename T, typename E>
bool Result<T, E>::is_success() const
{
    return _errors.empty() && _value != DEFAULT_FAIL_VALUE;
}

template <typename T, typename E>
T Result<T, E>::get_value() const
{
    return *_value;
}

template <typename T, typename E>
std::vector<E*>& Result<T, E>::get_errors()
{
    return _errors;
}

template <typename T, typename E>
void Result<T, E>::_copy_from(const Result& other)
{
    _value = other.is_success() ? new T(*other._value) : DEFAULT_FAIL_VALUE;
    for (typename std::vector<E*>::const_iterator it = other._errors.begin();
         it != other._errors.end(); ++it)
    {
        _errors.push_back(new E(**it));
    }
}

template <typename T, typename E>
void Result<T, E>::_delete_errors()
{
    for (typename std::vector<E*>::iterator it = _errors.begin(); it != _errors.end(); ++it)
    {
        delete *it;
    }
    _errors.clear();
}

template <typename E>
class Result<void, E>
{
public:
    Result();
    explicit Result(E* error);
    explicit Result(std::vector<E*>& errors);
    Result(const Result<void, E>& other);
    ~Result();
    static Result<void, E> ok();
    static Result<void, E> fail(E* error);
    static Result<void, E> fail(std::vector<E*>& errors);
    Result<void, E>& operator=(const Result<void, E>& other);
    bool is_success() const;
    std::vector<E*>& get_errors();

private:
    std::vector<E*> _errors;
    void _delete_errors();
};

template <typename E>
Result<void, E>::Result() : _errors()
{
}

template <typename E>
Result<void, E>::Result(E* error) : _errors()
{
    _errors.push_back(error);
}

template <typename E>
Result<void, E>::Result(std::vector<E*>& errors) : _errors(errors)
{
}

template <typename E>
Result<void, E>::Result(const Result<void, E>& other) : _errors(other._errors)
{
}

template <typename E>
Result<void, E>::~Result()
{
    _delete_errors();
}

template <typename E>
Result<void, E> Result<void, E>::ok()
{
    return Result();
}

template <typename E>
Result<void, E> Result<void, E>::fail(E* error)
{
    return Result(error);
}

template <typename E>
Result<void, E> Result<void, E>::fail(std::vector<E*>& errors)
{
    return Result(errors.front());
}

template <typename E>
Result<void, E>& Result<void, E>::operator=(const Result<void, E>& other)
{
    _errors = other._errors;
    return *this;
}

template <typename E>
bool Result<void, E>::is_success() const
{
    return _errors.empty();
}

template <typename E>
std::vector<E*>& Result<void, E>::get_errors()
{
    return _errors;
}

template <typename E>
void Result<void, E>::_delete_errors()
{
    for (typename std::vector<E*>::iterator it = _errors.begin(); it != _errors.end(); ++it)
    {
        delete *it;
    }
}
#endif //COURSEWORK_WUST_RESULT_H
