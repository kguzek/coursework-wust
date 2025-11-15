#include <cstdlib>
#include <string>
#include <sstream>

#include "ExpressionNode.h"
#include "Operation.h"

bool is_integer(const std::string& value)
{
    if (value.empty())
    {
        return false;
    }
    const size_t value_size = value.size();
    for (size_t i = 0; i < value_size; ++i)
    {
        if (!std::isdigit(value[i]))
        {
            return false;
        }
    }
    return true;
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
                _type = Variable;
                _name = token;
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
        default:
            _type = Variable;
            _name = token;
            break;
        }
    }
    _children = new ExpressionNode*[_children_count];
    input = input.substr(token_end);
    for (int i = 0; i < _children_count; i++)
    {
        _children[i] = new ExpressionNode(input);
    }
}

ExpressionNode::ExpressionNode(const ExpressionNode& other)
    : _children_count(other._children_count),
      _type(other._type),
      _name(other._name),
      _data()
{
    switch (other._type)
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
    _children = new ExpressionNode*[_children_count];
    for (int i = 0; i < _children_count; i++)
    {
        _children[i] = new ExpressionNode(*other._children[i]);
    }
}

ExpressionNode::~ExpressionNode()
{
    for (int i = 0; i < _children_count; i++)
    {
        delete _children[i];
    }
    delete[] _children;
}

std::ostream& operator<<(std::ostream& outs, const ExpressionNode& node)
{
    switch (node.get_type())
    {
    case Operator:
        switch (node.get_operation())
        {
        case Add:
            outs << '+';
            break;
        case Subtract:
            outs << '-';
            break;
        case Multiply:
            outs << '*';
            break;
        case Divide:
            outs << '/';
            break;
        case Sine:
            outs << "sin";
            break;
        case Cosine:
            outs << "cos";
            break;
        default:
            break;
        }
        break;
    case Constant:
        outs << node.get_constant();
        break;
    case Variable:
        outs << node.get_name();
        break;
    default:
        break;
    }
    const ExpressionNode* const* children = node.get_children();
    const int children_count = node.get_children_count();
    for (size_t i = 0; i < children_count; i++)
    {
        const ExpressionNode* child = children[i];
        outs << ' ' << *child;
    }
    return outs;
}
