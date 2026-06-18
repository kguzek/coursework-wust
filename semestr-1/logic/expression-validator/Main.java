package expressionvalidator;

import java.util.Scanner;


public class Main {
    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        do {
            try {
                takeInput();
            } catch (InterruptedException e) {
                break;
            }
        } while (true);
        System.out.println("Exiting program...");
        scanner.close();
    }

    private static void takeInput() throws InterruptedException {
        System.out.print("Enter an expression (type EXIT to quit):\n> ");
        String expression = scanner.nextLine();
        if (expression.equalsIgnoreCase("EXIT")) {
            throw new InterruptedException();
        }
        String validityPrefix = Validator.validate(expression) ? (Color.ANSI_GREEN) : (Color.ANSI_RED + "IN");
        System.out.println("Expression is " + validityPrefix + "VALID" + Color.ANSI_RESET);
    }
}