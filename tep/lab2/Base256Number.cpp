#include "Base256Number.h"

#include <algorithm>
#include <bitset>
#include <cmath>
#include <sstream>
#include <string>

Base256Number::Base256Number()
{
    _is_negative = false;
    _is_infinity = false;
    _length = NUMBER_DEFAULT_LENGTH;
    _value = new unsigned char[_length];
    _init_value();
}

Base256Number::Base256Number(const int length)
{
    _is_negative = false;
    _is_infinity = false;
    this->_length = length;
    _value = new unsigned char[_length];
    _init_value();
}

Base256Number::Base256Number(const Base256Number& other)
{
    _is_negative = other._is_negative;
    _is_infinity = other._is_infinity;
    _length = other._length;
    _value = new unsigned char[_length];
    for (int i = 0; i < _length; i++)
    {
        _value[i] = other._value[i];
    }
}

void Base256Number::set(const int new_value)
{
    delete[] _value;
    _is_negative = new_value < 0;
    int new_value_abs = std::abs(new_value);
    _length = new_value_abs == 0 ? 1 : static_cast<int>(std::floor(log2(new_value_abs)) / 8) + 1;
    _value = new unsigned char[_length];

    // stores the digits in reverse order
    for (int i = 0; i < _length; i++)
    {
        _value[i] = new_value_abs % NUMERIC_BASE;
        new_value_abs /= NUMERIC_BASE;
    }
}

void Base256Number::set(const Base256Number& new_value)
{
    delete[] _value;
    _is_negative = new_value._is_negative;
    _length = new_value._length;
    _value = new unsigned char[_length];
    for (int i = 0; i < _length; i++)
    {
        _value[i] = new_value._value[i];
    }
}

Base256Number Base256Number::add(const Base256Number& number) const
{
    if (_is_negative != number._is_negative)
    {
        return _is_negative ? number._subtract_abs(*this) : _subtract_abs(number);
    }
    Base256Number result = _add_abs(number);

    if (_is_negative) // number.is_negative is then implied
    {
        // (-a) + (-b) = -(a + b)
        result._is_negative = true;
    }
    return result;
}

Base256Number Base256Number::subtract(const Base256Number& number) const
{
    if (_is_negative)
    {
        if (number._is_negative)
        {
            // (-a) - (-b) <=> b - a
            return number._subtract_abs(*this);
        }
        // (-a) - b <=> -(a + b)
        Base256Number result = add(number);
        result._is_negative = true;
        return result;
    }
    if (number._is_negative)
    {
        // a - (-b) <=> a + b
        return add(number);
    }
    // a - b, where a and b are positive
    return _subtract_abs(number);
}

Base256Number Base256Number::multiply(const Base256Number& multiplier) const
{
    if (multiplier._length > _length)
    {
        return multiplier.multiply(*this);
    }
    const int result_length = _length + multiplier._length;
    Base256Number result(result_length);

    for (int i = 0; i < multiplier._length; i++)
    {
        int carry = 0;
        const int row_length = _length + i + 1;
        Base256Number row(row_length);
        for (int j = 0; j < _length; j++)
        {
            int digit = _value[j] * multiplier._value[i] + carry;
            carry = digit / NUMERIC_BASE;
            digit -= carry * NUMERIC_BASE;
            row._value[i + j] = digit;
        }
        row._value[i + _length] = carry;
        const Base256Number sum = result + row;
        result = sum;
    }

    if (_is_negative != multiplier._is_negative)
    {
        result._is_negative = true;
    }

    result._normalize();

    return result;
}

Base256Number Base256Number::divide(const Base256Number& divisor) const
{
    Base256Number result;
    result = 0;
    Base256Number remainder(*this);

    if (divisor._is_zero())
    {
        return infinity;
    }

    while (remainder._is_negative == divisor._is_negative)
    {
        remainder = remainder - divisor;
        result = result + 1;
    }
    result = result - 1;

    if (_is_negative != divisor._is_negative)
    {
        result._is_negative = true;
    }
    return result;
}

Base256Number Base256Number::modulo(const Base256Number& divisor) const
{
    return *this - *this / divisor * divisor;
}

Base256Number Base256Number::add(const int number) const
{
    Base256Number number_object;
    number_object = number;
    return add(number_object);
}

Base256Number Base256Number::subtract(const int number) const
{
    Base256Number number_object;
    number_object = number;
    return subtract(number_object);
}

Base256Number Base256Number::multiply(const int multiplier) const
{
    Base256Number multiplier_object;
    multiplier_object = multiplier;
    return multiply(multiplier_object);
}

Base256Number Base256Number::divide(const int divisor) const
{
    Base256Number divisor_object;
    divisor_object = divisor;
    return divide(divisor_object);
}

Base256Number Base256Number::modulo(const int divisor) const
{
    Base256Number divisor_object;
    divisor_object = divisor;
    return modulo(divisor_object);
}

std::string Base256Number::to_array_string() const
{
    std::ostringstream string_stream;
    string_stream << *this;
    return string_stream.str();
}

std::string Base256Number::to_hex_string() const
{
    std::string result = "0x";
    for (int i = _length - 1; i >= 0; i--)
    {
        const unsigned int left = _value[i] / 16;
        const unsigned int right = _value[i] - left * 16;
        result += HEX_DIGITS[left];
        result += HEX_DIGITS[right];
    }
    return result;
}

