package expressionvalidator;

public interface ExpressionPart {
    boolean isValid();

    boolean isOperator();

    boolean isOperator(String operator);
}
