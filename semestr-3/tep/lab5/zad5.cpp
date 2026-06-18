#include <iostream>
#include <utility>
#include "ExpressionTree.h"

ExpressionTree create_tree(const std::string& input)
{
    std::string input_copy = input;
    Result<ExpressionTree*, Error> result = ExpressionTree::parse(input_copy);

    if (!result.is_success())
    {
        return ExpressionTree(new ExpressionNode(input_copy));
    }

    ExpressionTree* tree = result.get_value();
    ExpressionTree copy = *tree;
    delete tree;
    return copy;
}

void test_assignment_copy()
{
    std::cout << "Test: copy assignment" << std::endl;
    ExpressionTree::reset_counters();

    ExpressionTree tree1 = create_tree("+ 1 2");
    ExpressionTree tree2 = create_tree("* 3 4");

    tree1 = tree2;

    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;
}

void test_assignment_move()
{
    std::cout << "\nTest: move assignment" << std::endl;
    ExpressionTree::reset_counters();

    ExpressionTree tree1 = create_tree("+ 1 2");
    ExpressionTree tree2 = create_tree("* 3 4");

    tree1 = std::move(tree2);

    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;
}

void test_constructor_copy()
{
    std::cout << "\nTest: copy constructor" << std::endl;
    ExpressionTree::reset_counters();

    ExpressionTree tree1 = create_tree("+ 1 2");
    ExpressionTree tree2 = tree1;

    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;
}

void test_constructor_move()
{
    std::cout << "\nTest: move constructor" << std::endl;
    ExpressionTree::reset_counters();

    ExpressionTree tree1 = create_tree("+ 1 2");
    ExpressionTree tree2 = std::move(tree1);

    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;
}

void test_operator_plus()
{
    std::cout << "\nTest: operator+ (lvalue + lvalue)" << std::endl;
    ExpressionTree::reset_counters();

    ExpressionTree tree1 = create_tree("+ 1 2");
    ExpressionTree tree2 = create_tree("* 3 4");
    ExpressionTree combined = tree1 + tree2;

    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;
}

void test_operator_plus_rvalue()
{
    std::cout << "\nTest: operator+ (rvalue + rvalue)" << std::endl;
    ExpressionTree::reset_counters();

    ExpressionTree tree1 = create_tree("+ 1 2");
    ExpressionTree tree2 = create_tree("* 3 4");
    ExpressionTree combined = std::move(tree1) + std::move(tree2);

    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;
}

void test_operator_plus_direct()
{
    std::cout << "\nTest: operator+ direct comparison" << std::endl;

    std::cout << "Creating temporary trees..." << std::endl;
    std::string s1 = "+ 1 2";
    std::string s2 = "* 3 4";
    ExpressionTree* t1 = ExpressionTree::parse(s1).get_value();
    ExpressionTree* t2 = ExpressionTree::parse(s2).get_value();

    std::cout << "\nLvalue + lvalue:" << std::endl;
    ExpressionTree::reset_counters();
    ExpressionTree result1 = *t1 + *t2;
    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;

    std::cout << "\nRvalue + rvalue:" << std::endl;
    ExpressionTree::reset_counters();
    ExpressionTree result2 = std::move(*t1) + std::move(*t2);
    std::cout << "  Copies: " << ExpressionTree::get_copy_count() << std::endl;
    std::cout << "  Moves: " << ExpressionTree::get_move_count() << std::endl;

    delete t1;
    delete t2;
}

int main()
{
    test_assignment_copy();
    test_assignment_move();
    test_constructor_copy();
    test_constructor_move();
    test_operator_plus();
    test_operator_plus_rvalue();
    test_operator_plus_direct();
    return 0;
}
