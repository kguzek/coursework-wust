#include <iostream>
#include "Base256Number.h"

int main()
{
    // zastąp XYZ nazwą klasy `Base256Number`
    typedef Base256Number Base256NumberClass;
    // zastąp xyzToHexString nazwą metody `toHexString`
    std::string (Base256Number::*toHexStringPtr)() const = &Base256NumberClass::to_hex_string;

    int passed = 0;
    const int TEST_COUNT = 27;
    Base256NumberClass a, b, c, d, e;
    a = 9760;
    b = 4641;
    c = 5205;
    d = 5714;
    e = 8590;
    Base256NumberClass result;
    std::string resultStr;

    // Test 1: a & b
    result = a & b;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x220" || resultStr == "0x0220")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 1 failed: 544 != " << resultStr << std::endl;
    }

    // Test 2: a & c
    result = a & c;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x400" || resultStr == "0x0400")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 2 failed: 1024 != " << resultStr << std::endl;
    }

    // Test 3: c & e
    result = c & e;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x4" || resultStr == "0x04")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 3 failed: 4 != " << resultStr << std::endl;
    }

    // Test 4: d & b
    result = d & b;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x1200" || resultStr == "0x01200")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 4 failed: 4608 != " << resultStr << std::endl;
    }

    // Test 5: a | b
    result = a | b;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x3621" || resultStr == "0x03621")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 5 failed: 13857 != " << resultStr << std::endl;
    }

    // Test 6: a | e
    result = a | e;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x27ae" || resultStr == "0x027ae" ||
        resultStr == "0x27AE" || resultStr == "0x027AE")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 6 failed: 10158 != " << resultStr << std::endl;
    }

    // Test 7: c | d
    result = c | d;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x1657" || resultStr == "0x01657")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 7 failed: 5719 != " << resultStr << std::endl;
    }

    // Test 8: e | b
    result = e | b;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x33af" || resultStr == "0x033af" ||
        resultStr == "0x33AF" || resultStr == "0x033AF")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 8 failed: 13231 != " << resultStr << std::endl;
    }

    // Test 9: a ^ b
    result = a ^ b;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x3401" || resultStr == "0x03401")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 9 failed: 13313 != " << resultStr << std::endl;
    }

    // Test 10: b ^ c
    result = b ^ c;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x674" || resultStr == "0x0674")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 10 failed: 1652 != " << resultStr << std::endl;
    }

    // Test 11: d ^ e
    result = d ^ e;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x37dc" || resultStr == "0x037dc" ||
        resultStr == "0x37DC" || resultStr == "0x037DC")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 11 failed: 14300 != " << resultStr << std::endl;
    }

    // Test 12: c ^ a
    result = c ^ a;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x3275" || resultStr == "0x03275")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 12 failed: 12917 != " << resultStr << std::endl;
    }

    // Test 13: ~a
    result = ~a;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x19df" || resultStr == "0x019df" ||
        resultStr == "0x19DF" || resultStr == "0x019DF")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 13 failed: 6623 != " << resultStr << std::endl;
    }

    // Test 14: ~b
    result = ~b;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0xdde" || resultStr == "0x0dde" || resultStr == "0xDDE" ||
        resultStr == "0x0DDE")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 14 failed: 3550 != " << resultStr << std::endl;
    }

    // Test 15: ~c
    result = ~c;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0xbaa" || resultStr == "0x0baa" || resultStr == "0xBAA" ||
        resultStr == "0x0BAA")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 15 failed: 2986 != " << resultStr << std::endl;
    }

    // Test 16: ~d
    result = ~d;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x9ad" || resultStr == "0x09ad" || resultStr == "0x9AD" ||
        resultStr == "0x09AD")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 16 failed: 2477 != " << resultStr << std::endl;
    }

    // Test 17: ~e
    result = ~e;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x1e71" || resultStr == "0x01e71" ||
        resultStr == "0x1E71" || resultStr == "0x01E71")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 17 failed: 7793 != " << resultStr << std::endl;
    }

    // Test 18: a << 2
    result = a << 2;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x9880" || resultStr == "0x09880")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 18 failed: 39040 != " << resultStr << std::endl;
    }

    // Test 19: b << 3
    result = b << 3;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x9108" || resultStr == "0x09108")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 19 failed: 37128 != " << resultStr << std::endl;
    }

    // Test 20: c << 1
    result = c << 1;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x28aa" || resultStr == "0x028aa" ||
        resultStr == "0x28AA" || resultStr == "0x028AA")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 20 failed: 10410 != " << resultStr << std::endl;
    }

    // Test 21: d << 4
    result = d << 4;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x16520" || resultStr == "0x016520")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 21 failed: 91424 != " << resultStr << std::endl;
    }

    // Test 22: e << 2
    result = e << 2;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x8638" || resultStr == "0x08638")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 22 failed: 34360 != " << resultStr << std::endl;
    }

    // Test 23: a >> 6
    result = a >> 6;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x98" || resultStr == "0x098")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 23 failed: 152 != " << resultStr << std::endl;
    }

    // Test 24: b >> 5
    result = b >> 5;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x91" || resultStr == "0x091")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 24 failed: 145 != " << resultStr << std::endl;
    }

    // Test 25: c >> 1
    result = c >> 1;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0xa2a" || resultStr == "0x0a2a" || resultStr == "0xA2A" ||
        resultStr == "0x0A2A")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 25 failed: 2602 != " << resultStr << std::endl;
    }

    // Test 26: d >> 4
    result = d >> 4;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x165" || resultStr == "0x0165")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 26 failed: 357 != " << resultStr << std::endl;
    }

    // Test 27: e >> 2
    result = e >> 2;
    resultStr = (result.*toHexStringPtr)();
    if (resultStr == "0x863" || resultStr == "0x0863")
    {
        passed++;
    }
    else
    {
        std::cout << "Test 27 failed: 2147 != " << resultStr << std::endl;
    }

    std::cout << "Passed " << passed << " out of " << TEST_COUNT << " tests."
        << std::endl;
    return 0;
}
