#ifndef COURSEWORK_WUST_NUMBER_H
#define COURSEWORK_WUST_NUMBER_H

#define NUMBER_DEFAULT_LENGTH 1
#define NUMERIC_BASE 10

#include <string>

class Number
{
public:
    Number();
    explicit Number(int length);
    Number(const Number& other);
    ~Number() { delete[] _value; }
    void set(int new_value);
    void set(const Number& new_value);
    Number add(const Number& number) const;
    Number subtract(const Number& number) const;
    Number multiply(const Number& multiplier) const;
    Number divide(const Number& divisor) const;
    Number modulo(const Number& divisor) const;
    Number add(int number) const;
    Number subtract(int number) const;
    Number multiply(int multiplier) const;
    Number divide(int divisor) const;
    Number modulo(int divisor) const;
    bool is_magnitude_greater_or_equal(const Number& target) const;
    std::string to_string() const;
    int get_length() const { return _length; }
    bool is_negative() const { return _is_negative; }
    bool is_infinity() const { return _is_infinity; }
    int* get_value() const { return _value; }
    Number& operator=(const Number& number);
    Number operator+(const Number& number) const { return add(number); }
    Number operator-(const Number& number) const { return subtract(number); }
    Number operator*(const Number& number) const { return multiply(number); }
    Number operator/(const Number& number) const { return divide(number); }
    Number operator%(const Number& number) const { return modulo(number); }
    Number& operator=(int number);
    Number operator+(const int number) const { return add(number); }
    Number operator-(const int number) const { return subtract(number); }
    Number operator*(const int number) const { return multiply(number); }
    Number operator/(const int number) const { return divide(number); }
    Number operator%(const int number) const { return modulo(number); }

    static const Number infinity;

private:
    int* _value;
    int _length;
    bool _is_negative;
    bool _is_infinity;
    void _init_value() const;
    void _normalize();
    Number _add_abs(const Number& number) const;
    Number _subtract_abs(const Number& number) const;
    bool _is_zero() const;
    static Number _create_infinity();
};

std::ostream& operator<<(std::ostream& outs, const Number& number);

#endif //COURSEWORK_WUST_NUMBER_H
