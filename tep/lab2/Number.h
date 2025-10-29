//
// Created by konrad on 29/10/2025.
//

#ifndef COURSEWORK_WUST_NUMBER_H
#define COURSEWORK_WUST_NUMBER_H

#define NUMBER_DEFAULT_LENGTH 10

class Number
{
public:
    Number()
    {
        length = NUMBER_DEFAULT_LENGTH;
        value = new int[length];
    };
    ~Number() { delete value; }
    void set(int new_value);
    void set(Number& new_value);
    Number add(Number& value);
    Number subtract(Number& value);
    Number multiply(Number& multiplier);
    Number divide(Number& divisor);
    Number add(int value);
    Number subtract(int value);
    Number multiply(int multiplier);
    Number divide(int divisor);

private:
    int* value;
    int length;
};

#endif //COURSEWORK_WUST_NUMBER_H
