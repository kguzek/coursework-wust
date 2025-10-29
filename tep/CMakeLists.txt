cmake_minimum_required(VERSION 3.22)
project(coursework_wust_tep)

set(CMAKE_CXX_STANDARD 98)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#region lab 1

add_executable(TEP-Lab1-Zad1
        lab1/zad1.cpp
        lab1/zad1.h
        common/io.cpp
        common/io.h
)

add_executable(TEP-Lab1-Zad2
        lab1/zad2.cpp
        lab1/zad2.h
        lab1/zad3.cpp
        lab1/zad3.h
        common/io.cpp
        common/io.h
)

add_executable(TEP-Lab1-Zad4
        lab1/zad4.cpp
        lab1/zad4.h
        common/io.cpp
        common/io.h
)

add_executable(TEP-Lab1-Modyfikacja
        lab1/modyfikacja.cpp
        lab1/modyfikacja.h
)

#endregion

#region lab 2

add_executable(TEP-Lab2
        lab2/Number.cpp
        lab2/Number.h
)

#endregion
