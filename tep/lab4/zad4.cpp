#include "Error.h"
#include "ExpressionTree.h"
#include "Result.h"
#include "ResultWriter.h"

int main()
{
    std::string input = "+ 1 2";
    const Result<ExpressionTree*, Error> result = ExpressionTree::parse(input);
    ResultWriter<ExpressionTree*>::write("test.txt", result);
}
