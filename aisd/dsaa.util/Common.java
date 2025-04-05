package dsaa.util;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Iterator;

public class Common {
    @SuppressWarnings("unchecked")
    public static <E> E[] listToArray(IList<E> list) {
        E[] result = (E[]) new Object[list.size()];
        Iterator<E> it = list.iterator();
        for (int i = 0; it.hasNext(); i++) {
            result[i] = it.next();
        }
        return result;
    }


    @SuppressWarnings("DuplicatedCode")
    public static void showArray(int[] arr) {
        if (arr.length == 0) {
            System.out.println();
            return;
        }
        StringBuilder bob = new StringBuilder(arr.length * 2 - 1).append(arr[0]);
        for (int i = 1; i < arr.length; i++) {
            bob.append(" ").append(arr[i]);
        }
        System.out.println(bob);
    }

    /**
     * Runs the provided runnable and returns its standard output as an array of strings.
     */
    public static String[] captureOutput(Runnable runnable) {
        // Redirect System.out to capture output
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outputStream));

        runnable.run();

        // Restore System.out
        System.setOut(originalOut);
        return outputStream.toString().split(System.lineSeparator());
    }
}
