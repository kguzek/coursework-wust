#include "Error.h"

Error::Error()
{
    _message = "<brak opisu>";
}

Error::Error(const std::string& message)
{
    _message = message;
}

Error::Error(const Error& other)
{
    _message = other._message;
}

std::string Error::get_message() const
{
    return _message;
}
