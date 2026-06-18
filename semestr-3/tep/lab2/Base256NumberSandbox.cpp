#include <iostream>
#include "Base256Number.h"


void flush()
{
    std::cout << "---------------" << std::endl;
}

std::string number_to_string(const Base256Number& number)
{
    return number.to_array_string();
}

void test_operations(const int first, const int second)
{
    Base256Number first_number;
    Base256Number second_number;
    first_number = first;
    second_number = second;

    // // test operator=
    // std::cout << first << " = " << first_number << std::endl;
    // std::cout << second << " = " << second_number << std::endl;
    //
    // // test operator+
    // std::cout << first << " + " << second << " = " << first_number + second_number << std::endl;
    // std::cout << second << " + " << first << " = " << second_number + first_number << std::endl;
    //
    // // test operator-
    // std::cout << first << " - " << second << " = " << first_number - second_number << std::endl;
    // std::cout << second << " - " << first << " = " << second_number - first_number << std::endl;
    //
    // // test operator*
    // std::cout << first << " * " << second << " = " << first_number * second_number << std::endl;
    // std::cout << second << " * " << first << " = " << second_number * first_number << std::endl;
    //
    // // test operator/
    // std::cout << first << " / " << second << " = " << first_number / second_number << std::endl;
    // std::cout << second << " / " << first << " = " << second_number / first_number << std::endl;
    //
    // // test operator%
    // std::cout << first << " % " << second << " = " << first_number % second_number << std::endl;
    // std::cout << second << " % " << first << " = " << second_number % first_number << std::endl;

    // test to_hex_string()
    // std::cout << first << " = " << first_number.to_hex_string() << std::endl;
    // std::cout << second << " = " << second_number.to_hex_string() << std::endl;

    // test to_decimal_string()
    // std::cout << first << " = " << first_number.to_decimal_string() << std::endl;
    // std::cout << second << " = " << second_number.to_decimal_string() << std::endl;

    // test to_binary_string()
    std::cout << first << " = " << first_number.to_binary_string() << std::endl;
    std::cout << second << " = " << second_number.to_binary_string() << std::endl;
    flush();

    // test operator&
    std::cout << "  " << number_to_string(first_number) << std::endl << "& " << number_to_string(second_number) <<
        std::endl << "= " << number_to_string(first_number & second_number) << std::endl;
    flush();

    // test operator|
    std::cout << "  " << number_to_string(first_number) << std::endl << "| " << number_to_string(second_number) <<
        std::endl << "= " << number_to_string(first_number | second_number) << std::endl;
    flush();

    // test operator^
    std::cout << "  " << number_to_string(first_number) << std::endl << "^ " << number_to_string(second_number) <<
        std::endl << "= " << number_to_string(first_number ^ second_number) << std::endl;
    flush();
    // test operator~
    std::cout << "~ " << number_to_string(first_number) << " = " << number_to_string(~first_number) << std::endl;
    std::cout << "~ " << number_to_string(second_number) << " = " << number_to_string(~second_number) << std::endl;

    // test operator<<
    std::cout << number_to_string(first_number) << " << " << second << " = " << number_to_string(first_number << second)
        << std::endl;
    flush();

    // test operator>>
    std::cout << number_to_string(first_number) << " >> " << second << " = " << number_to_string(first_number >> second)
        << std::endl;
    flush();
}

int main()
{
    // test_operations(1, 256);
    // test_operations(12345678, 9876);
    // test_operations(1253, 259);
    // test_operations(131, 731);
    // test_operations(256, 5478);
    // test_operations(1023, 0);
    // test_operations(5264, 0);
    // test_operations(123, 60);
    test_operations(60, 1);
    test_operations(123, 3);
    return 0;
}
