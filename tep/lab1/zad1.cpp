#include <iostream>

static const int ARRAY_FILL_VALUE = 34;

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

void alloc_array_fill_34(const int size)
{
    if (size < 0)
    {
        std::cerr << "Invalid size: " << size << std::endl;
        return;
    }
    int* array = new int[size];
    for (int i = 0; i < size; i++)
    {
        array[i] = ARRAY_FILL_VALUE;
    }
    print_array(array, size);
    delete[] array;
}

int main()
{
    alloc_array_fill_34(0);
    alloc_array_fill_34(3);
    alloc_array_fill_34(-5);
    alloc_array_fill_34(10);
    alloc_array_fill_34(9999);
    return 0;
}
