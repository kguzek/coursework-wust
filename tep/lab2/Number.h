#ifndef COURSEWORK_WUST_NUMBER_H
#define COURSEWORK_WUST_NUMBER_H

#define NUMBER_DEFAULT_LENGTH 10
#include <string>

class Number
{
public:
    Number();
    explicit Number(int length);
    Number(const Number& other);
    ~Number() { delete[] _value; }
    void set(int new_value);
    void set(Number& new_value);
    Number add(Number& number);
    Number subtract(Number& number);
    Number multiply(Number& multiplier);
    Number divide(Number& divisor);
    Number add(int number);
    Number subtract(int number);
    Number multiply(int multiplier);
    Number divide(int divisor);
    std::string toString() const;
    int get_length() const { return _length; }
    bool is_negative() const { return _is_negative; }
    int* get_value() const { return _value; }
    Number& operator=(int number);
    Number operator+(Number& number) { return add(number); }
    Number operator-(Number& number) { return subtract(number); }
    Number operator*(Number& number) { return multiply(number); }
    Number operator/(Number& number) { return divide(number); }
    Number operator+(int number) { return add(number); }
    Number operator-(int number) { return subtract(number); }
    Number operator*(int number) { return multiply(number); }
    Number operator/(int number) { return divide(number); }

private:
    int* _value;
    int _length;
    bool _is_negative;
    Number add_abs(Number& number);
    Number subtract_abs(Number& number);
};

std::ostream& operator<<(std::ostream& outs, const Number& number);

#endif //COURSEWORK_WUST_NUMBER_H
