#ifndef COURSEWORK_WUST_TEP_MODYFIKACJA_H
#define COURSEWORK_WUST_TEP_MODYFIKACJA_H

class Data
{
public:
    Data();

    Data(int length);

    ~Data();

    Data(Data& other);

    bool set(unsigned char* data, int length);

private:
    unsigned char* _data;
    int _length;
};

void allocate_data(Data** data, int length);

#endif //COURSEWORK_WUST_TEP_MODYFIKACJA_H
