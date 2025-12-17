#include <cstdlib>
#include <sstream>

#include "ExpressionNode.h"

#include <cmath>
#include <iostream>
#include <vector>

#include "Operation.h"

bool is_integer(const std::string& value)
{
    if (value.empty())
    {
        return false;
    }
    for (std::string::size_type i = 0; i < value.size(); ++i)
    {
        if (!std::isdigit(value[i]))
        {
            return false;
        }
    }
    return true;
}

std::string extract_alphanumeric(const std::string& input)
{
    std::string result;
    bool has_alphanumeric_characters = false;
    for (std::string::size_type i = 0; i < input.size(); ++i)
    {
        if (std::isalnum(static_cast<unsigned char>(input[i])))
        {
            result += input[i];
            has_alphanumeric_characters = true;
        }
    }
    return has_alphanumeric_characters ? result : "";
}

std::string int_to_string(const int value)
{
    std::ostringstream oss;
    oss << value;
    return oss.str();
}

ExpressionNode::ExpressionNode(std::string& input) : _children_count(0), _type(Constant), _data()
{
    int token_start;
    const size_t input_length = input.length();
    for (token_start = 0; token_start < input_length && input[token_start] == ' '; token_start++)
    {
    }
    int token_end;
    for (token_end = token_start; token_end < input_length && input[token_end] != ' '; token_end++)
    {
    }
    const int token_length = token_end - token_start;
    const std::string token = input.substr(token_start, token_length);

    if (is_integer(token))
    {
        _data.constant = std::atoi(token.c_str());
    }
    else
    {
        _data.constant = DEFAULT_CONSTANT_VALUE;
        switch (token_length)
        {
        case 0:
            _type = new Error("niewystarczająca ilość argumentów dla operacji");
            break;
        case 1:
            switch (input[token_start])
            {
            case '+':
                _type = Operator;
                _data.operation = Add;
                _children_count = 2;
                break;
            case '-':
                _type = Operator;
                _data.operation = Subtract;
                _children_count = 2;
                break;
            case '*':
                _type = Operator;
                _data.operation = Multiply;
                _children_count = 2;
                break;
            case '/':
                _type = Operator;
                _data.operation = Divide;
                _children_count = 2;
                break;
            default:
                _init_variable(token);
                break;
            }
            break;
        case 3:
            if (token == "sin")
            {
                _type = Operator;
                _data.operation = Sine;
                _children_count = 1;
                break;
            }
            if (token == "cos")
            {
                _type = Operator;
                _data.operation = Cosine;
                _children_count = 1;
                break;
            }
            _init_variable(token);
            break;
        default:
            _init_variable(token);
            break;
        }
    }
    input = input.substr(token_end);
    _children = new ExpressionNode*[_children_count];
    for (int i = 0; i < _children_count; ++i)
    {
        ExpressionNode* child = new ExpressionNode(input);
        _children[i] = child;
        if (!child->_type.is_success())
        {
            // propagate errors to parent
            _type = new Error(*child->_type.get_errors().front());
        }
    }
}

ExpressionNode::ExpressionNode(const ExpressionNode& other)
    : _children_count(other._children_count),
      _type(other._type),
      _variable_name(other._variable_name),
      _data()
{
    if (other._type.is_success())
    {
        switch (other._type.get_value())
        {
        case Constant:
            _data.constant = other._data.constant;
            break;
        case Operator:
            _data.operation = other._data.operation;
            break;
        default:
            break;
        }
    }
    _children = new ExpressionNode*[_children_count];
    for (int i = 0; i < _children_count; ++i)
    {
        _children[i] = new ExpressionNode(*other._children[i]);
    }
}

ExpressionNode::~ExpressionNode()
{
    for (int i = 0; i < _children_count; ++i)
    {
        delete _children[i];
    }
    delete[] _children;
}

void ExpressionNode::print_variable_children(std::ostream& os, std::set<std::string>& seen_variables) const
{
    if (
        _type.is_success()
        && _type.get_value() == Variable
        && seen_variables.find(_variable_name) == seen_variables.end()
    )
    {
        os << _variable_name << ' ';
        seen_variables.insert(_variable_name);
    }
    for (size_t i = 0; i < _children_count; ++i)
    {
        _children[i]->print_variable_children(os, seen_variables);
    }
}

