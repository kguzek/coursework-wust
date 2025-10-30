
#include "Modyfikacja.h"

Data::Data()
{
}

Data::Data(int length)
{
    _length = length;
    _data = new unsigned char[_length];
    for (int i = 0; i < _length; i++)
    {
        _data[i] = 0;
    }
}

Data::~Data()
{
    delete[] _data;
}

Data::Data(Data& other)
{
    _length = other._length;
    _data = new unsigned char[_length];
    for (int i = 0; i < _length; i++)
    {
        _data[i] = other._data[i];
    }
}

bool Data::set(unsigned char* data, int length)
{
    if (length < 1 || length > _length)
    {
        return false;
    }
    for (int i = 0; i < length; i++)
    {
        _data[i] = data[i];
    }
    for (int i = length; i < _length; i++)
    {
        _data[i] = 0;
    }
    return true;
}

void allocate_data(Data** data, int length)
{
    *data = new Data(length);
}

int main()
{
    Data* data;
    Data* data_with_length = new Data(8);
    allocate_data(&data, 10);
    delete data;
    delete data_with_length;
}
