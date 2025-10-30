#include "Number.h"

#include <algorithm>
#include <cmath>
#include <sstream>

Number::Number()
{
    _is_negative = false;
    _length = NUMBER_DEFAULT_LENGTH;
    _value = new int[_length];
    _init_value();
}

Number::Number(const int length)
{
    _is_negative = false;
    this->_length = length;
    _value = new int[_length];
    _init_value();
}

Number::Number(const Number& other)
{
    _is_negative = other._is_negative;
    _length = other._length;
    _value = new int[_length];
    for (int i = 0; i < _length; i++)
    {
        _value[i] = other._value[i];
    }
}

void Number::set(const int new_value)
{
    delete[] _value;
    _is_negative = new_value < 0;
    int new_value_abs = std::abs(new_value);
    _length = new_value_abs == 0 ? 1 : static_cast<int>(std::floor(std::log10(new_value_abs))) + 1;
    _value = new int[_length];

    // stores the digits in reverse order
    for (int i = 0; i < _length; i++)
    {
        _value[i] = new_value_abs % 10;
        new_value_abs /= 10;
    }
}

void Number::set(const Number& new_value)
{
    delete[] _value;
    _length = new_value._length;
    _value = new int[_length];
    for (int i = 0; i < _length; i++)
    {
        _value[i] = new_value._value[i];
    }
}

Number Number::add(const Number& number) const
{
    if (_is_negative != number._is_negative)
    {
        return _is_negative ? number.subtract(*this) : subtract(number);
    }
    Number result = _add_abs(number);

    if (_is_negative) // number.is_negative is then implied
    {
        // (-a) + (-b) = -(a + b)
        result._is_negative = true;
    }
    return result;
}

Number Number::subtract(const Number& number) const
{
    if (_is_negative)
    {
        if (number._is_negative)
        {
            // (-a) - (-b) <=> b - a
            return number._subtract_abs(*this);
        }
        // (-a) - b <=> -(a + b)
        Number result = add(number);
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

Number Number::multiply(const Number& multiplier) const
{
    if (multiplier._length > _length)
    {
        return multiplier.multiply(*this);
    }
    const int result_length = _length + multiplier._length;
    Number result(result_length);

    for (int i = 0; i < multiplier._length; i++)
    {
        int carry = 0;
        const int row_length = _length + i + 1;
        Number row(row_length);
        for (int j = 0; j < _length; j++)
        {
            int digit = _value[j] * multiplier._value[i] + carry;
            carry = digit / 10;
            digit -= carry * 10;
            row._value[i + j] = digit;
        }
        row._value[i + _length] = carry;
        const Number sum = result + row;
        result = sum;
    }

    if (_is_negative != multiplier._is_negative)
    {
        result._is_negative = true;
    }

    result._normalize();

    return result;
}

Number Number::divide(const Number& divisor) const
{
    return *new Number();
}

Number Number::add(const int number) const
{
    Number number_object;
    number_object = number;
    return add(number_object);
}

Number Number::subtract(const int number) const
{
    Number number_object;
    number_object = number;
    return subtract(number_object);
}

Number Number::multiply(const int multiplier) const
{
    Number multiplier_object;
    multiplier_object = multiplier;
    return multiply(multiplier_object);
}

Number Number::divide(const int divisor) const
{
    Number divisor_object;
    divisor_object = divisor;
    return divide(divisor_object);
}

std::string Number::toString() const
{
    std::ostringstream string_stream;
    string_stream << *this;
    return string_stream.str();
}

Number& Number::operator=(const Number& number)
{
    if (this != &number)
    {
        set(number);
    }
    return *this;
}

Number& Number::operator=(const int number)
{
    set(number);
    return *this;
}

void Number::_init_value() const
{
    for (int i = 0; i < _length; i++)
    {
        _value[i] = 0;
    }
}

void Number::_normalize()
{
    if (_length > 1 && _value[_length - 1] == 0)
    {
        // remove leading 0
        _length--;
    }
}

/* Adds the absolute value of `number` to the absolute value of `this`. */
Number Number::_add_abs(const Number& number) const
{
    const int result_length = number._length > _length ? number._length : _length;
    // add one to max length due to possible carry overflow
    Number result(result_length + 1);

    bool carry = false;
    for (int i = 0; i < result_length; i++)
    {
        const int left_digit = i < _length ? _value[i] : 0;
        const int right_digit = i < number._length ? number._value[i] : 0;
        int digit = left_digit + right_digit + carry;
        carry = false;
        if (digit >= 10)
        {
            carry = true;
            digit -= 10;
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

Number Number::_subtract_abs(const Number& number) const
{
    if (_length < number._length)
    {
        Number result = number.subtract(*this);
        result._is_negative = true;
        return result;
    }

    Number result(_length);
    bool was_carry = false;
    for (int i = 0; i < _length; i++)
    {
        int number_digit = i < number._length ? number._value[i] : 0;
        int digit = _value[i] - number_digit;
        _value[i] += was_carry;
        was_carry = false;
        if (digit < 0)
        {
            digit += 10;
            _value[i + 1] -= 1;
            was_carry = true;
        }
        result._value[i] = digit;
    }

    if (was_carry)
    {
        result._is_negative = true;
        result._value[_length - 1] = 10 - result._value[_length - 1];
    }
    result._normalize();

    return result;
}


std::ostream& operator<<(std::ostream& outs, const Number& number)
{
    if (number.is_negative())
    {
        outs << '-';
    }
    const int* value = number.get_value();
    for (int i = number.get_length() - 1; i >= 0; i--)
    {
        outs << value[i];
    }
    return outs;
}
