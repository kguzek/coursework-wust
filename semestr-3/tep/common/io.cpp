#include <iostream>

void print_array(const int array[], const int size)
{
    std::cout << "[";
    if (size > 0)
    {
        std::cout << array[0];
        for (int i = 1; i < size; i++)
        {
            std::cout << ", " << array[i];
        }
    }
    std::cout << "]" << std::endl;
}


void print_2d_array(int*** array, const int cols, const int rows)
{
    std::cout << "{" << std::endl;
    for (int i = 0; i < rows; i++)
    {
        print_array((*array)[i], cols);
    }
    std::cout << "}" << std::endl;
}
