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
add_executable(TEP-Lab3
        lab3/ExpressionNode.cpp
        lab3/ExpressionTree.cpp
        lab3/ExpressionParser.cpp
)
