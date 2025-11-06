#include <iostream>
#include "Number.h"

int main()
{
    // zastąp XYZ nazwą klasy `Number`
    typedef Number NumberClass;
    // zastąp xyzToString nazwą metody `toString`
    std::string (NumberClass::*toStringPtr)() const = &NumberClass::to_string;

    int passed = 0;
    const int TEST_COUNT = 8;
    NumberClass a, b, c, d, e;
    a = 9979;
    b = 8457;
    c = 4646;
    d = 9700;

    e = 1586;
    NumberClass result;
    std::string resultStr;

    // Test 1: a + b
    result = a + b;
    resultStr = (result.*toStringPtr)();
    if (resultStr == "18436")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 1 failed: a + b = " << resultStr << ", expected 18436\n";
    }

    // Test 2: a - b
    result = a - b;
    resultStr = (result.*toStringPtr)();
    if (resultStr == "1522")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 2 failed: a - b = " << resultStr << ", expected 1522\n";
    }

    // Test 3: c * d
    result = c * d;
    resultStr = (result.*toStringPtr)();
    if (resultStr == "45066200")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 3 failed: c * d = " << resultStr
            << ", expected 45066200\n";
    }

    // Test 4: d / e
    result = d / e;
    resultStr = (result.*toStringPtr)();
    if (resultStr == "6")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 4 failed: d / e = " << resultStr << ", expected 6\n";
    }

    // Test 5: (a * b * c * d * e + b) / c
    result = (a * b * c * d * e + b) / c;
    resultStr = (result.*toStringPtr)();
    if (resultStr == "1298309606232601")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 5 failed: (a * b * c * d * e + b) / c = " << resultStr
            << ", expected 1298309606232601\n";
    }

    // Test 6: c - e * b
    result = c - e * b;
    resultStr = (result.*toStringPtr)();
    if (resultStr == "-13408156")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 6 failed: c - e * b = " << resultStr
            << ", expected -13408156\n";
    }

    // Test 7: (a + d) * (b - e)
    result = (a + d) * (b - e);
    resultStr = (result.*toStringPtr)();
    if (resultStr == "135214409")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 7 failed: (a + d) * (b - e) = " << resultStr
            << ", expected 135214409\n";
    }

    // Test 8: (a - b - c) / e
    Number a_minus_b = a - b;
    result = (a_minus_b - c) / e;
    resultStr = (result.*toStringPtr)();
    if (resultStr == "-1")
    {
        ++passed;
    }
    else
    {
        std::cout << "Test 8 failed: (a - b - c) / e = " << resultStr
            << ", expected -1\n";
    }
    std::cout << "Passed " << passed << " out of " << TEST_COUNT << " tests."
        << std::endl;
}
