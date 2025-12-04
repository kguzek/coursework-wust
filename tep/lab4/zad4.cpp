#include "Error.h"
#include "ExpressionTree.h"
#include "Result.h"
#include "ResultWriter.h"

int main()
{
    std::string input = "+ 1 2";
    Result<ExpressionTree*, Error> result = ExpressionTree::parse(input);
    ResultWriter<ExpressionTree*, Error>::write("test.txt", result);
}
