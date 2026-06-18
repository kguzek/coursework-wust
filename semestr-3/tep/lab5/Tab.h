#ifndef COURSEWORK_WUST_TAB_H
#define COURSEWORK_WUST_TAB_H


#define DEF_TAB_SIZE 10
#include <iostream>

class Tab
{
public:
    Tab();
    Tab(const Tab& other);
    Tab(Tab&& other) noexcept;
    Tab& operator=(const Tab& other);
    ~Tab();
    bool set_size(int new_size);
    int get_size() const { return _size; }

private:
    void _copy(const Tab& other);
    int* _tab;
    int _size;
};


inline Tab::Tab()
{
    _tab = new int[DEF_TAB_SIZE];
    _size = DEF_TAB_SIZE;
}

inline Tab::Tab(const Tab& other)
{
    _copy(other);
    std::cout << "Copy ";
}

inline Tab::Tab(Tab&& other) noexcept
{
    _tab = other._tab;
    _size = other._size;
    other._tab = NULL;
    std::cout << "Move ";
}

inline Tab& Tab::operator=(const Tab& other)
{
    if (this == &other)
    {
        return *this;
    }
    if (_tab != NULL)
    {
        delete _tab;
    }
    _copy(other);
    std::cout << "operator= ";
    return *this;
}

inline Tab::~Tab()
{
    if (_tab != NULL)
    {
        delete _tab;
        std::cout << "Destructor ";
    }
}

inline bool Tab::set_size(const int new_size)
{
    if (new_size < _size)
    {
        return false;
    }
    int* new_tab = new int[new_size];
    for (int i = 0; i < _size; i++)
    {
        new_tab[i] = _tab[i];
    }
    delete _tab;
    _tab = new_tab;
    _size = new_size;
    return true;
}

inline void Tab::_copy(const Tab& other)
{
    _tab = new int[other._size];
    _size = other._size;
    for (int i = 0; i < other._size; i++)
    {
        _tab[i] = other._tab[i];
    }
}
#endif //COURSEWORK_WUST_TAB_H
