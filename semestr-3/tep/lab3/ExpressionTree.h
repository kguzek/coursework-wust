#ifndef COURSEWORK_WUST_TEP_EXPRESSION_TREE_H
#define COURSEWORK_WUST_TEP_EXPRESSION_TREE_H
#include <string>

#include "ExpressionNode.h"


class ExpressionTree
{
public:
    explicit ExpressionTree(std::string& input);
    ExpressionTree(const ExpressionTree& other);
    ~ExpressionTree() { delete _root; }
    ExpressionNode* get_root() const { return _root; }
    ExpressionTree operator+(const ExpressionTree& other) const;
    ExpressionTree& operator=(const ExpressionTree& other);
    std::string to_string() const;
    bool operator==(const ExpressionTree& other) const;

private:
    ExpressionNode* _root;
    std::map<std::string, int> _get_var_indices() const;
};

std::ostream& operator<<(std::ostream& outs, const ExpressionTree& tree);

#endif //COURSEWORK_WUST_TEP_EXPRESSION_TREE_H
