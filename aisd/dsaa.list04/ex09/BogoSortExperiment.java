package dsaa.list04.ex09;

import java.util.Arrays;
import java.util.Random;

public class BogoSortExperiment {
    private static final Random r = new Random();
    private static final int TARGET_SORT_TIME = 60_000;

    private static int[] generateRandomArray(int length) {
        final int upperBound = Math.max(length, 100);
        int[] arr = new int[length];
        for (int i = 0; i < length; i++) {
            arr[i] = r.nextInt(upperBound);
        }
        return arr;
    }

    /**
     * Returns the average time in milliseconds that it takes to sort this array over the given number of iterations.
     */
    @SuppressWarnings("SameParameterValue")
    private static long timeToSort(int[] arr, int iterations) {
        int[][] arrays = new int[iterations][arr.length];
        for (int i = 0; i < iterations; i++) {
            System.arraycopy(arr, 0, arrays[i], 0, arr.length);
        }
        final long startTime = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            BogoSort.sort(arrays[i]);
        }
        final long endTime = System.nanoTime();
        return (endTime - startTime) / iterations / 1_000_000;
    }

    public static void main(String[] args) {
        float lastTime = 0;
        for (int i = 5; lastTime < TARGET_SORT_TIME; i++) {
            int[] arr = generateRandomArray(i);
            System.out.println("Sorting array: " + Arrays.toString(arr) + "...");
            lastTime = timeToSort(arr, 3);
            System.out.printf("Average time to sort array with %d elements: %.1f s%n", i, lastTime / 1000);
        }
    }
}
