package dsaa.util;

import dsaa.list03.ex05.TwoWayCycledListWithSentinel;

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

    public static <E> String listToString(Iterable<E> list) {
        StringBuilder bob = new StringBuilder("[");
        Iterator<E> it = list.iterator();
        if (it.hasNext()) {
            bob.append(it.next());
        }
        while (it.hasNext()) {
            bob.append(", ").append(it.next());
        }
        bob.append("]");
        return bob.toString();
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

    public static IList<Integer> arrayToList(int[] input) {
        final IList<Integer> inputList = new TwoWayCycledListWithSentinel<>();
        for (int element : input) {
            inputList.add(element);
        }
        return inputList;
    }
}