std::string Base256Number::to_binary_string() const
{
    std::string result = "0b";
    for (int i = _length - 1; i >= 0; i--)
    {
        result += std::bitset<8>(_value[i]).to_string();
    }
    return result;
}


std::string Base256Number::to_decimal_string() const
{
    if (_is_infinity)
    {
        return "INFINITY";
    }
    std::string result;
    if (_is_negative)
    {
        result += "-";
    }
    for (int i = _length - 1; i >= 0; i--)
    {
        const int value = _value[i];
        result += dynamic_cast<std::ostringstream&>(std::ostringstream() << std::dec << value).str();
    }
    return result;
}

Base256Number& Base256Number::operator=(const Base256Number& number)
{
    if (this != &number)
    {
        set(number);
    }
    return *this;
}

Base256Number& Base256Number::operator=(const int number)
{
    set(number);
    return *this;
}

Base256Number Base256Number::operator&(const Base256Number& number) const
{
    if (number._length > _length)
    {
        return number & *this;
    }
    Base256Number result(_length);
    for (int i = 0; i < _length; i++)
    {
        result._value[i] = _value[i] & number._value[i];
    }
    return result;
}

Base256Number Base256Number::operator|(const Base256Number& number) const
{
    if (number._length > _length)
    {
        return number & *this;
    }
    Base256Number result(_length);
    for (int i = 0; i < _length; i++)
    {
        result._value[i] = _value[i] | number._value[i];
    }
    return result;
}

Base256Number Base256Number::operator^(const Base256Number& number) const
{
    if (number._length > _length)
    {
        return number & *this;
    }
    Base256Number result(_length);
    for (int i = 0; i < _length; i++)
    {
        result._value[i] = _value[i] ^ number._value[i];
    }
    return result;
}

Base256Number Base256Number::operator~() const
{
    Base256Number result(_length);
    for (int i = 0; i < _length; i++)
    {
        result._value[i] = ~_value[i];
    }
    return result;
}

Base256Number Base256Number::operator<<(const int number) const
{
    Base256Number result(_length);
    for (int i = 0; i < _length; i++)
    {
        result._value[i] = _value[i] << number;
    }
    return result;
}

Base256Number Base256Number::operator>>(const int number) const
{
    Base256Number result(_length);
    for (int i = 0; i < _length; i++)
    {
        result._value[i] = _value[i] >> number;
    }
    return result;
}

void Base256Number::_init_value() const
{
    for (int i = 0; i < _length; i++)
    {
        _value[i] = 0;
    }
}

void Base256Number::_normalize()
{
    while (_length > 1 && _value[_length - 1] == 0)
    {
        // remove leading 0
        _length--;
    }
}

/* Adds the absolute value of `number` to the absolute value of `this`. */
Base256Number Base256Number::_add_abs(const Base256Number& number) const
{
    const int result_length = number._length > _length ? number._length : _length;
    // add one to max length due to possible carry overflow
    Base256Number result(result_length + 1);

    bool carry = false;
    for (int i = 0; i < result_length; i++)
    {
        const int left_digit = i < _length ? _value[i] : 0;
        const int right_digit = i < number._length ? number._value[i] : 0;
        int digit = left_digit + right_digit + carry;
        carry = false;
        if (digit >= NUMERIC_BASE)
        {
            carry = true;
            digit -= NUMERIC_BASE;
        }
        result._value[i] = digit;
    }
    if (carry)
    {
        result._value[result_length] = 1;
    }
    else
    {
        // carry not needed - resize back to computed length
        result._length = result_length;
    }
    return result;
}

Base256Number Base256Number::_subtract_abs(const Base256Number& number) const
{
    if (_length < number._length)
    {
        Base256Number result = number.subtract(*this);
        result._is_negative = true;
        return result;
    }

    Base256Number result(_length);
    bool was_carry = false;
    for (int i = 0; i < _length; i++)
    {
        const int number_digit = i < number._length ? number._value[i] : 0;
        int digit = _value[i] - number_digit;
        _value[i] += was_carry;
        was_carry = false;
        if (digit < 0)
        {
            digit += NUMERIC_BASE;
            _value[i + 1] -= 1;
            was_carry = true;
        }
        result._value[i] = digit;
    }

    if (was_carry)
    {
        result._is_negative = true;
        result._value[_length - 1] = NUMERIC_BASE - result._value[_length - 1];
    }
    result._normalize();

    return result;
}

bool Base256Number::_is_zero() const
{
    return _length == 1 && _value[0] == 0;
}

const Base256Number Base256Number::infinity = _create_infinity();
const std::string Base256Number::HEX_DIGITS = "0123456789ABCDEF";

Base256Number Base256Number::_create_infinity()
{
    Base256Number inf;
    inf = 0;
    inf._is_infinity = true;
    return inf;
}

std::ostream& operator<<(std::ostream& outs, const Base256Number& number)
{
    if (number.is_infinity())
    {
        outs << "INFINITY";
        return outs;
    }
    if (number.is_negative())
    {
        outs << "- ";
    }
    const unsigned char* value = number.get_value();
    outs << "|";
    for (int i = number.get_length() - 1; i >= 0; i--)
    {
        outs << ' ' << static_cast<int>(value[i]) << " |";
    }
    return outs;
}
