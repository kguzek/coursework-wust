#ifndef COURSEWORK_WUST_TEP_EXPRESSION_NODE_H
#define COURSEWORK_WUST_TEP_EXPRESSION_NODE_H
#include <map>
#include <set>
#include <string>
#include <vector>

#include "Error.h"
#include "ExpressionNodeType.h"
#include "Operation.h"
#include "Result.h"

#define DEFAULT_CONSTANT_VALUE 1

class ExpressionNode
{
public:
    explicit ExpressionNode(std::string& input);
    ExpressionNode(const ExpressionNode& other);
    ~ExpressionNode();
    Result<ExpressionNodeType, Error> get_type() const { return _type; }
    ExpressionNode** get_children() const { return _children; }
    int get_children_count() const { return _children_count; }
    std::string get_name() const { return _variable_name; }
    int get_constant() const { return _data.constant; }
    Operation get_operation() const { return _data.operation; }
    bool has_children() const { return _children_count > 0; }
    ExpressionNode* get_last_child() const { return _children[_children_count - 1]; }
    void replace_last_child(ExpressionNode* new_child) const { _children[_children_count - 1] = new_child; }
    ExpressionNode* get_child() const { return get_last_child(); }
    void replace_child(ExpressionNode* new_child) const { replace_last_child(new_child); }
    bool has_grandchildren() const { return has_children() && get_child()->has_children(); }
    void print_variable_children(std::ostream& os, std::set<std::string>& seen_variables) const;
    double calculate_value(std::map<std::string, int>& variable_values) const;
    std::string to_string() const;
    bool equals(const ExpressionNode& other,
                std::map<std::string, int>& left_indices,
                std::map<std::string, int>& right_indices,
                std::vector<int>& left_vars,
                std::vector<int>& right_vars) const;

private:
    int _children_count;
    ExpressionNode** _children;
    Result<ExpressionNodeType, Error> _type;
    std::string _variable_name;

    union
    {
        int constant;
        Operation operation;
    } _data;

    void _init_variable(const std::string& token);
};

std::ostream& operator<<(std::ostream& outs, const ExpressionNode& node);

#endif //COURSEWORK_WUST_TEP_EXPRESSION_NODE_H
