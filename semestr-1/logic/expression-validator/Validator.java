package expressionvalidator;

import java.util.*;

public class Validator {
    private static Expression splitExpression(String string) throws ExpressionValidationException {
        Stack<Integer> stack = new Stack<>();
        List<ExpressionPart> parts = new ArrayList<>();
        char[] chars = string.toCharArray();
        int wordStartIdx = 0;
        boolean ensureBoundary = false;
        for (int i = 0; i < chars.length; i++) {
            char c = chars[i];
            switch (c) {
                case ')':
                    int expressionStartIdx;
                    try {
                        expressionStartIdx = stack.pop();
                    } catch (EmptyStackException e) {
                        throw new ExpressionValidationException("Unmatched closing parenthesis");
                    }
                    // Only add the outermost expression
                    if (stack.isEmpty())
                        parts.add(splitExpression(string.substring(expressionStartIdx, i)));
                    ensureBoundary = true;
                    continue;
                case '(':
                    stack.push(i + 1);
                    if (i > 0 && chars[i - 1] != ' ' && chars[i - 1] != '(')
                        throw new ExpressionValidationException("No space between expression and opening parenthesis");
                    break;
                case ' ':
                    if (!stack.isEmpty()) break;
                    if (!ensureBoundary)
                        parts.add(new Word(string.substring(wordStartIdx, i)));
                    ensureBoundary = false;
                    wordStartIdx = i + 1;
                    break;
                default:
                    if (i == chars.length - 1) {
                        if (!stack.isEmpty())
                            throw new ExpressionValidationException("Unmatched opening parenthesis");
                        parts.add(new Word(string.substring(wordStartIdx)));
                    }
                    break;
            }
            if (ensureBoundary && stack.isEmpty())
                throw new ExpressionValidationException("No space between closing parenthesis and expression");
        }
        return new Expression(parts);
    }

    public static boolean validate(String string) {
        Expression expression;
        try {
            expression = splitExpression(string);
        } catch (ExpressionValidationException e) {
            System.err.println("Expression syntax error: " + e.getMessage());
            return false;
        }
        return expression.isValid();
    }
}
