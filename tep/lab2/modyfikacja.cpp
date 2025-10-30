#include <iostream>
#include "Base256Number.h"


void test_operations(const int first, const int second)
{
    Base256Number first_number;
    Base256Number second_number;
    first_number = first;
    second_number = second;

    // test operator=
    std::cout << first << " = " << first_number << std::endl;
    std::cout << second << " = " << second_number << std::endl;

    // test operator+
    std::cout << first << " + " << second << " = " << first_number + second_number << std::endl;
    std::cout << second << " + " << first << " = " << second_number + first_number << std::endl;

    // test operator-
    std::cout << first << " - " << second << " = " << first_number - second_number << std::endl;
    std::cout << second << " - " << first << " = " << second_number - first_number << std::endl;

    // test operator*
    std::cout << first << " * " << second << " = " << first_number * second_number << std::endl;
    std::cout << second << " * " << first << " = " << second_number * first_number << std::endl;

    // test operator/
    std::cout << first << " / " << second << " = " << first_number / second_number << std::endl;
    std::cout << second << " / " << first << " = " << second_number / first_number << std::endl;

    // test operator%
    std::cout << first << " % " << second << " = " << first_number % second_number << std::endl;
    std::cout << second << " % " << first << " = " << second_number % first_number << std::endl;
}

int main()
{
    // test_operations(1, 256);
    // test_operations(12345678, 9876);
    test_operations(1253, 259);
    test_operations(131, 731);
    test_operations(256, 5478);
    return 0;
}
