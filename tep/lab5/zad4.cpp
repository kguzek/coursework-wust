#include <iostream>
#include "ExpressionTree.h"

int main()
{
    std::string input1 = "+ 1 2";
    std::string input2 = "* 3 4";

    const Result<ExpressionTree*, Error> result_1 = ExpressionTree::parse(input1);
    const Result<ExpressionTree*, Error> result_2 = ExpressionTree::parse(input2);

    if (!result_1.is_success() || !result_2.is_success())
    {
        std::cout << "Błąd parsowania" << std::endl;
        return 1;
    }

    ExpressionTree* tree_1 = result_1.get_value();
    ExpressionTree* tree_2 = result_2.get_value();

    std::cout << "Przed przeniesieniem:" << std::endl;
    std::cout << "tree_1: " << tree_1->to_string() << std::endl;
    std::cout << "tree_2: " << tree_2->to_string() << std::endl;

    *tree_1 = std::move(*tree_2);

    std::cout << "\nPo przeniesieniu (tree_1 = std::move(tree_2)):" << std::endl;
    std::cout << "tree_1: " << tree_1->to_string() << std::endl;

    delete tree_1;
    delete tree_2;

    return 0;
}
