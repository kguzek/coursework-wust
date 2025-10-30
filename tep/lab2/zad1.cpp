#include <iostream>

#include "Number.h"


void test_operations(int first, int second)
{
    Number first_number;
    Number second_number;
    first_number = first;
    second_number = second;

    // test operator=
    // std::cout << "number = " << first << ": " << first_number << std::endl;
    // std::cout << "number = " << second << ": " << second_number << std::endl;

    // test operator+
    // std::cout << first << " + " << second << " = " << first_number + second_number << std::endl;
    // std::cout << second << " + " << first << " = " << second_number + first_number << std::endl;

    // test operator-
    // std::cout << first << " - " << second << " = " << first_number - second_number << std::endl;
    // std::cout << second << " - " << first << " = " << second_number - first_number << std::endl;

    // test operator*
    std::cout << first << " * " << second << " = " << first_number * second_number << std::endl;
    std::cout << second << " * " << first << " = " << second_number * first_number << std::endl;
}

int main()
{
    test_operations(1, 3);
    test_operations(10, 3);
    test_operations(5, 7);
    test_operations(23, 67);
    test_operations(0, 7);
}
