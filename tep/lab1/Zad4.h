#ifndef COURSEWORK_WUST_TEP_ZAD4_H
#define COURSEWORK_WUST_TEP_ZAD4_H
#include <iostream>
#include <string>


class Array
{
public:
    Array();

    Array(std::string name, int array_length);

    Array(Array& other);

    ~Array();

    int* get_array();

    int get_size();

    void set_name(std::string name);

    bool set_size(int array_length);

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
     * Array cloned_array = new Array(array);
     *
     * @warning Przy użyciu tej funkcji nazwa nowego obiektu pozostaje bez zmian.
     * Konstruktor klonujący dopisuje przyrostek "_clone".
     */
    Array* clone();

private:
    std::string _name;
    int* _array;
    int _size;

    int* _clone_array();
};

#endif //COURSEWORK_WUST_TEP_ZAD4_H
