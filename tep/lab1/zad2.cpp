#include <iostream>
#include "zad3.h"
#include "../common/io.h"

bool alloc_2d_array(int*** array, int cols, int rows)
{
    if (cols < 0 || rows < 0)
    {
        return false;
    }
    *array = new int*[rows];
    for (int i = 0; i < rows; i++)
    {
        (*array)[i] = new int[cols];
    }
    return true;
}

void alloc_and_print_2d_array(const int cols, const int rows)
{
    int** array;
    alloc_2d_array(&array, cols, rows);
    print_2d_array(&array, cols, rows);
    dealloc_2d_array(&array, cols, rows);
}

int main()
{
    alloc_and_print_2d_array(5, 3);
    alloc_and_print_2d_array(2, 7);
    return 0;
}