double ExpressionNode::calculate_value(std::map<std::string, int>& variable_values) const
{
    if (!_type.is_success())
    {
        return DEFAULT_CONSTANT_VALUE;
    }
    switch (_type.get_value())
    {
    case Variable:
        return variable_values[_variable_name];
    case Constant:
        return _data.constant;
    case Operator:
        switch (_data.operation)
        {
        case Add:
            {
                const double first = _children[0]->calculate_value(variable_values);
                const double second = _children[1]->calculate_value(variable_values);
                return first + second;
            }
        case Subtract:
            {
                const double first = _children[0]->calculate_value(variable_values);
                const double second = _children[1]->calculate_value(variable_values);
                return first - second;
            }
        case Multiply:
            {
                const double first = _children[0]->calculate_value(variable_values);
                const double second = _children[1]->calculate_value(variable_values);
                return first * second;
            }
        case Divide:
            {
                const double first = _children[0]->calculate_value(variable_values);
                const double second = _children[1]->calculate_value(variable_values);
                return first / second;
            }
        case Sine:
            {
                const double operand = _children[0]->calculate_value(variable_values);
                return std::sin(operand);
            }
        case Cosine:
            {
                const double operand = _children[0]->calculate_value(variable_values);
                return std::cos(operand);
            }
        default:
            return DEFAULT_CONSTANT_VALUE;
        }
    default:
        return DEFAULT_CONSTANT_VALUE;
    }
}

std::string ExpressionNode::to_string() const
{
    if (!_type.is_success())
    {
        return "<error>";
    }
    switch (_type.get_value())
    {
    case Variable:
        return _variable_name;
    case Operator:
        switch (_data.operation)
        {
        case Add:
            return "+";
        case Subtract:
            return "-";
        case Multiply:
            return "*";
        case Divide:
            return "/";
        case Sine:
            return "sin";
        case Cosine:
            return "cos";
        default:
            return "";
        }
    case Constant:
        return int_to_string(_data.constant);
    default:
        return "";
    }
}

bool ExpressionNode::equals(const ExpressionNode& other,
                            std::map<std::string, int>& left_indices,
                            std::map<std::string, int>& right_indices,
                            std::vector<int>& left_vars,
                            std::vector<int>& right_vars) const
{
    if (this == &other)
    {
        return true;
    }
    if (_children_count != other._children_count)
    {
        return false;
    }
    if (
        !_type.is_success() || !other._type.is_success() ||
        _type.get_value() != other._type.get_value()
    )
    {
        return false;
    }
    switch (_type.get_value())
    {
    case Constant:
        if (_data.constant != other._data.constant)
        {
            return false;
        }
        break;
    case Operator:
        if (_data.operation != other._data.operation)
        {
            return false;
        }
        break;
    case Variable:
        left_vars.push_back(left_indices[_variable_name]);
        right_vars.push_back(right_indices[other._variable_name]);
        break;
    default:
        return false;
    }
    for (int i = 0; i < _children_count; ++i)
    {
        if (!_children[i]->equals(*other._children[i], left_indices, right_indices, left_vars, right_vars))
        {
            return false;
        }
    }
    return true;
}

void ExpressionNode::_init_variable(const std::string& token)
{
    const std::string extracted_token = extract_alphanumeric(token);
    if (extracted_token.empty() || extracted_token.size() != token.size())
    {
        _type = new Error("niewłaściwa nazwa zmiennej: '" + token + "'");
        return;
    }
    _type = Variable;
    _variable_name = extracted_token;
}

std::ostream& operator<<(std::ostream& outs, const ExpressionNode& node)
{
    outs << node.to_string();
    const ExpressionNode* const* children = node.get_children();
    const int children_count = node.get_children_count();
    for (size_t i = 0; i < children_count; ++i)
    {
        const ExpressionNode* child = children[i];
        outs << ' ' << *child;
    }
    return outs;
}
