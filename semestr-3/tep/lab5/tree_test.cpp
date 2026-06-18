#include <iostream>

#include "ExpressionTree.h"

int main()
{
    std::string expression1 = "+ 1 2";
    std::string expression2 = "- 2 3";
    Result<ExpressionTree*, Error> result1 = ExpressionTree::parse(expression1);
    Result<ExpressionTree*, Error> result2 = ExpressionTree::parse(expression2);
    if (!result1.is_success() || !result2.is_success())
    {
        return 1;
    }
    std::cout << "copy:" << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "move:" << ExpressionTree::get_move_count() << std::endl;
    ExpressionTree t1 = *result1.get_value();
    ExpressionTree t2 = *result2.get_value();
    ExpressionTree t3 = t1 + t2;
    std::cout << "copy:" << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "move:" << ExpressionTree::get_move_count() << std::endl;
    t3 = t1     + t2;
    std::cout << "-------" << std::endl;
    std::cout << "copy:" << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "move:" << ExpressionTree::get_move_count() << std::endl;
    ExpressionTree t4(t1 + t2);
    std::cout << "-------" << std::endl;
    std::cout << "copy:" << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "move:" << ExpressionTree::get_move_count() << std::endl;
    ExpressionTree t5(std::move(t1));
    std::cout << "-------" << std::endl;
    std::cout << "copy:" << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "move:" << ExpressionTree::get_move_count() << std::endl;
    return 0;
}
