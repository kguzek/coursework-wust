cmake_minimum_required(VERSION 3.22)
project(coursework_wust_tep)

set(CMAKE_CXX_STANDARD 98)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(TEP-Lab1-Zad1
        lab1/zad1.cpp
)

add_executable(TEP-Lab1-Zad2
        lab1/zad2.cpp
        lab1/zad3.cpp
        lab1/zad3.h
)