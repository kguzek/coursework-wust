#ifndef COURSEWORK_WUST_TEP_EXPRESSION_TREE_H
#define COURSEWORK_WUST_TEP_EXPRESSION_TREE_H
#include <string>

#include "ExpressionNode.h"


class ExpressionTree
{
public:
    explicit ExpressionTree(ExpressionNode* node);
    ExpressionTree(const ExpressionTree& other);
    ExpressionTree(ExpressionTree&& other) noexcept;
    ~ExpressionTree() { delete _root; }
    ExpressionNode* get_root() const { return _root; }
    ExpressionTree operator+(const ExpressionTree& other) const &;
    ExpressionTree operator+(ExpressionTree&& other) const &;
    ExpressionTree operator+(const ExpressionTree& other) &&;
    ExpressionTree operator+(ExpressionTree&& other) &&;
    ExpressionTree& operator=(const ExpressionTree& other);
    ExpressionTree& operator=(ExpressionTree&& other) noexcept;
    std::string to_string() const;
    bool operator==(const ExpressionTree& other) const;
    static Result<ExpressionTree*, Error> parse(std::string& input);

    static int get_copy_count() { return copy_count; }
    static int get_move_count() { return move_count; }

    static void reset_counters()
    {
        copy_count = 0;
        move_count = 0;
    }

private:
    ExpressionNode* _root;
    std::map<std::string, int> _get_var_indices() const;

    static int copy_count;
    static int move_count;
};

std::ostream& operator<<(std::ostream& outs, const ExpressionTree& tree);

#endif //COURSEWORK_WUST_TEP_EXPRESSION_TREE_H
