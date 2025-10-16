#include <iostream>
#include <string>
#include "../common/io.h"

static const std::string DEFAULT_NAME = "konrad";
static const int DEFAULT_ARRAY_LENGTH = 7;

class Array
{
private:
    std::string _name;
    int* _array;
    int _size;

    int* _clone_array()
    {
        int* cloned_array = new int[_size];
        for (int i = 0; i < _size; i++)
        {
            cloned_array[i] = _array[i];
        }
        return cloned_array;
    }

public:
    Array()
    {
        _name = DEFAULT_NAME;
        std::cout << "bezp: '" << _name << "'" << std::endl;
        _size = DEFAULT_ARRAY_LENGTH;
        _array = new int[_size];
    }

    Array(std::string name, int array_length)
    {
        _name = name;
        std::cout << "parametr: '" << _name << "'" << std::endl;
        _size = array_length;
        _array = new int[_size];
    }

    Array(Array& other)
    {
        _name = other._name + "_copy";
        std::cout << "kopiuj: '" << _name << "'" << std::endl;
        _array = other._clone_array();
    }

    ~Array()
    {
        std::cout << "usuwam: '" << _name << "'" << std::endl;
        delete[] _array;
    }

    int* get_array()
    {
        return _array;
    }

    int get_size()
    {
        return _size;
    }

    void setName(std::string name)
    {
        _name = name;
    }

    bool setNewSize(int array_length)
    {
        if (array_length < 1)
        {
            return false;
        }
        _size = array_length;
        _array = new int[_size];
        return true;
    }

    /**
     * @brief Klonuj tablicę
     *
     * Tworzy nowy obiekt z tymi samymi polami co obecny.
     *
     * @example
     * Array array;
     * Array* cloned_array = array.clone();
     *
     * @note Zamiast tej funkcji można użyć konstruktora klonującego:
     * Array array;
     * Array cloned_array = new Array(*array);
     *
     * @warning Przy użyciu tej funkcji nazwa nowego obiektu pozostaje bez zmian.
     * Konstruktor klonujący dopisuje przyrostek "_clone".
     */
    Array* clone()
    {
        Array* cloned = new Array();
        cloned->_name = _name;
        cloned->_array = _clone_array();
        cloned->_size = _size;
        return cloned;
    }
};


// Praca na wskaźnikach, bez tworzenia kopii
void modify_array(Array* array, int new_size)
{
    array->setNewSize(new_size);
}

// Zostanie utworzona lokalna kopia obiektu `array`
void modify_array(Array array, int new_size)
{
    array.setNewSize(new_size);
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
    print_array(array->get_array(), array->get_size());
    delete array;
    return 0;
}
