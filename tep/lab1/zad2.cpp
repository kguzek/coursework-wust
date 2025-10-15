#include <iostream>

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

void alloc_and_print_2d_array(const int cols, const int rows)
{
    int** array;
    alloc_2d_array(&array, cols, rows);
    print_2d_array(&array, cols, rows);
    for (int i = 0; i < rows; i++)
    {
        delete[] array[i];
    }
}

int main()
{
    alloc_and_print_2d_array(5, 3);
    alloc_and_print_2d_array(2, 7);
    return 0;
}
