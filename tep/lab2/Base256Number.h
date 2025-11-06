#ifndef COURSEWORK_WUST_BASE_256_NUMBER_H
#define COURSEWORK_WUST_BASE_256_NUMBER_H

#define NUMBER_DEFAULT_LENGTH 1
#define NUMERIC_BASE 256

#include <string>

class Base256Number
{
public:
    Base256Number();
    explicit Base256Number(int length);
    Base256Number(const Base256Number& other);
    ~Base256Number() { delete[] _value; }
    void set(int new_value);
    void set(const Base256Number& new_value);
    Base256Number add(const Base256Number& number) const;
    Base256Number subtract(const Base256Number& number) const;
    Base256Number multiply(const Base256Number& multiplier) const;
    Base256Number divide(const Base256Number& divisor) const;
    Base256Number modulo(const Base256Number& divisor) const;
    Base256Number add(int number) const;
    Base256Number subtract(int number) const;
    Base256Number multiply(int multiplier) const;
    Base256Number divide(int divisor) const;
    Base256Number modulo(int divisor) const;
    bool is_magnitude_greater_or_equal(const Base256Number& target) const;
    std::string to_array_string() const;
    std::string to_hex_string() const;
    std::string to_binary_string() const;
    int get_length() const { return _length; }
    bool is_negative() const { return _is_negative; }
    bool is_infinity() const { return _is_infinity; }
    unsigned char* get_value() const { return _value; }
    Base256Number& operator=(const Base256Number& number);
    Base256Number operator+(const Base256Number& number) const { return add(number); }
    Base256Number operator-(const Base256Number& number) const { return subtract(number); }
    Base256Number operator*(const Base256Number& number) const { return multiply(number); }
    Base256Number operator/(const Base256Number& number) const { return divide(number); }
    Base256Number operator%(const Base256Number& number) const { return modulo(number); }
    Base256Number& operator=(int number);
    Base256Number operator+(const int number) const { return add(number); }
    Base256Number operator-(const int number) const { return subtract(number); }
    Base256Number operator*(const int number) const { return multiply(number); }
    Base256Number operator/(const int number) const { return divide(number); }
    Base256Number operator%(const int number) const { return modulo(number); }
    Base256Number operator&(const Base256Number& number) const;
    Base256Number operator|(const Base256Number& number) const;
    Base256Number operator^(const Base256Number& number) const;
    Base256Number operator~() const;
    Base256Number operator<<(int number) const;
    Base256Number operator>>(int number) const;

    static const Base256Number infinity;
    static const std::string HEX_DIGITS;

private:
    unsigned char* _value;
    int _length;
    bool _is_negative;
    bool _is_infinity;
    void _init_value() const;
    void _normalize();
    Base256Number _add_abs(const Base256Number& number) const;
    Base256Number _subtract_abs(const Base256Number& number) const;
    bool _is_zero() const;
    static Base256Number _create_infinity();
};

std::ostream& operator<<(std::ostream& outs, const Base256Number& number);

#endif //COURSEWORK_WUST_BASE_256_NUMBER_H
