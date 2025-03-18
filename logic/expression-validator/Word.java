package expressionvalidator;

import java.util.Set;
import java.util.regex.Pattern;

public class Word implements ExpressionPart {
    private static final Set<String> OPERATORS = Set.of(
            "NOT",
            "AND",
            "OR",
            "IMPLIES",
            "IFF"
    );

    private static final Pattern variablePattern = Pattern.compile("[a-z01]|true|false");

    private final String value;

    public Word(String value) {
        this.value = value;
    }

    public boolean isOperator(String operator) {
        if (!OPERATORS.contains(operator))
            throw new IllegalArgumentException("Invalid operator: " + operator);
        return value.equalsIgnoreCase(operator);
    }

    public boolean isOperator() {
        return OPERATORS.contains(value.toUpperCase());
    }

    public boolean isVariable() {
        return variablePattern.matcher(value).matches();
    }

    public boolean isValid() {
        return isOperator() || isVariable();
    }

    @Override
    public String toString() {
        return "<" + (isValid() ? "VALID" : "INVALID") + " WORD '" + value + "'>";
    }
}
