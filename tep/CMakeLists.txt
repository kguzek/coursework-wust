cmake_minimum_required(VERSION 3.22)
project(coursework_wust_tep)

set(CMAKE_CXX_STANDARD 98)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#region lab 1

add_executable(TEP-Lab1-Zad1
        lab1/Zad1.cpp
        common/io.cpp
)

add_executable(TEP-Lab1-Zad2
        lab1/Zad2.cpp
        lab1/Zad3.cpp
        common/io.cpp
)

add_executable(TEP-Lab1-Zad4
        lab1/Zad4.cpp
        common/io.cpp
)

add_executable(TEP-Lab1-Modyfikacja
        lab1/Modyfikacja.cpp
)

#endregion

#region lab 2

add_executable(TEP-Lab2-Zad1
        lab2/Number.cpp
        lab2/Zad1.cpp
)

add_executable(TEP-Lab2-Sandbox
        lab2/Number.cpp
        lab2/NumberSandbox.cpp
)

add_executable(TEP-Lab2-Tests
        lab2/Number.cpp
        lab2/NumberTests.cpp
)

add_executable(TEP-Lab2-LiveCoding-Sandbox
        lab2/Base256Number.cpp
        lab2/Base256NumberSandbox.cpp
)

add_executable(TEP-Lab2-LiveCoding-Tests
        lab2/Base256Number.cpp
        lab2/Base256NumberTests.cpp
)

#endregion

#region lab 3

add_executable(TEP-Lab3
        lab3/ExpressionNode.cpp
        lab3/ExpressionTree.cpp
        lab3/ExpressionParser.cpp
)

#endregion

#region lab 4

add_executable(TEP-Lab4-Zad2
        lab4/Error.cpp
        lab4/zad2.cpp
)

add_executable(TEP-Lab4-Zad3
        lab4/Error.cpp
        lab4/ExpressionNode.cpp
        lab4/ExpressionTree.cpp
        lab4/ExpressionParser.cpp
)
add_executable(TEP-Lab4-Zad4
        lab4/Error.cpp
        lab4/ExpressionNode.cpp
        lab4/ExpressionTree.cpp
        lab4/zad4.cpp
)
add_executable(TEP-Lab4-LiveCoding
        lab4/livecoding.cpp
)

#endregion

#region lab 5

add_executable(TEP-Lab5-Tab
        lab5/Tab.cpp
)
set_target_properties(TEP-Lab5-Tab PROPERTIES
        CXX_STANDARD 23
        CXX_STANDARD_REQUIRED YES
)

add_executable(TEP-Lab5-Zad4
        lab5/Error.cpp
        lab5/ExpressionNode.cpp
        lab5/ExpressionTree.cpp
        lab5/SmartPointer.h
        lab5/zad4.cpp
)
set_target_properties(TEP-Lab5-Zad4 PROPERTIES
        CXX_STANDARD 23
        CXX_STANDARD_REQUIRED YES
)

add_executable(TEP-Lab5-Zad5
        lab5/Error.cpp
        lab5/ExpressionNode.cpp
        lab5/ExpressionTree.cpp
        lab5/SmartPointer.h
        lab5/zad5.cpp
)
set_target_properties(TEP-Lab5-Zad5 PROPERTIES
        CXX_STANDARD 23
        CXX_STANDARD_REQUIRED YES
)

add_executable(TEP-Lab5-LiveCoding
        lab5/SmartPointer.h
        lab5/SingleSmartPointer.h
        lab5/livecoding.cpp
        lab5/Product.h
)
set_target_properties(TEP-Lab5-LiveCoding PROPERTIES
        CXX_STANDARD 23
        CXX_STANDARD_REQUIRED YES
)

add_executable(TEP-Lab5-TreeTest
        lab5/ExpressionTree.cpp
        lab5/ExpressionNode.cpp
        lab5/Error.cpp
        lab5/tree_test.cpp
)
set_target_properties(TEP-Lab5-TreeTest PROPERTIES
        CXX_STANDARD 23
        CXX_STANDARD_REQUIRED YES
)

#endregion
