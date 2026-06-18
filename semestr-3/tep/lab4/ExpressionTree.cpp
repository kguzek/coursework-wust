#include <iostream>
#include <ostream>

#include "ExpressionTree.h"

#include <sstream>
#include <vector>

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

ExpressionTree::ExpressionTree(ExpressionNode* node) : _root(node)
{
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

bool ExpressionTree::operator==(const ExpressionTree& other) const
{
    std::map<std::string, int> left_indices = _get_var_indices();
    std::map<std::string, int> right_indices = other._get_var_indices();

    if (left_indices.size() != right_indices.size())
    {
        return false;
    }

    std::vector<int> left_variable_occurrences;
    std::vector<int> right_variable_occurrences;
    const bool node_types_equal = _root->equals(
        *other._root,
        left_indices,
        right_indices,
        left_variable_occurrences,
        right_variable_occurrences
    );
    return node_types_equal && left_variable_occurrences == right_variable_occurrences;
}

Result<ExpressionTree*, Error> ExpressionTree::parse(std::string& input)
{
    ExpressionNode* root = new ExpressionNode(input);
    if (!is_whitespace_only(input))
    {
        delete root;
        return Result<ExpressionTree*, Error>::fail(new Error("zbyt wiele argumentów; nadmiar: '" + input + "'"));
    }
    Result<ExpressionNodeType, Error> type = root->get_type();
    if (type.is_success())
    {
        return new ExpressionTree(root);
    }
    Error* error = new Error(*type.get_errors().front());
    delete root;
    return error;
}

std::map<std::string, int> ExpressionTree::_get_var_indices() const
{
    std::stringstream variable_names;
    std::set<std::string> seen_variables;
    _root->print_variable_children(variable_names, seen_variables);
    std::map<std::string, int> variable_indices;
    std::string name;
    for (int index = 0; variable_names >> name; ++index)
    {
        variable_indices[name] = index;
    }
    return variable_indices;
}

std::ostream& operator<<(std::ostream& outs, const ExpressionTree& tree)
{
    return outs << *tree.get_root();
}
