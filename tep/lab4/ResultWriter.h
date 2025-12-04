#ifndef COURSEWORK_WUST_RESULT_WRITER_H
#define COURSEWORK_WUST_RESULT_WRITER_H
#include <fstream>
#include <string>

#include "ExpressionTree.h"
#include "Result.h"

template <typename T, typename E>
class ResultWriter
{
public:
    static bool write(const std::string& filename, Result<T, E>& result);
};

template <typename T, typename E>
bool ResultWriter<T, E>::write(const std::string& filename, Result<T, E>& result)
{
    std::ofstream file(filename.c_str());

    if (!file.is_open())
    {
        return false;
    }

    if (!result.is_success())
    {
        const std::vector<E*>& errors = result.get_errors();
        for (typename std::vector<E*>::const_iterator it = errors.begin(); it != errors.end(); ++it)
        {
            file << it->get_message() << std::endl;
        }
    }

    file.close();
    return true;
}

template <typename E>
class ResultWriter<ExpressionTree*, E>
{
public:
    static bool write(const std::string& filename, Result<ExpressionTree*, E>& result);
};

template <typename E>
bool ResultWriter<ExpressionTree*, E>::write(const std::string& filename, Result<ExpressionTree*, E>& result)
{
    std::ofstream file(filename.c_str());

    if (!file.is_open())
    {
        return false;
    }

    if (result.is_success())
    {
        file << result.get_value() << std::endl;
    }
    else
    {
        const std::vector<E*>& errors = result.get_errors();
        for (typename std::vector<E*>::const_iterator it = errors.begin(); it != errors.end(); ++it)
        {
            file << it->get_message() << std::endl;
        }
    }

    file.close();
    return true;
}

#endif //COURSEWORK_WUST_RESULT_WRITER_H
