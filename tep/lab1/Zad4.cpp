#include "Zad4.h"

#include <iostream>
#include <string>
#include "../common/io.h"

static const std::string DEFAULT_NAME = "konrad";
static const int DEFAULT_ARRAY_LENGTH = 7;


Array::Array()
{
    _name = DEFAULT_NAME;
    std::cout << "bezp: '" << _name << "'" << std::endl;
    _size = DEFAULT_ARRAY_LENGTH;
    _array = new int[_size];
}

Array::Array(std::string name, int array_length)
{
    _name = name;
    std::cout << "parametr: '" << _name << "'" << std::endl;
    _size = array_length;
    _array = new int[_size];
}

Array::Array(Array& other)
{
    _name = other._name + "_copy";
    std::cout << "kopiuj: '" << _name << "'" << std::endl;
    _array = other._clone_array();
}

Array::~Array()
{
    std::cout << "usuwam: '" << _name << "'" << std::endl;
    delete[] _array;
}

int* Array::get_array()
{
    return _array;
}

int Array::get_size()
{
    return _size;
}

void Array::set_name(std::string name)
{
    _name = name;
}

bool Array::set_size(int array_length)
{
    if (array_length < 1)
    {
        return false;
    }
    _size = array_length;

    delete _array;
    _array = new int[_size];
    return true;
}

Array* Array::clone()
{
    Array* cloned = new Array();
    cloned->_name = _name;
    cloned->_array = _clone_array();
    cloned->_size = _size;
    return cloned;
}

int* Array::_clone_array()
{
    int* cloned_array = new int[_size];
    for (int i = 0; i < _size; i++)
    {
        cloned_array[i] = _array[i];
    }
    return cloned_array;
}

// Praca na wskaźnikach, bez tworzenia kopii
void modify_array(Array* array, int new_size)
{
    array->set_size(new_size);
}

// Zostanie utworzona lokalna kopia obiektu `array`
void modify_array(Array array, int new_size)
{
    array.set_size(new_size);
}

int main()
{
    Array* array;
    array = new Array();
    print_array(array->get_array(), array->get_size());
    Array* cloned_array = new Array(*array);
    delete cloned_array;
    cloned_array = array->clone();
    print_array(cloned_array->get_array(), cloned_array->get_size());
    delete cloned_array;
    modify_array(array, 10);
    modify_array(*array, 10);
    print_array(array->get_array(), array->get_size());
    delete array;
    return 0;
}
