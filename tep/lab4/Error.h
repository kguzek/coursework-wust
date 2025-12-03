#ifndef COURSEWORK_WUST_ERROR_H
#define COURSEWORK_WUST_ERROR_H
#include <string>


class Error
{
public:
    Error();
    explicit Error(const std::string& message);
    std::string get_message();

private:
    std::string _message;
};


#endif //COURSEWORK_WUST_ERROR_H
