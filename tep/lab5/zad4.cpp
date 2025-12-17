#include "SmartPointer.h"
#include "../lab3/ExpressionTree.h"

int main()
{
    std::string input = "+ 1 2";
    SmartPointer tree(new ExpressionTree(input));
}
