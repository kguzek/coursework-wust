#include "Error.h"

Error::Error()
{
    _message = "<brak opisu>";
}

Error::Error(const std::string& message)
{
    _message = message;
}

std::string Error::get_message()
{
    return _message;
}
