/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package mathematics;

/**
 * @author konrad
 */
public class GreatestCommonDivisor {

    private static int gcd(int a, int b) {
        int result = 1;
        for (int c = 2; c < a * b; c++) {
            if (a % c == 0 && b % c == 0) {
                result = c;
            }
        }
        return result;
    }

    public static void test() {
        test(21, 35);
    }

    public static void test(int a, int b) {
        int c = gcd(a, b);
        String message = String.format("GCD(%s, %s) = %s", a, b, c);
        System.out.println(message);
    }
}
