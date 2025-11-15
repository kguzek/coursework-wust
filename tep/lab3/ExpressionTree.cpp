#include <iostream>
#include <ostream>

#include "ExpressionTree.h"

#include <sstream>

bool is_whitespace_only(const std::string& s)
{
    for (size_t i = 0; i < s.size(); ++i)
    {
        if (s[i] != ' ')
        {
            return false;
        }
    }
    return true;
}

ExpressionTree::ExpressionTree(std::string& input)
{
    _root = new ExpressionNode(input);
    if (!is_whitespace_only(input))
    {
        std::cout <<
            "zignorowano nadmiarowe wyrażenia:" << input << std::endl <<
            "pomyślnie wczytano wyrażenie:     " << *this << std::endl;
    }
}

ExpressionTree::ExpressionTree(const ExpressionTree& other)
{
    _root = new ExpressionNode(*other._root);
}

ExpressionTree ExpressionTree::operator+(const ExpressionTree& other) const
{
    ExpressionTree new_tree(*this);
    ExpressionNode* new_child = new ExpressionNode(*other._root);
    ExpressionNode const* last_child = new_tree._root;
    if (last_child->has_children())
    {
        while (last_child->has_grandchildren())
        {
            last_child = last_child->get_child();
        }
        last_child->replace_child(new_child);
    }
    else
    {
        new_tree._root = new_child;
    }
    return new_tree;
}

ExpressionTree& ExpressionTree::operator=(const ExpressionTree& other)
{
    if (this != &other)
    {
        delete _root;
        _root = new ExpressionNode(*other._root);
    }
    return *this;
}

std::string ExpressionTree::to_string() const
{
    std::ostringstream string_stream;
    string_stream << *this;
    return string_stream.str();
}

std::ostream& operator<<(std::ostream& outs, const ExpressionTree& tree)
{
    return outs << *tree.get_root();
}
