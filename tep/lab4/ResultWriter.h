#ifndef COURSEWORK_WUST_RESULT_WRITER_H
#define COURSEWORK_WUST_RESULT_WRITER_H
#include <fstream>
#include <string>

#include "ExpressionTree.h"
#include "Result.h"

template <typename T>
class ResultWriter
{
public:
    static bool write(const std::string& filename, Result<T, Error*>& result);
};

template <typename T>
bool ResultWriter<T>::write(const std::string& filename, Result<T, Error*>& result)
{
    std::ofstream file(filename.c_str());

    if (!file.is_open())
    {
        return false;
    }

    if (!result.is_success())
    {
        const std::vector<Error*>& errors = result.get_errors();
        for (std::vector<Error*>::const_iterator it = errors.begin(); it != errors.end(); ++it)
        {
            file << (*it)->get_message() << std::endl;
        }
    }

    file.close();
    return true;
}

template <>
class ResultWriter<ExpressionTree*>
{
public:
    static bool write(const std::string& filename, Result<ExpressionTree*, Error> result)
    {
        std::ofstream file(filename.c_str());

        if (!file.is_open())
        {
            return false;
        }

        if (result.is_success())
        {
            file << *result.get_value() << std::endl;
        }
        else
        {
            const std::vector<Error*>& errors = result.get_errors();
            for (std::vector<Error*>::const_iterator it = errors.begin(); it != errors.end(); ++it)
            {
                file << (*it)->get_message() << std::endl;
            }
        }

        file.close();
        return true;
    }
};


#endif //COURSEWORK_WUST_RESULT_WRITER_H
