#include <iostream>
#include <ostream>

#include "Error.h"
#include "Result.h"

Result<double, Error> divide(double dividend, double divisor)
{
    if (divisor == 0)
    {
        return Result<double, Error>::fail(new Error("cannot divide by zero"));
    }
    return Result<double, Error>::ok(dividend / divisor);
}

void test_divide(const double dividend, const double divisor)
{
    Result<double, Error> result = divide(dividend, divisor);
    if (result.is_success())
    {
        std::cout << dividend << " / " << divisor << " = " << result.get_value() << std::endl;
    }
    else
    {
        const std::vector<Error*>& errors = result.get_errors();
        std::cout << dividend << " / " << divisor << " = " << errors.front()->get_message() << std::endl;
    }
}

int main()
{
    test_divide(0, 1);
    test_divide(0, 0);
    test_divide(5, 0);
    test_divide(10, -2);
}
