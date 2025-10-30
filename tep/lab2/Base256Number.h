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
    inline ~Base256Number() { delete[] _value; }
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
    std::string to_string() const;
    inline int get_length() const { return _length; }
    inline bool is_negative() const { return _is_negative; }
    inline bool is_infinity() const { return _is_infinity; }
    inline unsigned char* get_value() const { return _value; }
    Base256Number& operator=(const Base256Number& number);
    inline Base256Number operator+(const Base256Number& number) const { return add(number); }
    inline Base256Number operator-(const Base256Number& number) const { return subtract(number); }
    inline Base256Number operator*(const Base256Number& number) const { return multiply(number); }
    inline Base256Number operator/(const Base256Number& number) const { return divide(number); }
    inline Base256Number operator%(const Base256Number& number) const { return modulo(number); }
    Base256Number& operator=(int number);
    inline Base256Number operator+(const int number) const { return add(number); }
    inline Base256Number operator-(const int number) const { return subtract(number); }
    inline Base256Number operator*(const int number) const { return multiply(number); }
    inline Base256Number operator/(const int number) const { return divide(number); }
    inline Base256Number operator%(const int number) const { return modulo(number); }

    static const Base256Number infinity;

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
