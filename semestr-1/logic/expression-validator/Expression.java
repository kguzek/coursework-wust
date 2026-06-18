package expressionvalidator;

import java.util.List;

public class Expression implements ExpressionPart {
    private final List<ExpressionPart> parts;

    public Expression(List<ExpressionPart> parts) {
        this.parts = parts;
    }

    public boolean isOperator(String operator) {
        return isOperator();
    }

    public boolean isOperator() {
        return false;
    }

    public boolean isValid() {
        boolean expectingOperator = false;
        for (ExpressionPart part : parts) {
            if (!part.isValid())
                return false;
            if (expectingOperator) {
                if (!part.isOperator()) return false;
                expectingOperator = false;
                continue;
            }
            if (part.isOperator("NOT"))
                continue;
            if (part.isOperator()) return false;
            expectingOperator = true;
        }
        return expectingOperator;
    }

    @Override
    public String toString() {
        return "{" + (isValid() ? "VALID" : "INVALID") + " EXPRESSION: " + parts + "}";
    }
}
