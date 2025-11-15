#ifndef COURSEWORK_WUST_TEP_EXPRESSION_NODE_H
#define COURSEWORK_WUST_TEP_EXPRESSION_NODE_H
#include <string>

#include "ExpressionNodeType.h"
#include "Operation.h"

#define DEFAULT_CONSTANT_VALUE 1

class ExpressionNode
{
public:
    explicit ExpressionNode(std::string& input);
    ExpressionNode(const ExpressionNode& other);
    ~ExpressionNode();
    ExpressionNodeType get_type() const { return _type; }
    ExpressionNode** get_children() const { return _children; }
    int get_children_count() const { return _children_count; }
    std::string get_name() const { return _name; }
    int get_constant() const { return _data.constant; }
    Operation get_operation() const { return _data.operation; }
    bool has_children() const { return _children_count > 0; }
    ExpressionNode* get_last_child() const { return _children[_children_count - 1]; }
    void replace_last_child(ExpressionNode* new_child) const { _children[_children_count - 1] = new_child; }
    ExpressionNode* get_child() const { return get_last_child(); }
    void replace_child(ExpressionNode* new_child) const { replace_last_child(new_child); }
    bool has_grandchildren() const { return has_children() && get_child()->has_children(); }

private:
    int _children_count;
    ExpressionNode** _children;
    ExpressionNodeType _type;
    std::string _name;

    union
    {
        int constant;
        Operation operation;
    } _data;
};

std::ostream& operator<<(std::ostream& outs, const ExpressionNode& node);

#endif //COURSEWORK_WUST_TEP_EXPRESSION_NODE_H
