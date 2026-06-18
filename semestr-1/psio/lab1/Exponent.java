package mathematics;

public class Exponent {

    private static int power(int a, int b) throws ZeroToZerothException {
        if (b == 0) {
            if (a == 0) {
                throw new ZeroToZerothException("Cannot calculate 0^0");
            }
            return 1;
        }
        int c = a;
        while (b > 1) {
            c *= a;
            b -= 1;
        }
        return c;
    }

    public static void test() throws ZeroToZerothException {
        int a = 2;
        int b = 4;
        test(a, b);
    }

    public static void test(int a, int b) throws ZeroToZerothException {
        int c = power(a, b);
        String message = String.format("%s ^ %s = %s", a, b, c);
        System.out.println(message);
    }
}
